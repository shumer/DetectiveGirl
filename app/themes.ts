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

export const forestScenes = [
 { image: 'backgrounds/forest-depot.jpg', background: '#0c2423', surface: '#163732', raised: '#254a3e', border: '#638779', accent: '#dfd48f' },
 { image: 'backgrounds/forest-clearing.jpg', background: '#111e35', surface: '#1c3047', raised: '#2b435b', border: '#71879e', accent: '#ecd18d' },
 { image: 'backgrounds/forest-workshop.jpg', background: '#291b15', surface: '#3a2c22', raised: '#503e2b', border: '#978369', accent: '#f4c37a' },
 { image: 'backgrounds/forest-pavilions.jpg', background: '#1e1b35', surface: '#302b46', raised: '#443b57', border: '#898098', accent: '#f1cc84' },
];
export function forestScene(step: number) {
 return forestScenes[Math.max(0, Math.min(step, 3))];
}
