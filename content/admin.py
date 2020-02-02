from django.contrib import admin
from .models import TagType, NameContent, ContentTag


# auxiliary function constucts a set of fields (for foreign key field sets) with each category of tags
# this is for usability when there are many tags and types
def get_fieldsets_for_tags_by_type(foreign_key='tag'):
    fieldsets = ()
    for tag in TagType.choices():
        fieldsets = fieldsets + ((tag, {'fields': (foreign_key,)}),)
    return fieldsets


class ContentTagInline(admin.TabularInline):
    model = ContentTag


class NameContentAdmin(admin.ModelAdmin):
    inlines = [ContentTagInline]
    model = NameContent


admin.site.register(NameContent, NameContentAdmin)

