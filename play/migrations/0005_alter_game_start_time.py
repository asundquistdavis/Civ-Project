# Generated by Django 4.1.5 on 2023-01-15 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("play", "0004_remove_player_game_player_current_game_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="start_time",
            field=models.DateTimeField(default="2023-01-15T04:57:53"),
        ),
    ]
