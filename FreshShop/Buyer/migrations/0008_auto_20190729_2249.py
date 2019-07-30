# Generated by Django 2.1.8 on 2019-07-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0007_auto_20190729_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(default=1, verbose_name='订单状态'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='goods_image',
            field=models.ImageField(default=1, upload_to='', verbose_name='商品图片'),
            preserve_default=False,
        ),
    ]
