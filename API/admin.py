from django.contrib import admin

# Register your models here.
from API.models import Invoice,InvoiceItem,BuyerDetails,SellerDetails
admin.site.register(Invoice,)
admin.site.register(InvoiceItem,)
admin.site.register(BuyerDetails,)
admin.site.register(SellerDetails,)