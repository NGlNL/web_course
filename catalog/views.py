from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)

from .forms import ContactForm, ProductForm
from .models import Category, Product
from .services import ProductService, get_products_from_cache


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет прав для отмены публикации")

        product.unpublish = False
        product.save()
        return redirect("catalog:products_detail", pk=product_id)


class IndexListView(ListView):
    model = Product
    template_name = "catalog/index.html"
    context_object_name = "products"

    def get_queryset(self):
        return get_products_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        selected_category_id = self.request.GET.get("category_id")
        if selected_category_id:
            selected_category = get_object_or_404(Category, id=selected_category_id)
            context["selected_category"] = selected_category
            context["products"] = Product.objects.filter(category=selected_category)
            if selected_category_id and selected_category_id == Product.objects.all():
                selected_category = get_object_or_404(Category, id=selected_category_id)
                context["selected_category"] = selected_category
                context["products"] = Product.objects.filter(category=selected_category)
        else:
            context["products"] = Product.objects.all()
        return context


class ContactView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение отправлено.")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/products_details.html"

    def post(self, request, *args, **kwargs):
        product = super().get_object()
        if not (
            request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user == product.owner
        ):
            messages.error(request, "У вас нет прав для выполнения этого действия.")
            return redirect(
                "catalog:product_detail", product_id=self.kwargs.get(self.pk_url_kwarg)
            )

        product = self.get_object()
        product.status = "draft"
        product.save()
        messages.success(
            request, f"Продукт {product.name} был успешно снят с публикации."
        )
        return redirect("catalog:product_detail", product_id=product.id)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:index")

    def get_object(self):
        product = super().get_object()
        if not (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.change_product")
        ):
            messages.error(
                self.request, "У вас нет прав для редактирования этого продукта."
            )
            raise PermissionDenied
        return product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:index")

    def get_object(self):
        product = super().get_object()

        if not (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.delete_product")
        ):
            messages.error(self.request, "У вас нет прав для удаления этого продукта.")
            raise PermissionDenied

        return product
