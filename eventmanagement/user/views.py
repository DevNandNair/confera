from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.core.management import call_command
from django.contrib.auth.mixins import LoginRequiredMixin




def index(request):
    return render(request, "index.html")


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = auth.authenticate(request, username=username, password=pass1)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def conference_hall_details(request):
    # If the form has been submitted
    if request.GET.get('state') and request.GET.get('city'):
        # Get the selected state and city from the form
        selected_state = request.GET.get('state')
        selected_city = request.GET.get('city')
        # Query the Conference model to get all non-booked conference halls in the selected state and city
        conferences = Conference.objects.filter(
            Q(venue_state=selected_state) & Q(venue_city=selected_city) & Q(is_booked=False)
        )
    else:
        # If the form has not been submitted, display all non-booked conference halls
        conferences = Conference.objects.filter(is_booked=False)

    # Render the template with the list of conference halls
    return render(request, 'conference_hall_details.html', {'conferences': conferences})



class PaymentView(LoginRequiredMixin, View):
    def get(self, request, conference_id):
        # Retrieve the conference object
        conference = Conference.objects.get(id=conference_id)

        # Render the payment template with the conference object
        return render(request, 'payment.html', {'conference': conference})

    def post(self, request, conference_id):
        # Retrieve the authenticated user
        user = request.user

        # Retrieve the conference object
        conference = Conference.objects.get(id=conference_id)

        cvv = request.POST.get('cvv')
        card_number = request.POST.get('card_number')

        errors = []
        # Validate the form inputs
        if not cvv or not card_number:
            errors.append('All fields are required.')

        # Implement additional validation checks as per your requirements
        if cvv and len(str(cvv)) != 3:
            errors.append('CVV must be a 3-digit number.')

        if card_number and len(str(card_number)) != 16:
            errors.append('Card number must be a 16-digit number.')

        if errors:
            return render(request, 'payment.html', {'errors': errors, 'conference': conference})

        # Update the conference attributes with the form inputs
        conference.date = request.POST.get('date')
        conference.starting_time = request.POST.get('starting_time')
        conference.ending_time = request.POST.get('ending_time')
        conference.save()

        # Associate the conference with the authenticated user
        conference.user = user
        conference.is_booked = True
        conference.save()

        # Create the payment object and associate it with the conference and user
        payment = Payment.objects.create(
            conference=conference,
            cvv=cvv,
            card_number=card_number,
            user=user,
        )

        # Show success message
        messages.success(request, 'Payment successful!')

        return redirect('index')






@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    payments = Payment.objects.filter(user=user)  # Get payments made by the user
    conferences = [payment.conference for payment in payments]  # Get corresponding conferences

    return render(request, 'profile.html', {'conferences': conferences})


def contact(request):
    return render(request, 'contact.html')