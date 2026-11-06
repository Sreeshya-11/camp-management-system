from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from .models import usereg , product
from .models import Needs,Donor,Camp,Report,v_Notification,Notification,Volunteer,Volunteer_Request,DonationOffer, DonationRequest,DonationTracking
from .import models
from .models import Camp, Volunteer, v_Notification
# Create your views here.
def temp(request):
    return render(request,'temp.html')
def index(request):
    return render(request,'index.html')


def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        location=request.POST.get('location')
        Aadhaar_No=request.POST.get('Aadhaar_No')
        phone=request.POST.get('phone')
        Ward_No=request.POST.get('Ward_No')
        profilepic=request.FILES.get('profilepic')
        if models.usereg.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists');window.location.href='/register/';</script>")
        if models.usereg.objects.filter(Aadhaar_No=Aadhaar_No).exists():
            return HttpResponse("<script>alert('Aadhaar Number already exists');window.location.href='/register/';</script>")
        usereg(username=username,email=email,password=password,location=location,Aadhaar_No=Aadhaar_No,phone=phone,Ward_No=Ward_No,profilepic=profilepic,status='applied').save()
        return redirect('login')
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=usereg.objects.filter(email=email,password=password).first()
        if user:
            request.session['email']=email
            request.session['password']=password
            request.session['email']=user.email
            return redirect('home')
        else:
            error_msg="Invalid username or password"
            return render(request,'login.html',{'error_msg':error_msg})
    return render(request,'login.html')


def home(request):
    return render(request,'home.html')     

def profile(request):
    email=request.session.get('email')
    if email:
        user=usereg.objects.get(email=email)
        return render(request,'profile.html',{'user':user})
    else:
        return redirect('login')
    

def product1(request):
    if request.method=='POST':
        productname=request.POST.get('productname')
        price=request.POST.get('price')
        brand=request.POST.get('brand')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        product(productname=productname,price=price,brand=brand,description=description,image=image).save()
        return redirect('productlist')
    return render(request,'product1.html')

def productlist(request):
    prod=product.objects.all()
    return render(request,'productlist.html',{'prod':prod})

def profilelist(request):
    prof=usereg.objects.all()
    return render(request,'profilelist.html',{'prof':prof})

def editprofile(request):
    if request.method=='POST':
        email=request.session.get('email')
        user=usereg.objects.get(email=email)
        user.username=request.POST.get('username',user.username)
        user.password=request.POST.get('password',user.password)
        if 'profile_pic' in request.FILES:
            user.profilepic = request.FILES['profile_pic']
        
        user.save()
        return redirect('home')
    return render(request,'profile.html')


def deluser(request,id):
    temp=usereg.objects.get(id=id)
    temp.delete()
    return redirect('profilelist')


def delproduct(request,id):
    temp=product.objects.get(id=id)
    temp.delete()
    return redirect('productlist')
def delete_report(request, report_id):
    report = Report.objects.get(id=report_id)
    report.delete()
    return redirect('viewreport')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Camp

def camp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        contact_information = request.POST.get('contact_information')
        Facilities = request.POST.get('Facilities')

        if not name or not email or not password or not location or not contact_information or not Facilities:
            messages.error(request, "All fields are required.")
            return render(request, 'campform.html')

        if Camp.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'campform.html')

        camp = Camp.objects.create(
            name=name,
            email=email,
            password=password,
            location=location,
            contact_information=contact_information,
            Facilities=Facilities,
            is_approved=False
        )
        messages.success(request, "Registration successful! Awaiting approval.")
        return redirect('clogin')

    return render(request, 'campform.html')


def chome(request):
    return render(request,'chome.html')

def camplist(request):
    camps = Camp.objects.all()
    return render(request, 'camp_list.html', {'camps': camps})


def approve_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    camp.is_approved = True
    camp.save()
    messages.success(request, f"Camp {camp.name} has been approved.")
    return redirect('camplist')





def u_camplist(request):
    camps = Camp.objects.all()
    return render(request, 'u_camplist.html', {'camps': camps})

def clogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Camp.objects.filter(email=email, password=password).first()
        if user:
            if user.is_approved: 
                request.session['email'] = email
                request.session['password'] = password
                return redirect('chome')
            else:
                error_msg = "Your registration is pending approval. Please wait for admin approval."
                return render(request, 'clogin.html', {'error_msg': error_msg})
        else:
            error_msg = "Invalid email or password."
            return render(request, 'clogin.html', {'error_msg': error_msg})

    return render(request, 'clogin.html')


# def needs(request):
#     email = request.session.get('email')
#     user = Camp.objects.get(email=email)
#     if request.method == 'POST':
#         needs_list = request.POST.get('needs')
#         description = request.POST.get('description')
#         # Create a new Report instance
#         Needs.objects.create(
#             user=user,
#             needs=needs_list,
#             description=description,
#         )
#         return redirect('chome')   
#     return render(request, 'cneeds.html')


