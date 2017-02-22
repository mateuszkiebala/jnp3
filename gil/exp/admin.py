from django.contrib import admin
from models import SessionSettings, SelectionResults, GilResults, Tasks, DescriptionSettings, UserTasks, PilotModeSettings, PilotModeResults
import csv

# Register your models here.


def export_to_csv(self, request, queryset, filename):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(self.list_display)
        for q in queryset:
            writer.writerow([q.user] + [dict(q)[header] for header in self.list_display[1:]])


class TasksAdmin(admin.ModelAdmin):
    list_display = ('id', 'top_description', 'bottom_description', 'rule',
                    'card_choice_description', 'card_P', 'card_nP', 'card_Q', 'card_nQ')


class SessionSettingsAdmin(admin.ModelAdmin):
    list_display = ('pause', 'training_gil_session_time',
                    'survey_gil_session_time',
                    'training_selection_session_time',
                    'training_tasks')


class GilResultsAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_type', 'task_id', 'clicks')
    actions = ['_export_to_csv']
    list_filter = ['user']

    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'gil_results.csv')
    _export_to_csv.short_description = "Export GIL results to CSV file."

    def has_add_permission(self, request):
        return False


class SelectionResultsAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'external_task_number',
                    'task_id',
                    'cards_order',
                    'correctness',
                    'correct_cards',
                    'doing_task_time',
                    'solving_task_time',
                    'card_P_clicks',
                    'card_nP_clicks',
                    'card_Q_clicks',
                    'card_nQ_clicks',
                    'card_P_final',
                    'card_nP_final',
                    'card_Q_final',
                    'card_nQ_final',
                    'chosen_cards')
    actions = ['_export_to_csv']
    list_filter = ['user']

    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'selection_results.csv')
    _export_to_csv.short_description = "Export selection results to CSV file."

    def has_add_permission(self, request):
        return False


class DescriptionSettingsAdmin(admin.ModelAdmin):
    list_display = ('welcome_description',
                    'training_gil_description',
                    'survey_gil_description',
                    'training_selection_description',
                    'survey_selection_description',
                    'ending_description')


class UserTasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'tasks', 'done')


class PilotModeSettingsAdmin(admin.ModelAdmin):
    list_display = ('welcome_description',
                    'training_tasks')


class PilotModeResultsAdmin(SelectionResultsAdmin):
    def _export_to_csv(self, request, queryset):
        export_to_csv(self, request, queryset, 'pilot_mode_results.csv')
    _export_to_csv.short_description = "Export pilot mode results to CSV file."


admin.site.register(Tasks, TasksAdmin)
admin.site.register(SessionSettings, SessionSettingsAdmin)
admin.site.register(GilResults, GilResultsAdmin)
admin.site.register(SelectionResults, SelectionResultsAdmin)
admin.site.register(DescriptionSettings, DescriptionSettingsAdmin)
admin.site.register(UserTasks, UserTasksAdmin)
admin.site.register(PilotModeSettings, PilotModeSettingsAdmin)
admin.site.register(PilotModeResults, PilotModeResultsAdmin)
