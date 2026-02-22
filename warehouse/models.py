from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sku} - {self.name}"


class StockItem(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_items")

    quantity = models.IntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("warehouse", "product")

    def __str__(self) -> str:
        return f"{self.warehouse.name} - {self.product.sku} ({self.quantity})"