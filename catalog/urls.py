from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("contacts/", views.ContactView.as_view(), name="contacts"),
    path(
        "product/<int:pk>/", views.ProductDetailView.as_view(), name="products_detail"
    ),
]
