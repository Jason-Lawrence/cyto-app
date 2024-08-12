# Generated by Django 5.0.6 on 2024-08-10 02:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonalAccessToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=88)),
                ("name", models.CharField(max_length=50)),
                ("created", models.DateField(auto_now_add=True)),
                ("expires", models.DateField(blank=True, null=True)),
                ("revoked", models.BooleanField(default=False)),
                ("is_expired", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]