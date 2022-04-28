from django.contrib import admin

# Register your models here.
from .models import TypeLosses, Losses

admin.site.register(TypeLosses)
admin.site.register(Losses)