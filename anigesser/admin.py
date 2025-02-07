from django.contrib import admin
from .models import *

admin.site.register(Genre)
admin.site.register(Type)
admin.site.register(Source)
admin.site.register(Theme)
admin.site.register(Studio)

class TitleNameInline(admin.TabularInline):
    model = TitleName
    extra = 0

class TitleAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'get_title_names')
    inlines = [TitleNameInline]

    def get_title_names(self, obj):
        return ", ".join([alt.name for alt in obj.title_names.all()])
    get_title_names.short_description = "Альтернативные названия"

admin.site.register(Title, TitleAdmin)
admin.site.register(TitleName)

admin.site.register(Screenshots)
admin.site.register(Character)

admin.site.register(Day)

admin.site.register(Suggestion)