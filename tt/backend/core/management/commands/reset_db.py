from django.core.management.base import BaseCommand
from core.models import KnowledgeNode, KnowledgeLink, Question, PracticeHistory, UserProgress

class Command(BaseCommand):
    help = '重置知识点相关的数据（保留用户数据）'

    def handle(self, *args, **options):
        self.stdout.write('开始重置知识点相关数据...')
        
        # 删除知识点相关的数据
        self.stdout.write('删除练习历史...')
        PracticeHistory.objects.all().delete()
        
        self.stdout.write('删除题目...')
        Question.objects.all().delete()
        
        self.stdout.write('删除知识点关联...')
        KnowledgeLink.objects.all().delete()
        
        self.stdout.write('删除知识点...')
        KnowledgeNode.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('知识点相关数据重置完成！')) 