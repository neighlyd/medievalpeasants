from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@doe.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        self.assertEqual(1, len(mail.outbox))



class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        self.assertEqual(0, len(mail.outbox))


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)