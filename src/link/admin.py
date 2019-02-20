from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from link.forms import PasswordForm
from link.models import ProtectedResource

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class ProtectedResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action_change_password')

    def view_change_password(self, request, id, *args, **kwargs):
        protected_resource = self.get_object(request, id)

        if request.method != 'POST':
            form = PasswordForm()
        else:
            form = PasswordForm(request.POST)
            if form.is_valid():
                protected_resource.set_password(form.cleaned_data['password'])
                protected_resource.save()

                self.message_user(request, "New password set")
                url = reverse(
                    'admin:link_protectedresource_changelist',
                    current_app=self.admin_site.name,
                )
                return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['form'] = form
        context['opts'] = self.model._meta

        return TemplateResponse(
            request,
            'admin/change_password.html',
            context,
        )

    def action_change_password(self, obj):
        return format_html(
            '<a class="button" href="{}">Change password</a>',
            reverse('admin:protectedresource-changepassword', kwargs={'id': str(obj.id)}),
        )

    def get_urls(self):
        urls = super(ProtectedResourceAdmin, self).get_urls()

        change_password_url = path(
            '<uuid:id>/change_password',
            self.admin_site.admin_view(self.view_change_password),
            name='protectedresource-changepassword',
        )

        return urls + [change_password_url, ]


admin.site.register(ProtectedResource, ProtectedResourceAdmin)
