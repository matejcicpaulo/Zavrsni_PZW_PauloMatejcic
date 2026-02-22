from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/add/", views.ProductCreateView.as_view(), name="product_add"),
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("warehouses/", views.WarehouseListView.as_view(), name="warehouse_list"),
    path("warehouses/add/", views.WarehouseCreateView.as_view(), name="warehouse_add"),
    path("warehouses/<int:pk>/edit/", views.WarehouseUpdateView.as_view(), name="warehouse_edit"),
    path("warehouses/<int:pk>/delete/", views.WarehouseDeleteView.as_view(), name="warehouse_delete"),
    path("stock/", views.StockItemListView.as_view(), name="stock_list"),
    path("stock/add/", views.StockItemCreateView.as_view(), name="stock_add"),
    path("stock/<int:pk>/edit/", views.StockItemUpdateView.as_view(), name="stock_edit"),
    path("stock/<int:pk>/delete/", views.StockItemDeleteView.as_view(), name="stock_delete"),
]