def create_report(request):
    if request.method == 'POST':
        email = request.session.get('email')
        user = usereg.objects.get(email=email)
        report_type = request.POST.get('report_type')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        photo = request.FILES.get('photo', None)
        
        # Create a new Report instance
        Report.objects.create(
            user=user,
            report_type=report_type,
            location=location,
            description=description,
            photo=photo
        )
        
        return redirect('viewreport')
    
    return render(request, 'createreport.html')


def viewreports(request):
    email=request.session.get('email')
    if email:
        user=usereg.objects.get(email=email)
        reports = Report.objects.filter(user=user)
       # Redirect to the login page or handle unauthenticated access as needed

   
        return render(request, 'viewreports.html', {'reports': reports})
    return redirect('viewreport')


def reportlist(request):
    reports = Report.objects.all()
    return render(request, 'reportlist.html', {'reports': reports})


def logout(request):
    request.session.flush()
    return redirect('index')

# views.py

from django.shortcuts import render, get_object_or_404
from .models import DonationRequest, DonationOffer, DonationTracking

# def donation_requests_view(request):
#     email=request.session.get('email')
#     if email:
#         reports = Needs.objects.all()
#     return render(request, 'donation_requests_view.html', {'reports': reports})
from django.shortcuts import render
from .models import Needs

# def donation_requests_view(request):
#     # Donor doesn't need to be logged in (they can view without logging in)
#     # Get the selected category from the GET request or default to "all"
#     category = request.GET.get('category', 'all')
    
#     # If a category is selected, filter by that category, else show all needs
#     if category == 'all':
#         reports = Needs.objects.all()  # Show all needs
#     else:
#         reports = Needs.objects.filter(needs=category)  # Filter by selected category
    
#     return render(request, 'donation_requests.html', {'reports': reports, 'selected_category': category})

def donation_offer_view(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)
    if request.method == 'POST':
        # Process donation offer
        email = request.session.get('email')
        user = Donor.objects.get(email=email)
        DonationOffer.objects.create(
            donor=user,
            request=donation_request,
            offered_item=request.POST['offered_item'],
            offered_service=request.POST.get('offered_service', '')
        )
    return render(request, 'offer.html', {'donation_request': donation_request})

def donation_tracking_view(request):
    email = request.session.get('email')
    user = Donor.objects.get(email=email)
    offers = DonationOffer.objects.filter(donor=user)
    return render(request, 'tracking.html', {'offers': offers})



from django.shortcuts import render, redirect
from .models import Donor
from django.utils import timezone

def donor_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        Aadhaar_No = request.POST.get('Aadhaar_No')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        errors = {}

        if Donor.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        
        if Aadhaar_No and Donor.objects.filter(Aadhaar_No=Aadhaar_No).exists():
            errors['Aadhaar_No'] = 'Aadhaar Number already exists'
        
        if errors:
            return render(request, 'donorregistration.html', {'errors': errors})

        donor = Donor.objects.create(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            Aadhaar_No=Aadhaar_No,
            address=address,
            bio=bio,
            profile_picture=profile_picture,
            registration_date=timezone.now(),
            total_donations=0.00
        )
        return redirect('donorlogin')

    return render(request, 'donorregistration.html')


def donor_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=Donor.objects.filter(email=email,password=password).first()
        if user:
            request.session['email']=email
            request.session['password']=password
            request.session['username'] = user.username  # Ensure this is set
            request.session['phone_number'] = user.phone_number
            return redirect('donorhome')
        else:
            error_msg="Invalid username or password"
            return render(request,'login.html',{'error_msg':error_msg})
    return render(request,'donorlogin.html')

def donorprofile(request):
    email = request.session.get('email')
    user = Donor.objects.get(email=email)
    donor_profile = Donor.objects.get(email=email)
    return render(request, 'donorprofile.html', {'donor_profile': donor_profile})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Donor

def editdonorprofile(request):
    email = request.session.get('email')  # Assuming the donor is logged in with their email in the session
    donor = Donor.objects.get(email=email)
    
    if request.method == 'POST':
        # Get the form data
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        
        # Update donor profile fields
        donor.username = username
        donor.phone_number = phone_number
        donor.email = email
        
        # Update password only if it has been provided
        if password:
            donor.password = password
        
        donor.address = address
        donor.bio = bio

        # If a new profile picture is provided, update it
        if profile_picture:
            donor.profile_picture = profile_picture
        
        # Save the updated donor profile
        donor.save()

        # Send success message
        messages.success(request, 'Profile updated successfully!')
        
        # Redirect to the profile page after update
        return redirect('donorprofile')  # Change 'donorprofile' to your actual profile page URL name
    
    return render(request, 'donorprofile.html', {'donor': donor})

