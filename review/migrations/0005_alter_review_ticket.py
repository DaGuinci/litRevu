# Generated by Django 4.2.3 on 2023-07-04 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_ticket_description_ticket_image_ticket_time_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='review.ticket'),
        ),
    ]
