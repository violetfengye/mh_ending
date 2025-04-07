import axios from "axios";
import { useUserStore } from "../stores/user";
import type {
  OCRResult,
  KnowledgeMap,
  Question,
  UserProgress,
} from "../types/api";

const API_URL = "http://127.0.0.1:8000/api";

export async function uploadImage(file: File): Promise<OCRResult> {
  const formData = new FormData();
  formData.append("image", file);

  const userStore = useUserStore();
  const response = await axios.post(`${API_URL}/ocr/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${userStore.token}`,
    },
  });
  return response.data;
}

export async function getKnowledgeMap(): Promise<KnowledgeMap> {
  const userStore = useUserStore();
  const response = await axios.get(`${API_URL}/knowledge-nodes/map/`, {
    headers: {
      Authorization: `Bearer ${userStore.token}`,
    },
  });
  return response.data;
}

export async function getRecommendations(): Promise<Question[]> {
  const userStore = useUserStore();
  const response = await axios.get(`${API_URL}/practice/recommendations/`, {
    headers: {
      Authorization: `Bearer ${userStore.token}`,
    },
  });
  return response.data;
}

export async function submitAnswer(
  questionId: number,
  answer: string
): Promise<{ analysis: string }> {
  const userStore = useUserStore();
  const response = await axios.post(
    `${API_URL}/practice/submit/`,
    {
      question_id: questionId,
      answer: answer,
    },
    {
      headers: {
        Authorization: `Bearer ${userStore.token}`,
      },
    }
  );
  return response.data;
}

export async function getUserProgress(): Promise<UserProgress> {
  const userStore = useUserStore();
  const response = await axios.get(`${API_URL}/user/progress/`, {
    headers: {
      Authorization: `Bearer ${userStore.token}`,
    },
  });
  return response.data;
}
