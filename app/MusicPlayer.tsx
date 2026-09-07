import { useEffect, useRef, useState } from 'react';
import { Music2, Pause, Play, Volume2 } from 'lucide-react';
import { Field } from '@base-ui/react/field';
import { Slider } from '@/components/ui/slider';

export type MusicLabels = { play: string; pause: string; volume: string; loading: string; error: string; credit: string; waiting: string };
export default function MusicPlayer({ labels }: { labels: MusicLabels }) {
  const audio = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);
  const [enabled, setEnabled] = useState(true);
  const wanted = useRef(true);
  const [loading, setLoading] = useState(false);
  const [failed, setFailed] = useState(false);
  const [volume, setVolume] = useState(18);
  useEffect(() => {
    const player = audio.current;
    if (!player) return;
    let disposed = false;
    player.volume = 0.18;
    const start = () => {
      if (disposed || !wanted.current || document.hidden || !player.paused) return;
      void player.play().then(() => {
        if (disposed || !wanted.current || document.hidden) player.pause();
      }).catch((error: unknown) => {
        if (!disposed && error instanceof DOMException && error.name !== 'NotAllowedError' && error.name !== 'AbortError') setFailed(true);
      });
    };
    const onGesture = (event: Event) => {
      if (event.target instanceof Element && event.target.closest('.music-toggle')) return;
      start();
    };
    const onVisibility = () => { if (document.hidden) player.pause(); else start(); };
    start();
    document.addEventListener('pointerdown', onGesture);
    document.addEventListener('keydown', onGesture);
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      disposed = true;
      document.removeEventListener('pointerdown', onGesture);
      document.removeEventListener('keydown', onGesture);
      document.removeEventListener('visibilitychange', onVisibility);
      player.pause();
    };
  }, []);
  async function toggle() {
    const player = audio.current;
    if (!player) return;
    wanted.current = !wanted.current;
    setEnabled(wanted.current);
    if (!wanted.current) { player.pause(); return; }
    setLoading(true); setFailed(false);
    player.volume = volume / 100;
    try { await player.play(); if (!wanted.current || document.hidden) player.pause(); }
    catch { setFailed(true); wanted.current = false; setEnabled(false); }
    finally { setLoading(false); }
  }
  return <section className="music-player" aria-label={labels.credit}>
    {/* oxlint-disable-next-line jsx-a11y/media-has-caption -- Instrumental music only; no speech to caption. */}
    <audio ref={audio} src={`${import.meta.env.BASE_URL}audio/sneaky-snitch.mp3`} preload="auto" loop
      onPlaying={() => setPlaying(true)} onPause={() => setPlaying(false)} onError={() => { setFailed(true); setLoading(false); setPlaying(false); }} />
    <button className="music-toggle" onClick={() => { void toggle(); }} disabled={loading} aria-pressed={enabled}>
      {enabled ? <Pause size={17} /> : <Play size={17} />} {loading ? labels.loading : enabled ? labels.pause : labels.play}
    </button>
    <Field.Root className="music-volume"><Field.Label><Volume2 size={15} />{labels.volume}</Field.Label>
      <Slider value={[volume]} min={0} max={100} step={1} onValueChange={value => { const next = Array.isArray(value) ? value[0] : value; setVolume(next); if (audio.current) { audio.current.volume = next / 100; audio.current.muted = next === 0; } }} />
    </Field.Root>
    <div className="music-credit"><Music2 size={14} /><span><a href="https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100772" target="_blank" rel="noreferrer">Sneaky Snitch - Kevin MacLeod</a> · <a href="https://creativecommons.org/licenses/by/3.0/" target="_blank" rel="noreferrer">CC BY 3.0</a></span></div>
    {enabled && !playing && !loading && !failed && <output className="music-credit">{labels.waiting}</output>}
    {failed && <p className="music-error" role="alert">{labels.error}</p>}
  </section>;
}
