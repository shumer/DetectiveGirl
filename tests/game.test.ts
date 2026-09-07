import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { correctInterval, correctTime, correctOrder, correctPerson, correctReason } from '../app/game.ts';

await test('the photo interval is measured in minutes across the hour', () => {
  for (let number = 0; number < 100; number++) {
    const fits = number === 30 + 12;
    assert.equal(correctInterval(String(number)), fits, String(number));
  }
});

await test('the time answer supports a phone keypad and rejects near misses', () => {
  for (const answer of ['15:20', '1520', '15.20', '15 20', ' 15:20 ']) assert.ok(correctTime(answer));
  for (const answer of ['', '15:05', '15:10', '14:80', '3:20', '15:200', '15020']) assert.equal(correctTime(answer), false);
});

await test('camera chronology validates all permutations and rejects duplicate records', () => {
  const values = [15 * 60 + 7, 15 * 60 + 9, 15 * 60 + 11];
  for (const a of [0, 1, 2]) for (const b of [0, 1, 2]) for (const c of [0, 1, 2]) {
    const order = [a, b, c];
    assert.equal(correctOrder(order), values[a] < values[b] && values[b] < values[c]);
  }
  for (const order of [[], [0], [0, 1], [0, 1, 2, 3], [-1, 0, 1]]) assert.equal(correctOrder(order), false);
});

await test('deduction needs both presence and badge, followed by evidence rather than a guess', () => {
  const people = [{ yellow: true, present: false }, { yellow: false, present: true }, { yellow: true, present: true }];
  people.forEach((person, id) => assert.equal(correctPerson(id), person.yellow && person.present));
  assert.equal(correctReason(0), false);
  assert.equal(correctReason(1), true);
  assert.equal(correctReason(2), false);
});

function structure(value: unknown): unknown {
  if (typeof value === 'string') { assert.ok(value.trim().length > 0); return 'string'; }
  if (Array.isArray(value)) return value.map(structure);
  assert.ok(value && typeof value === 'object');
  return Object.fromEntries(Object.entries(value).sort(([a], [b]) => a.localeCompare(b)).map(([key, child]) => [key, structure(child)]));
}
const localeNames = ['ru', 'pl', 'en', 'uk'];
const locales = Object.fromEntries(localeNames.map(name => [name, JSON.parse(readFileSync(new URL(`../app/locales/${name}.json`, import.meta.url), 'utf8'))]));
await test('all four translations have identical complete shapes and no empty strings', () => {
  for (const name of localeNames) assert.deepEqual(structure(locales[name]), structure(locales.ru), name);
});
await test('each language preserves the camera facts and the final destination', () => {
  for (const name of localeNames) {
    const locale = locales[name];
    assert.equal(locale.note.records.length, 3);
    assert.ok(locale.note.records[0].includes('15:10'));
    assert.ok(locale.note.records[1].includes('15:04'));
    assert.ok(locale.note.records[2].includes('15:11'));
    assert.ok(locale.success[2].includes(locale.note.pieces[2]));
    assert.equal(locale.titles.length, 4);
    assert.equal(locale.hints.length, 4);
    for (const hints of locale.hints) assert.equal(hints.length, 3);
  }
});
await test('player-facing translations use plain dashes', () => {
  for (const name of localeNames) assert.doesNotMatch(JSON.stringify(locales[name]), /[\u2013\u2014]/);
});
