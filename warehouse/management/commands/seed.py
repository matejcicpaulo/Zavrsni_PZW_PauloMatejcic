import random
from django.core.management.base import BaseCommand
from warehouse.models import Warehouse, Product, StockItem


class Command(BaseCommand):
    help = "Generira testne podatke"

    def handle(self, *args, **options):
        StockItem.objects.all().delete()
        Product.objects.all().delete()
        Warehouse.objects.all().delete()

        w1 = Warehouse.objects.create(name="Skladište Zagreb", location="Zagreb", capacity=5000)
        w2 = Warehouse.objects.create(name="Skladište Split", location="Split", capacity=3000)

        products = []
        for i in range(1, 11):
            p = Product.objects.create(
                sku=f"SKU{i:03}",
                name=f"Proizvod {i}",
                category="Općenito",
                unit_price=random.randint(10, 200),
                is_active=True
            )
            products.append(p)

        for p in products:
            StockItem.objects.create(
                warehouse=random.choice([w1, w2]),
                product=p,
                quantity=random.randint(0, 100),
                reorder_level=10
            )

        self.stdout.write(self.style.SUCCESS("Seed uspješno izvršen ✅"))