from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_recipes', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', default='recipes/default-image.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    ingredients = models.TextField(default='')  # Campo per la lista degli ingredienti
    instructions = models.TextField(default='')  # Campo per le istruzioni

    preparation_time = models.CharField(max_length=50, null=True, blank=True)
    cooking_time = models.CharField(max_length=50, null=True, blank=True)
    servings = models.IntegerField(null=True, blank=True)

    # Campo per la categoria
    CATEGORY_CHOICES = [
        ('Aperitivo', 'Aperitivo'),
        ('Piatto Principale', 'Piatto Principale'),
        ('Secondo Piatto', 'Secondo Piatto'),
        ('Contorno', 'Contorno'),
        ('Dessert', 'Dessert'),


    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)

    # Campo per la difficoltà
    DIFFICULTY_CHOICES = [
        ('Facile', 'Facile'),
        ('Media', 'Media'),
        ('Difficile', 'Difficile'),
    ]
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, null=True, blank=True)

    # Campo per il voto medio
    average_rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"


class Follower(models.Model):
    objects = None
    user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'follower')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return self.user.username