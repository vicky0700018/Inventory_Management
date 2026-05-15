from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import Product, AccountDeletion
from .forms import ProductForm, UserRegistrationForm

# Product List View (accessible to all)
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'product/product_list.html', context)

# Product Detail View (accessible to all)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'is_authenticated': request.user.is_authenticated,
        'is_owner': request.user == product.created_by,
    }
    return render(request, 'product/product_detail.html', context)

# Create Product (only for logged-in users)
@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/create_product.html', {'form': form})

# Edit Product (only for product owner)
@login_required(login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user != product.created_by:
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product/edit_product.html', {'form': form, 'product': product})

# Delete Product (only for product owner)
@login_required(login_url='login')
@require_http_methods(["POST"])
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user != product.created_by:
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('product_list')
    
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send Welcome Email
            try:
                context = {
                    'username': user.username,
                    'email': user.email,
                    'site_url': request.build_absolute_uri('/'),
                    'image_url': request.build_absolute_uri('/static/images/inventory-welcome.png'),  # Optional: Add your image
                }
                html_message = render_to_string('product/welcome_email.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject='Welcome to Inventory Management System!',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(request, 'Registration successful! Welcome email has been sent to your email.')
            except Exception as e:
                # If email fails, still allow registration but show warning
                messages.warning(request, f'Registration successful! But email could not be sent. Error: {str(e)}')
            
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'product/register.html', {'form': form})

# User Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'product/login.html')

# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('product_list')

# User Profile View
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    user_products = Product.objects.filter(created_by=user).count()
    context = {
        'user': user,
        'products_count': user_products,
    }
    return render(request, 'product/profile.html', context)

# Request Account Deletion
@login_required(login_url='login')
def request_account_deletion(request):
    if request.method == 'POST':
        # Delete any existing deletion request
        AccountDeletion.objects.filter(user=request.user).delete()
        
        # Create new deletion request
        deletion_request = AccountDeletion.objects.create(user=request.user)
        
        # Send confirmation email
        confirmation_link = f"http://127.0.0.1:8000/confirm-deletion/{deletion_request.token}/"
        subject = '⚠️ Account Deletion Confirmation Required'
        message = f'''Hello {request.user.username},

Your account deletion request has been initiated.

To complete the deletion of your account and all associated data, please click the link below:

{confirmation_link}

This link will expire in 24 hours.

If you did not request this, please ignore this email.

Best regards,
Inventory Management Team
        '''
        
        html_message = f'''
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #fff3cd; border-radius: 8px; border-left: 4px solid #ff6b6b;">
                    <h2 style="color: #d9534f;">⚠️ Account Deletion Confirmation</h2>
                    
                    <p>Hello <strong>{request.user.username}</strong>,</p>
                    
                    <p>Your account deletion request has been initiated.</p>
                    
                    <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>To complete the deletion of your account:</strong></p>
                        <p>Click the button below to confirm:</p>
                        <p style="text-align: center; margin-top: 20px;">
                            <a href="{confirmation_link}" style="background-color: #d9534f; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                Confirm Account Deletion
                            </a>
                        </p>
                        <p style="font-size: 12px; color: #999; margin-top: 20px; word-break: break-all;">
                            Or copy this link: {confirmation_link}
                        </p>
                    </div>
                    
                    <p style="color: #d9534f; font-weight: bold;">⚠️ WARNING:</p>
                    <ul style="color: #d9534f;">
                        <li>This action is permanent and cannot be undone</li>
                        <li>All your products will be deleted</li>
                        <li>All your account data will be removed</li>
                        <li>This link expires in 24 hours</li>
                    </ul>
                    
                    <p style="margin-top: 20px; font-size: 12px; color: #999; border-top: 1px solid #ddd; padding-top: 20px;">
                        If you did not request this, please ignore this email.<br>
                        Best regards,<br>
                        <strong>Inventory Management Team</strong><br>
                        📧 {settings.EMAIL_HOST_USER}
                    </p>
                </div>
            </body>
        </html>
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, 'A confirmation email has been sent to your email address. Please check your inbox.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error sending confirmation email: {str(e)}')
            deletion_request.delete()
            return redirect('product_list')
    
    return render(request, 'product/request_deletion.html')

# Confirm Account Deletion
def confirm_account_deletion(request, token):
    try:
        deletion_request = AccountDeletion.objects.get(token=token)
    except AccountDeletion.DoesNotExist:
        messages.error(request, 'Invalid or expired deletion link.')
        return redirect('product_list')
    
    if request.method == 'POST':
        user = deletion_request.user
        username = user.username
        email = user.email
        
        # Delete user (this will cascade delete all products)
        user.delete()
        deletion_request.delete()
        
        # Send goodbye email
        subject = 'Account Successfully Deleted'
        message = f'''Hello,

Your account associated with email {email} and username {username} has been successfully deleted from Inventory Management System.

All your data has been permanently removed.

If this was done by mistake, you can always create a new account.

Best regards,
Inventory Management Team
        '''
        
        html_message = f'''
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #d4edda; border-radius: 8px; border-left: 4px solid #28a745;">
                    <h2 style="color: #155724;">✅ Account Deleted</h2>
                    
                    <p>Your account has been successfully deleted.</p>
                    
                    <div style="background-color: white; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Deleted Account Details:</strong></p>
                        <ul>
                            <li>Email: {email}</li>
                            <li>Username: {username}</li>
                            <li>Deleted on: {str(deletion_request.created_at)}</li>
                        </ul>
                    </div>
                    
                    <p>All your data has been permanently removed from our system.</p>
                    
                    <p>If you'd like to use our service again in the future, you're welcome to create a new account at any time.</p>
                    
                    <p style="margin-top: 20px; font-size: 12px; color: #999; border-top: 1px solid #ddd; padding-top: 20px;">
                        Best regards,<br>
                        <strong>Inventory Management Team</strong>
                    </p>
                </div>
            </body>
        </html>
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=True,  # Don't fail if email can't be sent (user is already deleted)
            )
        except:
            pass
        
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('product_list')
    
    return render(request, 'product/confirm_deletion.html', {'deletion_request': deletion_request})

