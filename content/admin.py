from django.contrib import admin
from .models import ContentTag, TagType


class ContentTagAdmin(admin.ModelAdmin):
    model = ContentTag


admin.site.register(ContentTag, ContentTagAdmin)
