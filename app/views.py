from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from app.models import Patient, Investigation
from app.forms import PatientRegistrationForm, UploadInvestigationForm



class RegisterPageView(CreateView):
    """Patient Registration View"""

    model = Patient
    template_name = 'register.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('login')


class DashboardPageView(LoginRequiredMixin, CreateView):
    """Dashboard view for listing and creating investigations"""

    model = Investigation
    context_object_name = 'investigation_list'
    form_class = UploadInvestigationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """Pass current user investigations to page"""

        context = super(DashboardPageView, self).get_context_data(**kwargs)
        context['investigation_list'] = Investigation.objects.filter(
            patient=self.request.user
        ).order_by('-created_at')
        return context

    def form_valid(self, form):
        """Set authenticated user to investigation form"""

        form.instance.patient = self.request.user
        return super(DashboardPageView, self).form_valid(form)