def donorhome(request):
    return render(request,'donorhome.html')

def adlogin(request):
    if request.method=='POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        u = 'admin'
        p = 'admin'
        if name==u:
            if password==p:
                return redirect('adhome')
            else:
             return render(request,"adlogin.html")
        else:
             return render(request,"adlogin.html")
    else:
         return render(request,"adlogin.html")
def adhome(request):
    return render(request,'adhome.html')

def add_notification(request):
    if request.method == 'POST':  # Corrected 'post' to 'POST'
        message = request.POST.get('message')
        if message:  # Check if message is not empty
            Notification.objects.create(message=message)
            return redirect('notif_list_from_admin')  # Redirect to notifications view
        else:
            return render(request, 'addnotification.html', {'error': 'Message cannot be empty.'})
    else:
        return render(request, 'addnotification.html')   


def notif_list_from_admin(request):
    n= Notification.objects.all()
    return render(request,'notif_list_from_admin.html',{'n':n})



def notifications(request):
    user_notifications = models.v_Notification.objects.all()
    return render(request, 'notifications.html', {'notifications': user_notifications})





from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Application, v_Notification

def apply(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        application = Application.objects.create(name=name, email=email, message=message)
        v_Notification.objects.create(name="New Volunteer Application",email=email,v_message=f"Volunteer {name} has successfully applied. Message: {message}",is_read=False)
        return HttpResponse("Application submitted successfully! Notification sent.")
    return render(request, "apply.html")



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Volunteer

def vregister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        skills = request.POST.getlist('skills')  # Collect multiple skills
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        Aadhaar_No = request.POST.get('Aadhaar_No')

        # Validate required fields
        if not username or not password or not gender or not age or not location or not phone or not Aadhaar_No:
            messages.error(request, "All fields are required.")
            return render(request, 'vregister.html', {'messages': messages.get_messages(request)})

        if Volunteer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'vregister.html')

        if Volunteer.objects.filter(Aadhaar_No=Aadhaar_No).exists():
            messages.error(request, "Aadhaar Number already exists.")
            return render(request, 'vregister.html')

        # Convert list of skills to a comma-separated string
        skills_str = ','.join(skills) if skills else ""

        # Save to database
        volunteer = Volunteer.objects.create(
            email=email,
            username=username,
            password=password,
            gender=gender,
            age=age,
            skills=skills_str,
            location=location,
            phone=phone,
            Aadhaar_No=Aadhaar_No,
            status='applied'
        )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('vlogin')

    return render(request, 'vregister.html')





# Login View
def vlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Volunteer.objects.filter(email=email, password=password).first()

        if user:
            if user.status != 'approved':  # Check if user is approved
                messages.error(request, 'Your account is not approved yet.')
                return render(request, 'vlogin.html')

            request.session['email'] = email  # Store session
            request.session['user_id'] = user.id
            messages.success(request, 'Login successful!')
            return redirect('vdashboard')  # Redirect to dashboard
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'vlogin.html')

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Volunteer

def update_volunteer_status(request, volunteer_id):
    if request.method == "POST":
        volunteer = get_object_or_404(Volunteer, id=volunteer_id)
        new_status = request.POST.get("status")

        if new_status in ["approved", "rejected", "applied"]:
            volunteer.status = new_status
            volunteer.save()
            messages.success(request, f"Volunteer {volunteer.username} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status update.")

    return redirect('volunteerlist')  # Redirect back to the volunteer list page



def vdashboard(request):
    email = request.session.get('email')
    
    profile = Volunteer.objects.get(email=email)

    return render(request, 'vdashboard.html',{'user': profile})

def vprofile(request):
    email = request.session.get('email')
    
    profile = Volunteer.objects.get(email=email)
    return render(request, 'vprofile.html', {'profile': profile})
def editvprofile(request):
    email = request.session.get('email')  # Assuming the donor is logged in with their email in the session
    profile = Volunteer.objects.get(email=email)
    
    if request.method == 'POST':
        # Get the form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        skills = request.POST.get('skills')
        location = request.POST.get('location')
        profile_picture = request.FILES.get('profile_picture')
        
        # Update donor profile fields
        profile.email = email
        profile.location = location
        profile.skills=skills
        if password:
            profile.password = password
        profile.location = location
        if profile_picture:
            profile.profile_picture = profile_picture
        
        # Save the updated donor profile
        profile.save()

        # Send success message
        messages.success(request, 'Profile updated successfully!')
        
        # Redirect to the profile page after update
        return redirect('vprofile')  # Change 'donorprofile' to your actual profile page URL name
    
    return render(request, 'vprofile.html', {'profile': profile})



from .models import EvacuationRoute

