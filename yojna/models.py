
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Best practice to reference the User model




# Create your models here.

class Farmer(AbstractUser):
    # Constants for District Choices (Example subset)
    DISTRICT_CHOICES = [
        ('AHMEDNAGAR', 'Ahmednagar (Ahilyanagar)'),
        ('AKOLA', 'Akola'),
        ('AMRAVATI', 'Amravati'),
        ('AURANGABAD', 'Aurangabad (Chhatrapati Sambhajinagar)'),
        ('BEED', 'Beed'),
        ('BHANDARA', 'Bhandara'),
        ('BULDHANA', 'Buldhana'),
        ('CHANDRAPUR', 'Chandrapur'),
        ('DHULE', 'Dhule'),
        ('GADCHIROLI', 'Gadchiroli'),
        ('GONDIA', 'Gondia'),
        ('HINGOLI', 'Hingoli'),
        ('JALGAON', 'Jalgaon'),
        ('JALNA', 'Jalna'),
        ('KOLHAPUR', 'Kolhapur'),
        ('LATUR', 'Latur'),
        ('MUMBAI_CITY', 'Mumbai City'),
        ('MUMBAI_SUBURBAN', 'Mumbai Suburban'),
        ('NAGPUR', 'Nagpur'),
        ('NANDED', 'Nanded'),
        ('NANDURBAR', 'Nandurbar'),
        ('NASHIK', 'Nashik'),
        ('OSMANABAD', 'Osmanabad (Dharashiv)'),
        ('PALGHAR', 'Palghar'),
        ('PARBHANI', 'Parbhani'),
        ('PUNE', 'Pune'),
        ('RAIGAD', 'Raigad'),
        ('RATNAGIRI', 'Ratnagiri'),
        ('SANGLI', 'Sangli'),
        ('SATARA', 'Satara'),
        ('SINDHUDURG', 'Sindhudurg'),
        ('SOLAPUR', 'Solapur'),
        ('THANE', 'Thane'),
        ('WARDHA', 'Wardha'),
        ('WASHIM', 'Washim'),
        ('YAVATMAL', 'Yavatmal'),
]


    # Existing AbstractUser already provides:
    # username, password, first_name, last_name, email, is_staff, etc.

    phone = models.CharField(max_length=15, unique=True, help_text="Enter a valid phone number")
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES)
    village_taluka = models.CharField(max_length=255, verbose_name="Village or Taluka")

    def __str__(self):
        return f"{self.username} - {self.district}"
    



class Scheme(models.Model):
    CATEGORY_CHOICES = [
        ('SUBSIDY', 'Subsidy'),
        ('LOAN', 'Loan'),
        ('INSURANCE', 'Insurance'),
        ('TRAINING', 'Training'),
        ('MARKETING', 'Marketing'),
    ]

    # Reference the same districts used in your Farmer model for consistency
    # DISTRICT_CHOICES = [
    #     ('AHMEDNAGAR', 'Ahmednagar (Ahilyanagar)'),
    #     ('AKOLA', 'Akola'),
    #     ('AMRAVATI', 'Amravati'),
    #     ('AURANGABAD', 'Aurangabad (Chhatrapati Sambhajinagar)'),
    #     ('BEED', 'Beed'),
    #     ('BHANDARA', 'Bhandara'),
    #     ('BULDHANA', 'Buldhana'),
    #     ('CHANDRAPUR', 'Chandrapur'),
    #     ('DHULE', 'Dhule'),
    #     ('GADCHIROLI', 'Gadchiroli'),
    #     ('GONDIA', 'Gondia'),
    #     ('HINGOLI', 'Hingoli'),
    #     ('JALGAON', 'Jalgaon'),
    #     ('JALNA', 'Jalna'),
    #     ('KOLHAPUR', 'Kolhapur'),
    #     ('LATUR', 'Latur'),
    #     ('MUMBAI_CITY', 'Mumbai City'),
    #     ('MUMBAI_SUBURBAN', 'Mumbai Suburban'),
    #     ('NAGPUR', 'Nagpur'),
    #     ('NANDED', 'Nanded'),
    #     ('NANDURBAR', 'Nandurbar'),
    #     ('NASHIK', 'Nashik'),
    #     ('OSMANABAD', 'Osmanabad (Dharashiv)'),
    #     ('PALGHAR', 'Palghar'),
    #     ('PARBHANI', 'Parbhani'),
    #     ('PUNE', 'Pune'),
    #     ('RAIGAD', 'Raigad'),
    #     ('RATNAGIRI', 'Ratnagiri'),
    #     ('SANGLI', 'Sangli'),
    #     ('SATARA', 'Satara'),
    #     ('SINDHUDURG', 'Sindhudurg'),
    #     ('SOLAPUR', 'Solapur'),
    #     ('THANE', 'Thane'),
    #     ('WARDHA', 'Wardha'),
    #     ('WASHIM', 'Washim'),
    #     ('YAVATMAL', 'Yavatmal'),
    # ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="YouTube or Video link")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SUBSIDY')
    
    # Target districts: multiple selection allowed
    # Note: Using a TextField or a separate M2M model is better for multiple districts
    #target_districts = models.JSONField(help_text="List of districts where this scheme is applicable")
    
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    benefit_amount = models.CharField(max_length=100, blank=True, help_text="e.g., ₹6,000/वर्ष or 50% सब्सिडी")
    apply_url = models.URLField(max_length=500, blank=True, null=True, help_text="Official government application link")
    thumbnail = models.ImageField(upload_to='scheme_thumbnails/', blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title
    




class Notification(models.Model):
    # Links to your Farmer model (User)
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    # Links to the Scheme
    scheme = models.ForeignKey(
        'Scheme', 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    sent_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Notification for {self.farmer.username} - {self.scheme.title}"

    def mark_as_read(self):
        """Helper method to mark notification as viewed with current timestamp"""
        from django.utils import timezone
        if not self.viewed:
            self.viewed = True
            self.viewed_at = timezone.now()
            self.save()


class WatchHistory(models.Model):
    """Tracks actual video watching behavior"""
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    last_watched_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    watch_duration_seconds = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['farmer', 'scheme']

class WatchLater(models.Model):
    """Tracks schemes saved for later viewing"""
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['farmer', 'scheme']