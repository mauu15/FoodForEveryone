from django.contrib import admin

from .models import Recipe, Comment, Follower


# Register your models here.

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Mostra l'autore nella lista delle ricette
    search_fields = ('title', 'author__username')  # Aggiungi la ricerca per autore

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment)


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower', 'created_at')
    search_fields = ('user__username', 'follower__username')