def add_route(request):
    if request.method == 'POST':
   
        start_location_name = request.POST.get('start_location_name')
        end_location_name = request.POST.get('end_location_name')
        distance_meters = request.POST.get('distance_meters')
        route_type = request.POST.get('route_type')
        is_accessible = request.POST.get('is_accessible') == 'on'
        is_safe_zone = request.POST.get('is_safe_zone') == 'on'


        route = EvacuationRoute(
            start_location_name=start_location_name,
            end_location_name=end_location_name,
            distance_meters=distance_meters,
            route_type=route_type,
            is_accessible=is_accessible,
            is_safe_zone=is_safe_zone
        )
        route.save()

        return redirect('route_list')
    
    return render(request, 'add_route.html')

def route_list(request):
    routes = EvacuationRoute.objects.all()
    return render(request, 'route_list.html', {'routes': routes})

# evacuation/views.py
def edit_route(request, route_id):
    route = get_object_or_404(EvacuationRoute, id=route_id)
    
    if request.method == 'POST':
        # Updating the route with new data
        route.start_location_name = request.POST.get('start_location_name')
        route.end_location_name = request.POST.get('end_location_name')
        route.distance_meters = request.POST.get('distance_meters')
        route.route_type = request.POST.get('route_type')
        route.is_accessible = request.POST.get('is_accessible') == 'on'
        route.is_safe_zone = request.POST.get('is_safe_zone') == 'on'
        route.save()

        return redirect('route_list')
    
    return render(request, 'edit_route.html', {'route': route})
# evacuation/views.py
def delete_route(request, route_id):
    route = get_object_or_404(EvacuationRoute, id=route_id)
    
    if request.method == 'POST':
        route.delete()
        return redirect('route_list')
    
    return render(request, 'route_list.html')

def update_status(request):
    if request.method=='POST':
        email=request.POST.get('email')
        status=request.POST.get('status')
        if not email or not status:
            return redirect('profilelist')
        if status not in ['applied','approved','rejected']:
            return redirect('profilelist')
        constr=get_object_or_404(usereg,email=email)
        constr.status=status
        constr.save()
        return redirect(profilelist)


from django.shortcuts import render, redirect
from .models import v_Notification
from datetime import datetime

