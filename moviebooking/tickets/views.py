"""
views.py — All view functions for the Movie Booking System.

Each function handles one page/action:
  - home              : list all movies
  - movie_detail      : movie info + showtimes + reviews
  - book_ticket       : reserve seats for a show
  - my_bookings       : list all bookings for logged-in user
  - cancel_booking    : delete a booking
  - add_review        : submit a review for a movie
  - edit_review       : update an existing review
  - delete_review     : remove a review
  - signup_view       : register a new account
  - login_view        : sign in
  - logout_view       : sign out
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  # Protect pages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import IntegrityError

from .models import Movie, Show, Booking, Review
from .forms import SignupForm, BookingForm, ReviewForm


# ──────────────────────────────────────────────
# HOME — List all movies
# ──────────────────────────────────────────────

def home(request):
    """Display all movies on the homepage. Supports search by title."""
    query = request.GET.get('q', '')  # Get search query from URL ?q=...
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()

    return render(request, 'tickets/home.html', {
        'movies': movies,
        'query': query,
    })


# ──────────────────────────────────────────────
# MOVIE DETAIL — Info + Showtimes + Reviews
# ──────────────────────────────────────────────

def movie_detail(request, movie_id):
    """Show full details of one movie, its showtimes, and all reviews."""
    movie = get_object_or_404(Movie, id=movie_id)
    shows = movie.show_set.order_by('show_time')        # Upcoming shows
    reviews = movie.review_set.select_related('user')   # All reviews

    # Check if the logged-in user already reviewed this movie
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, 'tickets/movie_detail.html', {
        'movie': movie,
        'shows': shows,
        'reviews': reviews,
        'user_review': user_review,
        'avg_rating': movie.average_rating(),
    })


# ──────────────────────────────────────────────
# BOOK TICKET — Reserve seats for a show
# ──────────────────────────────────────────────

@login_required  # Only logged-in users can book
def book_ticket(request, show_id):
    """Handle ticket booking for a specific show."""
    show = get_object_or_404(Show, id=show_id)
    available = show.available_seats()

    if available == 0:
        messages.error(request, "Sorry, this show is housefull!")
        return redirect('movie_detail', movie_id=show.movie.id)

    if request.method == 'POST':
        form = BookingForm(request.POST, available_seats=available)
        if form.is_valid():
            booking = form.save(commit=False)  # Don't save yet
            booking.user = request.user         # Attach current user
            booking.show = show                 # Attach the show
            booking.save()
            messages.success(
                request,
                f"🎉 Booking confirmed! {booking.seats_booked} seat(s) for {show.movie.title}."
            )
            return redirect('my_bookings')
    else:
        form = BookingForm(available_seats=available)

    return render(request, 'tickets/book_ticket.html', {
        'form': form,
        'show': show,
        'available': available,
    })


# ──────────────────────────────────────────────
# MY BOOKINGS — All bookings for logged-in user
# ──────────────────────────────────────────────

@login_required
def my_bookings(request):
    """Display all bookings made by the logged-in user."""
    bookings = Booking.objects.filter(user=request.user).select_related(
        'show', 'show__movie'
    ).order_by('-booked_at')  # Most recent first

    return render(request, 'tickets/my_bookings.html', {
        'bookings': bookings,
    })


# ──────────────────────────────────────────────
# CANCEL BOOKING
# ──────────────────────────────────────────────

@login_required
def cancel_booking(request, booking_id):
    """Cancel (delete) a booking. Only the owner can cancel."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        movie_title = booking.show.movie.title
        booking.delete()
        messages.success(request, f"Booking for '{movie_title}' has been cancelled.")
        return redirect('my_bookings')

    return render(request, 'tickets/confirm_cancel.html', {'booking': booking})


# ──────────────────────────────────────────────
# ADD REVIEW
# ──────────────────────────────────────────────

@login_required
def add_review(request, movie_id):
    """Submit a new review for a movie."""
    movie = get_object_or_404(Movie, id=movie_id)

    # Check if user already reviewed this movie
    if Review.objects.filter(user=request.user, movie=movie).exists():
        messages.warning(request, "You have already reviewed this movie. Edit your review instead.")
        return redirect('movie_detail', movie_id=movie.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()

    return render(request, 'tickets/review_form.html', {
        'form': form,
        'movie': movie,
        'action': 'Add',
    })


# ──────────────────────────────────────────────
# EDIT REVIEW
# ──────────────────────────────────────────────

@login_required
def edit_review(request, review_id):
    """Edit an existing review. Only the author can edit."""
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated!")
            return redirect('movie_detail', movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'tickets/review_form.html', {
        'form': form,
        'movie': review.movie,
        'action': 'Edit',
    })


# ──────────────────────────────────────────────
# DELETE REVIEW
# ──────────────────────────────────────────────

@login_required
def delete_review(request, review_id):
    """Delete a review. Only the author can delete."""
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == 'POST':
        movie_id = review.movie.id
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect('movie_detail', movie_id=movie_id)

    return render(request, 'tickets/confirm_delete_review.html', {'review': review})


# ──────────────────────────────────────────────
# AUTH — Signup, Login, Logout
# ──────────────────────────────────────────────

def signup_view(request):
    """Register a new user account."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            messages.success(request, f"Welcome, {user.username}! Account created successfully.")
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'tickets/signup.html', {'form': form})


def login_view(request):
    """Log in an existing user."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            # Redirect to next page if specified (e.g., after @login_required redirect)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'tickets/login.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect('home')
