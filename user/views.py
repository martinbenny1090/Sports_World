import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create own import.
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Contact, BillingAddress, Payment, Refund
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import win32api
from django.views import View
import random
import string
stripe.api_key = 'sk_test_S3eXvxJrVCROKaPdNikrD15300UsFQvwPS'

class About_as(View):

    def get(self, request):
        return render (request, 'about.html')
    

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class paymentView(View):
    def get(self, *args, **kwargs):
        #order
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order is not None:  
            if order.billing_address:
                context = {
                    'order': order,
                    
                }
                return render(self.request, "payment.html", context)
            else:
                messages.warning(self.request, "You do not have a billing address")    
                return redirect("user:checkout")
        else:
            messages.warning(self.request, "You do not have a active order")    
            return redirect("/")


    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        porder = Order.objects.filter(user=self.request.user, ordered=False)
        publishKey = settings.STRIPE_PUBLISHABLE_KEY #new
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total())
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
            print(token)
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            #pdf function 
            print(order.id)
            p = int(order.id)

            #assign the payment to the order
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.AddedDate = timezone.now()#OrderItem add date 
                item.order_id = order
                item.save()
            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()#order reference
            order.save()
            
            win32api.MessageBox(0, "Your order was sucessfull . we  will Contact you as soon as possible ", 'Sport world', 0x00001000) 
            
            return redirect('user:billingpage', p)  #new direcert here 
            # return redirect("/")
            
                
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
                  
            }
            billing_address_qs = BillingAddress.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("user:checkout")
        return render(self.request, 'checkout.html')


    def post(self, request):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if order is not None: 
                use_default_billing = request.POST.get('use_default_billing', '')
                if use_default_billing:
                    print("using default billing  address")
                    address_qs = BillingAddress.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request ,"No default Billing address")
                        return redirect("user:checkout") 
                else:
                    print("the user entering new Billing addres")
                    #new
                    street_address = request.POST.get('address1', '')
                    address2 = request.POST.get('address2', '')
                    counrty = request.POST.get('counrty', '')
                    state = request.POST.get('state', '')
                    zip = request.POST.get('zip', '') 
                    pinv = request.POST.get('pinv', '') 
                    phone = request.POST.get('phone', '')
                    if pinv == 'T':
                        #new
                        billing_address = BillingAddress(
                            user=self.request.user,
                            street_address=street_address,
                            apartment_address=address2,
                            country=counrty,
                            zip=zip,
                            address_type='B',
                            phone = phone
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info( self.request, "Plase verify the pincode to delivery item")
                        return redirect('user:checkout')
                    set_default_billing = request.POST.get('set_default_billing', '')
                    if set_default_billing:
                        billing_address.default = True
                        billing_address.save()

                    # else:
                    #     messages.info( self.request, "Please fill in the required billing address fields")
                    #     return redirect('user:checkout')
                            
                payment_option = request.POST.get('paymentMethod', '')
                #Todo: add redirect to the selected payment option 
                if payment_option == 'S':
                    return redirect('user:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('user:payment', payment_option='paypal')
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
            print(item)
            print(item.stock)
            print(order_item.quantity)
            print("hai")
            m = item.stock
            n = order_item.quantity
            if m > n:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quanditity updated")
                return redirect("user:order-summary")
            else:
                messages.info(request, "This item quanditity over stock")
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

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "request_refund.html")

    def post(self, request):
        ref_code = request.POST.get('ref_code')
        message = request.POST.get('email')
        email = request.POST.get('message')
        print (ref_code)
        print (message)
        print (email)
        try:
            order = Order.objects.get(ref_code=ref_code)
            order.refund_requested = True
            order.save()

            # store the refund
            refund = Refund()
            refund.order = order 
            refund.reason = email
            refund.email = message
            refund.save()

            messages.info(self.request, "Your request was received.")
            return redirect("user:request-refund")

        except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("user:request-refund")


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.description.lower() or query in item.title.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    items_temp = Item.objects.all()
    items = [item for item in items_temp if searchMatch(query, item)]
    params = {
        'items': items
        }
    count=0
    for i in items:
        count = 1
    if count == 0 or len(query)<3:
            messages.warning(request, "Plase make sure to enter the revelant search query No item found")
            return redirect("/")

    return render(request, "search.html", params)
        
def myorders(request):
    myitems = Order.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user, refund_requested=True)
    print(order)
    param = {
        'myitems': myitems,
        'order' : order,
    }    
    return render(request, 'myorders.html', param)


def myorderItemsView(request,id):
    items = OrderItem.objects.filter(user=request.user,order_id=id)
    return render(request, 'myorderitemview.html', {'items': items})

class billingpage(View):
    def get(self, request, p):
    
        d = Order.objects.filter(id=p)
        a = Order.objects.get(id=p)
        order_items = a.items.all()
    
        for i in order_items:
            m = i.quantity
            n = i.item.id
            q = i.item.stock
            b = q - m
            s = Item.objects.get(id=n)
            print(s.stock)
            s.stock = b
            s.save()

        context = {
            'd': d,
            'order_items': order_items,
        }
        return render(self.request, 'billingpage.html', context)

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



#Opens up page as PDF
class ViewPDF(View):

    def get(self, request, id):

        d = Order.objects.filter(id=id)
        p = Order.objects.get(id=id)
        order_items = p.items.all()
        data = {
        "company": "Sports World",

        "website": "Sports World",
        "email": "martin8086benny@gmail.com",
        "phone": "+91-9475843265",
        "zipcode": "686581",
        "d": d,
        "order_items": order_items,
        }

        pdf = render_to_pdf('pdf-billingpage.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

