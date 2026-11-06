from django.contrib import admin
# Register your models here.
from .models import usereg,product
from .models import*
admin.site.register(usereg)
admin.site.register(product)
admin.site.register(Camp)
admin.site.register(Report)
admin.site.register(DonationRequest)
admin.site.register(DonationOffer)
admin.site.register(DonationTracking)
admin.site.register(Donor)
admin.site.register(Notification)
admin.site.register(Volunteer)
admin.site.register(Needs)
admin.site.register(Volunteer_Request)
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'payment_status', 'created_at')  # Ensure 'status' is removed
    search_fields = ('user__id', 'payment_id', 'order_id')  

admin.site.register(Payment, PaymentAdmin)
