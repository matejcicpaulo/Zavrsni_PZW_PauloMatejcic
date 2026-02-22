from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render
from .models import Product, Warehouse, StockItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


def home(request):
    return render(request, "home.html")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(sku__icontains=q) |
                Q(category__icontains=q)
            )
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["sku", "name", "category", "unit_price", "is_active"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["sku", "name", "category", "unit_price", "is_active"]
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

class WarehouseListView(LoginRequiredMixin, ListView):
    model = Warehouse
    template_name = "warehouses/warehouse_list.html"
    context_object_name = "warehouses"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(location__icontains=q)
            )
        return qs

class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouse
    fields = ["name", "location", "capacity"]
    template_name = "warehouses/warehouse_form.html"
    success_url = reverse_lazy("warehouse_list")


class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = Warehouse
    fields = ["name", "location", "capacity"]
    template_name = "warehouses/warehouse_form.html"
    success_url = reverse_lazy("warehouse_list")


class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    model = Warehouse
    template_name = "warehouses/warehouse_confirm_delete.html"
    success_url = reverse_lazy("warehouse_list")

class StockItemListView(LoginRequiredMixin, ListView):
    model = StockItem
    template_name = "stock/stock_list.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = super().get_queryset().select_related("warehouse", "product")

        q = self.request.GET.get("q")
        warehouse_id = self.request.GET.get("warehouse")
        product_id = self.request.GET.get("product")

        if q:
            qs = qs.filter(
                Q(product__name__icontains=q) |
                Q(product__sku__icontains=q) |
                Q(warehouse__name__icontains=q)
            )

        if warehouse_id:
            qs = qs.filter(warehouse_id=warehouse_id)

        if product_id:
            qs = qs.filter(product_id=product_id)

        return qs

class StockItemCreateView(LoginRequiredMixin, CreateView):
    model = StockItem
    fields = ["warehouse", "product", "quantity", "reorder_level"]
    template_name = "stock/stock_form.html"
    success_url = reverse_lazy("stock_list")


class StockItemUpdateView(LoginRequiredMixin, UpdateView):
    model = StockItem
    fields = ["warehouse", "product", "quantity", "reorder_level"]
    template_name = "stock/stock_form.html"
    success_url = reverse_lazy("stock_list")


class StockItemDeleteView(LoginRequiredMixin, DeleteView):
    model = StockItem
    template_name = "stock/stock_confirm_delete.html"
    success_url = reverse_lazy("stock_list")

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")