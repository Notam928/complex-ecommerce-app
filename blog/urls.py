from django.urls import path

from blog.views import BlogView

app_name = "blog"

urlpatterns = [
    path("", BlogView.as_view(), name="blog_index"),
]
