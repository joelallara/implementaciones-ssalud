from django.db import models

from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides 'user' and self-updating
    'created' and 'modified' fields.
    """
    # user =
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha Creación",
        null=True
        )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha Modificación",
        null=True
        )

    class Meta:
        abstract = True


class ActivedModel(models.Model):
    """
    An abstract base class model that provides 'active','reason', self-
    updating 'disabled_date' and 'user' fields.
    """
    actived = models.BooleanField(default=True, verbose_name="Habilitado")
    reason = models.CharField(
        max_length=100,
        verbose_name="Motivo",
        null=True,
        blank=True)
    disabled_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha Baja"
        )
    # user =

    class Meta:
        abstract = True

    def desactivate(self, date=None, reason=None):
        if not date:
            date = timezone.now()
        self.disabled_date = date
        self.reason = reason
        self.actived = False
        self.save()


class PermalinkModel(models.Model):
    """
    An abstract base class model that provides 'slug' field.
    """
    slug = models.SlugField()

    class Meta:
        abstract = True
