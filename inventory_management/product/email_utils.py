# Email Utilities for Inventory Management System

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_welcome_email(user, request):
    """
    Send a welcome email to newly registered users.
    
    Args:
        user: The User object
        request: The HTTP request object
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        context = {
            'username': user.username,
            'email': user.email,
            'site_url': request.build_absolute_uri('/'),
            # Update the image_url to point to your actual image location
            'image_url': request.build_absolute_uri('/static/images/inventory-welcome.png'),
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
        return True
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False
