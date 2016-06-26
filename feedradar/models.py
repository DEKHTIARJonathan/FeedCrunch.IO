from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

import re, uuid, datetime
from validate_email import validate_email

############################# Localisation #####################################

class Continent(models.Model):
	name = models.CharField(primary_key=True, max_length=60)
	code = models.CharField(max_length=2)

class Country(models.Model):
	name = models.CharField(primary_key=True, max_length=60)
	code = models.CharField(max_length=2)
	continent = models.ForeignKey(Continent)

############################ USER MODEL ########################################

class FeedUserManager(models.Manager):
	##################### FeedUser.objects.create_user() ###############################

	def validate_parameters(self, username, email, password, country, sex, birth_year, birth_month, birth_day):
		today = datetime.date.today()

		if sex not in ['M', 'F']:
			raise ValueError("The given sex value is not valid : 'M' or 'F'.")

		elif not validate_email(email,verify=True):
			raise ValueError("The given email is not valid or not doesn''t exist.")

		elif re.match(r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,})', password) == None:
			raise ValueError("The password doesn't fit in our policies : At least 8 characters, 1 Uppercase letter 'A-Z', 1 Lowercase letter 'a-z', and 1 number '0-9'")

		elif not Country.objects.filter(name = country).exists():
			raise ValueError("The given country doesn't exist")

		elif not isinstance( birth_year, int ):
			raise ValueError("The given birth_year value is not valid, only integer values are accepted.")

		elif (not isinstance( birth_month, int )) or birth_month > 12:
			raise ValueError("The given birth_month value is not valid, only integer values are accepted and maximum value = 12.")

		elif (not isinstance( birth_day, int )) or birth_day > 31:
			raise ValueError("The given birth_day value is not valid, only integer values are accepted and maximum value = 31 (depends on the month).")

		else:
			try:
				birthdate = datetime.date(birth_year, birth_month, birth_day)
				if birthdate > today:
					raise ValueError("The given birthdate can't be in the future. Please provide a correct date.")

			except ValueError:
				raise ValueError("The given birthdate is not valid, please check the max_day for the given month")

		return True

	def create_user(self, username, email, password, country, sex, birth_year, birth_month, birth_day):

		if validate_parameters(username, email, password, country, sex, birth_year, birth_month, birth_day):

			user_tmp = FeedUser(user=User.objects.create_user(username=username, email=email, password=password), country=Country.objects.get(name=country), birthdate=birthdate, sex=sex)
			user_tmp.save()

			return user_tmp

		else:
			return False

	def create_superuser(self, username, email, password, country, sex, birth_year, birth_month, birth_day):

		if validate_parameters(username, email, password, country, sex, birth_year, birth_month, birth_day):

			user_tmp = FeedUser(user=User.objects.create_superuser(username=username, email=email, password=password), country=Country.objects.get(name=country), birthdate=birthdate, sex=sex)
			user_tmp.save()

			return user_tmp

		else:
			return False


