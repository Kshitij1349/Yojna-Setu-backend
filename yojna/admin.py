from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Farmer, Scheme, Notification

# Register your models here.
@admin.register(Farmer)
class FarmerAdmin(UserAdmin):
    model = Farmer
    # Show these columns in the farmer list
    list_display = ('username', 'phone', 'district', 'village_taluka', 'is_active')
    
    # Filter farmers by region
    list_filter = ('district', 'is_staff', 'is_active')
    
    # Search by name or phone
    search_fields = ('username', 'phone', 'village_taluka')

    fieldsets = UserAdmin.fieldsets + (
        ('Regional Details', {'fields': ('phone', 'district', 'village_taluka')}),
    )



@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('title', 'category', 'is_active', 'created_date')
    
    # Sidebar filters
    list_filter = ('category', 'is_active', 'created_date')
    
    # Search box for title and description
    search_fields = ('title', 'description')
    
    # Field grouping in the edit form
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Targeting & Media', {
            'fields': ('target_districts', 'video_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    # Optional: If you want to show the JSONField as a list of checkboxes 
    # (Requires a bit more customization, but this default will work for now)



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'scheme', 'sent_at', 'viewed', 'viewed_at')
    list_filter = ('viewed', 'sent_at')
    search_fields = ('farmer__username', 'scheme__title', 'farmer__phone')
    # Prevent manual editing of timestamps for integrity
    readonly_fields = ('sent_at', 'viewed_at')