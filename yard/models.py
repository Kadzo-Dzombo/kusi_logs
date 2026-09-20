import random
import string
from decimal import Decimal
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, value):
    slug = slugify(value)

    Klass = instance.__class__

    original_slug = slug
    counter = 1

    while Klass.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f'{original_slug}-{counter}'
        counter += 1

    return slug

SIZE_CHOICES = (
    ('20ft', '20ft'),
    ('40ft', '40ft'),
)

STATUS_CHOICES = (
    ('Available', 'Available'),
    ('Out of Yard', 'Out of Yard'),
    ('Reserved', 'Reserved'),
)


class Yard(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("yard_detail", kwargs={"slug": self.slug})


class Reference(models.Model):
    reference_no = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    yard = models.ForeignKey(Yard, on_delete=models.CASCADE, related_name='references')

    def __str__(self):
        return self.reference_no

    def get_absolute_url(self):
        return reverse("reference_detail", kwargs={"slug": self.slug})


class Container(models.Model):

    AVAILABLE = 'Available'
    OUT_OF_YARD = 'Out of Yard'
    RESERVED = 'Reserved'

    STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (OUT_OF_YARD, 'Out of Yard'),
        (RESERVED, 'Reserved'),
    )

    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, related_name='containers')
    container_no = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    size = models.CharField(max_length=120, choices=SIZE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, blank=True, null=True)

    client_name = models.CharField(max_length=120, blank=True, null=True)
    phone_number = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.container_no

    def get_absolute_url(self):
        return reverse("container_detail", kwargs={"slug": self.slug})


class Invoice(models.Model):

    invoice_no = models.CharField(
        max_length=120,
        unique=True
    )

    date = models.DateField()

    company_name = models.CharField(
        max_length=200
    )

    address = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    phone_no = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    email_address = models.EmailField(
        blank=True,
        null=True
    )

    attention = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    amount_in_words = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    grand_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )

    bill_of_sale = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    delivery = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )

    authorised_signature = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    buyer_acknowledgement = models.TextField(
        blank=True,
        null=True
    )

    buyer_signature = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse(
            "invoice_detail",
            kwargs={"pk": self.pk}
        )

    def calculate_grand_total(self):
        total = sum(
            item.total_amount
            for item in self.items.all()
        )

        self.grand_total = total
        return total


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    ser_no = models.CharField(
        max_length=120
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )

    def __str__(self):
        return self.ser_no

    def save(self, *args, **kwargs):

        self.total_amount = (
            self.quantity * self.unit_price
        )

        super().save(*args, **kwargs)


class Inquiry(models.Model):
    """A quote request submitted from the public homepage contact form."""

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'
        ARCHIVED = 'archived', 'Archived'

    CONTAINER_CHOICES = [
        ('20ft Standard Container', '20ft Standard Container'),
        ('40ft Standard Container', '40ft Standard Container'),
        ('40ft High Cube', '40ft High Cube'),
        ('45ft High Cube', '45ft High Cube'),
        ('Not sure - need advice', 'Not sure - need advice'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    container_type = models.CharField(
        max_length=100,
        choices=CONTAINER_CHOICES,
        blank=True,
    )
    delivery_location = models.CharField(
        max_length=200,
        help_text="Delivery zip or port",
    )
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']          # newest first, everywhere
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"{self.full_name} — {self.created_at:%d %b %Y}"

    @property
    def is_unread(self):
        return self.status == self.Status.NEW

    def mark_read(self):
        if self.status == self.Status.NEW:
            from django.utils import timezone
            self.status = self.Status.READ
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])


def yard_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance,
            instance.name
        )


def reference_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance,
            instance.reference_no
        )


def container_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance,
            instance.container_no
        )


pre_save.connect(
    yard_pre_save_receiver,
    sender=Yard
)

pre_save.connect(
    reference_pre_save_receiver,
    sender=Reference
)

pre_save.connect(
    container_pre_save_receiver,
    sender=Container
)