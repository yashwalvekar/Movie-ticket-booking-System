# 🎬 CineBook — Movie Ticket Booking System
### Built with Django + SQLite | Beginner-Friendly | Exam-Ready

---

## 📁 Project Structure

```
moviebooking/                   ← Project root
├── manage.py                   ← Django CLI entry point
├── setup.sh                    ← One-click setup script
├── db.sqlite3                  ← Auto-created database (after setup)
│
├── moviebooking/               ← Project configuration package
│   ├── settings.py             ← All Django settings
│   ├── urls.py                 ← Root URL dispatcher
│   └── wsgi.py                 ← Web server entry point
│
├── tickets/                    ← Main application (all features here)
│   ├── models.py               ← Database models (Movie, Show, Booking, Review)
│   ├── views.py                ← All view functions (page logic)
│   ├── urls.py                 ← App URL patterns
│   ├── forms.py                ← Django forms (Signup, Booking, Review)
│   ├── admin.py                ← Admin panel registration
│   ├── fixtures/
│   │   └── sample_data.json    ← Sample movies and shows
│   └── templates/tickets/      ← HTML templates
│       ├── home.html           ← Movie listing page
│       ├── movie_detail.html   ← Movie info + showtimes + reviews
│       ├── book_ticket.html    ← Ticket booking form
│       ├── my_bookings.html    ← User's booking history
│       ├── confirm_cancel.html ← Cancel booking confirmation
│       ├── review_form.html    ← Add / Edit review
│       ├── confirm_delete_review.html
│       ├── login.html
│       └── signup.html
│
└── templates/
    └── base.html               ← Shared layout (navbar, messages, footer)
```

---

## ⚡ Quick Setup (3 steps)

```bash
# Step 1: Install & set up everything
chmod +x setup.sh && ./setup.sh

# Step 2: Start the development server
python manage.py runserver

# Step 3: Open in browser
# http://127.0.0.1:8000
```

**Admin Panel:** http://127.0.0.1:8000/admin  
Login: `admin` / `admin123`

---

## 🗄️ Models Explained

### `Movie`
Stores details about each film.
```python
title, description, duration, genre, release_date
```
- `average_rating()` — calculates mean star rating from all reviews

### `Show`
A specific screening of a movie.
```python
movie (FK), show_time, total_seats
```
- `available_seats()` — subtracts booked seats from total
- `is_housefull()` — returns True when no seats remain

### `Booking`
A user's ticket reservation.
```python
user (FK), show (FK), seats_booked, booked_at
```
- `total_price()` — seats × ₹200

### `Review`
A user's star rating + comment.
```python
user (FK), movie (FK), rating (1-5), comment, created_at
```
- `unique_together = ('user', 'movie')` — one review per user per movie

---

## 🌐 URL Reference

| URL | View | Description |
|-----|------|-------------|
| `/` | `home` | Browse all movies |
| `/movie/<id>/` | `movie_detail` | Movie info, showtimes, reviews |
| `/show/<id>/book/` | `book_ticket` | Book tickets (login required) |
| `/my-bookings/` | `my_bookings` | View all your bookings (login required) |
| `/booking/<id>/cancel/` | `cancel_booking` | Cancel a booking (login required) |
| `/movie/<id>/review/add/` | `add_review` | Write a review (login required) |
| `/review/<id>/edit/` | `edit_review` | Edit your review (login required) |
| `/review/<id>/delete/` | `delete_review` | Delete your review (login required) |
| `/signup/` | `signup_view` | Register a new account |
| `/login/` | `login_view` | Login |
| `/logout/` | `logout_view` | Logout (POST only) |
| `/admin/` | Django Admin | Manage all data |

---

## 🔑 Key Django Concepts Used

| Concept | Where Used |
|---------|-----------|
| `models.ForeignKey` | Show→Movie, Booking→User+Show, Review→User+Movie |
| `@login_required` | Protects booking, review, my-bookings views |
| `get_object_or_404` | Safe object lookup in all detail views |
| `request.method == 'POST'` | Handles form submissions |
| `form.save(commit=False)` | Attach user/show before saving |
| `messages.success/error` | Flash messages after actions |
| `{% csrf_token %}` | Security token in all forms |
| `unique_together` | One review per user per movie |
| `auto_now_add=True` | Auto-set booked_at and created_at |

---

## 🎯 Features

- ✅ User registration, login, logout
- ✅ Browse all movies with search
- ✅ Movie detail page with showtimes and reviews
- ✅ Book tickets with live price calculator
- ✅ View and cancel your bookings
- ✅ Write, edit, delete your review
- ✅ Average rating display on movie cards
- ✅ Seat availability tracking (housefull detection)
- ✅ Django Admin panel for data management
- ✅ Sample data (6 movies, 12 shows) pre-loaded

---

## 🛠️ Manual Setup (without setup.sh)

```bash
pip install django
python manage.py makemigrations tickets
python manage.py migrate
python manage.py loaddata tickets/fixtures/sample_data.json
python manage.py createsuperuser
python manage.py runserver
```
