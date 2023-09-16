from django.db import models

class Categories(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'כללי'),
        ('career', 'קריירה'),
        ('personal_growth', 'התפתחות אישית'),
        ('relationship', 'זוגיות'),
        ('creative_thinking', 'חשיבה יצירתית'),
    ]

    TASK_TYPE_CHOICES = [
        ('survey', 'שאלון'),
        ('fill_in_the_blanks', 'השלמת משפטים'),
        ('text_or_image', 'רגשות מטקסט או תמונה'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    # Add more fields as needed