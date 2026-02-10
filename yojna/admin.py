from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Farmer, Scheme, Notification, WatchHistory, WatchLater
from django import forms




class SchemeAdminForm(forms.ModelForm):
    target_districts = forms.MultipleChoiceField(
        choices=Farmer.DISTRICT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select all districts where this scheme is applicable"
    )
    
    class Meta:
        model = Scheme
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.target_districts:
            self.initial['target_districts'] = self.instance.target_districts
    
    def clean_target_districts(self):
        return list(self.cleaned_data['target_districts'])




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
    # form = SchemeAdminForm  # ← REMOVE THIS LINE
    
    list_display = ('title', 'category', 'is_active', 'created_date')
    list_filter = ('category', 'is_active', 'created_date')
    search_fields = ('title', 'description')
    
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Media & Benefits', {
            'fields': ('video_url', 'thumbnail', 'benefit_amount', 'apply_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'scheme', 'sent_at', 'viewed', 'viewed_at')
    list_filter = ('viewed', 'sent_at')
    search_fields = ('farmer__username', 'scheme__title', 'farmer__phone')
    # Prevent manual editing of timestamps for integrity
    readonly_fields = ('sent_at', 'viewed_at')

    list_display = ('farmer', 'scheme', 'sent_at', 'viewed', 'viewed_at')  # Changed viewed → opened
    list_filter = ('viewed', 'sent_at')  # Changed viewed → opened




@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'scheme', 'started_at', 'last_watched_at', 'completed', 'watch_duration_seconds']
    list_filter = ['completed', 'started_at']
    search_fields = ['farmer__username', 'scheme__title']
    date_hierarchy = 'started_at'
    readonly_fields = ['started_at', 'last_watched_at']




@admin.register(WatchLater)
class WatchLaterAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'scheme', 'saved_at']
    list_filter = ['saved_at']
    search_fields = ['farmer__username', 'scheme__title']
    date_hierarchy = 'saved_at'
    readonly_fields = ['saved_at']