from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from API.serializers import UserSerializer, GroupSerializer, InvoiceSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path
from django.conf import settings
import pdftotext
from API.models import SellerDetails,BuyerDetails,Invoice,InvoiceItem  
#pdf extracter ---startt-
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
from datetime import datetime
import copy
from rest_framework import generics
from rest_framework import filters



#----------end------------


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

# ViewSets define the view behavior.
class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer
    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        if file_uploaded!=None:

            lst=["TOTAL:[\s+\S+]*₹(\S+)","Invoice Date\s+:\s+(\d\d.\d\d.\d\d\d\d)","Invoice Number\s+:\s+(\S+)","Sold By\s+:\s+([\s\S]*?\n)","Sold By\s+:\s+[\s\S]*?[*]\s+([\s\S]*?\d*IN)","Billing Address\s+:\s+[\s\S]*?\n([\s\S]*?IN)","Billing Address\s+:\s+([\s\S]*?\n)","Total\nAmount\n+\s+([\s\S]+?(For|TOTAL))","Sl.\nNo\n([\s\S]+?(Unit|TOTAL))",]

            output_string = StringIO()    
            parser = PDFParser(file_uploaded)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)      
            data=output_string.getvalue()

            lst1=[]
            for pattern in lst:
                data1=re.findall(pattern,data)
                lst1.append(data1)
        
            inv_Date=lst1[1][0]
            inv_Number=lst1[2][0]
            seller_name=lst1[3][0].replace("\n",'')
            Seller_Adress=lst1[4][0].replace("\n",'')
            buyer_Name=lst1[6][0].replace("\n",'')
            buyer_Adress=lst1[5][0].replace("\n",'')

            product_Name=[]
            product_other=[]
            product_temp=[]

            for i in lst1[8]:
                for k in i:
                    k=k[:-5]
                    k=re.sub("\n\n\D", "\n", k)
                    a=k.split('\n\n')
                    for j in a:
                        product_Name.append(j[1:].replace("\n",''))
                    break
                break
            for i in lst1[7]:
                for k in i:
                    a=k.split("\n\n")
                    for j in a:
                        if j.startswith('₹'):
                            b=j.split(" ")
                            if len(b)==2:
                                Tottal=b[1]
                            else:
                                for k in b:
                                    product_temp.append(k.replace('₹',''))
                                product_temp1=copy.deepcopy(product_temp)
                                product_other.append(product_temp1)
                                product_temp.clear()
                    break
                break
        
            buyer=BuyerDetails(name=buyer_Name,Adress=buyer_Adress)
            buyer.save()
            seller=SellerDetails(name=seller_name,Adress=Seller_Adress)
            seller.save()
            inv=Invoice(invNumber=inv_Number,invDate=inv_Date,sellerId=seller,buyerId=buyer)
            inv.save()

            Description=str()
            unit_price=float()
            qnty=int()
            net_amount=float()
            tax_rate=str()
            tax_type=str()
            tax_amt=float()
            tottal_amount=float()

            for i in range(0,len(product_other)):
                Description=product_Name[i]
                unit_price=float(product_other[i][0].replace(',',''))
                qnty=int(product_other[i][1].replace(',',''))
                net_amount=product_other[i][2].replace(',','')
                tax_rate=product_other[i][3].replace(',','')
                tax_type=product_other[i][4].replace(',','')
                tax_amt=float(product_other[i][5].replace(',',''))
                tottal_amount=float(product_other[i][6].replace(',',''))
                invItem=InvoiceItem(invId=inv,productDescription=Description,qnty=qnty,unit_price=unit_price,tax_amount=tax_amt,total_amount=tottal_amount)
                invItem.save()            
           
            content_type = file_uploaded.content_type
            response = "PDF is scucessfully Updated to the Database"
            return Response(response)
        else:
            response ="No file Fouond"
            return Response(response)




