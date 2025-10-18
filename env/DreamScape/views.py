from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q  
from django.db.models import Count
from django.core.mail import EmailMessage
import re
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, User, UserEvents, Payment # or your actual model names
from .forms import UpiPaymentForm,CardPaymentForm, NetbankingPaymentForm, PaytmPaymentForm
from .forms import ContactMessage
from .forms import ContactForm


# paymemt 
def pay_now(request, event_id):
    event = get_object_or_404(UserEvents, id=event_id)
    method = request.GET.get('method')

    if method == "upi":
        if request.method == "POST":
            form = UpiPaymentForm(request.POST)
            if form.is_valid():
                upi_id = form.cleaned_data['upi_id']
                txn_id = str(uuid.uuid4())

                Payment.objects.create(
                    user_event=event,
                    amount=event.amount,
                    upi_id=upi_id,
                    status="Success",
                    txn_id=txn_id
                )
                return render(request, "payment_success.html", {"event": event, "txn_id": txn_id})
        else:
            form = UpiPaymentForm()
        return render(request, "pay_upi.html", {"form": form, "event": event})
    elif method == "card":
        # Handle Credit/Debit Card payment
        if request.method == "POST":
            form = CardPaymentForm(request.POST)
            if form.is_valid():
                card_number = form.cleaned_data['card_number']
                txn_id = str(uuid.uuid4())
                Payment.objects.create(
                    user_event=event,
                    amount=event.amount,
                    card_number=card_number,
                    status="Success",
                    txn_id=txn_id
                )
                return render(request, "payment_success.html", {"event": event, "txn_id": txn_id})
        else:
            form = CardPaymentForm()
        return render(request, "pay_card.html", {"form": form, "event": event})

    elif method == "netbanking":
        # Handle Netbanking payment
        if request.method == "POST":
            form = NetbankingPaymentForm(request.POST)
            if form.is_valid():
                bank_account = form.cleaned_data['bank_account']
                txn_id = str(uuid.uuid4())
                Payment.objects.create(
                    user_event=event,
                    amount=event.amount,
                    bank_account=bank_account,
                    status="Success",
                    txn_id=txn_id
                )
                return render(request, "payment_success.html", {"event": event, "txn_id": txn_id})
        else:
            form = NetbankingPaymentForm()
        return render(request, "pay_netbanking.html", {"form": form, "event": event})

    elif method == "paytm":
        # Handle Paytm payment
        if request.method == "POST":
            form = PaytmPaymentForm(request.POST)
            if form.is_valid():
                paytm_number = form.cleaned_data['paytm_number']
                txn_id = str(uuid.uuid4())
                Payment.objects.create(
                    user_event=event,
                    amount=event.amount,
                    paytm_number=paytm_number,
                    status="Success",
                    txn_id=txn_id
                )
                return render(request, "payment_success.html", {"event": event, "txn_id": txn_id})
        else:
            form = PaytmPaymentForm()
        return render(request, "pay_paytm.html", {"form": form, "event": event})

    else:
        # If no valid payment method is selected, return an error or a fallback page
        return render(request, "payment_method_not_found.html", {"event": event})

