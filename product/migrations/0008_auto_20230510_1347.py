# Generated by Django 3.2.18 on 2023-05-10 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0003_mutations'),
        ('product', '0007_auto_20230510_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productitem',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='productservice',
            options={'managed': True},
        ),
    ]