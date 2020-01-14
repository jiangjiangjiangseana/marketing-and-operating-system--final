from django.shortcuts import render
from home.models import Store, Customer, Company, Product, Warehouse, Inventory, Storage, Order
from django.template import *
from django.http import HttpResponse

# Create your views here.

def supply(request):
 daily_demand = 10
 days = 7
 safety_inventory =20
 ROP = daily_demand*days+safety_inventory
 company_list =[]
 for i in Company.objects.all():
  company_list.append(i.company_id)

  storage_list_1 = []
  for s in Storage.objects.filter(company_id='001'):
   tmp =[]
   if s.storage_quantity<ROP:
    tmp.append(s.product_id)
    tmp.append(s.shoe_size)
    tmp.append(ROP-s.storage_quantity)
    tmp.append(s.warehouse_id)
    storage_list_1.append(tmp)

  storage_list_2 = []
  for s in Storage.objects.filter(company_id='002'):
   tmp =[]
   if s.storage_quantity<ROP:
    tmp.append(s.product_id)
    tmp.append(s.shoe_size)
    tmp.append(ROP-s.storage_quantity)
    tmp.append(s.warehouse_id)
    storage_list_2.append(tmp)

  storage_list_3 = []
  for s in Storage.objects.filter(company_id='003'):
   tmp =[]
   if s.storage_quantity<ROP:
    tmp.append(s.product_id)
    tmp.append(s.shoe_size)
    tmp.append(ROP-s.storage_quantity)
    tmp.append(s.warehouse_id)
    storage_list_3.append(tmp)

  storage_list_4 = []
  for s in Storage.objects.filter(company_id='004'):
   tmp =[]
   if s.storage_quantity<ROP:
    tmp.append(s.product_id)
    tmp.append(s.shoe_size)
    tmp.append(ROP-s.storage_quantity)
    tmp.append(s.warehouse_id)
    storage_list_4.append(tmp)



 return render(request,'庫存查詢系統.html', locals())




def d_done_001(request):
    storage = Storage.objects.filter(company_id = "001" )
    for s in storage:
      if s.storage_quantity <90:
        s.storage_quantity += 90
        s.save()
    return render(request,'製作成功001.html')

def d_done_002(request):
    storage = Storage.objects.filter(company_id = "002" )
    for s in storage:
      if s.storage_quantity <90:
        s.storage_quantity += 90
        s.save()
    return render(request,'製作成功002.html')

def d_done_003(request):
    storage = Storage.objects.filter(company_id = "003" )
    for s in storage:
      if s.storage_quantity <90:
        s.storage_quantity += 90
        s.save()
    return render(request,'製作成功003.html')



def d_done_004(request):
    storage = Storage.objects.filter(company_id = "004" )
    for s in storage:
      if s.storage_quantity <90:
        s.storage_quantity += 90
        s.save()
    return render(request,'製作成功004.html')



