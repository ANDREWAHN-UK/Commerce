from django.db import models
#  this is so a 1-to-1 user model can be built, i.e. each user=customer
from django.contrib.auth.models import User  

# Create your models here.


# customer means the person buying! 
# this is what was referred to with the import user. 
# CASCADE here  means that if this is deleted, the associated stuff is also deleted
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)    
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name


# product is the thing(in this case burger) being bought
# the property decorator instructs profucts to look for an image in the Products.image field
# if it finds one, the image is displayed
# if not, a blank image is displayed
class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	image = models.ImageField(null=True, blank=True)
	description = models.TextField(default='')

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
