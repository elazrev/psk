from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Questionnaire(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaires_created')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaires_owned', null=True, blank=True)
    title = models.CharField(max_length=200)
    creation_date = models.DateField(default=timezone.datetime.now)
    SURVEY_TYPE_CHOICES = [
        ('HOMEWORK', 'שיעורי בית'),
        ('DIGITAL_SESSION', 'סשן דיגיטלי'),
    ]
    survey_type = models.CharField(max_length=50, choices=SURVEY_TYPE_CHOICES)

    def __str__(self):
        return self.title

class QuestionSet(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='question_sets')
    title = models.CharField(max_length=200)
    explanation = models.TextField(null=True)
    hints = models.CharField(max_length=250, null=True, blank=True)
    SET_TYPE_CHOICES = [
        ('SIMPLE_SHORT', ' שאלות פתוחות קצרות'), #simple questions simple answrs (CharField)
         ('SIMPLE_LONG', ' שאלות פתוחות ארוכות'),#simple question LONG answrs (TextField)
        ('CLOSE', 'שאלות סגורות'), #yes no questions
        ('RATING', 'שאלות דירוג'),  #user need to rate the question in range of 5 
        ('POSTING', 'שאלות הצבה'),  #user need to place the questions according to his choose
        ('CHOOSING', 'שאלות בחירה'),#user need to choose one option from questions 
        ('MULTY_CHOOSE', 'בחירה מרובה'), #Add more here 
        ('SELF_RATING', ' דירוג עצמי'), #user will rate his answers in the order he is asked to by questions 
    ]
    set_type = models.CharField(max_length=50, choices=SET_TYPE_CHOICES)
    hierarchy_location = models.PositiveIntegerField()  

    def __str__(self):
        return self.title
    
    def hierarchy_counter(self):
        counter = QuestionSet.objects.filter(questionnaire=self.questionnaire).count()
        if counter:
            self.hierarchy_location = counter + 1
        else:
            self.hierarchy_location = 1
        self.save()

        
class Question(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    hierarchy_location = models.PositiveIntegerField()  # אולי נשתמש בזה להצגת השאלה בסדר המתאים

    def __str__(self):
        return self.question_text
    
#    def add_text_tail(self):
#        if self.question_text:
#            self.question_text = self.question_text + ','
#            self.save()
        
    def hierarchy_counter(self):
        counter = Question.objects.filter(question_set=self.question_set).count()
        if counter:
            self.hierarchy_location = counter + 1
        else:
            self.hierarchy_location = 1
        self.save()
        
    def text_seperator(self):
        text_sep_list = []
        sentence = ''
        for char in (self.question_text + ','): #Add tail to the text for include last sentence 
            if char == ',':
                text_sep_list.append(sentence)
                sentence = ''
            else:
                sentence += char
        return text_sep_list
        


class Answer(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()

    def __str__(self):
        return f"Answer to '{self.related_question.question_text}' by {self.responder.username}"
