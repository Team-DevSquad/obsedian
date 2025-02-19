from django.db import models

from authenticate.models import User

# Create your models here.

class Project(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=50)
    project_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Testing(models.Model):
    class TestingType(models.TextChoices):
        LLM = 'LLM', 'LLM'
        GitLeaks = 'GitLeaks', 'GitLeaks'
        Nuclie = 'Nuclie', 'Nuclie'
        CVEscan = 'CVEscan', 'CVEscan'
    
    class TestingStatus(models.TextChoices):
        Waiting = 'Waiting', 'Waiting'
        Cloning = 'Cloning', 'Cloning'
        InProgress = 'InProgress', 'InProgress'
        Completed = 'Completed', 'Completed'
        Failed = 'Failed', 'Failed'

    test_id = models.AutoField(primary_key=True, unique=True, editable=False, db_index=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    testing_type = models.CharField(max_length=50,choices=TestingType.choices, default=TestingType.LLM)
    source_url = models.URLField()
    LLM_test_result = models.URLField(null=True)
    CVEscan_test_result = models.URLField(null=True)
    GitLeaks_test_result = models.URLField(null=True)
    Nuclie_test_result = models.URLField(null=True)
    repo_folder_name = models.TextField(default='', blank=True)
    testing_status = models.CharField(max_length=50, choices=TestingStatus.choices, default=TestingStatus.Waiting)
    test_count = models.IntegerField(default=0)
    error_message = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
