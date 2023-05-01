from django.db import models
from core.models import User
from django.utils import timezone
from django.utils.text import slugify

class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        
        return super().save(*args, **kwargs)

class GoalCategory(BaseModel):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        
        return super().save(*args, **kwargs)
