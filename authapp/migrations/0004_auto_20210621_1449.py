# Generated by Django 3.2.4 on 2021-06-21 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_shopuser_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='key_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
