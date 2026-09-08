// Temporary adapter while cases are migrated individually to reviewed content.
import type { RevisedStory, RevisedStep } from './RevisionCase';
import forest from './forest.json';
import { stories } from './stories';
import { languages } from './i18n';
export function legacyStory(id: string): RevisedStory {
 const original=stories.find(story=>story.id===id);
 if(original)return {id,number:original.number,locales:Object.fromEntries(languages.map(({id:lang})=>{
  const t=original.locales[lang];return [lang,{...t,steps:t.steps.map((step,i)=>({title:step.title,situation:step.text,evidence:[],question:'',kind:'choice',options:step.options,answer:step.answer,explanation:step.explanation,outcome:step.explanation,next:forest[lang][5],hints:step.hints,scene:i}))}];
 })) as unknown as RevisedStory['locales']};
 return {id:'forest',number:'002',locales:Object.fromEntries(languages.map(({id:lang})=>{
  const t=forest[lang];return [lang,{title:t[0],intro:t[9],ending:t[27],question:t[28],steps:[0,1,2,3].map(i=>({title:t[10+i*4],situation:t[11+i*4],evidence:[],question:i===2?t[20]:'',kind:i===2?'time':'choice',options:i===2?[]:t[12+i*4].split('|'),answer:i===2?'18:15':1,explanation:t[13+i*4],outcome:t[13+i*4],next:t[5],hints:[t[13+i*4]],scene:i} as RevisedStep))}];
 })) as unknown as RevisedStory['locales']};
}
