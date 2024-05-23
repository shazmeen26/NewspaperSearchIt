from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Uploads, NewsRecord


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'is_staff', 'is_active',
                    'date_joined',  'name')

    list_filter = ('email', 'is_staff', 'is_active', 'name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'date_joined', 'name')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'date_joined', 'name')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)


class UploadsAdmin(admin.ModelAdmin):
    model = Uploads

    list_display = ('user', 'file')

    list_filter = ('user', )

    search_fields = ('user',)
    ordering = ('user',)


class NewsRecordAdmin(admin.ModelAdmin):
    model = NewsRecord

    list_display = ('user', 'file_path',
                    'external_file_path', 'extracted_text', 'timestamp')

    list_filter = ('user',  'file_path', 'timestamp')

    search_fields = ('user',  'file_path', 'timestamp')

    ordering = ('timestamp',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Uploads, UploadsAdmin)
admin.site.register(NewsRecord, NewsRecordAdmin)


admin.site.site_header = "Newspaper SearchIt Admin"
admin.site.site_title = "Newspaper SearchIt Admin Portal"
admin.site.index_title = "Welcome to Newspaper SearchIt Portal"
