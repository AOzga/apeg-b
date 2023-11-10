# Generated by Django 4.2.7 on 2023-11-09 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventurer',
            name='aclass',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='character.aclass'),
        ),
        migrations.AlterField(
            model_name='adventurer',
            name='money',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='adventurer',
            name='race',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='character.arace'),
        ),
    ]
