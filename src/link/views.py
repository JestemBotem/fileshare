from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, TemplateView

from link.forms import ProtectedResourceForm, PasswordForm
from link.models import ProtectedResource


class SecureUriView(LoginRequiredMixin, CreateView):
    template_name = 'link/new.html'
    form_class = ProtectedResourceForm
    success_url = reverse_lazy('link:created')

    def _generate_password(self):
        return str(uuid4())

    def form_valid(self, form):
        raw_password = self._generate_password()

        secure_uri = form.save(commit=False)
        secure_uri.user = self.request.user
        secure_uri.set_password(raw_password)
        secure_uri.save()

        messages.add_message(self.request, messages.INFO, "Password for this resource is: '{}'".format(
            raw_password
        ))

        resource_url = reverse('link:get', kwargs={'id': secure_uri.id})
        messages.add_message(self.request, messages.INFO, "Link for protected resource is: {}".format(
            self.request.build_absolute_uri(resource_url)
        ))

        return super(SecureUriView, self).form_valid(form)


class CreatedView(TemplateView):
    template_name = 'link/created.html'


class DownloadView(FormView):
    form_class = PasswordForm
    template_name = 'link/new.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(ProtectedResource, pk=self.kwargs['id'])

        if not self.object.is_available():
            raise Http404()

        return super(DownloadView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        raw_password = form.cleaned_data['password']

        if not self.object.is_valid_password(raw_password):
            form.add_error('password', 'Invalid password')
            return self.render_to_response(self.get_context_data(form=form))

        ProtectedResource.objects.increase_view_count(self.object.id)

        if self.object.uri:
            return HttpResponseRedirect(self.object.uri)

        response = HttpResponse()
        response['X-Accel-Redirect'] = '/uploads/' + self.object.file_name
        response['Content-Disposition'] = 'attachment; filename=%s' % self.object.file_name
        response['Content-Type'] = ''

        return response
