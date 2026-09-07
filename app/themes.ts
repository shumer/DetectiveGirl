/** Scene colours belong to the story, not the chosen UI language. */
export const owlScenes = {
  corridor: { image: 'scene.png', background: '#0c1c25', surface: '#142c37', raised: '#213d49', border: '#567481', accent: '#f9c653' },
  courtyard: { image: 'backgrounds/courtyard.webp', background: '#0a211f', surface: '#13352f', raised: '#214a3f', border: '#537f72', accent: '#c9e6a2' },
  library: { image: 'backgrounds/library.webp', background: '#191b30', surface: '#292940', raised: '#3b3750', border: '#77718a', accent: '#e9c988' },
  theatre: { image: 'backgrounds/theatre.webp', background: '#28141e', surface: '#3c222e', raised: '#52323f', border: '#886373', accent: '#f5c477' },
} as const;
export function owlScene(started: boolean, step: number, done: boolean) {
  if (done) return owlScenes.theatre;
  if (!started || step === 0) return owlScenes.corridor;
  if (step === 1) return owlScenes.courtyard;
  return owlScenes.library;
}
