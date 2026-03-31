"""
admin.py — Register models with Django Admin panel.
Access at: http://127.0.0.1:8000/admin/

Posters are uploaded here: go to Movies → select a movie → upload poster image.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Show, Booking, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ('poster_thumb', 'title', 'genre', 'duration', 'release_date')
    search_fields = ('title', 'genre')
    list_filter   = ('genre',)

    # Show poster preview in the change form
    readonly_fields = ('poster_preview',)

    # Arrange fields neatly in the edit form
    fieldsets = (
        ('Movie Info', {
            'fields': ('title', 'description', 'genre', 'duration', 'release_date')
        }),
        ('Poster Image', {
            'fields': ('poster', 'poster_preview'),
            'description': 'Upload a JPG or PNG poster. Leave blank to use the default emoji.'
        }),
    )

    def poster_thumb(self, obj):
        """Show a small thumbnail in the list view."""
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:45px; height:65px; '
                'object-fit:cover; border-radius:4px; border:1px solid #444;">',
                obj.poster.url
            )
        return '—'
    poster_thumb.short_description = 'Poster'

    def poster_preview(self, obj):
        """Show a larger preview on the edit page."""
        if obj.poster:
            return format_html(
                '<img src="{}" style="width:160px; height:230px; '
                'object-fit:cover; border-radius:8px; '
                'border:1px solid #555; margin-top:6px;">',
                obj.poster.url
            )
        return 'No poster uploaded yet.'
    poster_preview.short_description = 'Current Poster'


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'show_time', 'total_seats', 'available_seats')
    list_filter  = ('movie',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'seats_booked', 'booked_at')
    list_filter  = ('show__movie',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    list_filter  = ('rating', 'movie')
