
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from accounts.models import Retailer
from branches.models import Branch


def validate_support_file_size(file):
    max_size = 10 * 1024 * 1024  # 10 MB

    if file.size > max_size:
        raise ValidationError("File size cannot exceed 10 MB.")


class SupportCategory(models.Model):

    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(
                fields=["is_active"],
                name="supp_category_active_idx"
            ),
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
    retailer = models.ForeignKey(Retailer,on_delete=models.PROTECT,related_name="support_tickets")
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,related_name="support_tickets",null=True,blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="created_support_tickets",null=True,blank=True)
    category = models.ForeignKey(SupportCategory,on_delete=models.SET_NULL,related_name="support_tickets",null=True,blank=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20,choices=PRIORITY_CHOICES,default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="assigned_support_tickets",null=True,blank=True)
    is_private = models.BooleanField(default=True)
    resolved_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_number

    def clean(self):

        super().clean()

        if self.branch_id and self.retailer_id:

            if self.branch.retailer_id != self.retailer_id:
                raise ValidationError({
                    "branch": "Selected branch does not belong to this retailer."
                })

    def save(self, *args, **kwargs):

        if not self.ticket_number:
            date_part = timezone.now().strftime("%Y%m%d")
            unique_part = uuid.uuid4().hex[:12].upper()

            self.ticket_number = f"TKT-{date_part}-{unique_part}"

        previous_status = None

        if self.pk:
            previous_status = (
                SupportTicket.objects
                .filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        if self.status == "resolved":

            if not self.resolved_at or previous_status != "resolved":
                self.resolved_at = timezone.now()

        else:
            self.resolved_at = None

        self.full_clean()

        update_fields = kwargs.get("update_fields")

        if update_fields is not None:
            update_fields = set(update_fields)

            if previous_status != self.status:
                update_fields.add("resolved_at")

            kwargs["update_fields"] = update_fields

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["retailer", "status"],
                name="supp_tkt_ret_status_idx"
            ),
            models.Index(
                fields=["branch", "status"],
                name="supp_tkt_branch_status_idx"
            ),
            models.Index(
                fields=["created_by", "status"],
                name="supp_tkt_creator_status_idx"
            ),
            models.Index(
                fields=["assigned_to", "status"],
                name="supp_tkt_assign_status_idx"
            ),
            models.Index(
                fields=["priority", "status"],
                name="supp_tkt_priority_status_idx"
            ),
            models.Index(
                fields=["created_at"],
                name="supp_tkt_created_idx"
            ),
        ]


class SupportMessage(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="sent_support_messages",null=True,blank=True)
    message = models.TextField()
    is_platform_reply = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.ticket.ticket_number} - "
            f"Message {self.pk}"
        )

    class Meta:
        ordering = ["created_at"]

        indexes = [
            models.Index(
                fields=["ticket", "is_read"],
                name="supp_msg_ticket_read_idx"
            ),
            models.Index(
                fields=["created_at"],
                name="supp_msg_created_idx"
            ),
        ]


class SupportAttachment(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="attachments")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="uploaded_support_attachments",null=True,blank=True)

    file = models.FileField(
        upload_to="support_attachments/%Y/%m/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",
                    "csv",
                    "txt",
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                    "zip",
                ]
            ),
            validate_support_file_size,
        ]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ["-uploaded_at"]

        indexes = [
            models.Index(
                fields=["uploaded_at"],
                name="supp_attach_uploaded_idx"
            ),
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
            models.Index(
                fields=["is_active"],
                name="supp_info_active_idx"
            ),
        ]


class TicketActivity(models.Model):

    ticket = models.ForeignKey(SupportTicket,on_delete=models.CASCADE,related_name="activities")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name="support_activities",null=True,blank=True)
    action = models.CharField(max_length=100)
    remarks = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.ticket.ticket_number} - "
            f"{self.action}"
        )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["ticket", "created_at"],
                name="supp_activity_ticket_date_idx"
            ),
        ]
