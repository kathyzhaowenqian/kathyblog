# Generated by Django 3.2 on 2024-04-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20240412_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategory',
            name='category',
            field=models.CharField(blank=True, choices=[('饲养技巧', '饲养技巧'), ('饮食习性', '饮食习性'), ('医疗保健', '医疗保健')], max_length=255, null=True, verbose_name='文章分类'),
        ),
    ]