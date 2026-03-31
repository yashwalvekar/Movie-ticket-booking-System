"""
models.py — Defines all database tables for the Movie Booking System.

Tables:
  - Movie   : stores movie info
  - Show    : a scheduled screening of a movie
  - Booking : a user's ticket reservation for a show
  - Review  : a user's rating + comment on a movie
"""

from django.db import models
from django.contrib.auth.models import User  # Built-in Django user model
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    """Stores details about each movie."""

    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Thriller', 'Thriller'),
        ('Animation', 'Animation'),
        ('Documentary', 'Documentary'),
        ('Other', 'Other'),
    ]

    title        = models.CharField(max_length=200)
    description  = models.TextField()
    duration     = models.PositiveIntegerField(help_text="Duration in minutes")
    genre        = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_date = models.DateField()

    # Optional poster image — upload via Django Admin
    # Images are saved to: media/posters/<filename>
    poster = models.ImageField(
        upload_to='posters/',   # subfolder inside MEDIA_ROOT
        blank=True,             # poster is optional
        null=True,
        help_text="Upload a movie poster image (JPG, PNG, etc.)"
    )

    def __str__(self):
        return self.title

    def average_rating(self):
        """Calculate average star rating from all reviews."""
        reviews = self.review_set.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None  # No reviews yet


class Show(models.Model):
    """A specific screening of a movie at a certain time."""

    movie       = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time   = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.movie.title} — {self.show_time.strftime('%d %b %Y, %I:%M %p')}"

    def available_seats(self):
        """Calculate how many seats are still available."""
        booked = self.booking_set.aggregate(
            total=models.Sum('seats_booked')
        )['total'] or 0
        return self.total_seats - booked

    def is_housefull(self):
        return self.available_seats() == 0


class Booking(models.Model):
    """A user's ticket booking for a specific show."""

    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    show         = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)
    booked_at    = models.DateTimeField(auto_now_add=True)  # Timestamp set automatically

    def __str__(self):
        return f"{self.user.username} — {self.show} ({self.seats_booked} seat(s))"

    def total_price(self):
        """Simple pricing: ₹200 per seat."""
        return self.seats_booked * 200


class Review(models.Model):
    """A user's star rating and comment for a movie."""

    RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]

    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    movie   = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating  = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # One review per user per movie
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} → {self.movie.title} ({self.rating}★)"
