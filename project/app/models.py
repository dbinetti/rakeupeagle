# Django
# Standard Libary
import os
import secrets

# First-Party
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe
from django_fsm import FSMIntegerField
from django_fsm import transition
from hashid_field import HashidAutoField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField

# Local
from .managers import UserManager


def get_latest_event():
    return Event.objects.latest('date')


@deconstructible
class UploadPath(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
        short = secrets.token_urlsafe()[:8]
        return os.path.join(
            self.name,
            short,
        )


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-10, 'cancelled', 'Cancelled'),
        (0, 'new', 'New'),
        (10, 'pending', 'Pending'),
        (20, 'confirmed', 'Confirmed'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    SIZE = Choices(
        (110, 'small', 'Small (1-15 bags)'),
        (120, 'medium', 'Medium (16-30 bags)'),
        (130, 'large', 'Large (31+ bags)'),
    )
    size = models.IntegerField(
        blank=True,
        choices=SIZE,
        help_text="""Please provide the approximate yard size."""
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Please provide the location address to be raked."""
    )
    place = models.CharField(
        max_length=255,
        blank=True,
        default='',
    )
    is_precise = models.BooleanField(
        default=False,
    )
    point = models.PointField(
        null=True,
        blank=True,
    )
    geocode = models.JSONField(
        blank=True,
        null=True,
    )
    is_dog = models.BooleanField(
        blank=True,
        default=False,
        help_text=mark_safe("""If you have a dog, it must be contained in your home for us to rake. <em>Also, you must clean up all animal waste before we arrive or our team group will not be able to rake.</em>"""),
    )
    notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    admin_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Administrator Notes (from calling).""",
    )
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Actual Bags Used',
    )
    hours = models.FloatField(
        blank=True,
        null=True,
        help_text='Actual Hours Worked',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='recipients',
        null=False,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipients',
    )
    def __str__(self):
        return f"{self.name}, {self.location} - {self.get_size_display()}"

    @transition(field=state, source=[STATE.pending,STATE.new], target=STATE.confirmed)
    def confirm(self):
        return


class Team(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-10, 'cancelled', 'Cancelled'),
        (0, 'new', 'New'),
        (10, 'pending', 'Pending'),
        (20, 'confirmed', 'Confirmed'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    SIZE = Choices(
        (105, 'solo', 'Solo (1 Adult)'),
        (110, 'xs', 'Extra-Small (2-5 Adults)'),
        (120, 'small', 'Small (6-10 Adults)'),
        (130, 'medium', 'Medium (11-15 Adults)'),
        (140, 'large', 'Large (16-20 Adults)'),
        (150, 'xl', 'Extra-Large (21+ Adults)'),
    )
    size = models.IntegerField(
        blank=False,
        choices=SIZE,
        help_text='The size of your group. (Number of adults, or equivalent in children.)',
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    team = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Whimsical Team Name (ie, Robert's Rakers, Covey Courters, etc.)""",
    )
    reference = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""How did you hear about us?""",
    )
    actual = models.IntegerField(
        blank=True,
        null=True,
        help_text='The actual number of adults, or adult-equivalent in children.',
    )
    notes = models.TextField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Notes.""",
    )
    admin_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Administrator Notes (from calling).""",
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='teams',
        null=False,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams',
    )

    def __str__(self):
        return f"{self.team} - {self.get_size_display()}"

    @transition(field=state, source=[STATE.pending,STATE.new,], target=STATE.confirmed)
    def confirm(self):
        return


class Event(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
        (20, 'archived', 'Archived'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    name = models.CharField(
        max_length=100,
        blank=False,
    )
    year = models.IntegerField(
        null=False,
        blank=False,
    )
    deadline = models.DateField(
        blank=False,
        null=False,
    )
    date = models.DateField(
        blank=False,
        null=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.year}"


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (0, 'new', 'New'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    recipient = models.ForeignKey(
        'app.Recipient',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    team = models.ForeignKey(
        'app.Team',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return f"{self.id}"


class Message(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (0, 'new', 'New'),
        (10, 'sent', 'Sent'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    sid = models.CharField(
        max_length=100,
        blank=True,
    )
    to_phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    from_phone = PhoneNumberField(
        blank=True,
        null=True,
    )
    body = models.TextField(
        blank=True,
    )
    DIRECTION = Choices(
        (10, 'inbound', 'Inbound'),
        (20, 'outbound', 'Outbound'),
    )
    direction = models.IntegerField(
        choices=DIRECTION,
        null=True,
        blank=True,
    )
    raw = models.JSONField(
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.id}"


class Picture(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    image = models.ImageField(
        upload_to=UploadPath('image'),
        blank=True,
    )
    event = models.ForeignKey(
        'app.Event',
        on_delete=models.CASCADE,
        related_name='pictures',
        null=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )


class User(AbstractBaseUser):
    id = HashidAutoField(
        primary_key=True,
    )
    username = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=False,
        default='',
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
    )
    data = models.JSONField(
        null=True,
        editable=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
    ]

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
