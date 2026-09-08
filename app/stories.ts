import cloud from './cases/cloud.json';
import type { Language } from './i18n';
export type StoryStep = { title: string; text: string; options: string[]; answer: number; explanation: string; hints: string[] };
export type Story = { id: string; number: string; locales: Record<Language, { title: string; intro: string; ending: string; question: string; steps: StoryStep[] }> };
export const stories: Story[] = [cloud,];
