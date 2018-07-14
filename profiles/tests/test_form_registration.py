from django.test import TestCase
from ..forms import ProfileSignupForm


class RegistrationFormTest(TestCase):
    def test_form_has_fields(self):
        form = ProfileSignupForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)