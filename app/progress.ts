/** Solved cases are remembered per browser so the gallery can show them. */
export type CaseResult = { mistakes: number; hints: number; at: string; variants: number[] };
export type Progress = Record<string, CaseResult>;
const KEY = 'detective-girl-progress';
export function readProgress(): Progress {
  try {
    const raw = localStorage.getItem(KEY);
    const value = raw ? JSON.parse(raw) : {};
    if (!value || typeof value !== 'object') return {};
    for (const entry of Object.values(value) as CaseResult[]) if (!Array.isArray(entry.variants)) entry.variants = [0];
    return value;
  } catch {
    return {};
  }
}
export function saveResult(id: string, result: { mistakes: number; hints: number; variant: number }): Progress {
  const previous = readProgress()[id];
  const variants = Array.from(new Set([...(previous?.variants ?? []), result.variant])).sort((a, b) => a - b);
  const next = { ...readProgress(), [id]: { mistakes: result.mistakes, hints: result.hints, variant: result.variant, at: new Date().toISOString(), variants } };
  try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* Local storage is optional. */ }
  return next;
}
/** First sentences of the intro, short enough for a card. */
export function teaser(intro: string, limit = 120) {
  // Sentence ends are a full stop followed by a space and a capital letter or an opening quote.
  const ends = [...intro.matchAll(/[.!?](?=\s+[A-ZА-ЯЁІЇЄҐŁŚŻ«„“"])/g)].map(match => match.index + 1);
  let text = '';
  for (const end of ends) {
    const candidate = intro.slice(0, end).trim();
    if (text && candidate.length > limit) break;
    text = candidate;
  }
  return text || intro;
}
