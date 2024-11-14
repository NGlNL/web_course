from django.urls import path

from blog.views import (
    BlogView,
    PostCreateView,
    BlogDetailView,
    BlogUpdateView,
    BlogDeleteView,
)

app_name = "blog"


urlpatterns = [
    path("", BlogView.as_view(), name="blog"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),
]
