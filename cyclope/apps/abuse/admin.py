from django.contrib import admin
from models import AbuseType, AbuseReport, AbuseReportElement

class AbuseReportElementInline(admin.TabularInline):
    model = AbuseReportElement
    fields = ('abuse_type', 'user', 'date', 'text')
    readonly_fields = ('abuse_type', 'user', 'date', 'text')
    extra = 0

class AbuseReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'link', 'user', 'status', 'count', 'date')
    list_display_links = ('__unicode__',)
    list_editable = ('status', )
    list_filter = ('status', )
    inlines = [AbuseReportElementInline,]

admin.site.register(AbuseType)
admin.site.register(AbuseReport, AbuseReportAdmin)
