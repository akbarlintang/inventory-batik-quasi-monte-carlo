from django.db import models

class Outlet(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title

class Item(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.title