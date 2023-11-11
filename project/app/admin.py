# Django
# First-Party
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin

# Local
from .forms import UserChangeForm
from .forms import UserCreationForm
from .inlines import AssignmentInline
from .inlines import MessageArchiveInline
from .inlines import RakeInline
from .inlines import YardInline
# from .inlines import RecipientInline
# from .inlines import TeamInline
from .models import Assignment
from .models import Event
from .models import MessageArchive
from .models import Picture
from .models import Rake
from .models import Recipient
from .models import Team
from .models import User
from .models import Yard


@admin.register(Recipient)
class RecipientAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'location',
        'size',
        'is_veteran',
        'is_senior',
        'is_disabled',
        'is_dog',
        'user',
        'public_notes',
        'admin_notes',
        'bags',
    ]
    list_display = [
        'id',
        'user',
        'location',
        'size',
        'state',
    ]
    list_filter = [
        'state',
        'size',
        'is_veteran',
        'is_senior',
        'is_disabled',
        'is_dog',
        'created',
        'updated',
    ]
    search_fields = [
        'user__name',
        'user__phone',
        'location',
    ]
    list_editable = [
        'state',
        'user',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        YardInline,
    ]
    ordering = [
        'created',
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates


@admin.register(Yard)
class YardAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'recipient',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_display = [
        'state',
        'recipient',
        'public_notes',
        'admin_notes',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'recipient__size',
    ]
    search_fields = [
        'recipient__user__name',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'recipient',
        'event',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'recipient__user__name',
    ]
    readonly_fields = [
    ]


@admin.register(Rake)
class RakeAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'public_notes',
        'admin_notes',
        'team',
        'event',
    ]
    list_display = [
        'id',
        'state',
        'public_notes',
        'admin_notes',
        'team',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'team__size',
    ]
    search_fields = [
        'team__nickname',
        'team__user__name',
    ]
    list_editable = [
    ]
    autocomplete_fields = [
        'team',
        'event',
    ]
    inlines = [
        AssignmentInline,
    ]
    ordering = [
        'team__nickname',
        'team__user__name',
    ]
    readonly_fields = [
    ]


@admin.register(Team)
class TeamAdmin(VersionAdmin):

    save_on_top = True
    fields = [
        'state',
        'nickname',
        'size',
        'public_notes',
        'admin_notes',
        'user',
    ]
    list_display = [
        'nickname',
        'user',
        'size',
        # 'nickname',
        # 'recipient_sizes',
        'state',
        # 'created',
        # 'public_notes',
        # 'admin_notes',
        # 'latest_message',
    ]
    list_filter = [
        'state',
        'size',
        'created',
        'updated',
    ]
    search_fields = [
        'nickname',
        'user__name',
        'user__phone',
    ]
    list_editable = [
        'state',
    ]
    autocomplete_fields = [
        'user',
    ]
    inlines = [
        # AssignmentInline,
        RakeInline,
    ]
    ordering = [
    ]
    readonly_fields = [
        # 'latest_message',
        # 'user_url',
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(user__phone=search_term)
        return queryset, may_have_duplicates

@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'state',
        'event',
        'yard',
        'rake',
        'public_notes',
        'admin_notes',
    ]
    list_display = [
        'id',
        'state',
        'yard',
        # 'yard__size',
        'rake',
        # 'rake__size',
        'event',
    ]
    list_filter = [
        'event__year',
        'state',
        'yard__recipient__size',
        'rake__team__size',
        # 'team_state',
    ]

    list_editable = [
        'yard',
        'rake',
    ]
    autocomplete_fields = [
        'yard',
        'rake',
        'event',
    ]
    readonly_fields = [
        # 'yard__size',
        # 'rake__size',
    ]


@admin.register(Event)
class EventAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'year',
        'state',
        'deadline',
        'date',
        # 'created',
        # 'updated',
    ]
    list_display = [
        'year',
        'state',
        'deadline',
        'date',
        'created',
        'updated',
    ]
    list_filter = [
    ]
    inlines = [
        AssignmentInline,
    ]
    list_editable = [
    ]
    autocomplete_fields = [
    ]
    search_fields = [
        'year',
    ]


@admin.register(MessageArchive)
class MessageArchiveAdmin(VersionAdmin):

    # def user_url(self, obj):
    #     user_url = reverse('admin:app_user_change', args=[obj.user.id])
    #     return format_html("<a href='{url}'>User</a>", url=user_url)

    fields = [
        'id',
        'state',
        'body',
        'sid',
        'to_phone',
        'from_phone',
        'direction',
        'raw',
        'created',
        'updated',
    ]
    list_display = [
        'id',
        # 'user_url',
        'body',
        'direction',
        'created',
        'updated',
    ]
    list_editable = [
    ]
    list_filter = [
        'direction',
        'state',
    ]
    search_fields = [
    ]
    autocomplete_fields = [
    ]
    inlines = [
    ]
    ordering = [
        '-created',
    ]
    readonly_fields = [
        'id',
        'sid',
        # 'to_phone',
        'from_phone',
        'user_id',
        # 'direction',
        'created',
        'updated',
        'raw',
    ]


@admin.register(Picture)
class PictureAdmin(VersionAdmin):
    save_on_top = True
    fields = [
        'image',
    ]


@admin.register(User)
class UserAdmin(UserAdminBase):
    save_on_top = True
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    fieldsets = (
        (None, {
            'fields': [
                'name',
                'phone',
            ]
        }
        ),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_verified',)}),
    )
    list_display = [
        'name',
        'phone',
        'created',
        'last_login'
    ]
    list_filter = [
        'is_active',
        'is_admin',
        'is_verified',
        'created',
        'last_login',
    ]
    search_fields = [
        'phone',
        'name',
    ]
    ordering = [
        'phone',
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': [
                'is_admin',
                'is_active',
                'is_verified',
            ]
        }
        ),
    )
    filter_horizontal = ()
    inlines = [
        # MessageInline,
    ]
    readonly_fields = [
    ]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(phone=search_term)
        return queryset, may_have_duplicates


# Use Passwordless for login
admin.site.login = staff_member_required(
    admin.site.login,
    login_url=settings.LOGIN_URL,
)