# ✅ Event Booking
def User_event(request):
       # ✅ Check if user is logged in via custom session
    if 'user_id' not in request.session:
        messages.warning(request, "⚠️ Please sign up or log in first to book an event.")
        return redirect(f"/login/?next={request.path}")
    if request.method == "POST":
        name=request.POST['name']
        en=request.POST['eventname']
        email=request.POST['email']
        date=request.POST['date']
        mb=request.POST['mobile']
        mb1=request.POST['altmobile']
        amt=request.POST['amount']
        dis=request.POST['description']
        
        # ✅ Name validation: only letters and spaces, at least 2 characters
        if not re.match(r'^[A-Z][a-zA-Z ]{1,}$', name):
            messages.error(request, "Enter a valid name. It should start with a capital letter and contain only alphabets.")
            return redirect('userevent')
         # ✅ Validate mobile numbers (both primary and alternate)
        if not re.match(r'^[6-9]\d{9}$', mb):
            messages.error(request, "Enter a valid 10-digit mobile number starting with 6-9.")
            return redirect('userevent')  # Replace with the correct name of your booking page
        
        if mb1 and not re.match(r'^[6-9]\d{9}$', mb1):
            messages.error(request, "Enter a valid 10-digit alternate mobile number starting with 6-9.")
            return redirect('userevent')
         # Save to DB
        event = UserEvents.objects.create(
            name=name,
            email=email,
            eventname=en,
            date=date,
            mobile=mb,
            altmobile=mb1,
            amount=amt,
            description=dis
        )

        # Show message
        messages.success(request, 'Your event is booked successfully!')

        # Send email
        subject = f"Booking Confirmation for {name}"
        message = f"""
        Hi {name},

        Thank you for booking your event with us!

        Booking Details:
        Event: {en}
        Date: {date}
        Mobile: {mb}
        Alternate Mobile: {mb1}
        Amount: {amt}
        Description: {dis}

        We'll contact you soon to confirm all arrangements.

        Regards,
        Event Team
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        # Redirect to payment
        return redirect('payment', event_id=event.id)

    return render(request, 'book_event.html')
    
# ✅ payment page
# 
def payment_page(request, event_id):
    event = UserEvents.objects.get(id=event_id)
    return render(request, 'payment_page.html', {'event': event})

def choose_payment(request, event_id):
    event = UserEvents.objects.get(id=event_id)
    return render(request, 'choose_payment.html', {'event': event})

def pay_upi(request, event_id):
    if request.method == "POST":
        return redirect('payment_success')
    return render(request, 'pay_upi.html')

def pay_card(request, event_id):
    if request.method == "POST":
        return redirect('payment_success')
    return render(request, 'pay_card.html')

def pay_netbanking(request, event_id):
    if request.method == "POST":
        return redirect('payment_success')
    return render(request, 'pay_netbanking.html')

def pay_paytm(request, event_id):
    if request.method == "POST":
        return redirect('payment_success')
    return render(request, 'pay_paytm.html')

def payment_success(request):
    return render(request, 'payment_success.html')

#✅ signup page
def signup1(request):
    if request.method == "POST":
        print("Form submitted!")  

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
      

        errors = {}

#        # First name validation
        if not re.match(r'^[A-Za-z]{2,}$', fname):
            errors['fname'] = "First name should contain only letters and be at least 2 characters."

        # Last name validation
        if not re.match(r'^[A-Za-z]{2,}$', lname):
            errors['lname'] = "Last name should contain only letters and be at least 2 characters."
            # Phone number validation
        if not re.match(r'^[69]\d{9}$', phone):
            errors['phone'] = "Phone number should start with 6 or 9 and be exactly 10 digits."

         # Password match check
        if password != confirm_password:
            errors['password'] = "Passwords do not match."

        # If there are any errors, return them
        if errors:
            return render(request, 'signup.html', {'errors': errors, 'input': request.POST})

        # ✅ Simple user creation
        user = User(
            fname=fname,
            lname=lname,
            email=email,
            mobile=phone,
            password=password
        )
        user.save()


        return render(request, 'home.html', {'success': 'Signup successful!'})

 
    return render(request, 'signup.html', {'hide_auth_links': True})

# ✅ dashboard page
def dashboard(request):
    return render(request, 'dashboard.html')


# ✅ Home Page
def home(request):
    return render(request, 'home.html')

# ✅ Events Page
def events(request):
    return render(request, 'events.html')

# ✅ Booking Page
def booking(request):
    return render(request, 'booking.html')

# ✅ About Us Page
def about(request):
    return render(request, 'about.html')

# ✅ Contact Page
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        con=ContactMessage(name=name,email=email,message=message)
        con.save()

        # Sending Email (Optional)
        send_mail(
            f"Message from {name}",
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'contact.html')

# ✅ Engagement Page
def engagement(request):
    return render(request, 'engagement.html')

# ✅ Wedding Page
def wedding(request):
    return render(request, 'wedding.html')

# ✅ reception Page
def reception(request):
    return render(request, 'reception.html')

# ✅ Birthday Page
def birthday(request):
    return render(request, 'birthday.html')

# # ✅ bachelor Page
def bachelor(request):
    return render(request, 'bachelor.html')

# # ✅ bride & groom Page
def bride(request):
    return render(request, 'bride.html')

# # ✅ other events
def other_events(request):
   return render(request, 'other_events.html')

# ✅ admin login
def adminlogin(request):
    return render(request, 'adminlogin.html')
# ✅ Search Functionality
def search(request):
    query = request.GET.get('q', '')
    results = Event.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else []
    return render(request, 'search.html', {'query': query, 'results': results})


def login_view(request):
    next_url = request.GET.get('next') or 'home'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        customer = User.get_customer_by_email(email)

        if customer and customer.password == password:
            request.session['user_id'] = customer.id
            request.session['user_name'] = customer.fname
            messages.success(request, f"Welcome back, {customer.fname}!")

            return redirect(next_url)  # ✅ Go back to the page they came from
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home') 

# ✅ admin login
ADMIN_EMAIL = 'saniya4572@gmail.com'
ADMIN_PASSWORD = 'saniya4572'

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
           # 👇 Print statement to debug
        print(f"Email: {email}, Password: {password}")

        if email == 'saniya4572@gmail.com' and password == 'saniya4572':
            return redirect('dashboard')  # Make sure 'dashboard' is the name in urls.py
        else:
            messages.error(request, 'Invalid credentials. Try again.')

    return render(request, 'adminlogin.html')


# # ✅ Dashboard 
def dashboard(request):
    # Chart data for performance & highest booked
    event_data = UserEvents.objects.values('eventname').annotate(count=Count('eventname')).order_by('-count')
    labels = [entry['eventname'] for entry in event_data]
    counts = [entry['count'] for entry in event_data]

    # Extra context
    bookedevents = UserEvents.objects.all()
    count = UserEvents.objects.count()

    # Payment status map
    payment_status = {p.user_event.id: "Payment Successful" for p in Payment.objects.all()}

    context = {
        'labels': labels,
        'counts': counts,
        'bookedevents': bookedevents,
        'count': count,
        'payment_status': payment_status,  # If you want to display in dashboard
    }
    return render(request, 'dashboard.html', context)


def deleteevent(request, name, eventname):
    try:
        event = UserEvents.objects.filter(name=name, eventname=eventname).first()
        if event:
            event.delete()
            messages.success(request, "Event deleted successfully.")
        else:
            messages.error(request, "Event not found.")
    except Exception as e:
        messages.error(request, f"Error deleting event: {str(e)}")

    return redirect('dashboard')


def updateevent(request, name, eventname):
    request.session["name"] = name
    request.session["eventname"] = eventname
    try:
        userevent = UserEvents.objects.filter(name=name, eventname=eventname).first()
        if not userevent:
            messages.error(request, "Event not found.")
            return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('dashboard')

    return render(request, 'updateeventdetails.html', {
        'name': userevent.name,
        'eventname': userevent.eventname,
        'email': userevent.email,
        'date': userevent.date,
        'mobile': userevent.mobile,
        'altmobile': userevent.altmobile,
        'amount': userevent.amount,
        'description': userevent.description
    })


def updateeventdetails(request):
    name = request.session.get("name")
    eventname = request.session.get("eventname")

    if not name or not eventname:
        messages.error(request, "Session expired or invalid access. Please try again.")
        return redirect('dashboard')

    if request.method == 'POST':
        # Fetching form values
        updated_name = request.POST.get('name')
        updated_eventname = request.POST.get('eventname')
        semail = request.POST.get('email')
        date = request.POST.get('date')
        mobile = request.POST.get('mobile')
        altmobile = request.POST.get('altmobile')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        # Update in DB
        UserEvents.objects.filter(name=name, eventname=eventname).update(
            name=updated_name,
            eventname=updated_eventname,
            email=semail,
            date=date,
            mobile=mobile,
            altmobile=altmobile,
            amount=amount,
            description=description
        )

        # Send update email
        email = EmailMessage(
            "Event Booking",
            f"Hello {updated_name}, Your Booked Event is Updated by admin. Please check.",
            to=[semail]
        )
        email.send()

        messages.success(request, 'Event Updated Successfully. Check your mail for updates.')
        return redirect('dashboard')

    messages.error(request, "Invalid method. Please use the update button.")
    return redirect('dashboard')

# contact form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # Redirect to the contact page after success
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})