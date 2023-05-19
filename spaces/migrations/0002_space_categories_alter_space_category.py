# Generated by Django 4.1.2 on 2023-05-15 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_options'),
        ('spaces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='categories',
            field=models.ManyToManyField(related_name='multiple_categories_spaces', to='users.category'),
        ),
        migrations.AlterField(
            model_name='space',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='single_category_spaces', to='users.category'),
        ),
    ]
