from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import utc
import jsonfield

# Create your models here.


class Vendor(models.Model):
	name = models.CharField(max_length=20)
	alias = models.CharField(max_length=10)
	description = models.TextField(default="")
	location = models.TextField(default="")
	delivery_time=models.DurationField(default=60)
	tax = models.IntegerField(null=True)
	username = models.CharField(max_length=10, blank=True)
	password = models.CharField(max_length=10, blank=True)
	is_authenticated = models.BooleanField(default=False)
	is_open = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Genre(models.Model):
	name = models.CharField(max_length=10, default='Select')
	vendor = models.ForeignKey(Vendor, related_name='genre')

	def __str__(self):
		return self.name


class Item(models.Model):
	vendor = models.ForeignKey(Vendor, related_name='item')
	genre = models.ForeignKey(Genre, related_name='item', default=True)
	name = models.CharField(max_length=200)
	delivery_charge = models.IntegerField(null=True)
	description = models.CharField(max_length=300, null=True, blank=True)
	price = models.IntegerField(null=False)
	isveg = models.BooleanField(default=True)
	num = models.IntegerField()#number of items in stock
	isavailable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class location(models.Model):
	name = models.CharField(max_length=15)
	id = models.IntegerField()
	id = models.AutoField(primary_key=True,unique=True)

	def __str__(self):
		return self.name

class timeSlot(models.Model):
	start_time = models.TimeField()
	end_time = models.TimeField()
	max_limit = models.TimeField()

	def __str__(self):
		return str(str(self.start_time)+"--"+str(self.end_time))

class Order(models.Model):
	ORDER_STATE_PLACED = "Placed"
	ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
	ORDER_STATE_COMPLETED = "Completed"
	ORDER_STATE_CANCELLED = "Cancelled"
	ORDER_STATE_DISPATCHED = "Dispatched"

	ORDER_STATE_CHOICES = (
	    (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
	    (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
	    (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
	    (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
	    (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
	)
	ORDER_FULFILLMENT_MODE_DELIVERY = "delivery"
	ORDER_FULFILLMENT_MODE_PICKUP = "pickup"

	ORDER_FULFILLMENT_MODE_CHOICES = (
	    (ORDER_FULFILLMENT_MODE_DELIVERY, ORDER_FULFILLMENT_MODE_DELIVERY),
	    (ORDER_FULFILLMENT_MODE_PICKUP, ORDER_FULFILLMENT_MODE_PICKUP)
	)

	name = models.CharField(max_length=20)
	phone = models.CharField(max_length=15, null=True, blank=True, default=None)
	email = models.EmailField()
	slot = models.ForeignKey(timeSlot)
	delivery_address = models.ForeignKey(location)
	vendor = models.ForeignKey(Vendor, related_name='orderer')
	items = jsonfield.JSONField(default={})
	# items = models.ManyToManyField(Item, related_name='orders', through ='OrderItem' ,null=True)
	order_state = models.CharField(max_length=100, choices=ORDER_STATE_CHOICES, default=ORDER_STATE_PLACED)
	order_total = models.FloatField(default=0)
	fulfillment_mode = models.CharField(max_length=10, choices=ORDER_FULFILLMENT_MODE_CHOICES,
                                        default=ORDER_FULFILLMENT_MODE_DELIVERY)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return u"Ordered by %s from %s"% (self.name, self.vendor.name)

	def cancancelorder(self):
		created = self.created
		now = datetime.datetime.utcnow().replace(tzinfo=utc)
		timediff = now-created
		timediff = timediff.total_seconds()
		timediff = timediff/60
		if timediff>5:
			return False
		else:
			return True
		
class Feedback(models.Model):
	name = models.CharField(max_length = 30)
	phone = models.CharField(max_length = 15)
	email = models.EmailField(null=True)
	message = models.TextField()
	
	def __str__(self):
		return u"%s says %s"%(self.name,self.message)

		# def calcitem(self):
		# 	arr = self.items.all()
		# 	itemset = set(arr)
		# 	ret = {}
		# 	for item in list(itemset):
		# 		ret[item]=0
		# 	for item in arr:
		# 		ret[item]+=1
		# 	return ret


# class OrderItem(models.Model):
# 	item = models.ForeignKey(Item, related_name='orderitem')
# 	order = models.ForeignKey(Order, related_name='orderitem')
# 	number = models.IntegerField(blank=True)


# class UserProfile(models.Model):
# 	user = models.ForeignKey(User, related_name='user_profile', unique=True, db_index=True)

# 	phone = models.CharField("Phone Number", blank=True, null=True, max_length=20, default=None, db_index=True)
# 	address = models.CharField("Address", max_length=200, blank=True, null=True, default=None)
# 	created = models.DateTimeField(auto_now_add=True)

# 	def __unicode__(self):
# 		return u"%s" % self.user
