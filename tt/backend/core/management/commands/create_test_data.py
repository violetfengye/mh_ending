from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import KnowledgeNode, KnowledgeLink, Question, UserProgress

User = get_user_model()

class Command(BaseCommand):
    help = '创建测试数据'

    def handle(self, *args, **options):
        self.stdout.write('开始创建测试数据...')
        
        # 创建测试用户
        user, created = User.objects.get_or_create(
            username='testuser',
            email='test@example.com'
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('创建测试用户: testuser')
        
        # 创建知识点
        nodes_data = [
            {
                'title': '基础运算',
                'content': '包括加减乘除等基本运算',
                'category': '运算',
                'level': 1,
                'difficulty': 1
            },
            {
                'title': '分数运算',
                'content': '分数的加减乘除运算',
                'category': '运算',
                'level': 2,
                'difficulty': 2
            },
            {
                'title': '代数基础',
                'content': '代数式的基本概念和运算',
                'category': '代数',
                'level': 1,
                'difficulty': 2
            },
            {
                'title': '一元二次方程',
                'content': '一元二次方程的解法',
                'category': '代数',
                'level': 3,
                'difficulty': 3
            },
            {
                'title': '几何基础',
                'content': '基本几何概念和性质',
                'category': '几何',
                'level': 1,
                'difficulty': 1
            },
            {
                'title': '三角函数',
                'content': '三角函数的概念和性质',
                'category': '几何',
                'level': 4,
                'difficulty': 4
            },
            {
                'title': '微积分基础',
                'content': '导数和积分的基本概念',
                'category': '微积分',
                'level': 5,
                'difficulty': 5
            }
        ]
        
        nodes = {}
        for data in nodes_data:
            node, created = KnowledgeNode.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            nodes[data['title']] = node
            if created:
                self.stdout.write(f'创建知识点: {data["title"]}')
        
        # 创建知识点关联
        links_data = [
            ('基础运算', '分数运算', '包含'),
            ('代数基础', '一元二次方程', '使用'),
            ('几何基础', '三角函数', '使用'),
            ('三角函数', '微积分基础', '相关')
        ]
        
        for source_title, target_title, relation_type in links_data:
            link, created = KnowledgeLink.objects.get_or_create(
                source=nodes[source_title],
                target=nodes[target_title],
                defaults={'relation_type': relation_type}
            )
            if created:
                self.stdout.write(f'创建关联: {source_title} -> {target_title}')
        
        # 创建测试题目
        questions_data = [
            {
                'title': '基础加法',
                'content': '计算：1 + 1 = ?',
                'answer': '2',
                'analysis': '这是最基础的加法运算',
                'difficulty': 1,
                'knowledge_node': '基础运算'
            },
            {
                'title': '分数加法',
                'content': '计算：1/2 + 1/3 = ?',
                'answer': '5/6',
                'analysis': '需要通分后相加',
                'difficulty': 2,
                'knowledge_node': '分数运算'
            },
            {
                'title': '解方程',
                'content': '解方程：x² + 2x + 1 = 0',
                'answer': 'x = -1',
                'analysis': '使用完全平方公式',
                'difficulty': 3,
                'knowledge_node': '一元二次方程'
            }
        ]
        
        for data in questions_data:
            question, created = Question.objects.get_or_create(
                title=data['title'],
                defaults={k: v for k, v in data.items() if k != 'knowledge_node'}
            )
            if created:
                question.knowledge_nodes.add(nodes[data['knowledge_node']])
                self.stdout.write(f'创建题目: {data["title"]}')
        
        # 创建用户进度
        progress, created = UserProgress.objects.get_or_create(
            user=user,
            defaults={
                'total_practices': 0,
                'correct_practices': 0,
                'total_time_spent': 0
            }
        )
        if created:
            self.stdout.write('创建用户进度记录')
        
        self.stdout.write(self.style.SUCCESS('测试数据创建完成！')) 