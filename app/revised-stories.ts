import type { RevisedStory } from './RevisionCase';
import owl from './revised/owl.json';
import forest from './revised/forest.json';
import cloud from './revised/cloud.json';
import museum from './revised/museum.json';
import owlPilot from './pilot/owl.json';
export { localeOf } from './RevisionCase';
export const revisedStories: RevisedStory[] = [owlPilot as RevisedStory,owl as RevisedStory,forest as RevisedStory,cloud as RevisedStory,museum as RevisedStory];
