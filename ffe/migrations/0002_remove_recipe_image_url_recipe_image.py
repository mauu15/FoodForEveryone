# Generated by Django 4.1 on 2024-05-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ffe", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="image_url",
        ),
        migrations.AddField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                default="recipes/default.jpg", upload_to="recipes/"
            ),
        ),
    ]
