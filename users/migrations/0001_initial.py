# Generated by Django 4.1 on 2022-09-05 18:39

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200, unique=True, validators=[django.core.validators.EmailValidator])),
                ('password', models.CharField(max_length=100)),
                ('isConfirmed', models.BooleanField(default=False)),
                ('confirmationKey', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
