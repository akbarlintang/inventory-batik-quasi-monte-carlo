from django.db import models
from .utils import *

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'outlets'

    def __str__(self):
        return '%s' % self.name

class Item(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="img/items/", null=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    type = models.CharField(max_length=255, choices=ItemTypes.choices(), default=ItemTypes.MENTAH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return '%s' % self.name

class Purchase(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.CharField(max_length=255)
    amount = models.IntegerField()
    unit = models.CharField(max_length=255, choices=UnitTypes.choices(), default=UnitTypes.KG)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchases'

class Sales(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.CharField(max_length=255)
    amount = models.IntegerField()
    unit = models.CharField(max_length=255, choices=UnitTypes.choices(), default=UnitTypes.KG)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales'

class Transaction(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=255, choices=TypeTypes.choices(), default=TypeTypes.PURCHASE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'