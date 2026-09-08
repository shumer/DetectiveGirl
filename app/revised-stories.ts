import type { RevisedStory } from './RevisionCase';
import { legacyStory } from './legacy-stories';
import owl from './revised/owl.json';
import forest from './revised/forest.json';
export const revisedStories: RevisedStory[] = [owl as RevisedStory,forest as RevisedStory,legacyStory('cloud'),legacyStory('museum')];
