import type { RevisedStory } from './RevisionCase';
import { legacyStory } from './legacy-stories';
import owl from './revised/owl.json';
import forest from './revised/forest.json';
import cloud from './revised/cloud.json';
export const revisedStories: RevisedStory[] = [owl as RevisedStory,forest as RevisedStory,cloud as RevisedStory,legacyStory('museum')];
