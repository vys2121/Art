# Generated by Django 4.2.4 on 2023-09-29 05:52

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(upload_to=main.models.generate_filename, validators=[main.models.validate_file_extension]),
        ),
    ]