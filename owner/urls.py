from django.urls import path
from . import views
from  owner.views import VieworderPDF,Deletecontact, edit_order, order_item, orderitems, AddNEWC, ItemView,AddNewItem, EditItem, NewOwner, DeleteItem, contact, contactdetails, order, payment, refund, refundUpdate

app_name = 'owner'
urlpatterns = [
    path('', views.owhome, name="owhome"),
    path('NewOwner/', NewOwner.as_view(), name="NewOwner"),
    path('itemview/', ItemView.as_view(), name="itemview"),
    path('add-new-item/', AddNewItem.as_view(), name="add-new-item"),
    path('edit-item/<int:id>',EditItem.as_view(), name="edit-item"),
    path('DeleteItem/<int:id>', DeleteItem.as_view(), name="DeleteItem"),
    path('contact/', contact.as_view(), name="contact"),
    path('contactdetails/<int:id>', contactdetails.as_view(), name="contactdetails"),
    path('order/', order.as_view(), name="order"),
    path('payment/', payment.as_view(), name="payment"),
    path('refund/', refund.as_view(), name="refund"),
    path('refundUpdate/<int:id>', refundUpdate.as_view(), name="refundUpdate"),
    path('AddNEWC/', AddNEWC.as_view(), name="AddNEWC"),
    path('orderitems/<int:id>', orderitems.as_view(), name="orderitems"),  
    path('orderitemslist/', order_item.as_view(), name="orderitemslist"),
    path('edit-order/<int:id>', edit_order.as_view(), name="edit-order"),
    path('search/', views.search , name="search"),
    path('Deletecontact/<int:id>', Deletecontact.as_view(), name="Deletecontact"),
    path('pdf_order', VieworderPDF.as_view(), name="pdf_order"),
    
]