from django import forms
from django.db.models import Sum
from .models import StockItem

class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ["warehouse", "product", "quantity", "reorder_level"]

    def clean(self):
        cleaned = super().clean()
        warehouse = cleaned.get("warehouse")
        quantity = cleaned.get("quantity")

        if warehouse is None or quantity is None:
            return cleaned

        if quantity < 0:
            raise forms.ValidationError("Količina ne može biti negativna.")

        # Trenutno zauzeće skladišta (bez ove stavke ako se uređuje postojeća)
        current_total = (
            StockItem.objects
            .filter(warehouse=warehouse)
            .exclude(pk=self.instance.pk if self.instance else None)
            .aggregate(total=Sum("quantity"))
            .get("total") or 0
        )

        if current_total + quantity > warehouse.capacity:
            free = max(warehouse.capacity - current_total, 0)
            raise forms.ValidationError(
                f"Nema dovoljno mjesta u skladištu. Slobodno: {free}, pokušavaš dodati: {quantity}."
            )

        return cleaned