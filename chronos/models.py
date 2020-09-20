from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.username

    @staticmethod
    def get_user_or_create_it(username, password):
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Wrong login or password. Try again')
            else:
                return user
        else:
            user = User.objects.create_user(username=username, password=password)
            return user


class Course(models.Model):
    title = models.CharField(max_length=264)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @staticmethod
    def add_if_not_exist(course_name):
        if not isinstance(course_name, str):
            return
        len_query = len(Course.objects.filter(title=course_name).values('title'))
        if len_query == 0:
            new_course = Course(title=course_name)
            new_course.save()


class Group(models.Model):
    name = models.CharField(max_length=32)
    entity_id = models.IntegerField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_entity_id(group_name):
        key = 'entity_id'
        query = Group.objects.filter(name=group_name).values(key)
        return query[0][key] if len(query) > 0 else None


class Blacklist(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' : ' + self.course.title

    @staticmethod
    def get_blacklist(username):
        key = 'course__title'
        query = Blacklist.objects.filter(user__username=username).values(key)
        return [item[key] for item in list(query)]
    
    @staticmethod
    def save_blacklist(user, course_choice):
        blacklists = []
        courses = Course.objects.filter(id__in=course_choice)
        for course in courses:
            blacklists.append(Blacklist(course=course, user=user))
        # Override previous blacklist
        Blacklist.objects.filter(user=user.id).delete()
        # Save new one
        Blacklist.objects.bulk_create(blacklists)
