from django.contrib.auth.models import User, Group
from rest_framework import serializers
from API.models import Invoice,BuyerDetails,SellerDetails,InvoiceItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# class InvoicesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=Invoice
#         fields=['invoice Nmuber','Invoice Date',]

from rest_framework.serializers import Serializer, FileField

# Serializers define the API representation.
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerDetails
        fields = ['name','address']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerDetails
        fields = ['name','address']
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invNumber','invDate','BuyerDetails','SellerDetails']

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['Invoice','productDescription','unit_price','qnty','tax_amount','total_amount']
