from django.urls import path
from django.views.decorators.cache import cache_page

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path(
        "product/<int:pk>/", cache_page(60)(views.ProductDetailView.as_view()), name="products_detail"
    ),
    path("catalog/create", views.ProductCreateView.as_view(), name="products_create"),
    path(
        "catalog/<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="products_update",
    ),
    path(
        "catalog/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="products_delete",
    ),
    path(
        "catalog/unpublish/<int:product_id>/",
        views.UnpublishProductView.as_view(),
        name="unpublish_product",
    ),
]
