from django.shortcuts import render

from home.models import Order,Customer, Product,Store
import time
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from statistics import mean
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


# Create your views here.
def rfm(request):

    #R
    customer_rec = {}
    for o in Order.objects.all():
        if o.customer_id not in customer_rec:
            customer_rec[o.customer_id] = []
    for o in Order.objects.all():
        customer_rec[o.customer_id].append(int(str(o.order_date).replace('-', '')))
    for c in customer_rec:
        customer_rec[c] = max(customer_rec[c])
    customer_rec = sorted(customer_rec.items(),key=lambda d: d[1], reverse=True)
    import math
    r = math.ceil(len(customer_rec)/3)
    R1, R2, R3 = customer_rec[:r], customer_rec[r:r*2], customer_rec[r*2:]

    #F
    customer_freq = {}
    for o in Order.objects.all():
        if o.customer_id not in customer_freq:
            customer_freq[o.customer_id] = 1
        else:
            customer_freq[o.customer_id] += 1
    customer_freq = sorted(customer_freq.items(),key=lambda d: d[1], reverse=True)
    f = math.ceil(len(customer_freq)/3)
    F1, F2, F3 = customer_freq[:f], customer_freq[f:f*2], customer_freq[f*2:]

    #M
    customer_val = {}
    for o in Order.objects.all():
        if o.customer_id not in customer_val:
            customer_val[o.customer_id] = 0
    for o in Order.objects.all():
        price = Product.objects.get(product_id=o.product_id).product_price
        customer_val[o.customer_id] += int(price)
    customer_val = sorted(customer_val.items(),key=lambda d: d[1], reverse=True)
    v = math.ceil(len(customer_val)/3)
    V1, V2, V3 = customer_val[:v], customer_val[v:v*2], customer_val[v*2:]

    return render(request, 'RFM.html', locals())

def manage(request):
 return render(request,'總公司.html')

def report(request):

 y,y_ms,ms_list = calculate_ms()
 y1,y_sg,sg_list = calculate_sg()
 y2,y_scr,scr_list = calculate_scr()
 best_sale()
 store_performance()
 return render(request,'銷售報表.html',locals())

def cusanalysis(request):
 rr_list,sr_list,rr_mean,year_list = rate_calculation()
 ltv_calculate(rr_mean)
 return render(request,'顧客分析.html',locals())

def cuscluster(request):
 return render(request,'顧客分群.html')


def calculate_ms():
 this_year =  time.localtime(time.time()).tm_year
 total_list = []
 sum_list=[]
 market_share_list=[]

 for y in range(2010,this_year+1):
  total_list.append(random.randint(190000,210000))
  o_list = Order.objects.filter(order_date__year = y)

  sum = 0
  for i in range(len(o_list)):
   price = o_list[i].product_id.product_price
   sum += price
  sum_list.append(sum)
  for i in range(len(total_list)):
   market_share =100*(sum_list[i]/total_list[i])
  market_share_list.append(market_share)
  this_year_ms = round(market_share_list[-1],4)

 year_list=[]
 for y in range(2010,this_year+1):
  year_list.append(str(y))
 x = year_list
 y = market_share_list
 plt.xticks(rotation=45)
 plt.xlabel("year")
 plt.ylabel("market share (%)")
 plt.plot(x,y)

 plt.savefig('home/static/home/img/market_share.png',transparent = True)
 plt.clf()

 return this_year,this_year_ms,market_share_list


def calculate_sg():
 this_year =  time.localtime(time.time()).tm_year
 sum_list=[]
 sales_growth_list=[]


 for y in range(2010,this_year+1):
  o_list = Order.objects.filter(order_date__year = y)

  sum = 0
  for i in range(len(o_list)):
   price = o_list[i].product_id.product_price
   sum += price
  sum_list.append(sum)

  sg=0

  for i in range(1,len(sum_list)):
   diff= sum_list[i]-sum_list[i-1]
   sg = 100*(diff/sum_list[i-1])
  sales_growth_list.append(sg)
  this_year_sg = round(sales_growth_list[-1],4)

 year_list=[]
 for y in range(2011,this_year+1):
  year_list.append(str(y))
 x = year_list
 y = sales_growth_list[1:]
 plt.xticks(rotation=45)
 plt.xlabel("year")
 plt.ylabel("sales growth (%)")
 plt.plot(x,y)
 plt.savefig('home/static/home/img/sales_growth.png',transparent = True)
 plt.clf()

 return this_year,this_year_sg,sales_growth_list


