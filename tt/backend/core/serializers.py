from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import KnowledgeNode, KnowledgeLink, Question, PracticeHistory, UserProgress

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'date_joined')
        read_only_fields = ('id', 'date_joined')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class KnowledgeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeNode
        fields = '__all__'

class KnowledgeLinkSerializer(serializers.ModelSerializer):
    source = KnowledgeNodeSerializer(read_only=True)
    target = KnowledgeNodeSerializer(read_only=True)

    class Meta:
        model = KnowledgeLink
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    knowledge_nodes = KnowledgeNodeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class PracticeHistorySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = PracticeHistory
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class UserProgressSerializer(serializers.ModelSerializer):
    mastery_level = serializers.SerializerMethodField()

    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_mastery_level(self, obj):
        return obj.calculate_mastery_level() 