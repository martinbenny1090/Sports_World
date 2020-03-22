from django.conf import settings
from django.db import models
from django.shortcuts import reverse

# Create your models here.

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'success'),
    ('D', 'danger')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField()
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default="")
    category = models.CharField(max_length=50, default="")
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(default="")

    def __str__(self):
        return self.title

    def get_absolute(self):
        return reverse("user:product", kwargs={
            'slug': self.slug   
        })


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

