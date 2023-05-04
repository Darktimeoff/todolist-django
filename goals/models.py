from django.db import models
from core.models import User
from django.utils import timezone
from django.utils.text import slugify
from typing import List
class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Board(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        categories = self.categories.all()

        for category in categories:
            category.delete()

class BoardParticipant(BaseModel):
    class Meta:
        unique_together = ("board", "user")

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Администратор"
        reader = 3, "Читатель"

    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.owner)

class GoalCategory(BaseModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, blank=True, default='')

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='categories')
    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name='categories')

    def __str__(self):
        return self.slug


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        goals: List[Goal] = self.goals.all()

        for goal in goals:
            goal.status = goal.Status.archived
            goal.is_deleted = True
            goal.save()

        self.save()

        return self


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Высокий"

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True, default='')

    slug = models.SlugField(max_length=60, blank=True, default='')
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='goals')
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, related_name='goals')

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.medium)

    due_date = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True

        self.status = self.Status.archived
        
        self.save()

        return self
   

class GoalComment(BaseModel):
    goal = models.ForeignKey(Goal, related_name="comments", on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.PROTECT)
    text = models.CharField(max_length=1000)