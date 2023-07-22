from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Interviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Interviewed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    explanation = models.TextField()
    date_of_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only set the date_of_creation when creating a new instance
            self.date_of_creation = timezone.now().date()
        super().save(*args, **kwargs)

class QuestionFile(models.Model):
    QUESTION_TYPES = (
        ('regular', 'Regular'),
        ('scaling', 'Scaling'),
        ('rating', 'Rating'),
    )

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    title = models.CharField(max_length=100, default='', null=True)
    explanation = models.TextField(default='')  # Can be a text, image, link to video, or all of them together

    def __str__(self):
        return f"{self.get_file_type_display()} - {self.title}"

class Question(models.Model):
    question_file = models.ForeignKey(QuestionFile, on_delete=models.CASCADE)
    question_text = models.TextField(default='')

    def __str__(self):
        return self.question_text
