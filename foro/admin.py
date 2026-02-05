from django.contrib import admin
from .models import Post ,Categoria, Marca, ModeloDispositivo, Post

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(ModeloDispositivo)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "marca",
        "modelo",
        "estado",
        "publicado",
        "vistas",
        "creado",
    )

    list_filter = (
        "categoria",
        "marca",
        "estado",
        "publicado",
        "creado",
    )

    search_fields = (
        "titulo",
        "descripcion",
        "modelo__nombre",
        "marca__nombre",
    )

    prepopulated_fields = {"slug": ("titulo",)}
