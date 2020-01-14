from django.shortcuts import render

from home.models import Customer,Product,Store,Order, Inventory

from django.http import HttpResponse

# Create your views here.

def sales(request):
 return render(request,'銷售人員.html')

def newmember(request):
 return render(request,'新增會員.html')

def newsales(request):
 return render(request,'加入購買資訊.html')

def checkinventory(request):

 inventory_list = []
 for i in Inventory.objects.all():
  tmp = []
  s = Store.objects.get(store_name = i.store_id)
  tmp.append(str(i.store_id))
  tmp.append(str(s.store_district)+'-'+str(i.product_id))
  tmp.append(i.shoe_size)
  tmp.append(i.inventory_quantity)
  inventory_list.append(tmp)


 store_list = []
 for a in Store.objects.all():
  store_list.append(a.store_district)
 return render(request,'存貨查詢系統.html',locals())


def new_member(request):
 if 'id' in request.POST:
  cus_id = request.POST['id']
 if 'name' in request.POST:
  cus_name = request.POST['name']
 if 'telnum' in request.POST:
  cus_tel =  request.POST['telnum']
 if 'address' in request.POST:
  cus_addr = request.POST['address']
 if 'age' in request.POST:
  cus_age = request.POST['age']
 if 'email' in request.POST:
  cus_email = request.POST['email']
 if 'family_mem' in request.POST:
  cus_family_mem = request.POST['family_mem']
 if 'income' in request.POST:
  cus_income = request.POST['income']
 if 'mean_quantity' in request.POST:
  cus_mean_quan = request.POST['mean_quantity']
 if 'date' in request.POST:
  cus_date = request.POST['date']

 member = Customer(customer_id = cus_id,customer_name = cus_name,customer_tel = cus_tel,customer_address = cus_addr,customer_age = cus_age,email = cus_email,num_familymembers = cus_family_mem,average_quantity = cus_mean_quan,register_date = cus_date, monthly_income = cus_income)
 member.save()

 return render(request,'新增成功.html')

def new_order(request):
 if 'date' in request.POST:
  order_date = request.POST['date']
 if 'pay_method' in request.POST:
  order_method = request.POST['pay_method']
 if 'discount_rate' in request.POST:
  order_discount = request.POST['discount_rate']
 if 'member_id' in request.POST:
  cid = request.POST['member_id']
  order_member = Customer.objects.get(customer_id = cid)
 if 'product_id' in request.POST:
  pid = request.POST['product_id']
  order_product = Product.objects.get(product_id = pid)
 if 'store_id' in request.POST:
  sid = request.POST['store_id']
  order_store = Store.objects.get(store_id = sid)
 if 'shoe_size' in request.POST:
  order_size = request.POST['shoe_size']


 o = Order(order_date = order_date,order_method = order_method,discount_rate = order_discount,customer_id = order_member,product_id = order_product,store_id = order_store,size = order_size)
 o.save()
 inn = Inventory.objects.get(shoe_size = order_size,product_id = order_product,store_id = order_store)
 if inn.inventory_quantity>0:
  inn.inventory_quantity -= 1
 inn.save()

 return render(request,'新增成功.html')
