# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 23:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import encrypted_fields.fields
import feedcrunch.model_files.models_geo
import feedcrunch.model_files.models_options
import feedcrunch.model_files.models_user
import feedcrunch.model_files.models_tag
import feedcrunch.model_files.models_post
import uuid
import validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
		migrations.CreateModel(
			name='Continent',
			fields=[
				('name', models.CharField(max_length=60, primary_key=True, serialize=False)),
				('code', models.CharField(max_length=2)),
			],
		),
		migrations.CreateModel(
			name='Country',
			fields=[
				('name', models.CharField(max_length=60, primary_key=True, serialize=False)),
				('code', models.CharField(max_length=2)),
				('continent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedcrunch.Continent')),
			],
		),
		migrations.CreateModel(
			name='Option',
			fields=[
				('parameter', models.CharField(max_length=255, primary_key=True, serialize=False)),
				('value', encrypted_fields.fields.EncryptedCharField(default='', max_length=255)),
			],
		),
        migrations.CreateModel(
            name='FeedUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
				('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
				('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, primary_key=True, serialize=False, validators=[validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Required. 255 characters or fewer and a valid email.', max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
				('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedcrunch.Country')),
				('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], default='M', max_length=1)),
                ('rss_feed_title', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('description', models.TextField(blank=True, default='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam dui nisl, aliquam nec quam nec, laoreet porta odio. Morbi ultrices sagittis ligula ut consectetur. Aenean quis facilisis augue. Vestibulum maximus aliquam augue, ut lobortis turpis euismod vel. Sed in mollis tellus, eget eleifend turpis. Vivamus aliquam ornare felis at dignissim. Integer vitae cursus eros, non dignissim dui. Suspendisse porttitor justo nec lacus dictum commodo. Sed in fringilla tortor, at pharetra tortor. Vestibulum tempor sapien id justo molestie imperdiet. Nulla efficitur mattis ante, nec iaculis lorem consequat in. Nullam sit amet diam augue. Nulla ullamcorper imperdiet turpis a maximus. Donec iaculis porttitor ultrices. Morbi lobortis dui molestie ullamcorper varius. Maecenas eu laoreet ipsum orci aliquam.', null=True)),
                ('job', models.CharField(blank=True, default='Chief Admission Officer at', max_length=80, null=True)),
                ('company_name', models.CharField(blank=True, default='Holy Paradise Inc.', max_length=80, null=True)),
                ('company_website', models.URLField(blank=True, default='http://www.feedcrunch.io/', max_length=120, null=True)),
                ('apikey', encrypted_fields.fields.EncryptedCharField(default=uuid.uuid4, editable=False, max_length=500, unique=True)),
                ('profile_picture', models.ImageField(blank=True, default='images/user_photos/dummy_user.png', null=True, upload_to=feedcrunch.model_files.models_user.get_photo_path)),
                ('twitter_token', encrypted_fields.fields.EncryptedCharField(blank=True, default='', max_length=500, null=True)),
                ('twitter_token_secret', encrypted_fields.fields.EncryptedCharField(blank=True, default='', max_length=500, null=True)),
                ('social_dribbble', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_facebook', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_flickr', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_gplus', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_instagram', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_linkedin', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_pinterest', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_stumble', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_twitter', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_vimeo', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_youtube', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_docker', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_git', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_kaggle', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_coursera', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_google_scholar', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_orcid', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_researchgate', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_blog', models.URLField(blank=True, default='', max_length=60, null=True)),
                ('social_personalwebsite', models.URLField(blank=True, default='', max_length=60, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', feedcrunch.model_files.models_user.FeedUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(editable=False, max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=2000)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(default=feedcrunch.model_files.models_post.create_key, max_length=8)),
                ('clicks', models.IntegerField()),
                ('activeLink', models.BooleanField()),
				('tags', models.ManyToManyField(blank=True, related_name='rel_posts', to='feedcrunch.Tag')),
				('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
		migrations.CreateModel(
            name='Estimator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now_add=True)),
                ('object_file', models.FileField(blank=True, default='', editable=False, upload_to=feedcrunch.model_files.models_estimators.get_upload_path_instance)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
    ]
