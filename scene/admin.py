from django.contrib import admin
from .models import *


class SceneTypeTagInline(admin.TabularInline):
    model = SceneTypeTag


class SceneTagInline(admin.TabularInline):
    model = SceneTag


class FeatureTagInline(admin.TabularInline):
    model = FeatureTag


class SceneFeatureInline(admin.TabularInline):
    model = SceneFeature


class SceneTypeAdmin(admin.ModelAdmin):
    inlines = [SceneTypeTagInline]


class SceneAdmin(admin.ModelAdmin):
    inlines = [SceneTagInline, SceneFeatureInline]


class FeatureAdmin(admin.ModelAdmin):
    inlines = [FeatureTagInline]


admin.site.register(SceneType, SceneTypeAdmin)
admin.site.register(Scene, SceneAdmin)
admin.site.register(Feature, FeatureAdmin)