def camp_vol_req(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        v_message = request.POST.get('v_message', '')  # Prevent NULL constraint failure
        skills = request.POST.get('skills')
        cnumber = request.POST.get('cnumber')
        start_day = request.POST.get('start_day')

        if start_day:
            try:
                start_day = datetime.strptime(start_day, '%Y-%m-%d').date()
            except ValueError:
                start_day = None

        v_Notification.objects.create(
            name=name,
            email=email,
            v_message=v_message,  # Now always has a value
            skills=skills,
            start_day=start_day,
            cnumber=cnumber
        )
        return redirect('chome')

    return render(request, 'camp_vrequest.html')





def volunteerlist(request):
    volunteers = Volunteer.objects.all()
    return render(request, 'volunteerlist.html', {'volunteers': volunteers})



def volunteer_requests_view(request):
    email=request.session.get('email')
    if email:
        req = Volunteer_Request.objects.all()
        
       # Redirect to the login page or handle unauthenticated access as needed   
    return render(request, 'volunteer_requests_view.html', {'req': req})


def vol_notification(request):
    if request.method == 'POST':  # Corrected 'post' to 'POST'
        name = request.POST.get('name')
        email = request.POST.get('email')
        vol_message = request.POST.get('vol_message')
        if vol_message:  # Check if message is not empty
            v_Notification.objects.create(v_message=vol_message,name=name,email=email).save()
            alert="<script>alert('Applied Successfully');window.location.href='/volunteer_requests_view/';</script>"
            return HttpResponse(alert)  # Redirect to notifications view
        else:
            return render(request, 'vol_notification.html', {'error': 'Message cannot be empty.'})
    else:
        return render(request, 'vol_notification.html')
    

def v_notifications(request):
    user_notifications = v_Notification.objects.all()
    return render(request, 'v_notifications.html', {'v_notifications': user_notifications})


def detail(request,vol_id):
    detail_vol=Volunteer.objects.get(id=vol_id)
    return render(request,'detail.html',{'detail_info': detail_vol})




def donation_form(request):
    camps = Camp.objects.all()
    needs = Needs.objects.first() 
    return render(request, 'donation_form.html', {'camps': camps, 'needs': needs})


from django.shortcuts import render, redirect
from .models import Needs, Camp

def needs(request):
    email = request.session.get('email')
    user = Camp.objects.get(email=email)
    
    if request.method == 'POST':
        needs_list = request.POST.get('needs')
        description = request.POST.get('description')
        amount_required = request.POST.get('amount_required')

        # Create a new Needs report
        new_need = Needs(
            user=user,
            needs=needs_list,
            description=description
        )

        # If the selected need is 'cash', set the amount_required field
        if needs_list == "cash":
            if amount_required:
                new_need.amount_required = amount_required
            else:
                # Handle the case where the amount is not entered (if necessary)
                new_need.amount_required = 0  # Or some default value

        # Save the new need report to the database
        new_need.save()

        return redirect('chome')  # Redirect to the home page or wherever you want

    return render(request, 'cneeds.html')





def payment(request,nid):
    nid=models.Needs.objects.get(id=nid)
    return render(request,'payment_form.html',{'nid':nid})




import json
from django.http import JsonResponse
from django.shortcuts import render
import razorpay
from .models import Needs

RAZOR_KEY_ID = 'rzp_test_X5OfG2jiWrAzSj'
RAZOR_KEY_SECRET = 'SsCovWWZSwB1TGd1rSoIiwF3'

def payment_form(request, nid):
    try:
        need = Needs.objects.get(id=nid)
    except Needs.DoesNotExist:
        return JsonResponse({'error': 'Need not found'}, status=404)

    if request.method == 'GET':
        return render(request, 'payment_form.html', {'nid': need})

    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')

        if not amount:
            return JsonResponse({'error': 'Amount is required'}, status=400)

        client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
        order = client.order.create({
            'amount': amount * 100,
            'currency': 'INR',
            'payment_capture': '1'
        })

        return JsonResponse({
            'razorpay_key_id': RAZOR_KEY_ID,
            'amount': amount,
            'order_id': order['id']
        })
    

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Payment  # Ensure you import the Payment model

RAZOR_KEY_ID = 'rzp_test_X5OfG2jiWrAzSj'
RAZOR_KEY_SECRET = 'SsCovWWZSwB1TGd1rSoIiwF3'

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from .models import Payment  # Ensure you import the Payment model

RAZOR_KEY_ID = 'rzp_test_X5OfG2jiWrAzSj'
RAZOR_KEY_SECRET = 'SsCovWWZSwB1TGd1rSoIiwF3'

@csrf_exempt  # Disable CSRF for this view, since Razorpay will make a POST request here
def confirm_payment(request):
    if request.method == 'POST':
        try:
            # Load the data from the POST request body
            data = json.loads(request.body)

            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')

            # Ensure all necessary data is provided
            if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
                return JsonResponse({'success': False, 'error': 'Missing payment details'}, status=400)

            # Initialize Razorpay client
            client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            # Verify the payment signature using the Razorpay client (Correct method)
            client.payment.verify_payment_signature(params)

            # If signature is verified, update the payment status
            payment = Payment.objects.get(payment_id=razorpay_payment_id)
            payment.verified = True
            payment.payment_status = 'CONFIRMED'
            payment.save()

            # return JsonResponse({'success': True, 'message': 'Payment successfully verified'})
            return HttpResponse("<script>alert('Payment successfully verified');window.location.href='/donorhome/';</script>")
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)

        except Payment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Payment not found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# #payment 2
# import razorpay
# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import get_object_or_404
# from .models import Payment, Needs, Camp, Donor
# from django.conf import settings

# import json
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt

# # Initialize Razorpay client
# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



# @csrf_exempt
# def initiate_payment1(request, camp_id, amount):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             print(f"Request Data: {data}")  # Debugging Log

#             donor_id = data.get("donor_id")
#             if not donor_id:
#                 return JsonResponse({"error": "Donor ID is missing."}, status=400)

#             # Ensure donor_id is an integer
#             donor_id = int(donor_id)

#             donor = get_object_or_404(Donor, id=donor_id)
#             camp = get_object_or_404(Camp, id=camp_id)

#             amount_in_paise = int(amount) * 100  # Convert to paise

#             order_data = {
#                 "amount": amount_in_paise,
#                 "currency": "INR",
#                 "payment_capture": 1
#             }
#             order = razorpay_client.order.create(order_data)

#             payment = Payment.objects.create(
#                 user=donor, order_id=order["id"], amount=amount, payment_status="PENDING"
#             )

#             return JsonResponse({
#                 "order_id": order["id"],
#                 "amount": amount_in_paise,
#                 "donation_id": payment.id
#             })

#         except Exception as e:
#             print(f"Error: {str(e)}")  # Debugging Log
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)



# @csrf_exempt
# def confirm_payment1(request, order_id, payment_id, donation_id):
#     if request.method == "POST":
#         try:
#             payment = get_object_or_404(Payment, id=donation_id, order_id=order_id)

#             # Extract Razorpay signature from request
#             data = json.loads(request.body)
#             signature = data.get("razorpay_signature")

#             # Verify Razorpay payment signature
#             params_dict = {
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             razorpay_client.utility.verify_payment_signature(params_dict)

#             # Update payment details
#             payment.payment_id = payment_id
#             payment.razorpay_signature = signature
#             payment.payment_status = "CONFIRMED"
#             payment.verified = True
#             payment.save()

