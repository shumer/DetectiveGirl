import { useState, useRef, useEffect, type CSSProperties } from 'react';
import { Search, ArrowRight, Lightbulb, Check, Camera, Clock3, NotebookPen, Fingerprint, RotateCcw, Sparkles, ChevronLeft, Languages } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { languages, translations, isLanguage, type Language } from './i18n';
import { cameraRecords, correctInterval, correctTime, correctOrder, correctPerson, correctReason } from './game';

import MusicPlayer from './MusicPlayer';
import { owlScene } from './themes';

export default function Home() {
  const [language, setLanguage] = useState<Language>(() => {
    try { const saved = localStorage.getItem('detective-girl-language'); return isLanguage(saved) ? saved : 'ru'; }
    catch { return 'ru'; }
  });
  const t = translations[language];
  const [started, setStarted] = useState(false);
  const [step, setStep] = useState(0);
  const [done, setDone] = useState(false);
  const [solved, setSolved] = useState(false);
  const [code, setCode] = useState('');
  const [time, setTime] = useState('');
  const [order, setOrder] = useState<number[]>([]);
  const [hint, setHint] = useState(0);
  const [error, setError] = useState<string>('');
  const [usedHints, setUsedHints] = useState(false);
  const [reason, setReason] = useState(false);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(() => { document.documentElement.lang = language; document.title = `${t.title.join(' ')} · DetectiveGirl`; try { localStorage.setItem('detective-girl-language', language); } catch { /* Play remains available when storage is blocked. */ } }, [language, t]);
  useEffect(() => { if (started) heading.current?.focus(); }, [started, step, done]);
  function ok() { setSolved(true); setError(''); }
  function next() { setStep(step + 1); setSolved(false); setHint(0); setError(''); }
  function reset() { setStarted(false); setStep(0); setDone(false); setSolved(false); setCode(''); setTime(''); setOrder([]); setHint(0); setError(''); setUsedHints(false); setReason(false); }
  const messages: Record<string, string> = {
    short: t.lock.short, code: t.lock.wrong, time: t.time.wrong, order: t.note.wrong,
    mira: t.deduction.wrongPeople[0], lev: t.deduction.wrongPeople[1],
    place: t.deduction.wrongReasons[0], guess: t.deduction.wrongReasons[1],
  };
  function languagePicker() {
    return <div className="language-picker"><span id="language-label"><Languages size={18} />{t.language}</span>
      <RadioGroup value={language} onValueChange={value => { if (isLanguage(value)) setLanguage(value); }} aria-labelledby="language-label" className="language-options">
        {languages.map(l => <label key={l.id} lang={l.id} className={language === l.id ? 'language-option chosen' : 'language-option'}><RadioGroupItem value={l.id} aria-label={l.name} /><span>{l.name}</span></label>)}
      </RadioGroup></div>;
  }
  const scene = owlScene(started, step, done);
  const worldStyle = {
    '--scene-image': `url("${new URL(`${import.meta.env.BASE_URL}${scene.image}`, document.baseURI).href}")`,
    '--background': scene.background, '--scene-surface': scene.surface,
    '--scene-raised': scene.raised, '--scene-border': scene.border,
    '--primary': scene.accent, '--ring': scene.accent,
  } as CSSProperties;
  return <div className="world" style={worldStyle}><div className="scene-backdrop" aria-hidden="true" /><div className="shell">
    <header><button onClick={reset} className="brand" aria-label={t.brand.join(' ')}><Search size={23} /><span>{t.brand[0]}<b>{t.brand[1]}</b></span></button><span className="case-id">{t.case} 001 <span className="live-dot" /></span></header>
    <MusicPlayer labels={t.music} />
    {!started ? <main className="start-wrap">{languagePicker()}<div className="start">
      <section className="cover" style={{ backgroundImage: `url(${import.meta.env.BASE_URL}scene.png)` }}><div className="cover-shade" /><div className="cover-label"><Fingerprint size={19} />{t.secret}</div><div className="cover-title"><span className="eyebrow">{t.school}</span><h1>{t.title[0]}<br /><em>{t.title[1]}</em></h1><p>{t.subtitle}</p></div><div className="case-stamp">{t.unsolved}</div></section>
      <section className="brief"><span className="eyebrow">{t.first}</span><h2>{t.greeting}</h2><p>{t.intro}</p><div className="mission"><Search /><div><strong>{t.motto}</strong><p>{t.duration}</p></div></div><button className="primary" onClick={() => setStarted(true)}>{t.start}<ArrowRight size={20} /></button><p className="quiet">{t.calm}</p></section>
    </div></main> : <main className="game">{languagePicker()}<div className="game-top"><span className="eyebrow">{done ? t.closed : t.caseTitle}</span><span>{done ? '4 / 4' : `${step + 1} / 4`}</span></div><Progress value={done ? 100 : step * 25} aria-label={t.progress} />
      <div className="scene-window" aria-hidden="true" /><div className="game-grid"><section className="puzzle" key={done ? 'end' : step}>
        <div className="location"><span>{done ? <Sparkles /> : [<Camera key="lock" />, <Clock3 key="clock" />, <NotebookPen key="note" />, <Fingerprint key="print" />][step]}</span>{done ? t.end.location : t.locations[step]}</div><h1 ref={heading} tabIndex={-1}>{done ? t.end.title : t.titles[step]}</h1>
        {done ? <>
          <div className="finish-badge"><Check size={38} /><span>{t.case} 001<br /><strong>{t.end.solved}</strong></span></div><p>{t.end.intro}</p><blockquote>{t.end.quote}</blockquote><p>{t.end.summary}</p><div className="success"><strong>{t.end.rank}</strong><p>{usedHints ? t.end.helped : t.end.solo}</p></div><p className="quiet">{t.end.question}</p><button className="secondary" onClick={reset}><RotateCcw size={18} />{t.end.restart}</button>
        </> : <>
          {step === 0 && <><p>{t.lock.intro}</p><div className="paper"><span className="paper-label">{t.lock.label}</span><ul>{t.lock.rules.map(rule => <li key={rule}>{rule}</li>)}</ul></div><form onSubmit={event => { event.preventDefault(); if (!solved) { if (correctInterval(code)) ok(); else setError(code.length < 2 ? 'short' : 'code'); } }}><label htmlFor="code">{t.lock.input}</label><input id="code" className="time-input" value={code} onChange={event => { setCode(event.target.value.replace(/\D/g, '').slice(0, 2)); setError(''); }} disabled={solved} inputMode="numeric" enterKeyHint="done" maxLength={2} autoComplete="off" />{!solved && <button className="primary" type="submit">{t.lock.submit}<Camera size={18} /></button>}</form></>}
          {step === 1 && <><p>{t.time.intro}</p><blockquote>{t.time.quote}</blockquote><form onSubmit={event => { event.preventDefault(); if (!solved) { if (correctTime(time)) ok(); else setError('time'); } }}><label htmlFor="time">{t.time.input}</label><input id="time" className="time-input" inputMode="numeric" enterKeyHint="done" placeholder={t.time.placeholder} value={time} onChange={event => { const digits = event.target.value.replace(/\D/g, '').slice(0, 4); setTime(digits.length > 2 ? `${digits.slice(0, 2)}:${digits.slice(2)}` : digits); setError(''); }} disabled={solved} maxLength={5} autoComplete="off" />{!solved && <button className="primary" type="submit">{t.time.submit}<ArrowRight size={18} /></button>}</form></>}
          {step === 2 && <><p>{t.note.intro}</p><div className="assembled route-order" aria-live="polite">{[0, 1, 2].map((_, position) => <span key={position} className={order[position] !== undefined ? 'filled' : ''}>{order[position] !== undefined ? t.note.pieces[order[position]] : position + 1}</span>)}</div><div className="pieces route-records">{cameraRecords.map(piece => <button key={piece.id} disabled={solved || order.includes(piece.id)} onClick={() => { setOrder([...order, piece.id]); setError(''); }} aria-label={`${t.note.add} ${t.note.pieces[piece.id]}: ${t.note.records[piece.id]}`}><strong>{t.note.pieces[piece.id]}</strong><span>{t.note.records[piece.id]}</span></button>)}</div>{!solved && <><div className="row"><button className="text-button" disabled={!order.length} onClick={() => { setOrder(order.slice(0, -1)); setError(''); }}><ChevronLeft size={16} />{t.note.undo}</button><button className="text-button" disabled={!order.length} onClick={() => { setOrder([]); setError(''); }}>{t.note.clear}</button></div><button className="primary" disabled={order.length !== 3} onClick={() => correctOrder(order) ? ok() : setError('order')}>{t.note.submit}<ArrowRight size={18} /></button></>}</>}
          {step === 3 && <><p>{t.deduction.intro}</p><div className="suspects">{t.deduction.people.map((person, id) => <button className="suspect" key={id} disabled={reason || solved} onClick={() => { if (correctPerson(id)) { setReason(true); setError(''); } else setError(id === 0 ? 'mira' : 'lev'); }}><span className={`badge-dot ${id === 1 ? 'blue' : 'yellow'}`} /><strong>{person}</strong><span>{t.deduction.badges[id]}</span><small>{t.deduction.notes[id]}</small></button>)}</div>{reason && !solved && <div className="reason"><strong>{t.deduction.why}</strong>{t.deduction.answers.map((answer, id) => <button key={id} className="answer" onClick={() => correctReason(id) ? ok() : setError(id === 0 ? 'place' : 'guess')}>{answer}</button>)}</div>}</>}
          <div aria-live="polite" aria-atomic="true">{error && <p className="feedback">{messages[error]}</p>}{solved && <div className="success"><strong><Check size={19} />{t.success[step]}</strong><p>{step < 3 ? t.clues[step] : t.deduction.success}</p>{step < 3 && <p className="explain">{t.explanations[step]}</p>}<button className="primary" onClick={() => step === 3 ? setDone(true) : next()}>{step === 3 ? t.find : t.nextSteps[step]}<ArrowRight size={18} /></button></div>}</div>
          {!solved && <div className="hint-box"><button className="text-button" onClick={() => { setHint(Math.min(hint + 1, 3)); setUsedHints(true); }} disabled={hint === 3}><Lightbulb size={19} />{hint === 0 ? t.hint : hint === 3 ? t.allHints : t.moreHint}<span>{hint}/3</span></button>{hint > 0 && <p aria-live="polite">{t.hints[step][hint - 1]}</p>}</div>}
        </>}
      </section><aside className="notebook"><span className="eyebrow"><NotebookPen size={16} />{t.notebook}</span><h2>{t.notebookTitle}</h2>{t.clues.slice(0, done ? 3 : step + (solved && step < 3 ? 1 : 0)).map((clue, id) => <div className="clue" key={id}><span>{t.clue} 0{id + 1}</span><p>{clue}</p></div>)}{step === 0 && !solved && <p className="quiet">{t.empty}</p>}<div className="partner"><Lightbulb size={20} /><p>{t.partner}</p></div></aside></div>
    </main>}
    <footer><span>{t.brand.join(' ')}</span><span>{t.footer}</span></footer>
  </div></div>;
}
