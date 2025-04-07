from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """自定义用户模型"""
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class KnowledgeNode(models.Model):
    """知识节点"""
    DIFFICULTY_CHOICES = [
        (1, '入门'),
        (2, '基础'),
        (3, '进阶'),
        (4, '高级'),
        (5, '专家'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50)
    level = models.IntegerField(default=1)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class KnowledgeLink(models.Model):
    """知识节点之间的关联"""
    source = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE, related_name='outgoing_links')
    target = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE, related_name='incoming_links')
    relation_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'target', 'relation_type')

class Question(models.Model):
    """题目"""
    DIFFICULTY_CHOICES = [
        (1, '简单'),
        (2, '中等'),
        (3, '困难'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    answer = models.TextField()
    analysis = models.TextField(blank=True)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    knowledge_nodes = models.ManyToManyField(KnowledgeNode, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PracticeHistory(models.Model):
    """练习历史"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_history')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    time_spent = models.IntegerField()  # 单位：秒
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class UserProgress(models.Model):
    """用户学习进度"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    total_practices = models.IntegerField(default=0)
    correct_practices = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)  # 单位：秒
    last_practice_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_mastery_level(self):
        """计算掌握程度"""
        if self.total_practices == 0:
            return 0
        return (self.correct_practices / self.total_practices) * 100
