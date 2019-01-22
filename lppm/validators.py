import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumLengthValidator:
	def __init__(self, min_length=2):
		self.min_length = min_length

	def validate(self, password, user=None):
		if len(password) < self.min_length:
			raise ValidationError(
				_("Password kurang"),
				code='password_too_short',
				params={'min_length': self.min_length},
			)

	def get_help_text(self):
		return _(
			"Minimal Password 2 digit"
		)