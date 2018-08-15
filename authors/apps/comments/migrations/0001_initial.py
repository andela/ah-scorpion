# Generated by Django 2.0.6 on 2018-08-14 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('content', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('article',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to='articles.Article')),
                ('parent',
                 models.ForeignKey(
                     default=None,
                     null=True,
                     on_delete=django.db.models.deletion.CASCADE,
                     related_name='children',
                     to='comments.Comment')),
                ('user',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('createdAt', ),
            },
        ),
    ]
