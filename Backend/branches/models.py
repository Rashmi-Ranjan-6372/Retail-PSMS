from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db import models, transaction

class Branch(models.Model):
    retailer = models.ForeignKey("accounts.Retailer", on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='branch_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_branches")
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="deleted_branches")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_branch_code(self):
        last_branch = (
            Branch.objects
            .filter(retailer=self.retailer)
            .order_by("-id")
            .first()
        )

        next_number = 1

        if last_branch and last_branch.code:
            try:
                next_number = int(last_branch.code.split("-")[-1]) + 1
            except (ValueError, IndexError):
                next_number = last_branch.pk + 1

        return f"BRN-{next_number:04d}"

    def save(self, *args, **kwargs):

        if not self.code and self.retailer_id:

            with transaction.atomic():

                last_branch = (
                    Branch.objects
                    .select_for_update()
                    .filter(retailer_id=self.retailer_id)
                    .order_by("-id")
                    .first()
                )

                next_number = 1

                if last_branch and last_branch.code:
                    try:
                        next_number = int(
                            last_branch.code.split("-")[-1]
                        ) + 1
                    except (ValueError, IndexError):
                        next_number = last_branch.pk + 1

                self.code = f"BRN-{next_number:04d}"

                super().save(*args, **kwargs)

            return

        super().save(*args, **kwargs)

    # Soft Delete
    def soft_delete(self, user):

        if self.deleted_at is not None:
            return

        self.is_active = False
        self.deleted_at = timezone.now()
        self.deleted_by = user

        self.save(
            update_fields=[
                "is_active",
                "deleted_at",
                "deleted_by",
                "updated_at"
            ]
        )

    # Restore
    def restore(self):

        if self.is_active and self.deleted_at is None:
            return

        self.is_active = True
        self.deleted_at = None
        self.deleted_by = None

        self.save(
            update_fields=[
                "is_active",
                "deleted_at",
                "deleted_by",
                "updated_at"
            ]
        )

    # Permanent Delete
    def hard_delete(self):
        return super().delete()

    class Meta:

        verbose_name = "Branch"
        verbose_name_plural = "Branches"

        ordering = ["name"]

        indexes = [
            models.Index(
                fields=["name"],
                name="branch_name_idx"
            ),
            models.Index(
                fields=["code"],
                name="branch_code_idx"
            ),
            models.Index(
                fields=["is_active"],
                name="branch_active_idx"
            ),
            models.Index(
                fields=["retailer", "is_active"],
                name="branch_retailer_active_idx"
            ),
        ]

        constraints = [

            models.UniqueConstraint(
                fields=["retailer", "name"],
                condition=models.Q(
                    is_active=True,
                    deleted_at__isnull=True
                ),
                name="unique_active_branch_name_per_retailer"
            ),

            models.UniqueConstraint(
                fields=["retailer", "code"],
                name="unique_active_branch_code_per_retailer"
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
