from django.contrib import admin
from .models import Brand, Location, Collection, Polish, Worn, WornPhotos, WornLayers


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
    readonly_fields = ('created_at', 'updated_at', 'check_url_at',)
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

@admin.register(Worn)
class WornAdmin(admin.ModelAdmin):
    list_display = ('worn_at', 'notes',)
    search_fields = ('worn_at','notes',)
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('-worn_at',)

@admin.register(WornPhotos)
class WornPhotosAdmin(admin.ModelAdmin):
    list_display = ('worn', 'photo_type', 'image', 'notes',)
    search_fields = ('worn','photo_type',)
    raw_id_fields = ('worn',)
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('-worn__worn_at',)

@admin.register(WornLayers)
class WornLayersAdmin(admin.ModelAdmin):
    list_display = ('order', 'layer_type', 'polish',)
    raw_id_fields = ('worn',)
    ordering = ('-worn__worn_at','order',)
