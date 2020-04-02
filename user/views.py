from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create own import.
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Contact
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,  *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

        

def checkout(request):
    return render(request, 'checkout.html')

class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

@login_required
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
            return redirect("user:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to cart")
            return redirect("user:order-summary")
            
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to cart")
        return redirect("user:order-summary")
    return redirect("user:product")

@login_required
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
            return redirect("user:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("user:product", slug=slug)

    else:
        messages.info(request, "you do not have an active order")
        return redirect("user:product", slug=slug)

   
@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated")
            return redirect("user:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("user:product", slug=slug)

    else:
        messages.info(request, "you do not have an active order")
        return redirect("user:product", slug=slug)


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'contact.html')