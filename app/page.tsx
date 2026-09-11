import { useEffect, useState, type CSSProperties } from 'react';
import { Languages, Search } from 'lucide-react';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { isLanguage, languages, translations, type Language } from './i18n';
import MusicPlayer from './MusicPlayer';
import RevisionCase from './RevisionCase';
import CaseGallery from './CaseGallery';
import { revisedStories, localeOf } from './revised-stories';
import { storyScenes, owlScenes, storyMusic, defaultTrack } from './themes';
import { readProgress, type Progress } from './progress';
export default function Home(){
 const [language,setLanguage]=useState<Language>(()=>{try{const value=localStorage.getItem('detective-girl-language');return isLanguage(value)?value:'ru';}catch{return 'ru';}});
 const [caseId,setCaseId]=useState<string|null>(null),[step,setStep]=useState(-1),[run,setRun]=useState(0),[progress,setProgress]=useState<Progress>(()=>readProgress());
 const story=caseId?revisedStories.find(item=>item.id===caseId)??null:null,t=translations[language];
 useEffect(()=>{document.documentElement.lang=language;document.title=story?`${localeOf(story,language).title} · DetectiveGirl`:`${t.brand.join(' ')} · DetectiveGirl`;try{localStorage.setItem('detective-girl-language',language);}catch{/* Local storage is optional. */}},[language,story,t]);
 function select(id:string){setCaseId(id);setStep(-1);setRun(value=>value+1);}
 function exit(){setCaseId(null);setStep(-1);setProgress(readProgress());window.scrollTo({top:0});}
 const sceneIndex=step<0?0:localeOf(story??revisedStories[0],language).steps[Math.min(step,3)].scene;
 const scene=story?(storyScenes[story.id]??storyScenes.owl)[sceneIndex]:owlScenes.corridor;
 const style={'--scene-image':`url("${new URL(`${import.meta.env.BASE_URL}${scene.image}`,document.baseURI).href}")`,'--background':scene.background,'--scene-surface':scene.surface,'--scene-raised':scene.raised,'--scene-border':scene.border,'--primary':scene.accent,'--ring':scene.accent} as CSSProperties;
 const picker=<div className="language-picker"><span id="language-label"><Languages size={18}/>{t.language}</span><RadioGroup value={language} onValueChange={value=>{if(isLanguage(value))setLanguage(value);}} aria-labelledby="language-label" className="language-options">{languages.map(item=><label key={item.id} lang={item.id} className={item.id===language?'language-option chosen':'language-option'}><RadioGroupItem value={item.id} aria-label={item.name}/><span>{item.name}</span></label>)}</RadioGroup></div>;
 return <div className="world" style={style}><div className="scene-backdrop" aria-hidden="true"/><div className="shell"><header><button className="brand" aria-label={t.brand.join(' ')} onClick={exit}><Search size={23}/><span>{t.brand[0]}<b>{t.brand[1]}</b></span></button><span className="case-id">{story?<>{t.case} {story.number} <span className="live-dot"/></>:<>{revisedStories.length} · {t.gallery.title.toLowerCase()}</>}</span></header><MusicPlayer labels={t.music} track={story?storyMusic[story.id]??defaultTrack:defaultTrack}/>
 {story?<main className={step<0?'start-wrap':'game'}>{picker}<RevisionCase key={`${story.id}-${run}`} story={story} language={language} step={step} setStep={setStep} exit={exit} onSolved={()=>setProgress(readProgress())}/></main>
 :<main className="gallery-wrap">{picker}<CaseGallery stories={revisedStories} language={language} progress={progress} onSelect={select}/></main>}
 <footer><span>{t.brand.join(' ')}</span><span>{t.footer}</span></footer></div></div>;
}
