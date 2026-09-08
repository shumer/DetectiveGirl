import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
void test('published stories have four complete localized stages and real scene assets', () => {
 const root = new URL('../app/cases/', import.meta.url);
 for (const file of readdirSync(root).filter(name=>name.endsWith('.json'))) {
  const story = JSON.parse(readFileSync(new URL(file,root),'utf8'));
  assert.deepEqual(Object.keys(story.locales).sort(),['en','pl','ru','uk']);
  for (const language of ['ru','pl','en','uk']) {
   const t=story.locales[language];
   for (const key of ['title','intro','ending','question']) assert.ok(t[key]?.trim(),`${file} ${language} ${key}`);
   assert.equal(t.steps.length,4);
   t.steps.forEach((step:{title:string;text:string;explanation:string;options:string[];answer:number;hints:string[]},index:number)=>{
    assert.ok(step.title.trim() && step.text.trim() && step.explanation.trim());
    assert.equal(step.options.length,3);
    assert.equal(new Set(step.options).size,3);
    assert.ok(Number.isInteger(step.answer) && step.answer>=0 && step.answer<3);
    assert.equal(step.answer,story.locales.ru.steps[index].answer);
    assert.equal(step.hints.length,3);
    assert.ok(step.hints.every(hint=>hint.trim()));
    assert.ok(existsSync(new URL(`../public/backgrounds/${story.id}-${index}.jpg`,import.meta.url)));
   });
  }
  assert.ok(!/[\u2013\u2014]/.test(JSON.stringify(story)));
 }
});
