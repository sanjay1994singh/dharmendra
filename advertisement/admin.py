from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'position',
        'ad_type',
        'sponsor_name',
        'is_active',
        'starts_at',
        'ends_at',
        'display_order',
        'updated_at',
    )
    list_filter = ('position', 'ad_type', 'is_active')
    search_fields = ('title', 'sponsor_name', 'internal_note')
    list_editable = ('is_active', 'display_order')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Where this ad shows', {
            'fields': ('title', 'position', 'display_order', 'is_active')
        }),
        ('Ad content', {
            'fields': ('ad_type', 'sponsor_name', 'image', 'target_url', 'text', 'html_code')
        }),
        ('Schedule', {
            'fields': ('starts_at', 'ends_at')
        }),
        ('Tracking note', {
            'fields': ('internal_note',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at')
        }),
    )
