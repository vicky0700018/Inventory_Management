# 🚀 Quick Start Guide - Inventory Management System

## Project Created Successfully! ✅

Your complete Inventory Management System has been created with all the features you requested.

---

## 📋 Features Implemented

### ✅ User Authentication
- User registration with email validation
- Welcome email sent to new users
- User login/logout
- Session management

### ✅ Product Management
- **Product Model Fields:**
  - Name (CharField)
  - Price (DecimalField)
  - Image (ImageField)
  - Description (TextField)
  - Quantity (IntegerField)
  - Created By (ForeignKey to User)
  - Created At (DateTimeField)

### ✅ Access Control
- **Only Registered Users Can:**
  - Create products
  - Edit their own products
  - Delete their own products

- **Guest Users Can:**
  - View all products
  - View product details
  - Edit/Delete buttons are hidden and disabled

### ✅ Email Notifications
- Welcome email sent automatically when user registers
- Email configuration ready for production SMTP servers

---

## 🎯 Getting Started

### Step 1: Navigate to Project
```bash
cd C:\Users\Vicky Kumar\OneDrive\Desktop\INVENTRY_MANAGEMENT\inventory_management
```

### Step 2: Activate Virtual Environment
```bash
myenv\Scripts\activate
```

### Step 3: Start the Development Server
```bash
python manage.py runserver
```

### Step 4: Access the Application
Open your browser and go to:
```
http://127.0.0.1:8000/
```

---

## 🔗 Available URLs

| URL | Purpose | Access |
|-----|---------|--------|
| `/` | Product List | Everyone |
| `/product/<id>/` | Product Details | Everyone |
| `/create/` | Create Product | Login Required |
| `/product/<id>/edit/` | Edit Product | Owner Only |
| `/product/<id>/delete/` | Delete Product | Owner Only |
| `/register/` | User Registration | Everyone |
| `/login/` | User Login | Not Logged In |
| `/logout/` | User Logout | Logged In Users |
| `/admin/` | Admin Panel | Superuser Only |

---

## 👤 Testing the Application

### Test as a Guest User (Not Logged In)
1. Open `http://127.0.0.1:8000/`
2. Browse products
3. Try to create a product → Redirects to login
4. Edit/Delete buttons are hidden

### Test as a Registered User
1. Click "Register" button
2. Fill registration form with:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `SecurePass123!`
   - Confirm: `SecurePass123!`
3. Check console for welcome email
4. Create a new product
5. You can edit/delete your products
6. Other users cannot edit your products

---

## 📁 Project Structure

```
inventory_management/
├── inventory_management/     # Main project folder
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI config
├── product/                 # Product app
│   ├── models.py            # Product model
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin config
│   ├── signals.py           # Email signals
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── base.html
│   └── product/
│       ├── product_list.html
│       ├── product_detail.html
│       ├── create_product.html
│       ├── edit_product.html
│       ├── register.html
│       └── login.html
├── static/                  # CSS, JS, images
├── media/                   # Uploaded product images
├── manage.py               # Django CLI
└── db.sqlite3              # Database
```

---

## 🔐 Admin Panel

Access at: `http://127.0.0.1:8000/admin/`

**To create admin user:**
```bash
python manage.py createsuperuser
```

Features:
- View all products
- Filter by creator
- Search by name
- Delete any product
- Manage users

---

## 📧 Email Configuration

### Development (Console - Default)
Emails are printed to the console where you run the server.

### Production (Gmail)
Edit `inventory_management/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'  # Not your regular password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@inventorymanagement.com'
```

---

## 🎨 UI Features

- **Bootstrap 5** responsive design
- **Color-coded badges** for price and stock status
- **Permission-based UI** - Edit/Delete buttons hidden for non-owners
- **Modern cards** with hover effects
- **Gradient navbar** with user info
- **Alert messages** for user feedback
- **Mobile-friendly** layout

---

## 🔍 What Happens When...

### User Registers
1. Registration form validation
2. User account created
3. Welcome email sent to their email
4. User automatically logged in
5. Redirected to product list

### User Creates Product
1. Form validation
2. Product created with creator info
3. Image uploaded to media folder
4. Success message displayed
5. Redirected to product list

### User Edits Product
1. Only product owner can access edit page
2. Form pre-filled with current data
3. Image can be updated or kept the same
4. Success message on update
5. Redirected to product detail

### User Deletes Product
1. Only product owner can delete
2. Confirmation prompt
3. Product removed from database
4. Image file deleted
5. Success message
6. Redirected to product list

---

## 🐛 Troubleshooting

**Problem: "Port 8000 already in use"**
```bash
python manage.py runserver 8001
```

**Problem: Images not showing**
- Ensure `DEBUG = True` in settings.py
- Check `media/` folder exists
- Verify upload path in Product model

**Problem: Can't login after registration**
- Check username is correct
- Verify password is correct
- Check Django messages for errors

**Problem: Email not sending**
- Development: Check console output
- Production: Verify SMTP settings
- Check email address format

---

## 📚 Additional Commands

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test
```

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Forms](https://docs.djangoproject.com/en/6.0/topics/forms/)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Templates](https://docs.djangoproject.com/en/6.0/topics/templates/)

---

## 🎉 Ready to Use!

Your Inventory Management System is ready to go. Start the server and begin managing your inventory!

```bash
python manage.py runserver
```

Then open: `http://127.0.0.1:8000/`

---

**Enjoy your Inventory Management System! 📦✨**
