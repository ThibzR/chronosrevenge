from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template import loader
from django.contrib import messages
from .calendar import get_calendar
from .models import Course
from .forms import GroupForm, process_form
import arrow


def index(request):
    if request.method == 'GET':
        group_name = request.GET.get('classe', None)
        if group_name:
            # legacy parsing
            group_name = group_name.replace('.ics', '')
            # there is a login to extract
            # format is class@login.ics or class.ics
            if group_name.find('@') > 0:
                group_name_split = group_name.split('@')
                group_name = group_name_split[0]
                login = group_name_split[1]
            else:
                login = None
            calendar = get_calendar(group_name, login)
            if not calendar:
                return HttpResponse(status=404)
            ret = HttpResponse(str(calendar), content_type='text/calendar', charset='utf-8')
            ret.setdefault('Content-Disposition',
                        'attachment; filename={}'.format(arrow.now().format('YYYYMMDDHHmmss') + '.ics'))
            return ret
        else:
            context = {
            'form': GroupForm(),
            }
            return render(request, 'chronos/index.html', context)
    else:
        process_form(request)
        return redirect(reverse('index'))
