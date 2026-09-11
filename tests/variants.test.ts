import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import type { RevisedStep, RevisedStory } from '../app/RevisionCase';
import type { Language } from '../app/i18n';
import { validateResponse } from '../app/revision-game.ts';
import { pickVariant, render, renderStep, renderText } from '../app/variants.ts';
await test('render fills placeholders, formats decimals per language and picks plural forms',()=>{
 assert.equal(render('{a} и {b|минута|минуты|минут}',{a:'x',b:4},'ru'),'x и 4 минуты');
 assert.equal(render('{b|минута|минуты|минут}',{b:11},'ru'),'11 минут');
 assert.equal(render('{b|минута|минуты|минут}',{b:21},'uk'),'21 минута');
 assert.equal(render('{b|minuta|minuty|minut}',{b:5},'pl'),'5 minut');
 assert.equal(render('{b|minute|minutes}',{b:1},'en'),'1 minute');
 assert.equal(render('{d} cm',{d:4.5},'en'),'4.5 cm');
 assert.equal(render('{d} см',{d:4.5},'ru'),'4,5 см');
 assert.equal(render('{missing}',{},'ru'),'{missing}');
 assert.equal(render('блок {i#А|Б|В}',{i:1},'ru'),'блок Б');
 assert.equal(render('{i#one|two} and {n|minute|minutes}',{i:0,n:2},'en'),'one and 2 minutes');
});
await test('pickVariant prefers rounds that are not solved yet',()=>{
 assert.equal(pickVariant(4,[0,1,3],()=>0.99),2);
 assert.equal(pickVariant(4,[0,1,2,3],()=>0),0);
 assert.equal(pickVariant(0,[],()=>0),0);
});
await test('every round of every case renders completely and validates in every language',()=>{
 const root=new URL('../app/revised/',import.meta.url);
 for(const file of readdirSync(root).filter(name=>name.endsWith('.json'))){
  const story=JSON.parse(readFileSync(new URL(file,root),'utf8')) as RevisedStory;
  const variants=story.variants??[];
  if(!variants.length)continue;
  assert.equal(variants.length,4,`${file}: four rounds`);
  assert.equal(new Set(variants.map(v=>JSON.stringify(v.answers))).size,4,`${file}: rounds must differ`);
  for(const lang of ['ru','pl','en','uk'] as Language[]){
   const content=story.locales[lang];
   variants.forEach((variant,v)=>{
    const where=`${file}/${lang}/round${v}`;
    for(const text of [content.intro,content.ending,content.question])assert.doesNotMatch(renderText(text,variant,lang),/[{}]/,`${where}: unresolved placeholder`);
    content.steps.forEach((raw:RevisedStep,index:number)=>{
     const step=renderStep(raw,variant,index,lang);
     const texts=[step.title,step.situation,step.question,step.explanation,step.outcome,step.next,...step.evidence,...step.options,...step.hints,...(step.feedback??[])];
     for(const text of texts)assert.doesNotMatch(text,/[{}]/,`${where}/${index}: unresolved placeholder in ${text.slice(0,50)}`);
     const response=Array.isArray(step.answer)?step.answer:String(step.answer);
     assert.ok(validateResponse(step.kind,step.answer,response),`${where}/${index}: answer must validate`);
     if(step.kind==='choice'){
      assert.ok(typeof step.answer==='number'&&step.answer>=0&&step.answer<step.options.length);
      step.options.forEach((_,i)=>assert.equal(Boolean(step.feedback?.[i]?.trim()),i!==step.answer,`${where}/${index}/feedback/${i}`));
      assert.equal(new Set(step.options).size,step.options.length,`${where}/${index}: duplicate options`);
     }
     if(step.kind==='multi')assert.ok(Array.isArray(step.answer)&&step.answer.length>0&&step.answer.length<step.options.length);
     if(step.kind==='order')assert.deepEqual([...step.answer as number[]].sort((a,b)=>a-b),step.options.map((_,i)=>i));
     if(step.kind==='time'||step.kind==='number')for(const hint of step.hints)assert.ok(!hint.includes(String(step.answer)),`${where}/${index}: hint reveals answer`);
    });
   });
  }
 }
});
