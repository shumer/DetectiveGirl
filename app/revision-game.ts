export type ResponseKind = 'choice' | 'number' | 'time' | 'order';
export function validateResponse(kind: ResponseKind, expected: string | number | number[], response: string | number[]) {
  if (kind === 'order') return Array.isArray(expected) && Array.isArray(response) && response.length === expected.length && new Set(response).size === response.length && expected.every((id,index)=>id===response[index]);
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
