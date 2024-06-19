from apps.telegram_users.models import TelegramUsers

from django.contrib import admin


class TelegramUsersAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'chat_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'username', 'chat_id')


admin.site.register(TelegramUsers, TelegramUsersAdmin)
