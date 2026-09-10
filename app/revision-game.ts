export type ResponseKind = 'choice' | 'number' | 'time' | 'order' | 'multi';
/** Wrong answers before the next hint opens on its own. */
export const AUTO_HINT_AFTER = 2;
export function validateResponse(kind: ResponseKind, expected: string | number | number[], response: string | number[]) {
  if (kind === 'order') return Array.isArray(expected) && Array.isArray(response) && response.length === expected.length && new Set(response).size === response.length && expected.every((id,index)=>id===response[index]);
  if (kind === 'multi') {
    if (!Array.isArray(expected) || !Array.isArray(response) || response.length === 0) return false;
    const chosen = new Set(response);
    return chosen.size === response.length && chosen.size === expected.length && expected.every(id => chosen.has(id));
  }
  if (typeof response !== 'string' || Array.isArray(expected)) return false;
  const value=response.trim();
  if (kind === 'time') {
    if (!/^\d{2}[:. ]?\d{2}$/.test(value)) return false;
    const digits=value.replace(/[.:\s]/g,'');
    if (!/^\d{4}$/.test(digits) || Number(digits.slice(0,2)) > 23 || Number(digits.slice(2)) > 59) return false;
    return digits === String(expected).replace(':','');
  }
  if (kind === 'number') return /^\d+(?:[.,]\d+)?$/.test(value) && Number(value.replace(',','.')) === Number(expected);
  return /^\d+$/.test(value) && Number(value) === expected;
}
/** Rank shown at the end: fewer mistakes, higher rank. */
export function rankIndex(mistakes: number, hints: number) {
  if (mistakes === 0 && hints === 0) return 0;
  if (mistakes <= 2) return 1;
  return 2;
}
