# Generated by Django 2.1.8 on 2019-07-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_auto_20190725_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='address',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='card_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证'),
        ),
        migrations.AlterField(
            model_name='seller',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='store/images', verbose_name='用户头像'),
        ),
    ]
