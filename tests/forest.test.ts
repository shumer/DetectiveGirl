import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { forestCorrect } from '../app/forest-game.ts';
void test('forest answers match delivery quantities, time crossing an hour and both sketch conditions', () => {
  for (const step of [0, 1, 3]) {
    assert.equal(forestCorrect(step, '1'), true);
    for (const wrong of ['0','2','','3']) assert.equal(forestCorrect(step, wrong), false);
  }
  for (const time of ['18:15','1815','18.15','18 15']) assert.equal(forestCorrect(2,time), true);
  for (const time of ['17:75','18:05','18:35','', '18:150']) assert.equal(forestCorrect(2,time), false);
  assert.equal(forestCorrect(4,'1'), false);
});
void test('forest translations cover every screen and preserve three choices', () => {
  const copy = JSON.parse(readFileSync(new URL('../app/forest.json', import.meta.url), 'utf8'));
  assert.deepEqual(Object.keys(copy).sort(), ['en','pl','ru','uk']);
  for (const rows of Object.values(copy) as string[][]) {
    assert.equal(rows.length,31);
    assert.ok(rows.every(text => text.trim() && !/[\u2013\u2014]/.test(text)));
    for (const i of [12,16,24]) assert.equal(rows[i].split('|').length,3);
    assert.ok(rows[19].includes('17:40'));
    assert.ok(rows[21].includes('18:15'));
  }
});
