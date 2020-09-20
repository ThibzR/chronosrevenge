from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Course, User, Blacklist
import arrow


class GroupForm(forms.Form):
    group = forms.CharField(label='', widget=forms.TextInput(attrs=dict(placeholder='Your group')))
    need_blacklist = forms.ChoiceField(choices=[('no', 'No'), ('yes', 'Yes')],
                                       widget=forms.RadioSelect, label='Do you need to blacklist courses?')
    course_list = Course.objects.filter(date_added__gt=arrow.now().shift(months=settings.COURSE_PREVIEW_OFFSET).datetime).order_by('date_added').reverse()
    course_choice = forms.ModelMultipleChoiceField(label='Available course to blacklist',
                                                   widget=forms.CheckboxSelectMultiple,
                                                   queryset=course_list, required=False)
    username = forms.CharField(label='', max_length=64, required=False,
                               widget=forms.TextInput(attrs=dict(placeholder='Your login')))
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(placeholder='password')), required=False, label='')


def process_form(request):
    group = request.POST.get('group', None)
    if not group:
        messages.error(request, 'No group has been provided.')
        return
    course_choice = request.POST.getlist('course_choice', None)
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if username is not '' and password is not '' and len(course_choice) > 0:
        try:
            _process_user_blacklist(username, password, course_choice)
        except ValidationError as e:
            messages.error(request, e.message)
            return

    URL = settings.URL_DEBUG or 'https://chronosvenger.me'
    messages.success(request, 'Your calendar link: {}/?classe={}{}.ics \n'
                              'Paste this link in your calendar (not in your browser, '
                              'see tutorials on home page)'.format(URL, group,
                              '' if not username else '@{}'.format(username)))


def _process_user_blacklist(username, password, course_choice):
    user = User.get_user_or_create_it(username, password)
    Blacklist.save_blacklist(user, course_choice)