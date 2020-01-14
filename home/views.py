from django.shortcuts import render

# Create your views here.
def choose_identification(request):
	return render(request,'產銷首頁.html')

def supplier_login(request):
	return render(request,'登入_廠商.html')

def company_login(request):
	return render(request,'登入_總公司.html')

def sales_login(request):
	return render(request,'登入_銷售人員.html')

def delivery_login(request):
	return render(request,'登入_送貨人員.html')