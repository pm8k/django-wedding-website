from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'is_attending', 'meal', 'is_child')
    readonly_fields = ('first_name', 'last_name')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rehearsal_dinner', 'invitation_opened',
                    'is_attending')
    list_filter = ('category', 'is_attending', 'rehearsal_dinner', 'invitation_opened')
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'is_attending', 'is_child', 'meal')
    list_filter = ('is_attending', 'is_child', 'meal', 'party__category', 'party__rehearsal_dinner')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
