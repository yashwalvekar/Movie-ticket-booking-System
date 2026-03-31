# CineBook — Movie Ticket Booking System

> A full-stack Movie Ticket Booking System built with Django & Python as a mini project

---

## Features

- User authentication (signup, login, logout)
- Movie listings with poster images (uploaded via Admin panel)
- Show scheduling & real-time seat availability
- Ticket booking & cancellation
- Movie reviews with edit & delete
- Admin panel to manage all data

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Django | Web framework (MVT architecture) |
| HTML & CSS | Frontend templates |
| SQLite | Database |
| JavaScript | Live price calculator on booking page |

---

## Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/cinebook.git
cd cinebook

# 2. Install dependencies
pip install django pillow

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Load sample data (6 movies + 12 shows)
python manage.py loaddata tickets/fixtures/sample_data.json

# 5. Create admin account
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

Admin panel -> http://127.0.0.1:8000/admin

---

## Project Structure

```
moviebooking/
├── manage.py
├── moviebooking/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tickets/
    ├── models.py       <- Movie, Show, Booking, Review
    ├── views.py        <- All page logic
    ├── urls.py         <- URL routing
    ├── forms.py        <- Form validation
    ├── admin.py        <- Admin panel config
    └── templates/      <- HTML pages
```

---

## Database Models

- **Movie** — title, description, duration, genre, release_date, poster
- **Show** — movie (FK), show_time, total_seats
- **Booking** — user (FK), show (FK), seats_booked, booked_at
- **Review** — user (FK), movie (FK), rating, comment

---

## Future Implementations

- [ ] Payment gateway using Razorpay API
- [ ] Email confirmation — ticket delivered to Gmail with QR code
- [ ] GPS-based theatre locator to find nearest cinema

---

## About

Built as a mini project for 4th Semester at Parul University.

---

If you found this useful, give it a star.
