from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import Post


class BlogView(ListView):
    model = Post
    template_name = "blog/blog.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = ["name", "content", "is_published", "image"]

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        post.views_count += 1
        post.save()

        return post


class BlogUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = ["name", "content", "is_published", "image"]

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    model = Post
    template_name = "blog/blog_delete.html"
    success_url = reverse_lazy("blog:blog")
