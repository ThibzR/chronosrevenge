from ics import Calendar, Event
from django.conf import settings
from django.core.cache import cache
from .api import get_response
from .models import Group, Blacklist, Course
import arrow


def get_calendar(group_name=None, username=None):
    if not group_name:
        return
    entity_id = Group.get_entity_id(group_name)
    if not entity_id:
        return
    
    cache_key = _construct_cache_key(group_name, username)
    if cache.has_key(cache_key):
        return cache.get(cache_key)

    c = Calendar()

    # Getting current week to recover week_id
    response = get_response('/Week/GetCurrentWeek/{}/{}'.format(entity_id, settings.EPITA_ENTITY_ID))
    if not _process_response(response, c, username):
        return
    
    # Pull others weeks
    week_id = response.json()['Id']
    if not isinstance(week_id, int):
        return
    for i in range(1, settings.NUMBER_OF_WEEKS):
        next_week_response = get_response('/Week/GetWeek/{}/{}/{}'.format(week_id + i,
                                          entity_id, settings.EPITA_ENTITY_ID))
        if not _process_response(next_week_response, c, username):
            return
    cache.set(cache_key, str(c))
    return c


def _process_response(response, calendar, username=None):
    # Exit if status code < 200 or > 400
    if not response:
        return False
    try:
        response_json = response.json()
        blacklist = Blacklist.get_blacklist(username) if username else []
        for day in response_json['DayList']:
            for course in day['CourseList']:
                course_name = course['Name']
                # to have the front page displaying current courses
                Course.add_if_not_exist(course_name)
                # Skipping blacklisted course
                if course_name in blacklist:
                    continue
                # Get all staff names
                staff_list = [staff['Name'] for staff in course['StaffList']]
                # Get all room names
                rooms_list = [room['Name'] for room in course['RoomList']]
                # Get all group names
                class_list = [group['Name'] for group in course['GroupList']]
                # stringify lists
                list_str = ' '
                desc = list_str.join(rooms_list) + '\n' + list_str.join(staff_list) \
                       + '\n' + list_str.join(class_list)

                # Get begin and end datetime
                begin = arrow.get(course['BeginDate'])
                end = arrow.get(course[('EndDate')])

                e = Event(name=course_name, location=desc, begin=begin, end=end)
                calendar.events.add(e)
    except Exception as e:
        return False
    return True

def _construct_cache_key(group_name, username):
    return group_name if username is None else group_name + '_' + username