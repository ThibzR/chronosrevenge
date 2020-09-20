from django.contrib import admin, messages
from .models import User, Course, Group, Blacklist
from .actions import refresh_groups


# Custom actions
def fetch_groups_entity_id(modeladmin, request, queryset):
    if refresh_groups():
        messages.success(request, 'Refresh successful!')
    else:
        messages.error(request, 'An error has occurred! Time to debug.')

fetch_groups_entity_id.short_description = 'Refresh groups entity id'


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'entity_id', 'date_added']
    ordering = ['name']
    actions = [fetch_groups_entity_id]


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_added']
    readonly_fields = ('date_added',)


class BlacklistAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)


# Register your models here.
admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Blacklist, BlacklistAdmin)