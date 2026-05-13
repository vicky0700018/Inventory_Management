from django.contrib import admin
from .models import Product, AccountDeletion

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AccountDeletion)
class AccountDeletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_confirmed')
    list_filter = ('created_at', 'is_confirmed')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at')
