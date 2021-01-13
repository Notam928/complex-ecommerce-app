from django.urls import path

from core.views import (
    HomeView, ShopView, ProductDetail
    )

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("shop", ShopView.as_view(), name="shop"),
    path("products/<slug:slug>", ProductDetail.as_view(), name="product"),
]
