# Generated by Django 4.2.13 on 2024-05-24 06:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_sl_info_alter_les_info_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stu",
            name="img",
            field=models.ImageField(
                max_length=32, null=True, upload_to="photos", verbose_name="头像"
            ),
        ),
    ]
