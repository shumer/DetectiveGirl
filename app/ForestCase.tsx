import { useEffect, useRef, useState } from 'react';
import type { Language } from './i18n';
import copy from './forest.json';
import { translations } from './i18n';
import { Progress } from '@/components/ui/progress';
import { Search, ArrowRight, NotebookPen, Lightbulb, Check, MapPin, Fingerprint, Clock3, Sparkles } from 'lucide-react';
import { forestCorrect } from './forest-game';
export default function ForestCase({ language, exit, step, setStep }: { language: Language; exit: () => void; step: number; setStep: (step: number) => void }) {
  const t = copy[language];
  const shared = translations[language];
  const [answer, setAnswer] = useState('');
  const [solved, setSolved] = useState(false);
  const [hint, setHint] = useState(false);
  const [error, setError] = useState(false);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { heading.current?.focus(); }, [step]);
  const offset = 10 + step * 4;
  function check(value: string) { setAnswer(value); const correct = forestCorrect(step, value); setSolved(correct); setError(!correct); }
  if (step < 0) return <div className="start forest-start">
    <section className="cover forest-cover"><div className="cover-shade"/><div className="cover-label"><Fingerprint size={19}/>{shared.secret}</div><div className="cover-title"><span className="eyebrow">{shared.case} 002</span><h1 ref={heading} tabIndex={-1}>{t[0]}</h1><p>{t[30]}</p></div><div className="case-stamp">{shared.unsolved}</div></section>
    <section className="brief"><span className="eyebrow">{shared.case} 002</span><h2>{shared.greeting}</h2><p>{t[9]}</p><div className="mission"><Search/><div><strong>{shared.motto}</strong><p>{t[30]}</p></div></div><button className="primary" onClick={() => setStep(0)}>{t[3]}<ArrowRight size={20}/></button><p className="quiet">{shared.calm}</p><button className="text-button" onClick={exit}>{t[8]}</button></section>
  </div>;
  return <div className="forest-case">
    <div className="game-top"><span className="eyebrow">{step === 4 ? shared.closed : t[0]}</span><span>{Math.min(step+1,4)} / 4</span></div>
    <Progress value={step === 4 ? 100 : step*25} aria-label={shared.progress}/>
    <div className="scene-window forest-window" aria-hidden="true"/>
    <div className="game-grid"><section className="puzzle">
      <div className="location"><span>{step === 4 ? <Sparkles/> : step === 2 ? <Clock3/> : <MapPin/>}</span>{t[0]} / {step === 4 ? shared.closed : t[offset]}</div>
      <h1 ref={heading} tabIndex={-1}>{step === 4 ? t[26] : t[offset]}</h1>
      {step === 4 ? <><div className="finish-badge"><Check size={38}/><span>{shared.case} 002<br/><strong>{shared.end.solved}</strong></span></div><p>{t[27]}</p><blockquote>{t[28]}</blockquote></> : <>
        <p>{t[offset + 1]}</p>
        {step === 2 ? <form onSubmit={event => { event.preventDefault(); check(answer); }}><label htmlFor="forest-time">{t[20]}</label><input id="forest-time" className="time-input" inputMode="numeric" placeholder="18:05" value={answer} disabled={solved} onChange={event => { const n=event.target.value.replace(/\D/g,'').slice(0,4); setAnswer(n.length > 2 ? `${n.slice(0,2)}:${n.slice(2)}` : n); setError(false); }} />{!solved && <button className="primary">{t[4]}</button>}</form> : <div>{t[offset + 2].split('|').map((option,index) => <button className="answer" key={option} disabled={solved} onClick={() => check(String(index))}>{option}</button>)}</div>}
        <div aria-live="polite">{error && <p className="feedback">{t[7]}</p>}{solved && <div className="success"><p>{t[offset + 3]}</p><button className="primary" onClick={() => { setStep(step + 1); setSolved(false); setAnswer(''); setHint(false); setError(false); }}>{t[5]}</button></div>}</div>
        {!solved && <div className="hint-box"><button className="text-button" onClick={() => setHint(true)} disabled={hint}>{t[6]}</button>{hint && <p>{t[offset + 3]}</p>}</div>}

      </>}
      <button className="text-button" onClick={exit}>{t[8]}</button>
    </section><aside className="notebook"><span className="eyebrow"><NotebookPen size={16}/>{t[29]}</span><h2>{shared.notebookTitle}</h2>{step === 0 && !solved && <p className="quiet">{t[9]}</p>}{[0,1,2,3].slice(0,Math.min(4,step+(solved ? 1 : 0))).map(i => <div className="clue" key={i}><span>{shared.clue} 0{i+1}</span><p>{t[13+i*4]}</p></div>)}<div className="partner"><Lightbulb size={20}/><p>{shared.partner}</p></div></aside></div>
  </div>;
}
