from .models import Group, Course
from .api import get_response


def refresh_groups():
    response = get_response('/Group/GetGroups')
    if not response:
        return False
    try:
        resp_json = response.json()
        # response will contains multiple IONIS schools
        group_list = []
        for school in resp_json:
            if school['Name'] == 'EPITA':
                # need to iterate over prepa, ing etc...
                for group_level in school['Groups']:
                    # for each of them, there is a 'super' group
                    for groups in group_level['Groups']:
                        # Somehow, some groups are None...
                        if groups['Groups']:
                            # now dealing with actual groups
                            for group in groups['Groups']:
                                group_list.append(Group(name=group['Name'],
                                                            entity_id=group['Id']))
        # 1 SQL query to create all groups
        Group.objects.bulk_create(group_list)
        return True
    except:
        return False