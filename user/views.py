from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create own import.
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Contact, BillingAddress, Payment, Coupon
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

import stripe
stripe.api_key = 'sk_test_S3eXvxJrVCROKaPdNikrD15300UsFQvwPS'

class PaypalView(View):#paypal page
    def get(self, *args, **kwargs):
        return render(self.request, 'paypal.html')

class paymentView(View):#stripe  page
    def get(self, *args, **kwargs):
        #order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a billing address ")    
            return redirect("user:checkout")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        print(token)
        amount = int(order.get_total() * 100)
        try:
            # customer = stripe.Customer.create(
            #     name='namu',
            #     email='manu@gmail.com',
            #     description='3 sharts',
            #     source=token,
                
            # )
            # charge = stripe.Charge.create(
            #     customer=customer,
            #     amount=amount,  # cents
            #     currency="usd",
                
            #     description='3 sharts',
                
                
            # )
             
            # create the payment
            payment = Payment()
            payment.stripe_charge_id = token
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            #assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your order was sucessfull")    
            return redirect("/")
                
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
             # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")        
                
                
class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': True  
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("user:checkout")
        return render(self.request, 'checkout.html')

    def post(self, request):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if order is not None: 
                street_address = request.POST.get('address1', '')
                address2 = request.POST.get('address2', '')
                counrty = request.POST.get('counrty', '')
                state = request.POST.get('state', '')
                zip = request.POST.get('zip', '') 
                # same_billing_address = request.POST.get('same_billing_address', '')
                # save_info = request.POST.get('save_info', '')
                payment_option = request.POST.get('paymentMethod', '')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=address2,
                    country=counrty,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                #Todo: add redirect to the selected payment option 
                if payment_option == 'S':
                    return redirect('user:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('user:paypal', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('user:checkout')
                return redirect('user:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('user:checkout')

            
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect('user:order-summary')
        return render(self.request, 'checkout.html')


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

class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
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

   
@login_required(login_url='/accounts/login')
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

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon 
    except ObjectDoesNotExist:
        messages.info(request, "this coupon does not exist")
        return redirect('user:checkout')

class AddCouponView(View):
    def post(self, *args, **kwargs):
        code = request.POST.get('code','')
        try:
            code=code
            print(code)
            order = Order.objects.get(user=self.request.user, ordered=False)
            order.coupon = get_coupon(self.request, code)
            order.save()
            messages.success(self.request, "Successfully coupon added")
            return redirect('user:checkout')
        except ObjectDoesNotExist:
            messages.info(self.request, "you do not have an active order")
            return redirect('user:checkout')
    