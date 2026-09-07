export function forestCorrect(step: number, answer: string) {
  if (!Number.isInteger(step) || step < 0 || step > 3) return false;
  return step === 2 ? /^18[:. ]?15$/.test(answer.trim()) : answer === '1';
}
