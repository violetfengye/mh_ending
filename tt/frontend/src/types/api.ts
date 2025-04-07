export interface UserInfo {
  username: string;
  email: string;
  avatar?: string;
  profile: {
    learning_progress: Record<string, number>;
    practice_history: PracticeHistory[];
    recommendations: Question[];
  };
}

export interface PracticeHistory {
  id: number;
  date: string;
  title: string;
  score: number;
  time: string;
}

export interface Question {
  id: number;
  title: string;
  content: string;
  difficulty: number;
  analysis?: string;
}

export interface KnowledgeNode {
  id: string;
  name: string;
  value: number;
  category: string;
  difficulty: number;
  content: string;
}

export interface KnowledgeLink {
  source: string;
  target: string;
}

export interface KnowledgeMap {
  nodes: KnowledgeNode[];
  links: KnowledgeLink[];
  categories: string[];
}

export interface UserProgress {
  stats: {
    totalQuestions: number;
    correctRate: string;
    totalTime: string;
  };
  history: PracticeHistory[];
}

export interface OCRResult {
  text: string;
  message: string;
}
