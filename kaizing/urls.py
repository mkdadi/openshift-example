
from django.conf.urls import url

from views import *

urlpatterns = [
	url(r'^dashboard/$', vendorlogin, name='vendorlogin'),
	url(r'^dashboard/(?P<vendor_id>\d+)/$', index, name='index'),
	url(r'^dashboard/(?P<vendor_id>\d+)/logout/$', vendorlogout, name='vendorlogout'),
	url(r'^dashboard/(?P<item_id>\d+)/$', viewitem, name='item'),
	url(r'^dashboard/(?P<vendor_id>\d+)/(?P<order_id>\d+)/cancel/$', cancelorder, name='cancelorder'),
	url(r'^dashboard/(?P<vendor_id>\d+)/(?P<order_id>\d+)/acknowledge/$', acknowledgeorder, name='acknowledgeorder'),
	url(r'^dashboard/(?P<vendor_id>\d+)/(?P<order_id>\d+)/complete/$', completeorder, name='completeorder'),
	url(r'^dashboard/(?P<vendor_id>\d+)/(?P<order_id>\d+)/dispatch/$', dispatchorder, name='dispatchorder'),
	url(r'^dashboard/(?P<vendor_id>\d+)/(?P<order_id>\d+)/view/$', vieworder, name='vieworder'),
	#Frontend URL's
	url(r'^$', home, name='home'),
	url(r'^menu/(?P<vendor_id>\d+)/$', menudisplay, name='menudisplay'),
	url(r'^vendors/$', vendordisplay, name='vendordisplay'),
	url(r'^checkout/$', checkout, name='checkout'),
	url(r'^orderstatus/$',orderstatus,name='orderstatus'),
]