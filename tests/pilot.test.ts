import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import type { RevisedStep } from '../app/RevisionCase';
import { validateResponse } from '../app/revision-game.ts';
await test('pilot cases are complete in Russian, hints never spell out the answer, and every wrong option has feedback',()=>{
 const root=new URL('../app/pilot/',import.meta.url);
 const files=readdirSync(root).filter(name=>name.endsWith('.json'));
 assert.ok(files.length>0);
 for(const file of files){
  const story=JSON.parse(readFileSync(new URL(file,root),'utf8'));
  assert.ok(story.pilot);
  const content=story.locales.ru;
  for(const field of ['title','intro','ending','question'])assert.ok(content[field]?.trim(),`${file}/${field}`);
  assert.equal(content.steps.length,4);
  content.steps.forEach((step:RevisedStep,index:number)=>{
   for(const field of ['title','situation','question','explanation','outcome','next'] as const)assert.ok(step[field]?.trim(),`${file}/${index}/${field}`);
   assert.ok(step.evidence.length>0&&step.evidence.every(fact=>fact.trim()));
   assert.equal(step.hints.length,3);
   const response=Array.isArray(step.answer)?step.answer:String(step.answer);
   assert.ok(validateResponse(step.kind,step.answer,response));
   assert.equal(validateResponse(step.kind,step.answer,''),false);
   if(step.kind==='choice'){
    assert.ok(step.options.length>=4,`${file}/${index}: choice needs at least four options`);
    assert.equal(step.feedback?.length,step.options.length);
    step.options.forEach((_,i)=>{assert.equal(validateResponse('choice',step.answer,String(i)),i===step.answer);assert.equal(Boolean(step.feedback?.[i]?.trim()),i!==step.answer,`${file}/${index}/feedback/${i}`);});
   }
   if(step.kind==='multi'){assert.ok(Array.isArray(step.answer)&&step.answer.length>0&&step.answer.length<step.options.length);}
   if(step.kind==='time'||step.kind==='number'){for(const hint of step.hints)assert.ok(!hint.includes(String(step.answer)),`${file}/${index}: hint reveals answer`);}
   assert.doesNotMatch(JSON.stringify(step),/[–—]/);
  });
 }
});
