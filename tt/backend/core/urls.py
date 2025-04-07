from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserViewSet, KnowledgeNodeViewSet, KnowledgeLinkViewSet,
    QuestionViewSet, PracticeHistoryViewSet, UserProgressViewSet, OCRView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'knowledge-nodes', KnowledgeNodeViewSet)
router.register(r'knowledge-links', KnowledgeLinkViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'practice-history', PracticeHistoryViewSet)
router.register(r'user-progress', UserProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ocr/', OCRView.as_view(), name='ocr'),
] 