import { Check, Fingerprint } from 'lucide-react';
import { translations, type Language } from './i18n';
import type { RevisedStory } from './RevisionCase';
import { localeOf } from './RevisionCase';
import { storyScenes } from './themes';
import { teaser, type Progress } from './progress';
type Props = { stories: RevisedStory[]; language: Language; progress: Progress; onSelect: (id: string) => void };
export default function CaseGallery({ stories, language, progress, onSelect }: Props) {
  const t = translations[language], g = t.gallery;
  return <section className="gallery" aria-labelledby="gallery-title">
    <div className="gallery-head"><span className="eyebrow"><Fingerprint size={16} />{t.secret}</span><h1 id="gallery-title">{g.title}</h1><p>{g.subtitle}</p></div>
    <ul className="case-cards">
      {stories.map(story => {
        const locale = localeOf(story, language), scene = storyScenes[story.id]?.[0], result = progress[story.id];
        const image = scene ? new URL(`${import.meta.env.BASE_URL}${scene.image}`, document.baseURI).href : '';
        return <li key={story.id}>
          <button className={result ? 'case-card solved' : 'case-card'} style={{ '--card-accent': scene?.accent ?? 'var(--primary)' } as React.CSSProperties} onClick={() => onSelect(story.id)} aria-label={`${t.case} ${story.number}: ${locale.title}`}>
            <span className="case-card-image" style={{ backgroundImage: `url("${image}")` }} aria-hidden="true">
              <span className="case-card-number">{t.case} {story.number}</span>
              {result && <span className="case-card-check"><Check size={16} />{g.solved}</span>}
            </span>
            <span className="case-card-body">
              <strong>{locale.title}</strong>
              <span className="case-card-teaser">{teaser(locale.intro)}</span>
              <span className="case-card-foot">{result ? `${g.rounds}: ${result.variants.length} / ${story.variants?.length ?? 1}` : g.fresh}<em>{g.open}</em></span>
            </span>
          </button>
        </li>;
      })}
    </ul>
  </section>;
}
