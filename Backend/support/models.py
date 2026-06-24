from django.db import models
from django.conf import settings
from accounts.models import Retailer
from branches.models import Branch

class SupportCategory(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
        ]


class SupportTicket(models.Model):

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )

    ticket_number = models.CharField(max_length=50,unique=True,editable=False)
    retailer = models.ForeignKey(Retailer,on_delete=models.CASCADE,related_name="support_tickets")
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,related_name="support_tickets")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="created_tickets")
    category = models.ForeignKey(SupportCategory,on_delete=models.SET_NULL,null=True,blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default="medium")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="open")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="assigned_tickets")
    is_private = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_number

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["ticket_number"]),
            models.Index(fields=["retailer"]),
            models.Index(fields=["branch"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["assigned_to"]),
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["retailer", "status"]),
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["created_by", "status"]),
        ]


class SupportMessage(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    message = models.TextField()
    is_platform_reply = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.ticket.ticket_number}"
        )

    class Meta:
        ordering = ["created_at"]

        indexes = [
            models.Index(fields=["ticket"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["ticket", "is_read"]),
        ]


class SupportAttachment(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="attachments")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    file = models.FileField(upload_to="support_attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ["-uploaded_at"]

        indexes = [
            models.Index(fields=["ticket"]),
            models.Index(fields=["uploaded_by"]),
            models.Index(fields=["uploaded_at"]),
        ]


class PlatformSupportInfo(models.Model):

    company_name = models.CharField(max_length=255)
    support_email = models.EmailField()
    support_mobile = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    support_hours = models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Platform Support Information"
        verbose_name_plural = "Platform Support Information"

        indexes = [
            models.Index(fields=["is_active"]),
        ]


class TicketActivity(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="activities")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    action = models.CharField(max_length=100)
    remarks = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["ticket"]),
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
        ]