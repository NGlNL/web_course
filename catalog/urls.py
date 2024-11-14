from django.urls import path

from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.contacts, name="contacts"),
    path("product/<int:pk>/", views.products_details, name="products_detail"),
]
