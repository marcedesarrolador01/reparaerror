from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# =========================
# ESTADOS DE REPARACIÓN
# =========================
class EstadoReparacion(models.TextChoices):
    ABIERTO = "abierto", "Abierto"
    EN_PROCESO = "en_proceso", "En proceso"
    RESUELTO = "resuelto", "Resuelto"
    CERRADO = "cerrado", "Cerrado"


# =========================
# CATEGORÍAS
# =========================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# =========================
# MARCAS
# =========================
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# =========================
# MODELOS
# =========================
class ModeloDispositivo(models.Model):
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name="modelos"
    )
    nombre = models.CharField(max_length=100)

    class Meta:
        unique_together = ("marca", "nombre")
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


# =========================
# POSTS DEL FORO
# =========================
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    descripcion = models.TextField()

    imagen = CloudinaryField(
        "imagen",
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    marca = models.ForeignKey(
        Marca,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    modelo = models.ForeignKey(
        ModeloDispositivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    estado = models.CharField(
        max_length=20,
        choices=EstadoReparacion.choices,
        default=EstadoReparacion.ABIERTO
    )

    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts"
    )

    publicado = models.BooleanField(default=True)
    vistas = models.PositiveIntegerField(default=0)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["titulo"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["creado"]),
        ]

    def __str__(self):
        return self.titulo
