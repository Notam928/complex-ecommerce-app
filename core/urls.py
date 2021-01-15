from django.urls import path

from core.views import (
    HomeView, ShopView, ProductDetail,OrderSummaryView, add_to_cart
    )

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("shop", ShopView.as_view(), name="shop"),
    path("products/<slug:slug>", ProductDetail.as_view(), name="product"),
    path("add-to-cart/<slug:slug>/",add_to_cart, name="add_to_cart"),
    path("oder-summary/", OrderSummaryView.as_view(), name="order_summary"),
]

