from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models
from django.utils.safestring import mark_safe
from django_fsm import FSMIntegerField
# from django_fsm import transition
from hashid_field import HashidAutoField
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField

# Local
from .managers import UserManager


class Recipient(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-40, 'blocked', 'Blocked'),
        (-20, 'cancelled', 'Cancelled'),
        (-10, 'inactive', 'Inactive'),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
        (20, 'confirmed', 'Confirmed'),
        (30, 'assigned', 'Assigned'),
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
    bags = models.IntegerField(
        blank=True,
        null=True,
        help_text='Bags estimate',
    )
    location = models.CharField(
        max_length=512,
        blank=True,
        default='',
        help_text="""Please provide the street address to be raked (City of Eagle is assumed)."""
    )
    point = models.PointField(
        null=True,
        blank=True,
    )
    is_senior = models.BooleanField(
        default=False,
    )
    is_disabled = models.BooleanField(
        default=False,
    )
    is_veteran = models.BooleanField(
        default=False,
    )
    is_dog = models.BooleanField(
        blank=True,
        default=False,
        help_text=mark_safe("""If you have a dog, it must be contained in your home for us to rake. <em>Also, you must clean up all animal waste before we arrive or our team group will not be able to rake.</em>"""),
    )
    public_notes = models.TextField(
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
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='recipient',
    )
    def __str__(self):
        return f"{self.user.name} - {self.get_size_display()}"

    # @transition(field=state, source=[STATE.new], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Team(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-20, 'cancelled', 'Cancelled'),
        (-10, 'inactive', 'Inactive'),
        (0, 'new', 'New'),
        (10, 'active', 'Active'),
        (20, 'confirmed', 'Confirmed'),
        (30, 'assigned', 'Assigned'),
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
    adults = models.IntegerField(
        blank=True,
        null=True,
        help_text='The actual number of adults, or adult-equivalent in children.',
    )
    nickname = models.CharField(
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
    public_notes = models.TextField(
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
    user = models.OneToOneField(
        'app.User',
        on_delete=models.CASCADE,
        related_name='team',
    )
    def __str__(self):
        return f"{self.user.name} - {self.nickname}"

    # @transition(field=state, source=[STATE.new,], target=STATE.confirmed)
    # def confirm(self):
    #     return


class Assignment(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    STATE = Choices(
        (-20, 'failed', 'Failed'),
        (-10, 'cancelled', 'Cancelled'),
        (0, 'new', 'New'),
        (10, 'assigned', 'Assigned'),
        (40, 'started', 'Started'),
        (50, 'finished', 'Finished'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    public_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    admin_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Internal (private) notes.""",
    )
    recipient = models.ForeignKey(
        'app.Recipient',
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        'app.Team',
        on_delete=models.CASCADE,
        related_name='assignments',
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        'app.Event',
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


class Event(models.Model):
    id = HashidAutoField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="""Your full name."""
    )
    STATE = Choices(
        (-10, 'archive', 'Archive'),
        (0, 'new', 'New'),
        (10, 'current', 'Current'),
    )
    state = FSMIntegerField(
        choices=STATE,
        default=STATE.new,
    )
    year = models.IntegerField(
        blank=True,
        null=True
    )
    admin_notes = models.TextField(
        max_length=2000,
        blank=True,
        default='',
        help_text="""Please add any other notes you think we should know.""",
    )
    deadline =  models.DateField(
        null=True,
        blank=True,
    )
    date =  models.DateField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    def __str__(self):
        return f"{self.year}"


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
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    user = models.ForeignKey(
        'app.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='messages',
    )
    def __str__(self):
        return f"{self.id}"


class User(AbstractBaseUser):
    id = HashidAutoField(
        primary_key=True,
    )
    phone = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        null=False,
        default='',
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_verified = models.BooleanField(
        default=False,
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

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = [
        'phone',
    ]

    objects = UserManager()

    class Meta:
        ordering = (
            'phone',
        )


    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f"{self.phone} - {self.name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
