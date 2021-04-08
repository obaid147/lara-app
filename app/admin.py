from django.contrib import admin
from .models import LaraEnquiry, LaraEnquiryForm, FollowUp


class LaraAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    fields = (
        'name',
        'mobile',
        'email',
        'pass_out_Year',
        'latest_education',
        'branch',
        'percentages',
        'university_or_college',
        'state',
        'appointment_date',
        'Gender',
    )
    form = LaraEnquiryForm
    list_display = ('name', 'mobile', 'email', 'appointment_date')
    # search_fields = ('name', 'mobile')


admin.site.register(LaraEnquiry, LaraAdmin)
admin.site.register(FollowUp)
