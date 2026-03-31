#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
#  setup.sh  — CineBook one-click project setup
#  Run once after downloading the project:
#    chmod +x setup.sh && ./setup.sh
# ─────────────────────────────────────────────────────────

set -e  # Stop on any error

echo ""
echo "🎬  CineBook — Movie Ticket Booking System"
echo "==========================================="
echo ""

# 1. Install Django + Pillow (Pillow is required for ImageField / poster uploads)
echo "📦 Installing Django & Pillow..."
pip install django pillow --quiet
echo "   ✅ Django + Pillow installed"
echo ""

# 2. Create database tables
echo "🗄️  Setting up the database..."
python manage.py makemigrations tickets
python manage.py migrate
echo "   ✅ Database ready (db.sqlite3)"
echo ""

# 3. Load sample movies and shows
echo "🎥  Loading sample movies & showtimes..."
python manage.py loaddata tickets/fixtures/sample_data.json
echo "   ✅ 6 movies and 12 shows loaded"
echo ""

# 4. Create a superuser for admin panel
echo "👤  Creating admin account..."
echo "   Username: admin"
echo "   Password: admin123"
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@cinebook.com', 'admin123')
    print('   ✅ Admin account created')
else:
    print('   ℹ️  Admin already exists')
"
echo ""

echo "🚀  Setup complete! Start the server with:"
echo ""
echo "       python manage.py runserver"
echo ""
echo "   Then open: http://127.0.0.1:8000"
echo "   Admin:     http://127.0.0.1:8000/admin  (admin / admin123)"
echo ""
