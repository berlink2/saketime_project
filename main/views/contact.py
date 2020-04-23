from django.views.generic.edit import FormView
from main import forms
import logging
logger = logging.getLogger(__name__)


class ContactUsView(FormView):
    form_class = forms.ContactForm
    template_name = 'contact_us.html'
    success_url = '/'

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
