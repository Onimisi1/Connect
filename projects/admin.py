from django.contrib import admin

# Register your models here.

from .models import Project, Review, Tag


#class ProjectAdmin(admin.ModelAdmin):
 #   pass
    # list_display = ('title', 'vote_total', 'created',)


admin.site.register(Project) #ProjectAdmin)
admin.site.register(Review)
admin.site.register(Tag)
