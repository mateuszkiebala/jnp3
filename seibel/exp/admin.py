from django.contrib import admin
from models import UserSettings, UserResult, UserSessions
import csv

# Register your models here.


def export_to_csv(self, request, queryset, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(self.list_display)
        for q in queryset:
            writer.writerow([q.user] + [dict(q)[header] for header in self.list_display[1:]])


class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_limit', 'feedback_type', 'timer_type', 'time_gap')
    actions = ['_export_to_csv']
    list_filter = ['user']

    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'settings.csv')
    _export_to_csv.short_description = "Export settings to CSV file."


class UserResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'timer_type', 'session_number', 'configuration',
                    'start_time', 'end_time', 'total_time', 'errors_count', 'is_correct',
                    'bulb_1', 'bulb_2', 'bulb_3', 'bulb_4', 'bulb_5', 'bulb_6', 'bulb_7', 'bulb_8', 'bulb_9', 'bulb_10',
                    'fin_1', 'fin_2', 'fin_3', 'fin_4', 'fin_5', 'fin_6', 'fin_7', 'fin_8', 'fin_9', 'fin_10')
    list_filter = ['user']
    actions = ['_export_to_csv']

    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'results.csv')
    _export_to_csv.short_description = "Export results to CSV file."

    def has_add_permission(self, request):
        return False


class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'timer_type', 'session_number', 'training_done')
    actions = ['_export_to_csv']
    list_filter = ['user']

    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'sessions.csv')
    _export_to_csv.short_description = "Export sessions to CSV file."


admin.site.register(UserSessions, UserSessionAdmin)
admin.site.register(UserResult, UserResultAdmin)
admin.site.register(UserSettings, UserSettingsAdmin)