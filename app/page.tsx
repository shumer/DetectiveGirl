import { useEffect, useState, type CSSProperties } from 'react';
import { Languages, Search } from 'lucide-react';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { isLanguage, languages, translations, type Language } from './i18n';
import MusicPlayer from './MusicPlayer';
import RevisionCase from './RevisionCase';
import { revisedStories } from './revised-stories';
import { forestScenes, owlScenes } from './themes';
import forestCopy from './forest.json';
export default function Home(){
 const [language,setLanguage]=useState<Language>(()=>{try{const value=localStorage.getItem('detective-girl-language');return isLanguage(value)?value:'ru';}catch{return 'ru';}});
 const [caseId,setCaseId]=useState('owl'),[step,setStep]=useState(-1),[run,setRun]=useState(0);
 const story=revisedStories.find(item=>item.id===caseId)??revisedStories[0],t=translations[language];
 useEffect(()=>{document.documentElement.lang=language;document.title=`${story.locales[language].title} · DetectiveGirl`;try{localStorage.setItem('detective-girl-language',language);}catch{/* Local storage is optional. */}},[language,story]);
 function select(id:string){setCaseId(id);setStep(-1);setRun(value=>value+1);}
 const sceneIndex=step<0?0:story.locales[language].steps[Math.min(step,3)].scene;
 const owlList=[owlScenes.corridor,owlScenes.courtyard,owlScenes.library,owlScenes.theatre];
 const scene=story.id==='owl'?owlList[sceneIndex]:story.id==='forest'?forestScenes[sceneIndex]:{...forestScenes[sceneIndex],image:`backgrounds/${story.id}-${sceneIndex}.jpg`};
 const style={'--scene-image':`url("${new URL(`${import.meta.env.BASE_URL}${scene.image}`,document.baseURI).href}")`,'--background':scene.background,'--scene-surface':scene.surface,'--scene-raised':scene.raised,'--scene-border':scene.border,'--primary':scene.accent,'--ring':scene.accent} as CSSProperties;
 return <div className="world" style={style}><div className="scene-backdrop" aria-hidden="true"/><div className="shell"><header><button className="brand" aria-label={t.brand.join(' ')} onClick={()=>select('owl')}><Search size={23}/><span>{t.brand[0]}<b>{t.brand[1]}</b></span></button><span className="case-id">{t.case} {story.number} <span className="live-dot"/></span></header><MusicPlayer labels={t.music}/><main className={step<0?'start-wrap':'game'}><div className="language-picker"><span id="language-label"><Languages size={18}/>{t.language}</span><RadioGroup value={language} onValueChange={value=>{if(isLanguage(value))setLanguage(value);}} aria-labelledby="language-label" className="language-options">{languages.map(item=><label key={item.id} lang={item.id} className={item.id===language?'language-option chosen':'language-option'}><RadioGroupItem value={item.id} aria-label={item.name}/><span>{item.name}</span></label>)}</RadioGroup></div>{step<0&&<nav className="case-picker" aria-label={forestCopy[language][1]}>{revisedStories.map(item=><button key={item.id} className={item.id===story.id?'primary':'secondary'} aria-current={item.id===story.id?'page':undefined} onClick={()=>select(item.id)}>{item.number} · {item.locales[language].title}</button>)}</nav>}<RevisionCase key={`${story.id}-${run}`} story={story} language={language} step={step} setStep={setStep} exit={()=>select(story.id)}/></main><footer><span>{t.brand.join(' ')}</span><span>{t.footer}</span></footer></div></div>;
}