def calculate_scr():
    this_year = time.localtime(time.time()).tm_year
    scr_list=[]
    for y in range(2010,this_year+1):
        o_list = Order.objects.filter(order_date__year = y)
        average_sum = 0
        for o in o_list:
            cus = Customer.objects.get(customer_id=o.customer_id)
            average_sum += cus.average_quantity
        scr = 100*(len(o_list)/average_sum)
        scr_list.append(scr)
    this_year_scr = round(scr_list[-1],4)

    year_list=[]
    for y in range(2010,this_year+1):
          year_list.append(str(y))
    x = year_list
    y = scr_list
    plt.xticks(rotation=45)
    plt.xlabel("year")
    plt.ylabel("scr (%)")
    plt.plot(x,y)

    plt.savefig('home/static/home/img/scr.png',transparent = True)
    plt.clf()

    return this_year,this_year_scr,scr_list


def rate_calculation ():
 this_year =  time.localtime(time.time()).tm_year
 sum_list=[]
 market_share_list=[]
 retention_rate_list=[]

 for y in range(2011,this_year+1):
  customer_list=[]
  customer_list_prev=[]
  o_list = Order.objects.filter(order_date__year = y)

  for i in range(len(o_list)):
   member = o_list[i].customer_id
   customer_list.append(member)

  o_list_prev = Order.objects.filter(order_date__year = y-1)

  for i in range(len(o_list_prev)):
   member = o_list_prev[i].customer_id
   customer_list_prev.append(member)
   prev_num_of_cus = len(customer_list)

  s1=set(customer_list)
  s2=set(customer_list_prev)
  rr_cus_list=list(s1.intersection(s2))

  retention_rate = 100*(len(rr_cus_list)/prev_num_of_cus)
  retention_rate_list.append(round(retention_rate,2))
  mean_rr = mean(retention_rate_list)

  survival_rate_list =[]
  survival_rate_list.append(0)
  survival_rate_list[0]=retention_rate_list[0]
  for i in range(1,len(retention_rate_list)):
   temp = (0.01*retention_rate_list[i]) * (0.01*survival_rate_list[i-1])
   sr = 100*temp
   survival_rate_list.append(round(sr,2))

  year_list=[]
  for y in range(2011,this_year+1):
    year_list.append(str(y))

 return retention_rate_list,survival_rate_list,mean_rr,year_list


def ltv_calculate(rr):
  c_list = Customer.objects.all()
  c_id_list=[]
  for c in c_list:
      c_id = c.customer_id
      c_id_list.append(c_id)
      for c_id in c_id_list:
        o_list = Order.objects.filter(customer_id = c_id)
        sum = float(0)
        for i in range(len(o_list)):
            price = float(o_list[i].product_id.product_price)
            sum += price
        rr2 = 0.01*rr
        ltv = sum * (rr2/(1.07-rr2))
      c.customer_value = ltv
      c.save()

def collect_info(request):
        return render(request,"羅吉斯回歸.html")

def logistic_regression(request):
    #logistic regression
    customer_list = Customer.objects.all()
    sum_value = 0

#將目標變數"value"轉換為0與1
    for c in customer_list:
        sum_value += c.customer_value
    average_value = sum_value/len(customer_list)

    for c in customer_list:
        if c.customer_value >= average_value:
            c.customer_logic = 1
            c.save()
        else:
            c.customer_logic = 0
            c.save()

#分割自變數(X)與應變數(y)
    age_list=[]
    num_family_list=[]
    income_list=[]
    average_shoe_list=[]
    logic_list=[]

    for c in customer_list:
        age_list.append(c.customer_age)
        num_family_list.append(c.num_familymembers)
        income_list.append(c.monthly_income)
        average_shoe_list.append(c.average_quantity)
        logic_list.append(c.customer_logic)

    customer_dict = {
        "ages" : age_list,
        "family members" : num_family_list,
        "monthly incomes" : income_list,
        "average num of shoes" : average_shoe_list,
        "logistic signal" : logic_list
        }

    customer_df = pd.DataFrame(customer_dict)

    X = customer_df.iloc[:,0:4]
    y = customer_df["logistic signal"]

#建構羅吉斯迴歸模型
    logreg = LogisticRegression()
    logreg.fit(X,y)

    if 'age' in request.POST:
      cus_age = request.POST['age']
    if 'family_mem' in request.POST:
      cus_mem = request.POST['family_mem']
    if 'income' in request.POST:
      cus_income = request.POST['income']
    if 'mean_quantity' in request.POST:
      cus_mean = request.POST['mean_quantity']

    dic={
      "ages" : cus_age,
      "family members" : cus_mem,
      "monthly incomes" : cus_income,
      "average num of shoes" : cus_mean
    }

    df = pd.DataFrame(dic,index=[0])

    y_pred = logreg.predict(df[:])
    res = y_pred[0]
    ress=""
    if res == 0:
      ress = "此類顧客不適合投資!"
    else:
      ress = "此類顧客適合投資!"

    return render(request,'結果.html',locals())

    
