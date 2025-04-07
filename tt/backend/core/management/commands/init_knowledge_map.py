from django.core.management.base import BaseCommand
from core.models import KnowledgeNode, KnowledgeLink

class Command(BaseCommand):
    help = '初始化知识图谱数据'

    def handle(self, *args, **kwargs):
        # 清除现有数据
        KnowledgeNode.objects.all().delete()
        KnowledgeLink.objects.all().delete()

        # 创建知识节点
        nodes = {
            '代数': KnowledgeNode.objects.create(
                title='代数',
                content='代数是数学的一个重要分支，主要研究数学符号和处理数学式子的规则。它包括了方程、多项式、代数结构等内容。',
                category='基础数学',
                level=5
            ),
            '方程': KnowledgeNode.objects.create(
                title='方程',
                content='方程是含有未知数的等式。解方程就是找出未知数的值，使等式成立。方程是数学中最基本的工具之一。',
                category='代数',
                level=4
            ),
            '一元二次方程': KnowledgeNode.objects.create(
                title='一元二次方程',
                content='一元二次方程是形如ax²+bx+c=0（a≠0）的方程。它在实际问题中有广泛的应用，可以通过多种方法求解。',
                category='方程',
                level=3
            ),
            '因式分解': KnowledgeNode.objects.create(
                title='因式分解',
                content='因式分解是将一个多项式写成几个多项式乘积的形式。它是解方程的重要方法之一，也是研究多项式性质的重要工具。',
                category='代数',
                level=3
            ),
            '配方法': KnowledgeNode.objects.create(
                title='配方法',
                content='配方法是解一元二次方程的一种方法，通过恰当变形，将方程化为完全平方式，从而得到方程的解。',
                category='解题方法',
                level=2
            ),
            '求根公式': KnowledgeNode.objects.create(
                title='求根公式',
                content='一元二次方程ax²+bx+c=0的求根公式为：x=[-b±√(b²-4ac)]/(2a)。它是解一元二次方程最直接的方法。',
                category='公式',
                level=2
            ),
            '判别式': KnowledgeNode.objects.create(
                title='判别式',
                content='判别式Δ=b²-4ac用于判断一元二次方程的解的情况。Δ>0时有两个不同实根，Δ=0时有两个相等实根，Δ<0时有两个共轭复根。',
                category='代数',
                level=2
            ),
            '韦达定理': KnowledgeNode.objects.create(
                title='韦达定理',
                content='韦达定理说明了一元二次方程的根与系数之间的关系。如果x₁、x₂是方程ax²+bx+c=0的两个根，那么x₁+x₂=-b/a，x₁x₂=c/a。',
                category='定理',
                level=3
            ),
            '复数': KnowledgeNode.objects.create(
                title='复数',
                content='复数是实数的扩充，引入虚数单位i（i²=-1）后，任何一元二次方程都有解。复数的引入使代数理论更加完善。',
                category='代数',
                level=4
            ),
        }

        # 创建知识关联
        links = [
            ('代数', '方程', '包含'),
            ('方程', '一元二次方程', '包含'),
            ('一元二次方程', '因式分解', '使用'),
            ('一元二次方程', '配方法', '使用'),
            ('一元二次方程', '求根公式', '使用'),
            ('一元二次方程', '判别式', '相关'),
            ('一元二次方程', '韦达定理', '相关'),
            ('一元二次方程', '复数', '相关'),
            ('判别式', '求根公式', '使用'),
            ('韦达定理', '求根公式', '相关'),
            ('复数', '求根公式', '扩展'),
        ]

        for source, target, relation_type in links:
            KnowledgeLink.objects.create(
                source=nodes[source],
                target=nodes[target],
                relation_type=relation_type
            )

        self.stdout.write(self.style.SUCCESS('成功初始化知识图谱数据')) 