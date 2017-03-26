# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enc_char_field', encrypted_fields.fields.EncryptedCharField(max_length=396)),
                ('enc_text_field', encrypted_fields.fields.EncryptedTextField()),
                ('enc_date_field', encrypted_fields.fields.EncryptedDateField(max_length=100, null=True)),
                ('enc_date_now_field', encrypted_fields.fields.EncryptedDateField(auto_now=True, max_length=100, null=True)),
                ('enc_date_now_add_field', encrypted_fields.fields.EncryptedDateField(auto_now_add=True, max_length=100, null=True)),
                ('enc_datetime_field', encrypted_fields.fields.EncryptedDateTimeField(max_length=100, null=True)),
                ('enc_boolean_field', encrypted_fields.fields.EncryptedBooleanField(default=True, max_length=100)),
                ('enc_null_boolean_field', encrypted_fields.fields.EncryptedNullBooleanField(max_length=100)),
                ('enc_integer_field', encrypted_fields.fields.EncryptedIntegerField(null=True)),
                ('enc_positive_integer_field', encrypted_fields.fields.EncryptedPositiveIntegerField(null=True)),
                ('enc_small_integer_field', encrypted_fields.fields.EncryptedSmallIntegerField(null=True)),
                ('enc_positive_small_integer_field', encrypted_fields.fields.EncryptedPositiveSmallIntegerField(null=True)),
                ('enc_big_integer_field', encrypted_fields.fields.EncryptedBigIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
