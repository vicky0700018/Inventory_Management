# 📦 Inventory Management System

A Django-based inventory management application that allows registered users to create, edit, and delete products. Non-registered users can view the product list.

## Features

✅ **User Authentication**
- User registration with email validation
- Welcome email sent to new users
- User login and logout
- Session management

✅ **Product Management**
- Create products (name, price, image, description, quantity)
- View all products
- Edit your own products
- Delete your own products
- View detailed product information

✅ **Security**
- Only authenticated users can create/edit/delete products
- Users can only edit/delete their own products
- CSRF protection on all forms
- Secure password handling

✅ **User Interface**
- Responsive Bootstrap 5 design
- Modern and user-friendly interface
- Product cards with images
- Permission-based UI (edit/delete buttons hidden for non-owners)

## Installation & Setup

### 1. Navigate to project directory
```bash
cd C:\Users\Vicky Kumar\OneDrive\Desktop\INVENTRY_MANAGEMENT\inventory_management
```

### 2. Activate virtual environment
```bash
# On Windows
myenv\Scripts\activate
```

### 3. Install required packages
```bash
pip install django pillow
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create superuser (admin account)
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### For Visitors (Not Logged In)
- ✅ View all products
- ✅ View product details
- ❌ Cannot create products
- ❌ Cannot edit/delete products
- ❌ Edit/Delete buttons are disabled

### For Registered Users
- ✅ View all products
- ✅ Create new products
- ✅ Edit your own products
- ✅ Delete your own products
- ✅ View product details

## Project Structure

```
inventory_management/
├── inventory_management/      # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── product/                  # Product app
│   ├── models.py            # Product model
│   ├── views.py             # View functions
│   ├── forms.py             # Form classes
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   ├── signals.py           # Signal handlers (email sending)
│   ├── apps.py              # App configuration
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── product/
│       ├── product_list.html      # Product listing
│       ├── product_detail.html    # Product details
│       ├── create_product.html    # Create product form
│       ├── edit_product.html      # Edit product form
│       ├── register.html          # Registration form
│       └── login.html             # Login form
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── manage.py               # Django management script
└── db.sqlite3              # Database file
```

## Models

### Product Model
```python
- name: CharField (Product name)
- price: DecimalField (Product price in INR)
- image: ImageField (Product image)
- description: TextField (Product description)
- quantity: IntegerField (Stock quantity)
- created_by: ForeignKey to User (Product creator)
- created_at: DateTimeField (Creation timestamp)
- updated_at: DateTimeField (Last update timestamp)
```

## Database

The application uses SQLite by default. To switch to PostgreSQL:

1. Update `inventory_management/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'InventoryManagement',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

2. Install psycopg2:
```bash
pip install psycopg2-binary
```

3. Run migrations:
```bash
python manage.py migrate
```

## Email Configuration

### Development (Console Backend)
By default, emails are printed to the console. To see emails:
- Check terminal where `python manage.py runserver` is running

### Production (Gmail)
Update `inventory_management/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@inventorymanagement.com'
```

## API Endpoints

```
GET     /                          # Product list
GET     /product/<id>/             # Product detail
POST    /create/                   # Create product (login required)
POST    /product/<id>/edit/        # Edit product (owner only)
POST    /product/<id>/delete/      # Delete product (owner only)
POST    /register/                 # User registration
POST    /login/                    # User login
GET     /logout/                   # User logout
GET     /admin/                    # Admin panel (superuser only)
```

## Admin Panel

Access Django admin at: `http://127.0.0.1:8000/admin/`

Features:
- View all products
- Filter by creator and date
- Search products by name
- Admin can delete any product

## Troubleshooting

### "django-admin not found" error
```bash
python -m django startproject inventory_management
```

### Image not showing
Ensure `media/` directory exists and DEBUG=True in settings.py

### Email not sending
Check that EMAIL_BACKEND is configured and DEBUG mode is appropriate

### Database errors
```bash
python manage.py migrate
python manage.py migrate product --fake-initial
```

## Security Notes

⚠️ Production Checklist:
- [ ] Set DEBUG = False
- [ ] Update SECRET_KEY
- [ ] Add domain to ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Configure secure cookies
- [ ] Set up proper email service
- [ ] Use environment variables for sensitive data
- [ ] Enable CSRF protection
- [ ] Keep dependencies updated

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please contact the development team.

---

**Happy Inventory Managing! 📦✨**
