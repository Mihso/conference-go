# Generated by Django 4.0.3 on 2022-07-15 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0004_remove_accountvo_updated_alter_attendee_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
