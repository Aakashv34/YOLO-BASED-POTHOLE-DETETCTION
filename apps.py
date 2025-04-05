from django.apps import AppConfig

from django.contrib import admin

# @admin.register(DetectionHistory)
# class DetectionHistoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'timestamp', 'result')
#     ordering = ('-timestamp',)


class DetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'detection'
