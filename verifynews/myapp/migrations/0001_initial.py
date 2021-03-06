# Generated by Django 3.1.13 on 2021-08-09 10:24

from django.db import migrations, models
import django.db.models.deletion
import verifynews.myapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.FileField(upload_to='images', validators=[verifynews.myapp.validators.validate_file_extension])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('real', 'Real'), ('fake', 'Fake'), ('unsorted', 'Unsorted')], default='unsorted', max_length=20)),
                ('pdq', models.TextField()),
                ('fileType', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('unknown', 'Unknown')], default='unknown', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.image')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('Image', models.ManyToManyField(through='myapp.Upload', to='myapp.Image')),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
    ]
