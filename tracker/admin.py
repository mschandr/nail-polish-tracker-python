from django.contrib import admin
from .models import Brand, Location, Collection, Polish, WornPhotos, WornLayers


admin.site.site_header = "Suzanne's Nail Polish Tracker Admin"
admin.site.site_title = "Nail Polish Tracker Admin Portal"
admin.site.index_title = "Welcome to the Nail Polish Tracker Portal"

# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Polish)
class PolishAdmin(admin.ModelAdmin):
    autocomplete_fields = ['brand', 'location', 'collection']
    list_display = ('name', 'brand', 'location', 'is_available', 'shade', 'polish_type', 'collection',)
    list_filter = ('brand', 'shade', 'polish_type',  'is_available',)
    readonly_fields = ('is_available', 'product_url', 'created_at', 'updated_at', 'check_url_at',)
    search_fields = ('name','brand__name', 'shade', 'polish_type', 'collection__name',)
    list_select_related = ('brand', 'location', 'collection',)
    ordering = ('name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('brand', 'name',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(WornPhotos)
class WornPhotosAdmin(admin.ModelAdmin):
    list_display = ('photo_type', 'image', 'notes', 'worn_at')
    search_fields = ('worn','photo_type',)
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('-worn_at',)

@admin.register(WornLayers)
class WornLayersAdmin(admin.ModelAdmin):
    list_display = ('order', 'finger', 'layer_type', 'polish',)
    ordering = ('-wornphotos__worn_at','order', 'finger')
