from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Inventory Management System'
        message = f'''Hello {instance.username},

Welcome to our Inventory Management System!

Your account has been successfully created. You can now:
- View all products
- Create new products
- Edit and delete your own products
- Manage your inventory

Start by creating your first product!

Best regards,
Inventory Management Team

---
Email: vs2734514@gmail.com
Website: Inventory Management System
        '''
        
        html_message = f'''
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
                    <h2 style="color: #e94560;">Welcome to Inventory Management System! 📦</h2>
                    
                    <p>Hello <strong>{instance.username}</strong>,</p>
                    
                    <p>Your account has been successfully created. You're now ready to manage your inventory!</p>
                    
                    <h3 style="color: #1a1a2e; margin-top: 20px;">What you can do:</h3>
                    <ul style="background-color: white; padding: 20px; border-radius: 5px; border-left: 4px solid #e94560;">
                        <li>✅ View all products in the catalog</li>
                        <li>✅ Create and add new products</li>
                        <li>✅ Edit your own products</li>
                        <li>✅ Delete your own products</li>
                        <li>✅ Manage your inventory</li>
                    </ul>
                    
                    <p style="margin-top: 20px;">
                        <a href="http://127.0.0.1:8000/" style="background-color: #e94560; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Get Started Now
                        </a>
                    </p>
                    
                    <p style="margin-top: 30px; font-size: 12px; color: #999; border-top: 1px solid #ddd; padding-top: 20px;">
                        Best regards,<br>
                        <strong>Inventory Management Team</strong><br>
                        📧 Email: {settings.EMAIL_HOST_USER}<br>
                        This is an automated email. Please do not reply.
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
                [instance.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"✅ Welcome email sent successfully to {instance.email}")
        except Exception as e:
            print(f"❌ Error sending email to {instance.email}: {str(e)}")
