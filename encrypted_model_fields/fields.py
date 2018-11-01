from __future__ import unicode_literals

import django.db
import django.db.models
from django.utils.six import PY2
from django.utils.six import string_types
from django.utils.functional import cached_property
from django.core import validators
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import cryptography.fernet


def parse_key(key):
    """
    If the key is a string we need to ensure that it can be decoded
    :param key:
    :return:
    """
    return cryptography.fernet.Fernet(key)


def get_crypter():
    configured_keys = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)

    if configured_keys is None:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY must be defined in settings')

    try:
        # Allow the use of key rotation
        if isinstance(configured_keys, (tuple, list)):
            keys = [parse_key(k) for k in configured_keys]
        else:
            # else turn the single key into a list of one
            keys = [parse_key(configured_keys), ]
    except Exception as e:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY defined incorrectly: {}'.format(str(e)))

    if len(keys) == 0:
        raise ImproperlyConfigured('No keys defined in setting FIELD_ENCRYPTION_KEY')

    return cryptography.fernet.MultiFernet(keys)


CRYPTER = get_crypter()


def encrypt_str(s):
    # be sure to encode the string to bytes
    return CRYPTER.encrypt(s.encode('utf-8'))


def decrypt_str(t):
    # be sure to decode the bytes to a string
    return CRYPTER.decrypt(t.encode('utf-8')).decode('utf-8')


def calc_encrypted_length(n):
    # calculates the characters necessary to hold an encrypted string of
    # n bytes
    return len(encrypt_str('a' * n))


class EncryptedMixin(object):
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, (bytes, string_types[0])):
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            try:
                value = decrypt_str(value)
            except cryptography.fernet.InvalidToken:
                pass

        return super(EncryptedMixin, self).to_python(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedMixin, self).get_db_prep_save(value, connection)

        if value is None:
            return value
        if PY2:
            return encrypt_str(str(value, errors='ignore', encoding='utf-8'))
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return (encrypt_str(str(value))).decode('utf-8')

    def get_internal_type(self):
        return "TextField"

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedMixin, self).deconstruct()

        if 'max_length' in kwargs:
            del kwargs['max_length']

        return name, path, args, kwargs


class EncryptedCharField(EncryptedMixin, django.db.models.CharField):

    def __init__(self, *args, **kwargs):
        super(EncryptedCharField, self).__init__(*args, **kwargs)


class EncryptedTextField(EncryptedMixin, django.db.models.TextField):

    def __init__(self, *args, **kwargs):
        super(EncryptedTextField, self).__init__(*args, **kwargs)


class EncryptedDateField(EncryptedMixin, django.db.models.DateField):

    def __init__(self, *args, **kwargs):
        super(EncryptedDateField, self).__init__(*args, **kwargs)


class EncryptedDateTimeField(EncryptedMixin, django.db.models.DateTimeField):

    def __init__(self, *args, **kwargs):
        super(EncryptedDateTimeField, self).__init__(*args, **kwargs)


class EncryptedEmailField(EncryptedMixin, django.db.models.EmailField):

    def __init__(self, *args, **kwargs):
        super(EncryptedEmailField, self).__init__(*args, **kwargs)


class EncryptedBooleanField(EncryptedMixin, django.db.models.BooleanField):

    def __init__(self, *args, **kwargs):
        super(EncryptedBooleanField, self).__init__(*args, **kwargs)

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        if value is True:
            value = '1'
        elif value is False:
            value = '0'
        if PY2:
            return encrypt_str(str(value, errors='ignore', encoding='utf-8'))
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return encrypt_str(str(value)).decode('utf-8')


class EncryptedNullBooleanField(EncryptedMixin, django.db.models.NullBooleanField):

    def __init__(self, *args, **kwargs):
        super(EncryptedNullBooleanField, self).__init__(*args, **kwargs)

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        if value is True:
            value = '1'
        elif value is False:
            value = '0'
        if PY2:
            return encrypt_str(str(value, errors='ignore', encoding='utf-8'))
        # decode the encrypted value to a unicode string, else this breaks in pgsql
        return encrypt_str(str(value)).decode('utf-8')


class EncryptedNumberMixin(EncryptedMixin):
    max_length = 20

    def __init__(self, *args, **kwargs):
        super(EncryptedNumberMixin, self).__init__(*args, **kwargs)

    @cached_property
    def validators(self):
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        range_validators = []
        internal_type = self.__class__.__name__[9:]
        min_value, max_value = django.db.connection.ops.integer_field_range(internal_type)
        if min_value is not None:
            range_validators.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            range_validators.append(validators.MaxValueValidator(max_value))
        return super(EncryptedNumberMixin, self).validators + range_validators


class EncryptedIntegerField(EncryptedNumberMixin, django.db.models.IntegerField):
    description = "An IntegerField that is encrypted before " \
                  "inserting into a database using the python cryptography " \
                  "library"

    def __init__(self, *args, **kwargs):
        super(EncryptedIntegerField, self).__init__(*args, **kwargs)


class EncryptedPositiveIntegerField(EncryptedNumberMixin, django.db.models.PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        super(EncryptedPositiveIntegerField, self).__init__(*args, **kwargs)


class EncryptedSmallIntegerField(EncryptedNumberMixin, django.db.models.SmallIntegerField):

    def __init__(self, *args, **kwargs):
        super(EncryptedSmallIntegerField, self).__init__(*args, **kwargs)


class EncryptedPositiveSmallIntegerField(EncryptedNumberMixin, django.db.models.PositiveSmallIntegerField):

    def __init__(self, *args, **kwargs):
        super(EncryptedPositiveSmallIntegerField, self).__init__(*args, **kwargs)


class EncryptedBigIntegerField(EncryptedNumberMixin, django.db.models.BigIntegerField):

    def __init__(self, *args, **kwargs):
        super(EncryptedBigIntegerField, self).__init__(*args, **kwargs)
