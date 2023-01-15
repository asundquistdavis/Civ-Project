# Generated by Django 4.1.5 on 2023-01-15 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("play", "0002_alter_game_start_time"),
    ]

    operations = [
        migrations.CreateModel(
            name="Phase",
            fields=[
                (
                    "id",
                    models.CharField(max_length=2, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name="game",
            name="start_time",
            field=models.DateTimeField(default="2023-01-15T16:05:44"),
        ),
        migrations.AddField(
            model_name="game",
            name="phase",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="play.phase",
            ),
        ),
    ]