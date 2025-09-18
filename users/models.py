from django.db import models
from django.utils import timezone

class UserAccount(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # demo only
    status = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    device_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user_id
    
    def login_user(self, session_key, device_ip):
        """Login user and set session details"""
        self.is_logged_in = True
        self.session_key = session_key
        self.device_ip = device_ip
        self.login_time = timezone.now()
        self.last_login = timezone.now()
        self.save()
    
    def logout_user(self):
        """Logout user and clear session details"""
        self.is_logged_in = False
        self.session_key = None
        self.logout_time = timezone.now()
        self.save()
    
    def is_online(self):
        """Check if user is currently online"""
        return self.is_logged_in and self.session_key is not None
