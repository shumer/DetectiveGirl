import { useEffect, useRef, useState } from 'react';
import { ArrowRight, Check, Fingerprint, Lightbulb, MapPin, NotebookPen, Search, Sparkles } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { translations, type Language } from './i18n';
import type { Story } from './stories';
import forestCopy from './forest.json';
export default function StoryCase({ story, language, step, setStep, exit }: { story: Story; language: Language; step: number; setStep: (value: number) => void; exit: () => void }) {
  const t = story.locales[language];
  const shared = translations[language];
  const buttons = forestCopy[language];
  const [solved, setSolved] = useState(false);
  const [hint, setHint] = useState(0);
  const [wrong, setWrong] = useState(false);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { heading.current?.focus({ preventScroll: true }); }, [step]);
  const done = step === t.steps.length;
  const task = t.steps[step];
  const advance = () => { setSolved(false); setWrong(false); setHint(0); setStep(step + 1); };
  if (step < 0) return <div className="start forest-start">
    <section className="cover forest-cover"><div className="cover-shade"/><div className="cover-label"><Fingerprint size={19}/>{shared.secret}</div><div className="cover-title"><span className="eyebrow">{shared.case} {story.number}</span><h1 ref={heading} tabIndex={-1}>{t.title}</h1><p>{buttons[30]}</p></div><div className="case-stamp">{shared.unsolved}</div></section>
    <section className="brief"><span className="eyebrow">{shared.case} {story.number}</span><h2>{shared.greeting}</h2><p>{t.intro}</p><div className="mission"><Search/><div><strong>{shared.motto}</strong><p>{buttons[30]}</p></div></div><button className="primary" onClick={() => setStep(0)}>{shared.start}<ArrowRight size={20}/></button><p className="quiet">{shared.calm}</p><button className="text-button" onClick={exit}>{buttons[8]}</button></section>
  </div>;
  return <div className="forest-case">
    <div className="game-top"><span className="eyebrow">{done ? shared.closed : t.title}</span><span>{Math.min(step+1,4)} / 4</span></div><Progress value={done ? 100 : step*25} aria-label={shared.progress}/>
    <div className="scene-window forest-window" aria-hidden="true"/>
    <div className="game-grid"><section className="puzzle"><div className="location"><span>{done ? <Sparkles/> : <MapPin/>}</span>{shared.case} {story.number} / {done ? shared.closed : task.title}</div><h1 ref={heading} tabIndex={-1}>{done ? shared.end.solved : task.title}</h1>
      {done ? <><div className="finish-badge"><Check size={38}/><span>{shared.case} {story.number}<br/><strong>{shared.end.solved}</strong></span></div><p>{t.ending}</p><blockquote>{t.question}</blockquote></> : <>
        <p className="story-task-text">{task.text}</p><div className="story-options">{task.options.map((option,index)=><button className="answer" key={index} disabled={solved} onClick={()=>{ const correct = index === task.answer; setSolved(correct); setWrong(!correct); }}><span className="option-index" aria-hidden="true">{index+1}</span><span>{option}</span></button>)}</div>
        <div aria-live="polite">{wrong && <p className="feedback">{buttons[7]}</p>}{solved && <div className="success"><strong><Check size={19}/>{{ ru: '\u0412\u0435\u0440\u043d\u043e!', pl: 'Dobrze!', en: 'Correct!', uk: '\u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e!' }[language]}</strong><p>{task.explanation}</p><button className="primary" onClick={advance}>{buttons[5]}<ArrowRight size={18}/></button></div>}</div>
        {!solved && <div className="hint-box"><button className="text-button" disabled={hint === task.hints.length} onClick={()=>setHint(hint+1)}><Lightbulb size={19}/>{hint ? shared.moreHint : shared.hint}<span>{hint}/{task.hints.length}</span></button>{hint > 0 && <p aria-live="polite">{task.hints[hint-1]}</p>}</div>}
      </>}
      <button className="text-button" onClick={exit}>{buttons[8]}</button>
    </section><aside className="notebook"><span className="eyebrow"><NotebookPen size={16}/>{buttons[29]}</span><h2>{shared.notebookTitle}</h2>{step === 0 && !solved && <p className="quiet">{t.intro}</p>}{t.steps.slice(0,done ? 4 : step+(solved ? 1 : 0)).map((item,index)=><div className="clue" key={index}><span>{shared.clue} 0{index+1}</span><p>{item.explanation}</p></div>)}<div className="partner"><Lightbulb size={20}/><p>{shared.partner}</p></div></aside></div>
  </div>;
}
