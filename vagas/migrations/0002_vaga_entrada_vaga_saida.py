# Generated by Django 5.2.1 on 2025-07-02 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='entrada',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vaga',
            name='saida',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
