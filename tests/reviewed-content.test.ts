import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import type { RevisedStep } from '../app/RevisionCase';
import { validateResponse } from '../app/revision-game.ts';
import { storyScenes, storyMusic } from '../app/themes.ts';
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
    const where=`${file}/${lang}/${index}`;
    for(const field of ['title','situation','question','explanation','outcome','next'] as const)assert.ok(step[field]?.trim(),`${where}/${field}`);
    assert.ok(step.evidence.length>0 && step.evidence.every((fact:string)=>fact.trim()));
    assert.equal(step.hints.length,3);assert.ok(step.hints.every((hint:string)=>hint.trim()));
    for(const field of ['kind','answer','scene'] as const)assert.deepEqual(step[field],original[field],`${where}/${field}`);
    assert.equal(step.options.length,original.options.length,`${where}/options`);
    assert.ok(Number.isInteger(step.scene)&&step.scene>=0&&step.scene<=3);
    const response=Array.isArray(step.answer)?step.answer:String(step.answer);
    assert.ok(validateResponse(step.kind,step.answer,response),`${where}: answer must validate`);
    assert.equal(validateResponse(step.kind,step.answer,''),false);
    if(step.kind==='choice'){
     assert.ok(step.options.length>=4,`${where}: choice needs at least four options`);
     assert.ok(typeof step.answer==='number'&&step.answer>=0&&step.answer<step.options.length);
     assert.equal(step.feedback?.length,step.options.length,`${where}: feedback per option`);
     step.options.forEach((_:string,i:number)=>{assert.equal(validateResponse('choice',step.answer,String(i)),i===step.answer);assert.equal(Boolean(step.feedback?.[i]?.trim()),i!==step.answer,`${where}/feedback/${i}`);});
    }
    if(step.kind==='multi'){assert.ok(Array.isArray(step.answer)&&step.answer.length>0&&step.answer.length<step.options.length);assert.ok((step.answer as number[]).every(i=>Number.isInteger(i)&&i>=0&&i<step.options.length));}
    if(step.kind==='order'){assert.ok(Array.isArray(step.answer));assert.equal(step.answer.length,step.options.length);assert.deepEqual([...step.answer as number[]].sort((a,b)=>a-b),step.options.map((_:string,i:number)=>i));}
    if(step.kind==='time'||step.kind==='number'){for(const hint of step.hints)assert.ok(!hint.includes(String(step.answer)),`${where}: hint reveals the answer`);}
    assert.doesNotMatch(JSON.stringify(step),/[–—]/);
   });
  }
  const scenes=storyScenes[story.id];
  assert.ok(scenes&&scenes.length===4,`${file}: four scenes in themes.ts`);
  for(const scene of scenes)assert.ok(existsSync(new URL(`../public/${scene.image}`,import.meta.url)),scene.image);
  const track=storyMusic[story.id];
  assert.ok(track,`${file}: music track in themes.ts`);
  assert.ok(existsSync(new URL(`../public/${track.file}`,import.meta.url)),track.file);
  assert.ok(readFileSync(new URL('../MUSIC-LICENSE.md',import.meta.url),'utf8').includes(track.file.replace('audio/','')),`${track.file} listed in MUSIC-LICENSE.md`);
 }
});
