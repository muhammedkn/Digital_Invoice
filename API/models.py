from django.db import models

class SellerDetails(models.Model):
    name=models.CharField(max_length=20)
    Adress=models.TextField()
    def __str__(self): 
        return self.name

class BuyerDetails(models.Model):
    name=models.CharField(max_length=20)
    Adress=models.TextField()
    def __str__(self): 
        return self.name

class Invoice(models.Model):
    invNumber=models.CharField(max_length=20)
    invDate=models.CharField(max_length=20)
    sellerId=models.ForeignKey(SellerDetails,on_delete = models.CASCADE)
    buyerId=models.ForeignKey(BuyerDetails,on_delete = models.CASCADE)
    def __str__(self): 
        return self.invNumber
   

class InvoiceItem(models.Model): 
    invId=models.ForeignKey(Invoice,on_delete=models.CASCADE)
    productDescription=models.CharField(max_length=100)
    unit_price=models.FloatField()
    qnty=models.IntegerField()
    tax_amount=models.FloatField()
    total_amount=models.FloatField()
    def __str__(self): 
        return self.productDescription

