import ru from './locales/ru.json';
import pl from './locales/pl.json';
import en from './locales/en.json';
import uk from './locales/uk.json';
export const languages = [
  { id: 'ru', name: 'Русский' },
  { id: 'pl', name: 'Polski' },
  { id: 'en', name: 'English' },
  { id: 'uk', name: 'Українська' },
] as const;
export type Language = (typeof languages)[number]['id'];
export const translations: Record<Language, typeof ru> = { ru, pl, en, uk };
export function isLanguage(value: unknown): value is Language {
  return languages.some(({ id }) => id === value);
}