class FeedUser(models.Model):
	"""
	#################################### Fields ####################################

	** username: Required. 30 characters or fewer.
				Usernames may contain alphanumeric, _, @, +, . and - characters.

	** first_name: Optional. 30 characters or fewer.

	** last_name: Optional. 30 characters or fewer.

	** email: Optional. Email address.

	** password: Required. A hash of, and metadata about, the password.
				(Django doesn't store the raw password.) Raw passwords can be arbitrarily long and can contain any character. See the password documentation.

	** groups: Many-to-many relationship to Group

	** user_permissions: Many-to-many relationship to Permission

	** is_staff: Boolean. Designates whether this user can access the admin site.

	** is_active: Boolean. Designates whether this user account should be considered active.
				We recommend that you set this flag to False instead of deleting accounts; that way, if your applications have any foreign keys to users, the foreign keys won't break.

				This doesn't necessarily control whether or not the user can log in.
				Authentication backends aren't required to check for the is_active flag, and the default backends do not.
				If you want to reject a login based on is_active being False, it's up to you to check that in your own login view or a custom authentication backend.
				However, the AuthenticationForm used by the login() view (which is the default) does perform this check,
				as do the permission-checking methods such as has_perm() and the authentication in the Django admin. All of those functions/methods will return False for inactive users.

	** is_superuser: Boolean. Designates that this user has all permissions without explicitly assigning them.

	** last_login: A datetime of the user's last login.

	** date_joined: A datetime designating when the account was created. Is set to the current date/time by default when the account is created.

	#################################### Methods ####################################

	** get_username(): Returns the username for the user.
				Since the User model can be swapped out, you should use this method instead of referencing the username attribute directly.

	** is_anonymous(): Always returns False. This is a way of differentiating User and AnonymousUser objects. Generally, you should prefer using is_authenticated() to this method.

	** is_authenticated(): Always returns True (as opposed to AnonymousUser.is_authenticated() which always returns False).
				This is a way to tell if the user has been authenticated. This does not imply any permissions, and doesn't check if the user is active or has a valid session.
				Even though normally you will call this method on request.user to find out whether it has been populated by the AuthenticationMiddleware (representing the currently logged-in user),
				you should know this method returns True for any User instance.

	** get_full_name(): Returns the first_name plus the last_name, with a space in between.

	** get_short_name(): Returns the first_name.

	** set_password(raw_password): Sets the user's password to the given raw string, taking care of the password hashing. Doesn't save the User object.
				When the raw_password is None, the password will be set to an unusable password, as if set_unusable_password() were used.

	** check_password(raw_password): Returns True if the given raw string is the correct password for the user. (This takes care of the password hashing in making the comparison.)

	** set_unusable_password(): Marks the user as having no password set. This isn't the same as having a blank string for a password. check_password() for this user will never return True. Doesn't save the User object.
				You may need this if authentication for your application takes place against an existing external source such as an LDAP directory.

	** has_usable_password(): Returns False if set_unusable_password() has been called for this user.

	** get_group_permissions(obj=None): Returns a set of permission strings that the user has, through their groups.
				If obj is passed in, only returns the group permissions for this specific object.

	** get_all_permissions(obj=None): Returns a set of permission strings that the user has, both through group and user permissions.
				If obj is passed in, only returns the permissions for this specific object.

	** has_perm(perm, obj=None): Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>". (see documentation on permissions).
				If the user is inactive, this method will always return False.
				If obj is passed in, this method won't check for a permission for the model, but for this specific object.

	** has_perms(perm_list, obj=None): Returns True if the user has each of the specified permissions, where each perm is in the format "<app label>.<permission codename>".
				If the user is inactive, this method will always return False.
				If obj is passed in, this method won't check for permissions for the model, but for the specific object.

	** has_module_perms(package_name): Returns True if the user has any permissions in the given package (the Django app label). If the user is inactive, this method will always return False.

	** email_user(subject, message, from_email=None, **kwargs): Sends an email to the user. If from_email is None, Django uses the DEFAULT_FROM_EMAIL. Any **kwargs are passed to the underlying send_mail() call.

	#################################### Manager methods ####################################

	** create_user(username, email=None, password=None, **extra_fields): Creates, saves and returns a User.
				The username and password are set as given.
				The domain portion of email is automatically converted to lowercase, and the returned User object will have is_active set to True.

				If no password is provided, set_unusable_password() will be called.
				The extra_fields keyword arguments are passed through to the User's __init__ method to allow setting arbitrary fields on a custom User model.

	** create_superuser(username, email, password, **extra_fields): Same as create_user(), but sets is_staff and is_superuser to True.

	"""

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	birthdate = models.DateField()
	apikey = models.UUIDField(default=uuid.uuid4, editable=False)
	sex = models.CharField(
		max_length=1,
		choices=(('M', 'Male'),('F', 'Female')),
		default='M',
	)
	objects = FeedUserManager()

############################## ARTICLE MODEL ###################################

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=255)
	link = models.URLField(max_length=2000)
	when = models.DateTimeField(auto_now_add=True)
	clicks = models.IntegerField()
	activeLink = models.BooleanField()
	user = models.ForeignKey(User)

	def get_date(self):
		return self.when.strftime("%Y/%m/%d %H:%M")

	def get_domain(self):
		starts = [match.start() for match in re.finditer(re.escape("/"), self.link)]
		if len(starts) > 2:
			return self.link[starts[1]+1:starts[2]]
		elif len(starts) == 2:
			return self.link[starts[1]+1:]
		else:
			return str("error")
