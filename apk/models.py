import random
from django.utils import timezone
from django.db import models
# Create your models here.
class usereg(models.Model):
    STATUS=(
        ('applied','Applied'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )
    username=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=10)
    location=models.CharField(max_length=30,blank=True,null=True)
    profilepic=models.ImageField(upload_to='profilepic/',blank=True,null=True)
    Aadhaar_No=models.CharField(unique=True,max_length=12,null=True,blank=True)
    phone=models.CharField(max_length=50,null=True,blank=True)
    Ward_No=models.CharField(max_length=20)
    status=models.CharField(max_length=20,choices=STATUS,default='applied')  
    otp = models.IntegerField(null=True, blank=True)  # Store OTP for verification


    def generate_otp(self):
        self.otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        self.save()
        return self.otp


from django.db import models
from django.utils import timezone

class Donor(models.Model):
    STATUS = (
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    Aadhaar_No = models.CharField(unique=True, max_length=12, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)
    total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    otp = models.IntegerField(null=True, blank=True)  # Store OTP for verification


    def __str__(self):
        return self.username
    
    def generate_otp(self):
        self.otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        self.save()
        return self.otp


class product(models.Model):
    productname=models.CharField(max_length=50)
    price=models.IntegerField()
    brand=models.CharField(max_length=50)
    description=models.CharField(max_length=1000)
    image=models.ImageField(upload_to='image/',blank=True,null=True)

class Camp(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email=models.EmailField()
    password=models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    contact_information = models.IntegerField(blank=True,null=True)
    Facilities = models.TextField()
    is_approved=models.BooleanField(default=False)
    # status=models.CharField(max_length=20,choices=STATUS,default='applied') 
    otp = models.IntegerField(null=True, blank=True)  # Store OTP for verification


    def generate_otp(self):
        self.otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        self.save()
        return self.otp

    def __str__(self):
        return self.name
    
class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('damage', 'Damage Report'),
        ('needs', 'Needs Assessment'),
    ]

    user = models.ForeignKey(usereg, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='reports/', blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_report_type_display()} by {self.user.username} on {self.reported_at}"
    

class Needs(models.Model):
    user = models.ForeignKey(Camp, on_delete=models.CASCADE)
    don=models.ForeignKey(Donor, on_delete=models.CASCADE,null=True,blank=True)
    needs_choices= (
        ('clothes','Clothes'),
        ('firstaid','First Aid Kit'),
        ('food','Food'),
        ('groceries','Groceries'),
        ('stationary','Stationary'),
        ('cash','Cash'),
    )
    needs = models.CharField(max_length=10, choices=needs_choices)
    amount_required=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    description = models.TextField()    



from django.db import models

class DonationRequest(models.Model):
    donor = models.ForeignKey('Donor', on_delete=models.CASCADE)
    need = models.ForeignKey('Needs', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.name} for {self.need}"



class DonationOffer(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    offered_item = models.CharField(max_length=255)
    offered_service = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('delivered', 'Delivered')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.donor.username} for {self.request.title}"

class DonationTracking(models.Model):
    offer = models.ForeignKey(DonationOffer, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('delivered', 'Delivered')])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking for {self.offer}"
    


class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Volunteer(models.Model):
    user = models.ForeignKey(usereg, on_delete=models.CASCADE, null=True, blank=True)
    STATUS=(
        ('applied','Applied'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    )
    email=models.EmailField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    Aadhaar_No=models.CharField(unique=True,max_length=12,null=True,blank=True)
    phone=models.CharField(max_length=50,null=True,blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other','Other'),
    ]
    age=models.CharField(max_length=2)
    skills = models.TextField() 
    location = models.CharField(max_length=255)
    profile_picture=models.ImageField(upload_to='vphoto/',blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    status=models.CharField(max_length=20,choices=STATUS,default='applied')
    otp = models.IntegerField(null=True, blank=True)  # Store OTP for verification


    def generate_otp(self):
        self.otp = random.randint(100000, 999999)  # Generate 6-digit OTP
        self.save()
        return self.otp 

    def __str__(self):
        return self.username


# Define a Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return self.title
class EvacuationRoute(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('P', 'Primary'),
        ('S', 'Secondary')
    ]
    
    # Locations
    start_location_name = models.CharField(max_length=100)
    end_location_name = models.CharField(max_length=100)
    
    # Additional Information
    distance_meters = models.FloatField()
    route_type = models.CharField(max_length=1, choices=ROUTE_TYPE_CHOICES, default='P')
    is_accessible = models.BooleanField(default=True)
    is_safe_zone = models.BooleanField(default=False)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.start_location_name} to {self.end_location_name} - {self.get_route_type_display()}"



# class Volunteer_Request(models.Model):
#     user = models.ForeignKey(Camp, on_delete=models.CASCADE, related_name='volunteer_requests')
#     days = models.PositiveIntegerField()
#     skills = models.ManyToManyField(Skill, related_name='volunteer_requests')  # Many-to-many relationship

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.name} - {self.days} days"

#     class Meta:
#         verbose_name = 'Volunteer Request'
#         verbose_name_plural = 'Volunteer Requests'

class Volunteer_Request(models.Model):
    # user = models.ForeignKey(Camp, on_delete=models.CASCADE)
    skills_choices= (
        ('communication','Communication'),
        ('firstaid','First Aid'),
        ('physical fitness','Physical Fitness'),
        ('technology skills','Technology Skills'),
        ('organzing skills','Organizing Skills'),
        ('others','Others'),
    )
    skills = models.CharField(max_length=30, choices=skills_choices)
    # needs_list = models.TextField()  # Comma-separated list of skills
    days = models.TextField()
    cname = models.CharField(max_length=255)
    cnumber = models.TextField()
    description = models.TextField() 



class v_Notification(models.Model):
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, null=True, blank=True)
    v_message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    skills_choices = (
        ('communication', 'Communication'),
        ('firstaid', 'First Aid'),
        ('physical fitness', 'Physical Fitness'),
        ('technology skills', 'Technology Skills'),
        ('organizing skills', 'Organizing Skills'),
        ('others', 'Others'),
    )
    skills = models.CharField(max_length=30, choices=skills_choices)
    start_day = models.DateField(null=True, blank=True, default=None)
    cnumber = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.v_message

  


from django.db import models
from .models import Camp, v_Notification, Volunteer

class Application(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)  
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)  
    notification = models.ForeignKey(v_Notification, on_delete=models.CASCADE)  
    message = models.TextField(blank=True, null=True)  
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  
    status_choices = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')  
    applied_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.volunteer.username} -> {self.camp.name} ({self.status})"






class Payment(models.Model):
    user = models.ForeignKey(Needs, on_delete=models.SET_NULL, null=True, blank=True, db_column="needs_id") 
    payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    order_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default prevents null issues
    verified = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    payment_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id or 'N/A'} - {self.payment_status} - {self.amount} INR"




