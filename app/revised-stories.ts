import type { RevisedStory } from './RevisionCase';
import { legacyStory } from './legacy-stories';
import owl from './revised/owl.json';
export const revisedStories: RevisedStory[] = [owl as RevisedStory,legacyStory('forest'),legacyStory('cloud'),legacyStory('museum')];
