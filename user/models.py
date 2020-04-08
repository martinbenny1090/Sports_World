from django.db import models
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'success'),
    ('D', 'danger'),
    ('N', 'null')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(default=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, default="")
    category = models.CharField(max_length=50, default="")
    slug = models.SlugField()
    description = models.TextField(default="")
    image = models.ImageField()
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("user:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("user:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("user:remove-from-cart", kwargs={
            'slug':self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price 

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price  

    def get_ammount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_prise(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

  

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_prise()
        return total 
       

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name 


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username 

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
 
