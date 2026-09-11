import type { Language } from './i18n';
import type { RevisedStep } from './RevisionCase';
export type Answer = string | number | number[];
/** One set of numbers for a case: placeholder values, the answer of every step and the option order per step. */
export type Variant = { values: Record<string, string | number>; answers: Answer[]; orders?: (number[] | null)[] };
function pluralForm(n: number, lang: Language, forms: string[]) {
  if (forms.length === 1) return forms[0];
  const abs = Math.abs(n), last = abs % 10, last2 = abs % 100;
  if (lang === 'en') return forms[Number.isInteger(abs) && abs === 1 ? 0 : forms.length - 1];
  if (forms.length === 2) return forms[last === 1 && last2 !== 11 ? 0 : 1];
  if (!Number.isInteger(abs)) return forms[1];
  if (last === 1 && last2 !== 11) return forms[0];
  if (last >= 2 && last <= 4 && (last2 < 12 || last2 > 14)) return forms[1];
  return forms[2];
}
function formatValue(value: string | number, lang: Language) {
  if (typeof value === 'string') return value;
  if (Number.isInteger(value)) return String(value);
  return lang === 'en' ? String(value) : String(value).replace('.', ',');
}
/** Replace {key} with the value and {key|one|few|many} with the value followed by its plural form. */
export function render(template: string, values: Record<string, string | number>, lang: Language) {
  // {key#a|b|c} picks the entry whose index equals the value (used for letters, ordinals and fraction words).
  const indexed = template.replace(/\{([a-zA-Z0-9_]+)#([^{}]*)\}/g, (whole, key: string, list: string) => {
    const value = values[key];
    if (value === undefined) return whole;
    return list.split('|')[Number(value)] ?? whole;
  });
  return indexed.replace(/\{([a-zA-Z0-9_]+)((?:\|[^{}|]*)*)\}/g, (whole, key: string, formsRaw: string) => {
    const value = values[key];
    if (value === undefined) return whole;
    if (!formsRaw) return formatValue(value, lang);
    const forms = formsRaw.slice(1).split('|');
    return `${formatValue(value, lang)} ${pluralForm(Number(value), lang, forms)}`;
  });
}
/** Step text with the variant's numbers filled in and its options reordered. */
export function renderStep(step: RevisedStep, variant: Variant | null, index: number, lang: Language): RevisedStep {
  if (!variant) return step;
  const values = variant.values, r = (text: string) => render(text, values, lang);
  const order = variant.orders?.[index] ?? step.options.map((_, i) => i);
  const options = order.map(i => r(step.options[i]));
  const feedback = step.feedback ? order.map(i => r(step.feedback?.[i] ?? '')) : undefined;
  const base = variant.answers[index];
  const answer: Answer = step.kind === 'choice' ? order.indexOf(base as number) : step.kind === 'multi' ? (base as number[]).map(i => order.indexOf(i)) : step.kind === 'order' ? (base as number[]).map(i => order.indexOf(i)) : String(base);
  return { ...step, title: r(step.title), situation: r(step.situation), evidence: step.evidence.map(r), question: r(step.question), options, feedback, answer, explanation: r(step.explanation), outcome: r(step.outcome), next: r(step.next), hints: step.hints.map(r) };
}
export function renderText(text: string, variant: Variant | null, lang: Language) {
  return variant ? render(text, variant.values, lang) : text;
}
/** Pick a variant the player has not solved yet; any variant once all are done. */
export function pickVariant(count: number, solved: number[], random = Math.random) {
  if (count <= 0) return 0;
  const fresh = Array.from({ length: count }, (_, i) => i).filter(i => !solved.includes(i));
  const pool = fresh.length ? fresh : Array.from({ length: count }, (_, i) => i);
  return pool[Math.floor(random() * pool.length)] ?? 0;
}