#             return JsonResponse({"status": "success"})

#         except razorpay.errors.SignatureVerificationError:
#             return JsonResponse({"status": "error", "message": "Invalid payment signature"}, status=400)

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=400)





RAZOR_KEY_ID = 'rzp_test_X5OfG2jiWrAzSj'
RAZOR_KEY_SECRET = 'SsCovWWZSwB1TGd1rSoIiwF3'


from django.http import JsonResponse
import json
import razorpay
from .models import Payment, Needs
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment_form1(request, camp_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            donor_id = data.get("donor_id")
            needs_id = data.get("needs_id")
            amount = data.get("amount")

            if not donor_id or not needs_id or not amount:
                return JsonResponse({"error": "Invalid data received"}, status=400)

            try:
                needs_instance = Needs.objects.get(id=needs_id)
            except Needs.DoesNotExist:
                return JsonResponse({"error": "Needs ID is invalid"}, status=404)

            payment = Payment.objects.create(
                user=needs_instance, 
                amount=amount,
                payment_status='PENDING',
            )

            order = client.order.create({
                "amount": int(amount) * 100,
                "currency": "INR",
                "payment_capture": "1"
            })

            payment.order_id = order["id"]
            payment.save()

            return JsonResponse({
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "order_id": order["id"]
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON received"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def confirm_payment1(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_signature = data.get('razorpay_signature')

            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                return JsonResponse({'success': False, 'error': 'Missing payment details'}, status=400)

            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.verified = True
            payment.payment_status = 'CONFIRMED'
            payment.payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()

            return JsonResponse({'success': True, 'message': 'Payment successfully verified'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



from django.shortcuts import redirect
from .models import Payment, Needs

def cleanup_invalid_payments(request):
    invalid_payments = Payment.objects.exclude(user__in=Needs.objects.all())
    invalid_payments.delete()
    return redirect('/')
#


from django.http import JsonResponse
from .models import Payment

def check_payments(request):
    payments = Payment.objects.all().values("id", "user_id", "amount", "payment_status")
    return JsonResponse(list(payments), safe=False)



def fix_broken_payments(request):
    Payment.objects.exclude(user_id__in=Needs.objects.values_list('id', flat=True)).delete()
    return JsonResponse({"status": "Deleted broken payments"})




from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Camp, v_Notification

def v_notif_from_camp(request):
    if 'email' in request.session:
        semail = request.session['email']
        try:
            camp = Camp.objects.get(email=semail)
        except Camp.DoesNotExist:
            return HttpResponse("<script>alert('Camp not found'); window.location.href='/clogin/';</script>")
        notifications = v_Notification.objects.filter(email=camp.email) 
        return render(request, 'v_notif_from_camp.html', {'camp': camp, 'notifications': notifications})
    return redirect('clogin')



from django.shortcuts import render
from .models import v_Notification, Camp

def v_notif_to_volunteer(request):
    notifications = v_Notification.objects.all()
    camps = Camp.objects.all()
    return render(request, 'v_notif_to_volunteer.html', {'notifications': notifications, 'camps': camps})



def apply2(request, nid):
    if 'email' in request.session:
        email = request.session['email']
        volunteer = get_object_or_404(Volunteer, email=email)
        notification = get_object_or_404(v_Notification, id=nid)
        camp=get_object_or_404(Camp,email=notification.email)
        # Explicitly get the camp from notification to ensure it's available
        # camp = notification.camp
        
        if camp is None:
            return HttpResponse("<script>alert('Camp not found');window.location.href='/v_notif_to_volunteer/';</script>")
        
        if Application.objects.filter(volunteer=volunteer, notification=notification).exists():
            return HttpResponse("<script>alert('You already applied');window.location.href='/v_notif_to_volunteer/';</script>")
        
        if request.method == 'POST' and request.FILES.get('resume'):
            resume = request.FILES['resume']
            message = request.POST.get('message')
            
            # Create application with the retrieved camp
            Application.objects.create(
                volunteer=volunteer,
                camp=camp,
                notification=notification,
                resume=resume,
                message=message,
                status='pending'
            )
            return HttpResponse("<script>alert('Applied successfully');window.location.href='/v_notif_to_volunteer/';</script>")
        
        # Pass both notification and camp to the template
        context = {
            'notification': notification,
            'camp': camp
        }
        return render(request, 'apply2.html', context)
    
    return HttpResponse("<script>alert('Login required');window.location.href='/vlogin/';</script>")


def applications(request):
    if 'email' in request.session:
        email = request.session['email']
        volunteer = get_object_or_404(Volunteer, email=email)
        applications = Application.objects.filter(volunteer=volunteer)
        return render(request, 'applications.html', {'applications': applications})
    return HttpResponse("<script>alert('Login required');window.location.href='/vlogin/';</script>")




def camp_applications(request):
    if 'email' in request.session:
        email = request.session['email']
        camp = get_object_or_404(Camp, email=email)
        applications = Application.objects.filter(camp=camp)
        return render(request, 'camp_applications.html', {'applications': applications, 'camp': camp})
    return HttpResponse("<script>alert('Login required');window.location.href='/clogin/';</script>")

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import Application

def update_application_status(request, application_id):
    if 'email' in request.session:
        application = get_object_or_404(Application, id=application_id)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'accepted', 'rejected']:
            application.status = new_status
            application.save()
        return redirect('camp_applications') 
    return HttpResponse("<script>alert('Login required');window.location.href='/clogin/';</script>")



def donation_details(request):
    if 'email' in request.session:
        email = request.session['email']
        donor = get_object_or_404(Donor, email=email)
        donations = models.DonationRequest.objects.filter(donor=donor)
        return render(request, 'donation_details.html', {'donations': donations, 'donor': donor})
    return HttpResponse("<script>alert('Login required');window.location.href='/clogin/';</script>")



import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Needs, Donor, DonationRequest

def donation_requests_view(request):
    reports = Needs.objects.all()
    return render(request, "donation_requests.html", {"reports": reports})


@csrf_exempt
def confirm_donation(request, need_id):
    if request.method == "POST":
        try:
            if 'email' not in request.session:
                return JsonResponse({'error': 'User not logged in'}, status=400)

            email = request.session['email']
            name = request.session.get('username', '')
            phone = request.session.get('phone_number', '')

            donor, _ = Donor.objects.get_or_create(email=email, defaults={'username': name, 'phone_number': phone})
            donor.username = name
            donor.phone_number = phone
            donor.save()

            need = get_object_or_404(Needs, id=need_id)
            DonationRequest.objects.create(donor=donor, need=need, name=name, phone=phone, email=email)

            return JsonResponse({'success': 'Donation confirmed!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.http import JsonResponse

def get_user_session(request):
    if 'email' not in request.session:
        return JsonResponse({'error': 'User not logged in'}, status=400)

    return JsonResponse({
        'username': request.session.get('username', ''),
        'email': request.session.get('email', ''),
        'phone_number': request.session.get('phone_number', '')
    })




def notif_from_camp_to_evry1(request):
    if 'email' not in request.session:
        return HttpResponse("<script>alert('Login required');window.location.href='/clogin/';</script>")
    camp = Camp.objects.filter(email=request.session['email']).first()
    if not camp:
        return HttpResponse("<script>alert('Camp not found');window.location.href='/chome/';</script>")
    if request.method == 'POST':
        message=request.POST.get('message')
        Notification.objects.create(message=message)
        return HttpResponse("<script>alert('Notification Sended');window.location.href='/chome/';</script>")
    return render(request, 'notif_from_camp_to_evry1.html', {'camp': camp})


def not_list_from_camp(request):
    if 'email' not in request.session:
        return redirect('clogin')
    email = request.session['email']
    camp = get_object_or_404(Camp, email=email)
    notifications = Notification.objects.all()
    return render(request, 'not_list_from_camp.html', {'n': notifications, 'camp': camp})

def delete_notif(request,id):
    n=models.Notification.objects.get(id=id)
    n.delete()
    return redirect('not_list_from_camp')


def delete_all_notifs(request):
    models.Notification.objects.all().delete()
    return redirect('not_list_from_camp')


def notif_on_user(request):
    n=models.Notification.objects.all()
    return render(request,'notif_on_user.html',{'n':n})




#donor
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import Donor
import random
import time

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Donor.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            request.session['reset_email'] = email
            request.session['otp_timestamp'] = time.time()

            return redirect('verify_otp')
        except Donor.DoesNotExist:
            return HttpResponse("<script>alert('Email not found'); window.location.href='/forgot-password/';</script>")
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')
        otp_timestamp = request.session.get('otp_timestamp', 0)

        if time.time() - otp_timestamp > 30:
            return HttpResponse("<script>alert('OTP expired! Request a new one.'); window.location.href='/forgot-password/';</script>")
        try:
            user = Donor.objects.get(email=email)
            if str(user.otp) == otp_entered:
                return redirect('reset_password')
            else:
                return HttpResponse("<script>alert('Invalid OTP'); window.location.href='/verify-otp/';</script>")
        except Donor.DoesNotExist:
            return redirect('forgot_password')
    return render(request, 'verify_otp.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('new_password')
        try:
            user = Donor.objects.get(email=email)
            user.password = new_password
            user.otp = None
            user.save()
            return HttpResponse("<script>alert('Password reset successful!'); window.location.href='/login/';</script>")
        except Donor.DoesNotExist:
            return redirect('forgot_password')
    return render(request, 'reset_password.html')



#user
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import usereg
import random
import time

def forgot_pwd_emp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = usereg.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            request.session['reset_email'] = email
            request.session['otp_timestamp'] = time.time()

            return redirect('verify_otp_emp')
        except usereg.DoesNotExist:
            return HttpResponse("<script>alert('Email not found'); window.location.href='/forgot_pwd_emp/';</script>")
    return render(request, 'forgot_pwd_emp.html')

def verify_otp_emp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')
        otp_timestamp = request.session.get('otp_timestamp', 0)

        if time.time() - otp_timestamp > 30:
            return HttpResponse("<script>alert('OTP expired! Request a new one.'); window.location.href='/forgot_pwd_emp/';</script>")
        try:
            user = usereg.objects.get(email=email)
            if str(user.otp) == otp_entered:
                return redirect('reset_password_emp')
            else:
                return HttpResponse("<script>alert('Invalid OTP'); window.location.href='/verify_otp_emp/';</script>")
        except usereg.DoesNotExist:
            return redirect('forgot_pwd_emp')
    return render(request, 'verify_otp_emp.html')

def reset_password_emp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('new_password')
        try:
            user = usereg.objects.get(email=email)
            user.password = new_password
            user.otp = None
            user.save()
            return HttpResponse("<script>alert('Password reset successful!'); window.location.href='/login/';</script>")
        except usereg.DoesNotExist:
            return redirect('forgot_pwd_emp')
    return render(request, 'reset_password_emp.html')



#Volunteer
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import Volunteer
import random
import time

def forgot_pwd_vol(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Volunteer.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            request.session['reset_email'] = email
            request.session['otp_timestamp'] = time.time()

            return redirect('verify_otp_vol')
        except Volunteer.DoesNotExist:
            return HttpResponse("<script>alert('Email not found'); window.location.href='/forgot_pwd_vol/';</script>")
    return render(request, 'forgot_pwd_vol.html')

def verify_otp_vol(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')
        otp_timestamp = request.session.get('otp_timestamp', 0)

        if time.time() - otp_timestamp > 30:
            return HttpResponse("<script>alert('OTP expired! Request a new one.'); window.location.href='/forgot_pwd_vol/';</script>")
        try:
            user = Volunteer.objects.get(email=email)
            if str(user.otp) == otp_entered:
                return redirect('reset_password_vol')
            else:
                return HttpResponse("<script>alert('Invalid OTP'); window.location.href='/verify_otp_vol/';</script>")
        except Volunteer.DoesNotExist:
            return redirect('forgot_pwd_vol')
    return render(request, 'verify_otp_vol.html')

def reset_password_vol(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('new_password')
        try:
            user = Volunteer.objects.get(email=email)
            user.password = new_password
            user.otp = None
            user.save()
            return HttpResponse("<script>alert('Password reset successful!'); window.location.href='/vlogin/';</script>")
        except Volunteer.DoesNotExist:
            return redirect('forgot_pwd_vol')
    return render(request, 'reset_password_vol.html')




#Camp
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import Camp
import random
import time

def fpwd_camp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Camp.objects.get(email=email)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()

            subject = "Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

            request.session['reset_email'] = email
            request.session['otp_timestamp'] = time.time()

            return redirect('votp_camp')
        except Camp.DoesNotExist:
            return HttpResponse("<script>alert('Email not found'); window.location.href='/fpwd_camp/';</script>")
    return render(request, 'fpwd_camp.html')

def votp_camp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp_entered = request.POST.get('otp')
        otp_timestamp = request.session.get('otp_timestamp', 0)

        if time.time() - otp_timestamp > 30:
            return HttpResponse("<script>alert('OTP expired! Request a new one.'); window.location.href='/fpwd_camp/';</script>")
        try:
            user = Camp.objects.get(email=email)
            if str(user.otp) == otp_entered:
                return redirect('rpwd_camp')
            else:
                return HttpResponse("<script>alert('Invalid OTP'); window.location.href='/votp_camp/';</script>")
        except Camp.DoesNotExist:
            return redirect('fpwd_camp')
    return render(request, 'votp_camp.html')

def rpwd_camp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('new_password')
        try:
            user = Camp.objects.get(email=email)
            user.password = new_password
            user.otp = None
            user.save()
            return HttpResponse("<script>alert('Password reset successful!'); window.location.href='/clogin/';</script>")
        except Camp.DoesNotExist:
            return redirect('fpwd_camp')
    return render(request, 'rpwd_camp.html')

from django.shortcuts import render, get_object_or_404
from geopy.geocoders import Nominatim
from .models import Report

def view_on_map(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(report.location) if report.location else None

    latitude = location.latitude if location else None
    longitude = location.longitude if location else None

    return render(request, 'view_on_map.html', {
        'report': report,
        'latitude': latitude,
        'longitude': longitude
    })
