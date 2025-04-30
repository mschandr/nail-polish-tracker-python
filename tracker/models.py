from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Brand"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ['name']

    def __str__(self):
        return f"Brand: {self.name}" if self.name else "Unnamed Brand"

class Location(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Location Name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["name"]

    def __str__(self):
        return f"Location: {self.name}" if self.name else "Unnamed Location"

class Collection(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand id"))
    name = models.CharField(max_length=150, verbose_name=_("Collection Name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ["name"]

    def __str__(self):
        if self.brand and self.name:
            return f"{self.brand.name}: {self.name}"
        elif self.name:
            return self.name
        else:
            return "Unnamed Collection"


class PolishType(models.TextChoices):
    BASECOAT = "BC", _("Base Coat")
    NAILPOLISH = "NP", _("Nail Polish")
    TOPCOAT = "TC", _("Top Coat")
    TOPPER = "TO", _("Nail Polish Topper")
    UNICORNSKIN = "US", _("Unicorn Skin")


class Shade(models.TextChoices):
    BLACK  = "black",   _("Black")
    BLUE   = "blue",    _("Blue")
    GREEN  = "green",   _("Green")
    GREY   = "grey",    _("Grey")
    ORANGE = "orange",  _("Orange")
    PINK   = "pink",    _("Pink")
    PURPLE = "purple",  _("Purple")
    RED    = "red",     _("Red")
    WHITE  = "white",   _("White")
    YELLOW = "yellow",  _("Yellow")


class Polish(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"))
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_("Location"))
    name = models.CharField(max_length=150, verbose_name=_("Polish Name"))
    product_url = models.URLField(verbose_name=_("Product URL"), null=True, blank=True)
    check_url_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Last checked URL at"))
    is_available = models.BooleanField(default=True, verbose_name=_("Is available online"))
    shade = models.CharField(
        max_length=20,
        choices=Shade.choices,
        default=Shade.PINK,
        verbose_name=_("Colour/Shade"),
    )
    polish_type = models.CharField(
        max_length=2,
        choices=PolishType.choices,
        default=PolishType.NAILPOLISH,
        verbose_name=_("Polish Type"),
    )
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Collection name")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Polish")
        verbose_name_plural = _("Polishes")
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["brand", "location", "name"], name="unique_brand_location_name_idx"
            )
        ]

    def __str__(self):
        name_display = self.name[:15] + "..." if len(self.name) > 15 else self.name

        if self.collection:
            return f"{self.brand.name}: {name_display} (Collection: {self.collection.name})"
        else:
            return f"{self.brand.name}: {name_display}"


class Worn(models.Model):
    worn_at = models.DateTimeField(auto_now_add=True, blank=False, verbose_name=_("Date worn"))
    notes = models.CharField(max_length=255, verbose_name=_("Notes"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Worn")
        verbose_name_plural = _("Worn")
        ordering = ['-worn_at']

    def __str__(self):
        return f"Worn #{self.id} on {self.worn_at.strftime('%Y-%m-%d %H:%M')}"

class WornPhotos(models.Model):
    worn = models.ForeignKey(Worn, on_delete=models.CASCADE)
    notes = models.CharField(max_length=255, verbose_name=_("Notes"), null=True, blank=True)
    thumbnail = models.ImageField(
        'Thumbnail URL',
        upload_to='photos/thumbnails/',
        blank=True,
        verbose_name=_("Thumbnail Image")
    )
    photo = models.ImageField(
        'Photo URL',
        upload_to='photos/',
        blank=True,
        verbose_name=_("Full Image")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Worn Photo")
        verbose_name_plural = _("Worn Photos")
        ordering = ['-created_at']

    def __str__(self):
        thumbnail_display = self.thumbnail.url if self.thumbnail else "No thumbnail"
        photo_display = self.photo.url if self.photo else "No photo"

        return f"Worn #{self.worn.id} with {thumbnail_display} and {photo_display}"

class WornLayers(models.Model):
    worn = models.ForeignKey(Worn, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name=_("Layer Order"))
    layer_type = models.CharField(
        max_length=2,
        choices=PolishType.choices,
        default=PolishType.BASECOAT,
        verbose_name=_("Layer Type")
    )
    polish = models.ForeignKey(Polish, on_delete=models.CASCADE, verbose_name=_("Polish Used"))
    class Meta:
        verbose_name = _("Worn Layers")
        verbose_name_plural = _("Worn Layers")
        ordering = ['order']
        unique_together = ('worn', 'order')

    def __str__(self):
        return f"{self.worn.id} - Layer {self.order}: {self.polish.name} ({self.get_layer_type_display()})"