from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from user.models import Item, OrderItem, Contact, Order, OrderItem, Payment, Refund, BillingAddress
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, auth
from .filters import OrderFilters, paymentFilters, orderitemsFilters
from django.contrib import messages
from datetime import date 
# Create your views here.
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

class order_report(View):
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
        return render( request, "owner/order-report.html", context)

class owner_item_view(ListView):
    model = Item 
    paginate_by = 8
    template_name = "owner/owner-item-view.html"
    
def search(request):
    query = request.GET.get('search')
    orders = Order.objects.filter(ref_code=query)
    m = 0
    for i in orders:
        m=i.id

    items = OrderItem.objects.filter(order_id=m)
    
    params = {
        'orders': orders,
        'items': items
        }
    

    rcount=0
    for i in orders:
        rcount = 1
    if rcount == 0 or len(query)<3:
            messages.warning(request, "Plase make sure to enter the revelant search query No item found")
            return redirect("/owner/")
    return render(request, "owner/search.html", params)

class order_item(View):
    def get(self, request):
        items = OrderItem.objects.all()
        myfilter = orderitemsFilters(request.GET,queryset=items)
        items = myfilter.qs
        return render(request, "owner/order-items.html", {'items': items,'myfilter': myfilter })





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
        orders = Order.objects.filter(id=id)
        for i in orders:
           m=i.id 
        items = OrderItem.objects.filter(order_id=m)
        param = {
            'order': order,
            'items': items
        }
        return render(self.request, 'owner/edit-order.html', param)

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
        print(id)
        item = OrderItem.objects.filter(order_id=id)
        if item is not None:
            return render(request, "owner/orderlist-items.html", {'item': item })
        else:
            messages.warning(self.request, "You do not have any order items")    
            return redirect("owner:order")

class contact(View):
    def get(self, request):
        con = Contact.objects.all()
        return render(request, 'owner/contact.html', {'con': con})

class contactdetails(View):
    def get(self, request, id):
        con = Contact.objects.filter(msg_id=id)
        return render(request, "owner/contactdetails.html", {'con': con[0]} )

class Deletecontact(ListView):
    def get(self,request, id):
        item = Contact.objects.filter(msg_id=id)
        return render(self.request, 'owner/Deletecontact.html', {'item': item[0]} )

    def post(self,request, id):
        item = Contact.objects.filter(msg_id=id)
        item.delete()
        return redirect("owner:contact")

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
            return redirect('owner:NewOwner')

        else:    
            user = User.objects.create_user(username=email, password=password1, email=email,first_name=name, is_superuser="True", is_staff="True")
            user.save()
            messages.info(request,'Sucessfully Registred')
            return render(request,'owner/owhome.html')

def owhome(request):
    
   
    scount = Item.objects.filter(stock=0).count()
    today = date.today()
    count = Refund.objects.filter(date__day=today.day).count()
    rcount = Refund.objects.all().count()

    print(today)
    ocount = Order.objects.filter(ordered_date__year=today.year, ordered_date__month=today.month, ordered_date__day=today.day,ordered=True).count()
    torder = Order.objects.filter(ordered=True).count()
    titem = Item.objects.all().count()
    tcontact = Contact.objects.all().count()
    items = Payment.objects.filter(timestamp__year=today.year,timestamp__month=today.month,timestamp__day=today.day).count()
    Titem = Payment.objects.all().count()
    USCount = User.objects.filter(is_superuser=False).count()

    #total stock
    Iall = Item.objects.all()
    stockTotal = 0
    for i in Iall:
        stockTotal += i.stock
     
    #items sell today
    Isell = OrderItem.objects.filter(AddedDate__day=today.day,AddedDate__month=today.month,AddedDate__year=today.year)
    items_selling_today=0
    for i in Isell:
        items_selling_today += i.quantity
    
    
    
    param ={
        'count': count,
        'scount': scount,
        'ocount': ocount,
        'torder': torder,
        'titem': titem,
        'tcontact': tcontact,
        'items': items,
        'Titem': Titem,
        'rcount': rcount,
        'USCount': USCount,
        'stockTotal': stockTotal,
        'items_selling_today': items_selling_today,
    }
    return render(request, 'owner/owhome.html', param)

class ItemView(ListView):
    model = Item
    paginate_by = 8
    template_name = "owner/itemview.html"
    # ordering = ['-']
    # def get(self) 
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


        if Item.objects.filter(slug=slug).exists():
            messages.info(request,'slug id all ready taken')
            return redirect("/owner/add-new-item/")


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
        return redirect("owner:itemview")
        

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
        myfilter = paymentFilters(request.GET,queryset=pay)
        pay = myfilter.qs
        return render(request, "owner/patment.html", {'pays': pay, 'myfilter': myfilter})

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
        if eaccepted =='T':
            r.update(accepted=True)
        return redirect("/owner/refund/")

class AddNEWC(ListView):

    model = BillingAddress
    template_name = "owner/billingAddress1.html"