def best_sale():
	this_year =  time.localtime(time.time()).tm_year
	o_list = Order.objects.filter(order_date__year = this_year)
	product1 = 0
	product2 = 0
	product3 = 0
	product4 = 0
	product5 = 0
	product_list=[]

	for p in Product.objects.all():
		if p not in product_list:
			product_list.append(p)


	
	for o in o_list:
		if o.product_id == product_list[0]:
			product1 += 1
		if o.product_id == product_list[1]:
			product2 += 1
		if o.product_id == product_list[2]:
			product3 += 1
		if o.product_id == product_list[3]:
			 product4 += 1
		if o.product_id == product_list[4]:
			product5 += 1


	dict = {
		"0001" : product1,
		"0002" : product2,
		"0003" : product3,
		"0004" : product4,
		"0005" : product5
		}

	dict_sorted = sorted(dict.items(),key=lambda d: d[1], reverse=True)
	df = pd.DataFrame(dict_sorted)

	labels = df[0] 
	size = df[1] 
	plt.pie(size,                           # 數值
        labels = labels,                # 標籤
        autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
        pctdistance = 0.6,              # 數字距圓心的距離
        textprops = {"fontsize" : 12},  # 文字大小
        shadow=True)
                            # 設定陰影
	plt.savefig('home/static/home/img/product.png',transparent = True)
	plt.clf()

	

	o_list_last = Order.objects.filter(order_date__year = this_year-1)
	product1_last = 0
	product2_last = 0
	product3_last = 0
	product4_last = 0
	product5_last = 0
	

	
	for o in o_list_last:
		if o.product_id == product_list[0]:
			product1_last += 1
		if o.product_id == product_list[1]:
			product2_last += 1
		if o.product_id == product_list[2]:
			product3_last += 1
		if o.product_id == product_list[3]:
			 product4_last += 1
		if o.product_id == product_list[4]:
			product5_last += 1


	dict_last = {
		"0001" : product1_last,
		"0002" : product2_last,
		"0003" : product3_last,
		"0004" : product4_last,
		"0005" : product5_last
		}

	dict_sorted_last = sorted(dict_last.items(),key=lambda d: d[1], reverse=True)
	df_last = pd.DataFrame(dict_sorted_last)

	labels_last = df_last[0] 
	size_last = df_last[1] 
	plt.pie(size_last,                           # 數值
        labels = labels_last,                # 標籤
        autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
        pctdistance = 0.6,              # 數字距圓心的距離
        textprops = {"fontsize" : 12},  # 文字大小
        shadow=True)
                            # 設定陰影
	plt.savefig('home/static/home/img/product_last.png',transparent = True)
	plt.clf()



def store_performance():
	this_year =  time.localtime(time.time()).tm_year
	o_list = Order.objects.filter(order_date__year = this_year)


	tp = 0
	tc = 0
	tn = 0
	store_list=[]
	for s in Store.objects.all():
		if s not in store_list:
			store_list.append(s.store_district)

	store_list.sort()

	for o in o_list:
		if o.store_id.store_district == store_list[0]:
			tc += 1
		if o.store_id.store_district == store_list[1]:
			tc += 1
		if o.store_id.store_district == store_list[2]:
			tc += 1
		if o.store_id.store_district == store_list[3]:
			tc += 1
		if o.store_id.store_district == store_list[4]:
			tc += 1
		
		if o.store_id.store_district == store_list[5]:
			tp += 1
		if o.store_id.store_district == store_list[6]:
			tp += 1
		if o.store_id.store_district == store_list[7]:
			tp += 1
		if o.store_id.store_district == store_list[8]:
			tp += 1

		if o.store_id.store_district == store_list[9]:
			tn += 1
		if o.store_id.store_district == store_list[10]:
			tn += 1
		if o.store_id.store_district == store_list[11]:
			tn += 1
		if o.store_id.store_district == store_list[12]:
			tn += 1
		if o.store_id.store_district == store_list[13]:
			tn += 1



	dict = {
		"Taipei" : tp,
		"Taichung" : tc,
		"Tainan" : tn,
		}

	dict_sorted = sorted(dict.items(),key=lambda d: d[1], reverse=True)

	df = pd.DataFrame(dict_sorted)

	labels = df[0] 
	size = df[1] 
	plt.pie(size,                           # 數值
        labels = labels,                # 標籤
        autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
        pctdistance = 0.6,              # 數字距圓心的距離
        textprops = {"fontsize" : 12},  # 文字大小
        shadow=True)
                            # 設定陰影
	plt.savefig('home/static/home/img/store.png',transparent = True)
	plt.clf()
