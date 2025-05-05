from django.db import models
from django.utils.translation import gettext_lazy as _

#Abstract models
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


# Create your models here.
class PolishType(models.TextChoices):
    TOPCOAT         = "TC", _("Top Coat")
    BASECOAT        = "BC", _("Base Coat")
    NAILPOLISH      = "NP", _("Nail Polish")
    UNICORNSKIN     = "US", _("Unicorn Skin")
    TOPPER          = "TO", _("Nail Polish Topper")

    def __str__(self):
        return f"PolishType: {self.name}"

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

    def __str__(self):
        return f"Shade: {self.name}"


class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Brand"))

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        ordering = ['name']

    def __str__(self):
        return f"Brand: {self.name}"


class Location(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Location Name"))

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["name"]

    def __str__(self):
        return f"Location: {self.name}" if self.name else "Unnamed Location"


class Collection(TimeStampedModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand id"))
    name  = models.CharField(max_length=150, verbose_name=_("Collection Name"))

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")
        ordering = ["name"]

    def __str__(self):
        brand_name = self.brand.name if self.brand else "Unknown Brand"
        return f"{brand_name}: {self.name or 'Unnamed Collection'}"

class Polish(TimeStampedModel):
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


class Worn(TimeStampedModel):
    worn_at = models.DateTimeField(auto_now_add=True, blank=False, verbose_name=_("Date worn"))
    notes = models.CharField(max_length=255, verbose_name=_("Notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("Worn")
        verbose_name_plural = _("Worn")
        ordering = ['-worn_at']

    def __str__(self):
        return f"Worn #{self.id} on {self.worn_at.strftime('%Y-%m-%d %H:%M')}"


class WornPhotos(TimeStampedModel):
    worn = models.ForeignKey(Worn, on_delete=models.CASCADE, related_name='photos', verbose_name=_("Worn"))
    photo_type = models.CharField(max_length=50, verbose_name=_("Photo Type"),
        help_text=_("Example: 'flash on', 'macro', 'sunlight'. Try to reuse existing labels.")
    )
    image = models.ImageField(
        upload_to="photos/",
        verbose_name=_("Photo")
    )
    notes = models.CharField(max_length=255, verbose_name=_("Notes"), null=True, blank=True)

    class Meta:
        verbose_name = _("Worn Photo")
        verbose_name_plural = _("Worn Photos")
        ordering = ['-created_at']

    def __str__(self):
        return f"Worn #{self.worn} - {self.photo_type or 'Unknown'}"


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
        ordering = ['worn','order']
        constraints = [
            models.UniqueConstraint(fields=['worn', 'order'], name='unique_worn_order')
        ]

    def __str__(self):
        return f"{self.worn.id} - Layer {self.order}: {self.polish.name} ({self.get_layer_type_display()})"