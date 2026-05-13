# ⚙️ Configuration Guide

## Environment Setup

### Python Virtual Environment

The project uses a virtual environment at `myenv/`

**Activate it:**
```bash
myenv\Scripts\activate
```

**Deactivate it:**
```bash
deactivate
```

---

## Django Settings

### Location
`inventory_management/settings.py`

### Key Settings

#### 1. **DEBUG Mode**
```python
DEBUG = True  # Set to False in production
```

#### 2. **ALLOWED_HOSTS**
```python
ALLOWED_HOSTS = []  # Add your domain names here for production
```

#### 3. **INSTALLED_APPS**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',  # Our app
]
```

#### 4. **Database**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To use PostgreSQL instead:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'InventoryManagement',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then install: `pip install psycopg2-binary`

#### 5. **Templates**
```python
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        ...
    }
]
```

#### 6. **Static Files**
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

#### 7. **Media Files**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### 8. **Email Configuration**

**Development (Console):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production (Gmail):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'app-password'  # Use app-specific password
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@inventorymanagement.com'
```

**To get Gmail app password:**
1. Enable 2-Factor Authentication
2. Go to myaccount.google.com/apppasswords
3. Generate app password for "Mail" and "Windows"
4. Copy and use in EMAIL_HOST_PASSWORD

---

## Product App Configuration

### Model Fields

**Product Model** (product/models.py):
```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    quantity = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Forms

**ProductForm** (product/forms.py):
- Excludes created_by (auto-filled from request.user)
- Excludes created_at and updated_at (auto-generated)
- Includes Bootstrap CSS classes

**UserRegistrationForm** (product/forms.py):
- Extended from Django's UserCreationForm
- Adds email field
- Password validation

---

## URL Configuration

### Main URLs (inventory_management/urls.py)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
]

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Product URLs (product/urls.py)
```
/                    → product_list
/product/<id>/       → product_detail
/create/             → create_product (login_required)
/product/<id>/edit/  → edit_product (owner only)
/product/<id>/delete/ → delete_product (owner only)
/register/           → register
/login/              → login_view
/logout/             → logout_view
```

---

## Database Migrations

### Create Migration
```bash
python manage.py makemigrations
```

### Apply Migration
```bash
python manage.py migrate
```

### View Migration Status
```bash
python manage.py showmigrations
```

### Fake Migration (if needed)
```bash
python manage.py migrate --fake
```

---

## Admin Interface

### Register Model
In `product/admin.py`:
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
```

### Access Admin
```
http://127.0.0.1:8000/admin/
```

### Create Superuser
```bash
python manage.py createsuperuser
```

---

## Authentication

### Login Required Decorator
```python
@login_required(login_url='login')
def create_product(request):
    # Only logged-in users can access
    pass
```

### Check if User is Owner
```python
if request.user != product.created_by:
    # User is not the owner
    pass
```

### Get Current User
```python
user = request.user  # In views
{{ user.username }}  # In templates
```

---

## Signals for Email Sending

### Signal Handler (product/signals.py)
Automatically sends welcome email when user is created:
```python
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Send email to new user
        send_mail(...)
```

### Register Signal (product/apps.py)
```python
def ready(self):
    import product.signals
```

---

## Security Settings

### Production Checklist

```python
# 1. Set DEBUG to False
DEBUG = False

# 2. Update SECRET_KEY
SECRET_KEY = 'your-very-long-random-secret-key'

# 3. Set ALLOWED_HOSTS
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# 4. Enable HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 5. Set HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 6. Set X-Frame-Options
X_FRAME_OPTIONS = 'DENY'

# 7. Update CORS settings if needed
```

---

## Performance Tips

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Optimization
```python
# Use select_related for ForeignKey
products = Product.objects.select_related('created_by')

# Use prefetch_related for reverse relationships
users = User.objects.prefetch_related('products')

# Use only() to fetch specific fields
products = Product.objects.only('name', 'price')
```

### Pagination
```python
from django.core.paginator import Paginator

paginator = Paginator(products, 12)  # 12 per page
page_obj = paginator.get_page(page_number)
```

---

## Logging

### Configure Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Dependencies

### Required Packages
- `Django==6.0.3`
- `pillow==10.1.0` (Image handling)
- `asgiref==3.11.1` (ASGI utilities)
- `sqlparse==0.5.5` (SQL parsing)
- `tzdata==2025.3` (Timezone data)

### Install All
```bash
pip install -r requirements.txt
```

---

## Useful Commands

```bash
# Run server with specific settings
python manage.py runserver 0.0.0.0:8000

# Create app
python manage.py startapp appname

# Django shell
python manage.py shell

# Run management command
python manage.py command_name

# Check for problems
python manage.py check

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Flush database
python manage.py flush

# Create dump
python manage.py dumpdata > dump.json

# Load dump
python manage.py loaddata dump.json
```

---

## Deployment Checklist

- [ ] Change DEBUG to False
- [ ] Update SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set up proper email service
- [ ] Configure database (PostgreSQL recommended)
- [ ] Collect static files
- [ ] Set environment variables
- [ ] Configure security headers
- [ ] Set up monitoring/logging
- [ ] Test all functionality
- [ ] Backup database strategy

---

**Configuration complete! Your Inventory Management System is ready.** ✅
