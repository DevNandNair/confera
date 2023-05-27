from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone



    

class Conference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    venue_name = models.CharField(max_length=100)
    venue_state = models.CharField(max_length=100)
    venue_city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', null=True)
    venue_booking_price = models.IntegerField()
    capacity = models.IntegerField()
    food = models.CharField(max_length=100)
    props = models.CharField(max_length=100)
    is_booked = models.BooleanField(default=False)
    starting_time = models.TimeField(null=True, blank=True)
    ending_time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def clean(self):
        if self.date and self.date < timezone.now().date():
            raise ValidationError("The date cannot be in the past.")

    # Alternatively, you can use clean_fields() to validate individual fields
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.date and self.date < timezone.now().date():
            raise ValidationError("The date cannot be in the past.") 

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=True)
    cvv = models.IntegerField()
    card_number = models.IntegerField()

    def clean(self):
        super().clean()
        # Implement any custom validation logic specific to the Payment model here
        if self.cvv and len(str(self.cvv)) != 3:
            raise ValidationError("CVV must be a 3-digit number.")

        if self.card_number and len(str(self.card_number)) != 16:
            raise ValidationError("Card number must be a 16-digit number.")
