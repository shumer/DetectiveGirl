import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import type { RevisedStep } from '../app/RevisionCase';
import { validateResponse } from '../app/revision-game.ts';
await test('reviewed cases preserve puzzles across languages and contain every player-facing field',()=>{
 const root=new URL('../app/revised/',import.meta.url);
 for(const file of readdirSync(root).filter(name=>name.endsWith('.json'))){
  const story=JSON.parse(readFileSync(new URL(file,root),'utf8'));
  assert.deepEqual(Object.keys(story.locales).sort(),['en','pl','ru','uk']);
  for(const lang of ['ru','pl','en','uk']){
   const content=story.locales[lang];
   for(const field of ['title','intro','ending','question'])assert.ok(content[field]?.trim(),`${file}/${lang}/${field}`);
   assert.equal(content.steps.length,4);
   content.steps.forEach((step:RevisedStep,index:number)=>{
    const original=story.locales.ru.steps[index];
    for(const field of ['title','situation','question','explanation','outcome','next'] as const)assert.ok(step[field]?.trim(),`${file}/${lang}/${index}/${field}`);
    assert.ok(step.evidence.length>0 && step.evidence.every((fact:string)=>fact.trim()));
    assert.equal(step.hints.length,3);assert.ok(step.hints.every((hint:string)=>hint.trim()));
    for(const field of ['kind','answer','scene'] as const)assert.deepEqual(step[field],original[field],`${file}/${lang}/${index}/${field}`);
    assert.ok(Number.isInteger(step.scene)&&step.scene>=0&&step.scene<=3);
    if(step.kind==='choice'){assert.ok(step.options.length>=2);assert.ok(typeof step.answer==='number'&&step.answer>=0&&step.answer<step.options.length);}
    if(step.kind==='order'){assert.ok(Array.isArray(step.answer));assert.equal(step.answer.length,step.options.length);assert.deepEqual([...step.answer].sort((a,b)=>a-b),step.options.map((_:string,i:number)=>i));}
    const response=Array.isArray(step.answer)?step.answer:String(step.answer);
    assert.ok(validateResponse(step.kind,step.answer,response));
    assert.equal(validateResponse(step.kind,step.answer,''),false);
    if(step.kind==='choice')step.options.forEach((_:string,i:number)=>assert.equal(validateResponse(step.kind,step.answer,String(i)),i===step.answer));
    assert.doesNotMatch(JSON.stringify(step),/[\u2013\u2014]/);
   });
  }
  const paths=story.id==='owl'?['scene.png','backgrounds/courtyard.webp','backgrounds/library.webp','backgrounds/theatre.webp']:story.id==='forest'?['depot','clearing','workshop','pavilions'].map(id=>`backgrounds/forest-${id}.jpg`):[0,1,2,3].map(i=>`backgrounds/${story.id}-${i}.jpg`);
  for(const path of paths)assert.ok(existsSync(new URL(`../public/${path}`,import.meta.url)),path);
 }
});
