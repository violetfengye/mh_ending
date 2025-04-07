from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import KnowledgeNode, KnowledgeLink, Question, PracticeHistory, UserProgress
from .serializers import (
    UserSerializer, UserCreateSerializer, KnowledgeNodeSerializer,
    KnowledgeLinkSerializer, QuestionSerializer, PracticeHistorySerializer,
    UserProgressSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import pytesseract
from PIL import Image
import io
import os
import re
import requests
import json
from django.conf import settings

# 设置 Tesseract-OCR 可执行文件路径
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# Deepseek API 配置
DEEPSEEK_API_KEY = 'sk-5c5fd7f2995542e1ab0507eecf8e1100'
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def process_with_deepseek(text):
    """使用Deepseek API处理文本"""
    # 预处理OCR文本
    cleaned_text = text.replace('X', '×').replace('十', '+').replace('\n\n', '\n').strip()
    print(f"预处理后的文本:\n{cleaned_text}")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""作为一个数学教育专家，请先整理题目内容，然后解答以下数学题目：

原始题目：
{cleaned_text}

请按以下格式返回JSON：
{{
    "question": {{
        "main": "题目主要要求",
        "sub_questions": [
            {{
                "id": "1",
                "content": "59×2.5×0.4=□×(□×□)"
            }},
            // ... 其他小题
        ]
    }},
    "analysis": {{
        "1": "第1题的解题思路",
        "2": "第2题的解题思路",
        // ... 其他小题的解题思路
    }},
    "answer": {{
        "1": "第1题的答案",
        "2": "第2题的答案",
        // ... 其他小题的答案
    }}
}}

注意：
1. 请确保sub_questions中的content包含完整的算式，包括等号和空格位置
2. 对于需要填空的位置，使用□符号表示
3. 保持原题的格式和符号
4. 请直接返回JSON，不要添加其他说明文字"""

    try:
        print(f"发送到Deepseek的请求:\n{prompt}")
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 2000
            },
            timeout=30,
            verify=False
        )
        
        print(f"Deepseek API 状态码: {response.status_code}")
        print(f"Deepseek API 响应:\n{response.text}")
        
        if response.status_code == 200:
            result = response.json()
            try:
                content = result['choices'][0]['message']['content']
                print(f"API返回的content:\n{content}")
                
                # 处理可能的 Markdown 格式
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                elif content.startswith("```"):
                    content = content.replace("```", "").strip()
                
                parsed_result = json.loads(content)
                
                # 重新组织返回的数据结构
                return {
                    "question": parsed_result["question"]["main"],
                    "sub_questions": parsed_result["question"]["sub_questions"],
                    "analysis": parsed_result["analysis"],
                    "answer": parsed_result["answer"]
                }
            except (KeyError, json.JSONDecodeError) as e:
                print(f"解析API响应时出错: {str(e)}")
                return {
                    "question": cleaned_text,
                    "analysis": "抱歉，解析AI响应时出错，请稍后重试。",
                    "answer": "无法生成答案"
                }
        else:
            print(f"API调用失败: {response.status_code} - {response.text}")
            return {
                "question": cleaned_text,
                "analysis": f"API调用失败: {response.status_code}",
                "answer": "请稍后重试"
            }
            
    except Exception as e:
        print(f"调用Deepseek API时出错: {str(e)}")
        return {
            "question": cleaned_text,
            "analysis": f"API调用出错: {str(e)}",
            "answer": "请稍后重试"
        }

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'register':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'register':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class KnowledgeNodeViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeNode.objects.all()
    serializer_class = KnowledgeNodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def map(self, request):
        """获取完整的知识图谱数据"""
        nodes = KnowledgeNode.objects.all()
        links = KnowledgeLink.objects.all()
        
        # 获取所有分类
        categories = list(set(node.category for node in nodes))
        
        # 构建知识图谱数据
        nodes_data = [{
            'id': str(node.id),
            'name': node.title,
            'value': node.level,
            'category': node.category,
            'content': node.content,
            'difficulty': node.difficulty
        } for node in nodes]
        
        links_data = [{
            'source': str(link.source.id),
            'target': str(link.target.id),
            'value': 1,
            'relation_type': link.relation_type
        } for link in links]
        
        return Response({
            'nodes': nodes_data,
            'links': links_data,
            'categories': categories
        })

class KnowledgeLinkViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeLink.objects.all()
    serializer_class = KnowledgeLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        # TODO: 实现智能推荐算法
        questions = Question.objects.all()[:5]
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

class PracticeHistoryViewSet(viewsets.ModelViewSet):
    queryset = PracticeHistory.objects.all()
    serializer_class = PracticeHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        obj, created = UserProgress.objects.get_or_create(user=self.request.user)
        return obj

class OCRView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return Response(
                {'error': '请选择要上传的图片'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            image_file = request.FILES['image']
            image = Image.open(image_file)
            
            # OCR识别
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            text = text.strip()
            print(f"原始OCR识别结果:\n{text}")
            
            # 使用Deepseek处理
            result = process_with_deepseek(text)
            
            if result:
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({
                    'text': text,
                    'analysis': '抱歉，AI处理失败，请稍后重试。',
                    'answer': '无法生成答案'
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"处理请求时出错: {str(e)}")
            return Response(
                {
                    'error': str(e),
                    'detail': '图片处理失败，请确保上传了正确的图片格式'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
