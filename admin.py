from django.contrib import admin
from .models import DetectionHistory

# Register your models here.

from .models import DetectionHistory

@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'result')
    ordering = ('-timestamp',)

class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'detection_result', 'confidence', 'timestamp')
    list_filter = ('timestamp',)


    search_fields = ('result',)

