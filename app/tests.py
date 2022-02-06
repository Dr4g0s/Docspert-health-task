from django.test import TestCase, Client
from django.urls import reverse
import csv
from django.core.files import File
import os

from app.models import Patient, Investigation
from app.forms import PatientRegistrationForm, UploadInvestigationForm


LOGIN_URL = reverse('login')
REGISTER_URL = reverse('register')
DASHBOARD_URL = reverse('dashboard')


class LoginViewTests(TestCase):

    def setUp(self):
        self.user = Patient.objects.create(email='test_user@mail.com')
        self.user.set_password('pass123')
        self.user.save()
        self.client = Client()

    def test_retrieve_login_page(self):
        res = self.client.get(LOGIN_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'login.html')

    def test_login(self):
        self.client.login(email=self.user.email, password='pass123')
        res = self.client.get(DASHBOARD_URL)
        self.assertEqual(res.status_code, 200)


class RegisterationViewTests(TestCase):

    def test_retrieve_register_page(self):
        res = self.client.get(REGISTER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'register.html')

    def test_register_form(self):
        data = {
            'name': 'test name',
            'email': 'email@mail.com',
            'password1': 'test0073'
        }

        form = PatientRegistrationForm(data=data)
        self.failUnless(form.is_valid())
        res = self.client.post(REGISTER_URL, form.data)
        self.assertEqual(Patient.objects.count(), 1)
        

class DashboardViewTests(TestCase):

    def generate_file(self):
        try:
            myfile = open('test.csv', 'w', encoding='UTF8', newline='')
            wr = csv.writer(myfile)
            wr.writerow(('Patient ID','Title', 'FILES'))
            wr.writerow(('1','Title1', 'FILE1'))
            wr.writerow(('2','Title2', 'FILE2'))
            wr.writerow(('3','Title3', 'FILE3'))
        finally:
            myfile.close()

        return myfile

    def setUp(self):
        self.user = Patient.objects.create(email='test_user@mail.com')
        self.user.set_password('pass123')
        self.user.save()
        self.client = Client()
        self.client.login(email='test_user@mail.com', password='pass123')

    def test_login_redirect(self):
        res = self.client.get(LOGIN_URL)
        self.assertEqual(res.status_code, 302)

    def test_retrieve_dashboard_page(self):
        res = self.client.get(DASHBOARD_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'dashboard.html')

    def test_create_investigation(self):
        myfile = self.generate_file()
        file = File(open(myfile.name, "r"))
        data = {
            'patient': self.user,
            'title': 'test title',
            'file': file
        }
        form = UploadInvestigationForm(data=data, files={'file': data['file']})
        self.failUnless(form.is_valid())
        res = self.client.post(DASHBOARD_URL, form.data, format='multipart')
        file.close()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Investigation.objects.count(), 1)
        os.remove(myfile.name)

    def test_retrieve_investigations(self):
        myfile = self.generate_file()
        file = File(open(myfile.name, "r"))
        investigation = Investigation.objects.create(
            patient=self.user,
            title='test title',
            file=file.read()
        )
        file.close()
        res = self.client.get(DASHBOARD_URL)
        self.assertContains(res, investigation.title)
        self.assertContains(res, investigation.file.url)
        os.remove(myfile.name)
