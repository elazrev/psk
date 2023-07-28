from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User


class Questionnaire(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=now)
    allows_multiple_responses = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Obj(models.Model):
    OBJ_TYPE_CHOICES = (
        ('title', 'כותרת'),
        ('explanation', 'הסבר'),
        ('image', 'תמונה'),
        ('divider', 'מפצל'),
        ('hints', 'רמזים'),
        ('open_question', 'שאלה פתוחה'),
        ('single_choice', 'שאלת בחירה בודדת'),
        ('multiple_choice', 'שאלת בחירה מרובה'),
        ('rating', 'שאלת דירוג'),
        ('agreement', 'שאלת הצבה'),
        ('self_rating', 'שאלת דירוג עצמי'),
        ('self_choice', 'שאלת בחירה עצמית'),
    )
    
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='objs')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_objs')
    obj_type = models.CharField(max_length=20, choices=OBJ_TYPE_CHOICES)
    content = models.TextField()
    hierarchy_counter = models.CharField(max_length=20, blank=True)
    hierarchy_position = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.hierarchy_counter:
            if self.parent:
                siblings = self.parent.sub_objs.all()
                siblings_count = siblings.count()
                if siblings_count == 0:
                    self.hierarchy_counter = '1'
                else:
                    last_sibling = siblings.order_by('hierarchy_counter').last()
                    last_sibling_hierarchy = last_sibling.hierarchy_counter
                    last_sibling_number = int(last_sibling_hierarchy.split('.')[-1])
                    new_sibling_number = last_sibling_number + 1
                    self.hierarchy_counter = f'{last_sibling_hierarchy.rsplit(".", 1)[0]}.{new_sibling_number}'
            else:
                siblings = self.questionnaire.objs.filter(parent__isnull=True)
                siblings_count = siblings.count()
                if siblings_count == 0:
                    self.hierarchy_counter = '1'
                else:
                    last_sibling = siblings.order_by('hierarchy_counter').last()
                    last_sibling_number = int(last_sibling.hierarchy_counter)
                    self.hierarchy_counter = str(last_sibling_number + 1)
        super().save(*args, **kwargs)
    
    def hierarchy_position(self):
        counter = Obj.objects.filter(questionnaire=self.questionnaire).count()
        if counter:
            self.hierarchy_position = counter + 1
        else:
            self.hierarchy_position  = 1
        self. Save()

    def __str__(self):
        return self.content
    
class Answer(models.Model):
    obj_temp_id = models.IntegerField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_sender")
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_responder")
    content = models.TextField()
    created = models.DateTimeField(default=now)

    def obj(self):
        return Obj.objects.get(pk=self.obj_temp_id)

    def __str__(self):
        return self.content