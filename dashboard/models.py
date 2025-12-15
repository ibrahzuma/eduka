from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    verb = models.CharField(max_length=255) # Short description e.g. "New Sale"
    message = models.TextField() # Detailed message
    link = models.CharField(max_length=255, blank=True, null=True) # Link to action
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.verb} - {self.recipient.username}"

class GlobalSettings(models.Model):
    site_name = models.CharField(max_length=100, default='eDuka SaaS')
    maintenance_mode = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)
    default_currency = models.CharField(max_length=10, default='TZS')
    support_email = models.EmailField(blank=True, null=True)
    trial_days = models.IntegerField(default=14)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Global System Settings"

    def save(self, *args, **kwargs):
        # Singleton logic
        if not self.pk and GlobalSettings.objects.exists():
            return
        return super(GlobalSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
