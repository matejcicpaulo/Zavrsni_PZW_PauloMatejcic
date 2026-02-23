from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.shortcuts import render
from .models import Product, Warehouse, StockItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import StockItemForm
from django.db.models import Sum


@login_required
def home(request):
    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()

    low_stock_count = StockItem.objects.filter(
        quantity__lte=F("reorder_level")
    ).count()

    context = {
        "total_products": total_products,
        "total_warehouses": total_warehouses,
        "low_stock_count": low_stock_count,
    }

    return render(request, "home.html", context)


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
    
    def get_queryset(self):
        qs = super().get_queryset().select_related("warehouse", "product")

        q = self.request.GET.get("q")
        warehouse_id = self.request.GET.get("warehouse")
        product_id = self.request.GET.get("product")
        low = self.request.GET.get("low")  

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

        if low == "1":  
            qs = qs.filter(quantity__lte=F("reorder_level"))

        return qs

class StockItemCreateView(LoginRequiredMixin, CreateView):
    model = StockItem
    form_class = StockItemForm
    template_name = "stock/stock_form.html"
    success_url = reverse_lazy("stock_list")


class StockItemUpdateView(LoginRequiredMixin, UpdateView):
    model = StockItem
    form_class = StockItemForm
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

@require_POST
def stock_inc(request, pk):
    item = get_object_or_404(StockItem, pk=pk)
    item.quantity += 1
    item.save()

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    return redirect("stock_list")


@require_POST
def stock_dec(request, pk):
    item = get_object_or_404(StockItem, pk=pk)
    if item.quantity > 0:
        item.quantity -= 1
        item.save()

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)

    return redirect("stock_list")

@require_POST
def stock_inc(request, pk):
    item = get_object_or_404(StockItem, pk=pk)

    total = (
        StockItem.objects
        .filter(warehouse=item.warehouse)
        .aggregate(total=Sum("quantity"))
        .get("total") or 0
    )

    if total >= item.warehouse.capacity:
        next_url = request.POST.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("stock_list")

    item.quantity += 1
    item.save()

    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("stock_list")