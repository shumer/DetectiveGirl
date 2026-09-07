export const cameraRecords = [
  { id: 2, shownMinutes: 15 * 60 + 11, correction: 0 },
  { id: 0, shownMinutes: 15 * 60 + 10, correction: -3 },
  { id: 1, shownMinutes: 15 * 60 + 4, correction: 5 },
];
export function correctInterval(value: string) {
  return /^\d+$/.test(value.trim()) && Number(value) === (15 * 60 + 12) - (14 * 60 + 30);
}
export function correctTime(value: string) {
  const normalized = value.trim().replace(/[.\s]/g, ':');
  return normalized === '15:20' || normalized === '1520';
}
export function correctOrder(value: number[]) {
  if (value.length !== cameraRecords.length || new Set(value).size !== value.length) return false;
  const times = value.map(id => {
    const record = cameraRecords.find(item => item.id === id);
    return record ? record.shownMinutes + record.correction : Number.NaN;
  });
  return times.every((time, index) => Number.isFinite(time) && (index === 0 || times[index - 1] < time));
}
export const correctPerson = (id: number) => id === 2;
export const correctReason = (id: number) => id === 1;
