export enum UnitClass {
  Infantry = 'infantry',
  Artillery = 'artillery',
  Air = 'air'
}

export enum TechnologyTier {
  I = 1,
  II = 2,
  III = 3
}

export type FactionId = 'alpha' | 'omega';

export interface UnitBlueprint {
  id: string;
  name: string;
  unitClass: UnitClass;
  tier: TechnologyTier;
  health: number;
  damage: number;
  speed: number;
  buildTime: number;
  cost: number;
  counterMultipliers: Partial<Record<UnitClass, number>>;
}

export interface BuildingBlueprint {
  id: string;
  name: string;
  tierRequired: TechnologyTier;
  unlocksUnits?: string[];
  providesShield?: boolean;
  buildTime: number;
  cost: number;
}

export interface UnitInstance {
  id: string;
  blueprint: UnitBlueprint;
  owner: FactionId;
  lane: number;
  position: number;
  health: number;
}

export interface BuildQueueItem {
  blueprint: UnitBlueprint | BuildingBlueprint;
  progress: number;
}

export interface ResourceState {
  credits: number;
  incomePerMinute: number;
}

export interface CombatResult {
  attacker: UnitInstance;
  defender: UnitInstance;
  damageDealt: number;
  defenderRemaining: number;
}
