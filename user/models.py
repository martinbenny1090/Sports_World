from django.conf import settings
from django.db import models

# Create your models here.

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'success'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default="")
    category = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.username

