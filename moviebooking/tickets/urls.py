"""
urls.py — URL patterns for the tickets app.

Maps URL paths to view functions.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Home ──
    path('', views.home, name='home'),

    # ── Movies ──
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),

    # ── Booking ──
    path('show/<int:show_id>/book/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),

    # ── Reviews ──
    path('movie/<int:movie_id>/review/add/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # ── Auth ──
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
