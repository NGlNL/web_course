from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    date_posted = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"
        ordering = ["-date_posted"]

    def __str__(self):
        return self.name
