from django.conf import settings
from django.db import models
from django.db.models import CASCADE

from url_shortener.utils import create_shortened_url


class Url(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    redirect_count = models.PositiveIntegerField(default=0)
    long_url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = create_shortened_url(self)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
