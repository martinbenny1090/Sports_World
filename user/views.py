from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create own import.
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.utils import timezone

class HomeView(ListView):
    model = Item
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the  order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quanditity updated")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to cart")
            return redirect("user:product", slug=slug)
            
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to cart")
        return redirect("user:product", slug=slug)
    return redirect("user:product", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False   
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order item is in the  order
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from  cart")
            return redirect("user:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("user:product", slug=slug)

    else:
        messages.info(request, "you do not have an active order")
        return redirect("user:product", slug=slug)

   
