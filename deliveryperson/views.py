from django.shortcuts import render
from home.models import Store, Customer, Company, Product, Warehouse, Inventory, Storage, Order
import random
# Create your views here.





def delivery(request):

#  warehouse_list = []
#  for i in Warehouse.objects.all():
#   warehouse_list.append(i.warehouse_id)


 deliver_list = []
 for i in Inventory.objects.all():
  tmp = []
  if i.inventory_quantity<10:
    s = Store.objects.get(store_name = i.store_id)
    tmp.append(str(i.store_id)+"-"+str(s.store_district))
    tmp.append(str(i.product_id)+"-"+str(i.shoe_size))
    tmp.append(10-i.inventory_quantity)
    deliver_list.append(tmp)

 tp=[[0, 30, 55, 44, 20, 70],
     [30, 0, 43, 78, 26, 76],
     [55, 43, 0, 22, 94, 54],
     [44, 78, 22, 0, 12, 34],
     [20, 26, 94, 12, 0, 77],
     [70, 76, 54, 34, 77, 0]]

 tc=[[0, 55, 33, 87, 90, 13],
     [55, 0, 21, 65, 78, 44],
     [33, 21, 0, 23, 11, 54],
     [87, 65, 23, 0, 43, 70],
     [90, 78, 11, 43, 0, 64],
     [13, 44, 54, 70, 64, 0]]

 tn=[[0, 109, 54, 77],
     [109, 0, 65, 12],
     [54, 65, 0, 10],
     [77, 12, 10, 0]]

 dis = tn[0][1]+ tn[1][3] + tn[3][0]
 

 

 tp_list=[]
 store_tp_list = ["101","102","103","104"]
 random.shuffle(store_tp_list)
 for s in store_tp_list:
    inn = Inventory.objects.filter(store_id = s )
    for i in inn:
        if i.inventory_quantity <10:
            if s not in tp_list:
                tp_list.append(s)
 district_tp_list=[]
 for tp in tp_list:
    store = Store.objects.filter(store_id = tp)
    for s in store:
        if s.store_district not in district_tp_list:
            district_tp_list.append(s.store_district)
 
 tc_list=[]
 store_tc_list = ["201","202","203","204","205"]
 random.shuffle(store_tc_list)
 for s in store_tc_list:
    inn = Inventory.objects.filter(store_id = s )
    for i in inn:
        if i.inventory_quantity <10:
            if s not in tp_list:
                tc_list.append(s)
 district_tc_list=[]
 for tc in tc_list:
    store = Store.objects.filter(store_id = tc)
    for s in store:
        if s.store_district not in district_tc_list:
            district_tc_list.append(s.store_district)


 tn_list=[]
 store_tn_list = ["301","302","303","304","305"]
 random.shuffle(store_tn_list)
 for s in store_tn_list:
    inn = Inventory.objects.filter(store_id = s )
    for i in inn:
        if i.inventory_quantity <10:
            if s not in tn_list:
                tn_list.append(s)
 district_tn_list=[]
 for tn in tn_list:
    store = Store.objects.filter(store_id = tn)
    for s in store:
        if s.store_district not in district_tn_list:
            district_tn_list.append(s.store_district)

 tp_min = district_tp_list
 tｃ_min = district_tc_list
 tｎ_min = district_tn_list




 return render(request,'待送訂單.html', locals())


def d_done_n(request):
    for s in ["101","102","103","104"]:
        inn = Inventory.objects.filter(store_id = s )
        for i in inn:
            if i.inventory_quantity <10:
                i.inventory_quantity += 10
                i.save()
    return render(request,'出貨成功北.html')

def d_done_m(request):
    for s in ["201","202","203","204","205"]:
        inn = Inventory.objects.filter(store_id = s )
        for i in inn:
            if i.inventory_quantity <10:
                i.inventory_quantity += 10
                i.save()
    return render(request,'出貨成功中.html')

def d_done_s(request):
    for s in ["301","302","303","304","305"]:
        inn = Inventory.objects.filter(store_id = s )
        for i in inn:
            if i.inventory_quantity <10:
                i.inventory_quantity += 10
                i.save()
    return render(request,'出貨成功南.html')


