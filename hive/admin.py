from django.contrib import admin
from content.admin import get_fieldsets_for_tags_by_type
from .models import Actor, ActorTag, GroupMember


class ActorTagInline(admin.TabularInline):
    model = ActorTag


class GroupInline(admin.TabularInline):
    model = GroupMember


class ActorAdmin(admin.ModelAdmin):
    inlines = [ActorTagInline, GroupInline]
    fieldsets = (
        ('Hive', {'fields': ('hive',)}),
        ('Personal Details', {'fields': ('name',)}),
    ) + get_fieldsets_for_tags_by_type('tags')

    # TODO: on edit, override the foreign key to only display values which match actor's tags
    '''def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "name":
            print(str(request))
            # intersection of NameContent tags and actor tags
            kwargs["queryset"] = self.tags.all() & self.name.tags.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)'''


admin.site.register(Actor, ActorAdmin)
