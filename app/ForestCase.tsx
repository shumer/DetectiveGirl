import { useEffect, useRef, useState } from 'react';
import type { Language } from './i18n';
import copy from './forest.json';
import { forestCorrect } from './forest-game';
export default function ForestCase({ language, exit }: { language: Language; exit: () => void }) {
  const t = copy[language];
  const [step, setStep] = useState(-1);
  const [answer, setAnswer] = useState('');
  const [solved, setSolved] = useState(false);
  const [hint, setHint] = useState(false);
  const [error, setError] = useState(false);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { heading.current?.focus(); }, [step]);
  const offset = 10 + step * 4;
  function check(value: string) { setAnswer(value); const correct = forestCorrect(step, value); setSolved(correct); setError(!correct); }
  return <div className="forest-case">
    <div className="forest-art" aria-hidden="true"><span>✦</span><i className="tree one"/><i className="tree two"/><i className="tree three"/><div className="mushroom m1">✦</div><div className="mushroom m2">✦</div><div className="mushroom m3">✦</div></div>
    <section className="puzzle">
      <p className="eyebrow">002 · {t[0]} · {step >= 0 ? `${Math.min(step + 1, 4)} / 4` : t[30]}</p>
      <h1 ref={heading} tabIndex={-1}>{step < 0 ? t[0] : step === 4 ? t[26] : t[offset]}</h1>
      {step < 0 ? <><p>{t[9]}</p><button className="primary" onClick={() => setStep(0)}>{t[3]}</button></> : step === 4 ? <><p>{t[27]}</p><blockquote>{t[28]}</blockquote></> : <>
        <p>{t[offset + 1]}</p>
        {step === 2 ? <form onSubmit={event => { event.preventDefault(); check(answer); }}><label htmlFor="forest-time">{t[20]}</label><input id="forest-time" className="time-input" inputMode="numeric" placeholder="18:05" value={answer} disabled={solved} onChange={event => { const n=event.target.value.replace(/\D/g,'').slice(0,4); setAnswer(n.length > 2 ? `${n.slice(0,2)}:${n.slice(2)}` : n); setError(false); }} />{!solved && <button className="primary">{t[4]}</button>}</form> : <div>{t[offset + 2].split('|').map((option,index) => <button className="answer" key={option} disabled={solved} onClick={() => check(String(index))}>{option}</button>)}</div>}
        <div aria-live="polite">{error && <p className="feedback">{t[7]}</p>}{solved && <div className="success"><p>{t[offset + 3]}</p><button className="primary" onClick={() => { setStep(step + 1); setSolved(false); setAnswer(''); setHint(false); setError(false); }}>{t[5]}</button></div>}</div>
        {!solved && <div className="hint-box"><button className="text-button" onClick={() => setHint(true)} disabled={hint}>{t[6]}</button>{hint && <p>{t[offset + 3]}</p>}</div>}
      </>}
      {step > 0 && <aside className="notebook"><h2>{t[29]}</h2>{[0,1,2,3].slice(0,step).map(i => <p className="clue" key={i}>{t[13+i*4]}</p>)}</aside>}
      <button className="text-button" onClick={exit}>{t[8]}</button>
    </section>
  </div>;
}
