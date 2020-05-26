from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from user.models import Item, OrderItem, Contact, Order, OrderItem, Payment, Refund, BillingAddress
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, auth
# Create your views here.
from .filters import OrderFilters

class order_item(View):
    def get(self, request):
        items = OrderItem.objects.all()
        return render(request, "owner/order-items.html", {'items': items})


class order(View):
    def get(self, request):
        items = OrderItem.objects.all()
        orders = Order.objects.all()
        myfilter = OrderFilters(request.GET,queryset=orders)
        orders = myfilter.qs
        context = {
            'orders': orders,
            'items': items,
            'myfilter': myfilter
        }
        return render(request, "owner/orderlist.html", context)

class edit_order(View):

    def get(self, request, id):
        order = Order.objects.get(id=id)
        return render(self.request, 'owner/edit-order.html', {'order': order})

    def post(self, request, id):
        p = Order.objects.filter(id=id)
        being_delivered = request.POST.get('being_delivered')
        received = request.POST.get('received')
        refund_granted = request.POST.get('refund_granted')

        if being_delivered == 'T':
            p.update(being_delivered=True)

        if received == 'T':
            p.update(received=True)

        if refund_granted == 'T':
            p.update(refund_granted=True)

        return redirect("/owner/order/")
    
        
        

        
class orderitems(View):
    def get(self, request,id):
        item = OrderItem.objects.filter(user_id=id)
        if item is not None:
            return render(request, "owner/orderlist-items.html", {'item': item })
        else:
            messages.warning(self.request, "You do not have any order items")    
            return redirect("/owner/order/")
class contact(View):
    def get(self, request):
        con = Contact.objects.all()
        return render(request, 'owner/contact.html', {'con': con})

class contactdetails(View):
    def get(self, request, id):
        con = Contact.objects.filter(msg_id=id)
        return render(request, "owner/contactdetails.html", {'con': con[0]} )


class NewOwner(View):
    def get(self, *args, **kwargs):
        return render(self.request, "owner/newowner.html")

    def post(self, request):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')

        if User.objects.filter(username=email).exists():
            # print('user taken')
            messages.info(request,'E-mail Id already using')
            return redirect('register')

        else:    
            user = User.objects.create_user(username=email, password=password1, email=email,first_name=name, is_superuser="True", is_staff="True")
            user.save()
            return render(request,'owner/owhome.html')

def owhome(request):
    return render(request, 'owner/owhome.html')

class ItemView(ListView):
    model = Item
    paginate_by = 8
    template_name = "owner/itemview.html"
    # ordering = ['-']

class AddNewItem(View):
    def get(self, request):
        return render(request, 'owner/AddNewItem.html')

    def post(self, request):
        title = request.POST.get('title', '')
        price = request.POST.get('price', '')
        discount_price = request.POST.get('discount_price'," ")
        stock = request.POST.get('stock', '')
        category = request.POST.get('category', '')
        slug = request.POST.get('slug', '')
        description = request.POST.get('description', '')
        image = request.FILES['image']


        item = Item(image=image, title=title, price=price, discount_price=discount_price, category=category, stock=stock, slug=slug, description=description)
        item.save()
        return redirect("/owner/itemview/")

class EditItem(ListView):
    def get(self, request, id):
        #item
        item = Item.objects.filter(id=id)
        return render(request, 'owner/update_item.html', {'item': item[0]} )

    def post(self, request, id):
        m = Item.objects.get(id=id)
        print(m.image)
        etitle = request.POST.get('etitle', '')
        eprice = request.POST.get('eprice', '')
        ediscount_price = request.POST.get('ediscount_price'," ")
        estock = request.POST.get('estock', '')
        ecategory = request.POST.get('ecategory', '')
        eslug = request.POST.get('eslug', '')
        edescription = request.POST.get('edescription', '')
        eimage = request.FILES['eimage']
        
        m.title = etitle
        m.save() 
        m.price = eprice
        m.save()
        m.discount_price = ediscount_price
        m.save()
        m.stock = estock
        m.save()
        m.category = ecategory
        m.save()
        m.slug = eslug
        m.save()
        m.description = edescription
        m.save()
        m.image = eimage
        m.save()
        return redirect("/owner/itemview/")

class DeleteItem(ListView):
    def get(self,request, id):
        item = Item.objects.filter(id=id)
        return render(self.request, 'owner/DeleteItem.html', {'item': item[0]} )

    def post(self,request, id):
        item = Item.objects.filter(id=id)
        item.delete()
        return redirect("/owner/itemview/")
 

#model =OrderItem



class payment(View):
    def get(self, request):
        pay = Payment.objects.all()
        return render(request, "owner/patment.html", {'pays': pay})

class refund(View):
    def get(self, request):
        req = Refund.objects.all()
        return render(request, "owner/refund.html", {'reqs': req} )

class refundUpdate(View):
    def get(self, request, id):
        ref = Refund.objects.filter(id=id)
        return render(request, "owner/refund-update.html", {'ref': ref[0]} )

    def post(self, request, id):
        r = Refund.objects.filter(id=id)
        eaccepted = request.POST.get('eaccepted')
        print(eaccepted)
        if eaccepted == 'T':
            r.update(accepted=True)
        return redirect("/owner/refund/")

class AddNEWC(ListView):

    model = BillingAddress
    template_name = "owner/billingAddress1.html"

