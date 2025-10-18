from django.contrib import admin
from .models import User, UserEvents, Payment, ContactMessage


# Custom admin view for UserEvents
class UserEventsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'eventname', 'date',
        'mobile', 'altmobile', 'amount', 'description'
    )
    list_filter = ('date',)
    search_fields = ('name', 'email', 'eventname', 'mobile')
    ordering = ('-date',)
    list_per_page = 30

# ✅ Custom admin view for Payment
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user_event', 'amount', 'upi_id', 'txn_id', 'status'
    )
    search_fields = ('txn_id', 'upi_id', 'user_event__name', 'user_event__email')
    list_filter = ('status',)
    ordering = ('-id',)
# ✅ user model
class UserAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'mobile')  # Password not shown for security
    search_fields = ('fname', 'lname', 'email', 'mobile')
    ordering = ('-id',)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'created_at')
    search_fields = ('name', 'email',  'message')
    ordering = ('-created_at',)

    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'
# Register your models
admin.site.register(User,UserAdmin)
admin.site.register(UserEvents, UserEventsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
