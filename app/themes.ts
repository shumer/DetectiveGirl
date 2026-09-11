/** Scene colours belong to the story, not the chosen UI language. */
export type Scene = { image: string; background: string; surface: string; raised: string; border: string; accent: string };
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
export const forestScenes: Scene[] = [
 { image: 'backgrounds/forest-depot.jpg', background: '#0c2423', surface: '#163732', raised: '#254a3e', border: '#638779', accent: '#dfd48f' },
 { image: 'backgrounds/forest-clearing.jpg', background: '#111e35', surface: '#1c3047', raised: '#2b435b', border: '#71879e', accent: '#ecd18d' },
 { image: 'backgrounds/forest-workshop.jpg', background: '#291b15', surface: '#3a2c22', raised: '#503e2b', border: '#978369', accent: '#f4c37a' },
 { image: 'backgrounds/forest-pavilions.jpg', background: '#1e1b35', surface: '#302b46', raised: '#443b57', border: '#898098', accent: '#f1cc84' },
];
export function forestScene(step: number) {
 return forestScenes[Math.max(0, Math.min(step, 3))];
}
/** Four scenes per story: one palette per location, images generated for the case. */
function palette(id: string, ext: string, colours: [string, string, string, string, string][]): Scene[] {
 return colours.map(([background, surface, raised, border, accent], i) => ({ image: `backgrounds/${id}-${i}.${ext}`, background, surface, raised, border, accent }));
}
export const storyScenes: Record<string, Scene[]> = {
 owl: [owlScenes.corridor, owlScenes.courtyard, owlScenes.library, owlScenes.theatre],
 forest: forestScenes,
 cloud: forestScenes.map((scene, i) => ({ ...scene, image: `backgrounds/cloud-${i}.jpg` })),
 museum: forestScenes.map((scene, i) => ({ ...scene, image: `backgrounds/museum-${i}.jpg` })),
 greenhouse: palette('greenhouse', 'jpg', [['#0b1a2e','#14273f','#1f3a55','#5f7f9c','#7fe3d1'],['#0d2233','#173245','#224559','#5f8496','#9fe8c4'],['#101a30','#1a2843','#273a58','#63769a','#8ed7ff'],['#0e1f2a','#183040','#244455','#5d8090','#b8f0a8']]),
 theatre: palette('theatre', 'jpg', [['#2a0f16','#3d1a24','#552735','#8f5f6c','#f2c66b'],['#1d1224','#2c1b36','#3f2a4c','#7a6386','#f0c47a'],['#31121a','#452029','#5c2f3c','#966a78','#ffd27f'],['#241014','#37191f','#4b262d','#87626a','#f4cf85']]),
 aquarium: palette('aquarium', 'jpg', [['#061c2e','#0d2b42','#153d58','#4f7f9a','#ff9f7a'],['#07222f','#0f3344','#17475a','#4f8496','#7fe6e0'],['#0a1a33','#132a4a','#1c3d62','#5677a0','#ffc07a'],['#052430','#0c3644','#164a5a','#4d8a99','#8ef0d6']]),
 bakery: palette('bakery', 'jpg', [['#2a1a10','#3d281a','#523825','#957a5e','#f4c56a'],['#241b14','#372a20','#4b3a2c','#8d7a68','#ffd58a'],['#2b1c12','#402b1d','#563c2a','#9a7f66','#f7cf7a'],['#1f1610','#32241a','#463326','#87715c','#ffe08f']]),
 lighthouse: palette('lighthouse', 'jpg', [['#071528','#0f2340','#183356','#4f6c94','#ffe27a'],['#0a1a30','#132a48','#1d3c60','#557398','#9fd8ff'],['#0b1730','#152646','#20385f','#5a7299','#ffd76a'],['#081a2c','#112b44','#1a3d5b','#4f7392','#fff0a0']]),
 library: palette('library', 'jpg', [['#1d1226','#2d1d3a','#3f2c4e','#7a6688','#e9c27a'],['#211525','#332338','#48344d','#84708a','#f0cd86'],['#1a1420','#2a2132','#3c3146','#75697f','#e6c58c'],['#231628','#36243c','#4a3450','#8a7290','#f3d38f']]),
 park: palette('park', 'jpg', [['#0c2418','#163726','#224b35','#5f8c72','#ffd866'],['#0f2a2c','#183f40','#245455','#5e8f90','#9fe0ff'],['#122413','#1d3820','#2a4c2d','#6a8f6c','#ffe27a'],['#0e1f2d','#183143','#224458','#5d7f94','#ffd76e']]),
};
/** Background music per case: Kevin MacLeod tracks under CC BY, see MUSIC-LICENSE.md. */
export type Track = { file: string; title: string; url: string };
const km = (file: string, title: string, search = title): Track => ({ file, title, url: `https://incompetech.com/music/royalty-free/index.html?keywords=${encodeURIComponent(search)}` });
export const defaultTrack: Track = { file: 'audio/sneaky-snitch.mp3', title: 'Sneaky Snitch', url: 'https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100772' };
export const storyMusic: Record<string, Track> = {
 owl: defaultTrack,
 forest: km('audio/fairytale-waltz.m4a', 'Fairytale Waltz'),
 cloud: km('audio/airship-serenity.m4a', 'Airship Serenity'),
 museum: km('audio/investigations.m4a', 'Investigations'),
 greenhouse: km('audio/dreamer.m4a', 'Dreamer'),
 theatre: km('audio/bushwick-tarantella.m4a', 'Bushwick Tarantella'),
 aquarium: km('audio/water-prelude.m4a', 'Water Prelude'),
 bakery: km('audio/cheery-monday.m4a', 'Cheery Monday'),
 lighthouse: km('audio/moonlight-hall.m4a', 'Moonlight Hall'),
 library: km('audio/thinking-music.m4a', 'Thinking Music'),
 park: km('audio/pixel-peeker-polka.m4a', 'Pixel Peeker Polka (faster)', 'Pixel Peeker Polka'),
};
