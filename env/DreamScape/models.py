from django.db import models
from django.contrib.auth.models import User


# user model
class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
   

    def __str__(self):
        return f"{self.fname}-{self.lname}"
    
    @staticmethod
    def get_customer_by_email(email):
        try:
            return User.objects.get(email=email)
        except:
            return False

class UserEvents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Link to your custom User model
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    eventname = models.CharField(max_length=200, blank=False)  # ✅ Add this line
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    mobile = models.CharField(max_length=200, blank=False)
    altmobile = models.CharField(max_length=200, blank=False)
    amount = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, default='', blank=False)


#event

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

# payment
class Payment(models.Model):
    user_event = models.ForeignKey('UserEvents', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_id = models.CharField(max_length=255, null=True, blank=True)
    txn_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='Pending')