"""
forms.py — Django forms for user input.

Forms:
  - SignupForm   : register a new user
  - BookingForm  : choose number of seats
  - ReviewForm   : write a review (rating + comment)
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review


class SignupForm(UserCreationForm):
    """Extended registration form that also collects email."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class BookingForm(forms.ModelForm):
    """Form to choose how many seats to book."""

    class Meta:
        model = Booking
        fields = ['seats_booked']
        widgets = {
            'seats_booked': forms.NumberInput(attrs={
                'min': 1, 'max': 10,
                'class': 'form-input',
                'placeholder': 'Number of seats'
            })
        }
        labels = {
            'seats_booked': 'Number of Seats'
        }

    def __init__(self, *args, available_seats=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.available_seats = available_seats

    def clean_seats_booked(self):
        seats = self.cleaned_data['seats_booked']
        if seats < 1:
            raise forms.ValidationError("You must book at least 1 seat.")
        if seats > 10:
            raise forms.ValidationError("You can book a maximum of 10 seats at once.")
        if self.available_seats is not None and seats > self.available_seats:
            raise forms.ValidationError(
                f"Only {self.available_seats} seat(s) available."
            )
        return seats


class ReviewForm(forms.ModelForm):
    """Form to submit or edit a review."""

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-input'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Share your thoughts about this movie...'
            })
        }
        labels = {
            'rating': 'Your Rating',
            'comment': 'Your Review'
        }
