from django.db import models

# Create your models here.
class Store(models.Model):
	store_id = models.CharField(max_length=20,primary_key = True)
	store_name = models.CharField(max_length=20)
	store_tel=models.CharField(max_length=20)
	store_address=models.CharField(max_length=20)
	store_district=models.CharField(max_length=10)

	def __str__(self):
		return self.store_name

class Customer(models.Model):
	customer_id = models.CharField(max_length = 20,primary_key = True)
	customer_name = models.CharField(max_length=20)
	customer_tel=models.CharField(max_length=20,blank=True)
	customer_address=models.CharField(max_length=20,blank=True)
	customer_age=models.DecimalField(max_digits=10,decimal_places=0)
	email=models.CharField(max_length=30,blank=True)
	num_familymembers=models.DecimalField(max_digits=10,decimal_places=0)
	register_date=models.DateField()
	monthly_income=models.DecimalField(max_digits=100,decimal_places=0)
	average_quantity = models.DecimalField(max_digits=100,decimal_places=0)
	customer_value = models.DecimalField(max_digits=40,decimal_places=4,blank=True,default=0)
	customer_rfm = models.CharField(max_length=5,blank=True)
	customer_logic = models.IntegerField(blank=True,default = 0)


	def __str__(self):
		return self.customer_id

class Company(models.Model):
	company_id = models.CharField(max_length=20,primary_key = True)
	company_name = models.CharField(max_length=20)
	company_tel=models.CharField(max_length=20)
	company_address=models.CharField(max_length=20)

	def __str__(self):
		return self.company_name

class Product(models.Model):
	product_id = models.CharField(max_length=20,primary_key = True)
	product_name = models.CharField(max_length=20)
	product_cost=models.DecimalField(max_digits=20,decimal_places=0)
	product_price=models.DecimalField(max_digits=20,decimal_places=0)
	company_id = models.ForeignKey(Company, on_delete= models.CASCADE)

	def __str__(self):
	    return self.product_id

class Warehouse(models.Model):
	warehouse_id = models.CharField(max_length=20,primary_key = True)
	warehouse_address = models.CharField(max_length=20)

	def __str__(self):
		return self.warehouse_id

class Inventory(models.Model):
	shoe_size = models.CharField(max_length=2)
	inventory_quantity = models.DecimalField(max_digits=10,decimal_places=0)
	product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
	store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

	#def __str__(self):
	#	s = str(self.product_id) + str(self.store_id) + str(self.shoe_size)
	#	return s

	def __str__(self):

	 	result = str(self.store_id)+","+str(self.product_id)+","+str(self.shoe_size)
	 	return result

	class Meta:
	 	unique_together = ("product_id","store_id","shoe_size")



class Storage(models.Model):
	shoe_size = models.CharField(max_length=20)
	product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
	storage_quantity = models.DecimalField(max_digits=10, decimal_places=0)
	company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
	warehouse_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

	def __str__(self):

	 	result = str(self.warehouse_id)+","+str(self.product_id)+","+str(self.shoe_size)
	 	return result
	class Meta:
	 	unique_together = ("product_id","warehouse_id","shoe_size")

class Order(models.Model):
	order_date = models.DateField()
	order_method = models.CharField(max_length=20)


	discount_rate = models.DecimalField(max_digits = 10, decimal_places = 3)
	customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
	size = models.CharField(max_length=20)


	def __str__(self):

		result = str(self.customer_id)+","+str(self.order_date)
		return result
