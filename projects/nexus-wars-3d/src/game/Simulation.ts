import { CombatSystem } from './systems/CombatSystem';
import { EconomySystem } from './systems/EconomySystem';
import { ProductionSystem } from './systems/ProductionSystem';
import { TechSystem, TechUnlock } from './systems/TechSystem';
import {
  BuildingBlueprint,
  BuildQueueItem,
  FactionId,
  TechnologyTier,
  UnitBlueprint,
  UnitClass,
  UnitInstance
} from './types';

let unitCounter = 0;

function nextUnitId() {
  unitCounter += 1;
  return `unit-${unitCounter}`;
}

const UNIT_BLUEPRINTS: Record<string, UnitBlueprint> = {
  marine: {
    id: 'marine',
    name: 'Marine Squad',
    unitClass: UnitClass.Infantry,
    tier: TechnologyTier.I,
    health: 60,
    damage: 8,
    speed: 6,
    buildTime: 6,
    cost: 55,
    counterMultipliers: { [UnitClass.Air]: 0.5, [UnitClass.Artillery]: 1.2 }
  },
  artillery: {
    id: 'artillery',
    name: 'Artillery Crawler',
    unitClass: UnitClass.Artillery,
    tier: TechnologyTier.II,
    health: 140,
    damage: 24,
    speed: 3,
    buildTime: 12,
    cost: 120,
    counterMultipliers: { [UnitClass.Infantry]: 1.6 }
  },
  interceptor: {
    id: 'interceptor',
    name: 'Interceptor Wing',
    unitClass: UnitClass.Air,
    tier: TechnologyTier.II,
    health: 85,
    damage: 18,
    speed: 10,
    buildTime: 10,
    cost: 150,
    counterMultipliers: { [UnitClass.Artillery]: 1.8 }
  },
  dreadnought: {
    id: 'dreadnought',
    name: 'Dreadnought Carrier',
    unitClass: UnitClass.Artillery,
    tier: TechnologyTier.III,
    health: 500,
    damage: 110,
    speed: 2,
    buildTime: 24,
    cost: 450,
    counterMultipliers: { [UnitClass.Infantry]: 2, [UnitClass.Air]: 1.2 }
  },
  archangel: {
    id: 'archangel',
    name: 'Archangel Squadron',
    unitClass: UnitClass.Air,
    tier: TechnologyTier.III,
    health: 320,
    damage: 84,
    speed: 9,
    buildTime: 26,
    cost: 500,
    counterMultipliers: { [UnitClass.Artillery]: 2.2 }
  }
};

const BUILDINGS: Record<string, BuildingBlueprint> = {
  barracks: {
    id: 'barracks',
    name: 'Barracks',
    tierRequired: TechnologyTier.I,
    unlocksUnits: ['marine'],
    buildTime: 8,
    cost: 120
  },
  foundry: {
    id: 'foundry',
    name: 'Foundry',
    tierRequired: TechnologyTier.II,
    unlocksUnits: ['artillery'],
    buildTime: 12,
    cost: 220
  },
  hangar: {
    id: 'hangar',
    name: 'Star Hangar',
    tierRequired: TechnologyTier.II,
    unlocksUnits: ['interceptor'],
    buildTime: 14,
    cost: 260
  },
  shield: {
    id: 'shield',
    name: 'Aegis Shield',
    tierRequired: TechnologyTier.II,
    providesShield: true,
    buildTime: 15,
    cost: 280
  },
  ion: {
    id: 'ion',
    name: 'Ion Cannon',
    tierRequired: TechnologyTier.III,
    unlocksUnits: ['dreadnought', 'archangel'],
    buildTime: 22,
    cost: 420
  }
};

const TECH_TREE: TechUnlock[] = [
  { tier: TechnologyTier.II, buildings: ['foundry', 'hangar', 'shield'], cost: 320 },
  { tier: TechnologyTier.III, buildings: ['ion'], cost: 620 }
];

function blueprintAvailable(blueprint: UnitBlueprint, built: Set<string>, tier: TechnologyTier): boolean {
  if (blueprint.tier > tier) {
    return false;
  }
  return Array.from(built).some((buildingId) => BUILDINGS[buildingId]?.unlocksUnits?.includes(blueprint.id));
}

export interface FactionState {
  id: FactionId;
  economy: EconomySystem;
  production: ProductionSystem;
  tech: TechSystem;
  builtStructures: Set<string>;
  units: UnitInstance[];
  queueSnapshot: BuildQueueItem[];
  resources: { credits: number; incomePerMinute: number };
}

export interface ActionAvailability {
  units: { id: string; name: string; cost: number; available: boolean }[];
  buildings: { id: string; name: string; cost: number; available: boolean }[];
  tech: { tier: TechnologyTier; cost: number; available: boolean }[];
}

export class Simulation {
  private readonly factions: Record<FactionId, FactionState>;
  private readonly combat = new CombatSystem();

  constructor(private readonly lanes = 3) {
    this.factions = {
      alpha: this.createFaction('alpha'),
      omega: this.createFaction('omega')
    };
  }

  private createFaction(id: FactionId): FactionState {
    const builtStructures = new Set<string>(['barracks']);
    const tech = new TechSystem(TECH_TREE);
    return {
      id,
      economy: new EconomySystem(),
      production: new ProductionSystem((blueprint) => this.spawnFromQueue(id, blueprint)),
      tech,
      builtStructures,
      units: [],
      queueSnapshot: [],
      resources: { credits: 0, incomePerMinute: 0 }
    };
  }

  private spawnFromQueue(owner: FactionId, blueprint: UnitBlueprint | BuildingBlueprint) {
    if ('unitClass' in blueprint) {
      const lane = Math.floor(Math.random() * this.lanes);
      const unit: UnitInstance = {
        id: nextUnitId(),
        owner,
        blueprint,
        lane,
        position: owner === 'alpha' ? -55 : 55,
        health: blueprint.health
      };
      this.factions[owner].units.push(unit);
    } else {
      this.factions[owner].builtStructures.add(blueprint.id);
      if (blueprint.providesShield) {
        this.factions[owner].economy.addIncome(30);
      }
    }
  }

  public tick(delta: number) {
    for (const faction of Object.values(this.factions)) {
      faction.economy.tick(delta, faction.tech.getTier());
      faction.production.tick(delta);
      faction.queueSnapshot = faction.production.snapshot();
      faction.resources = faction.economy.snapshot();
      this.advanceUnits(faction.units, faction.id, delta);
    }

    const allUnits = [...this.factions.alpha.units, ...this.factions.omega.units];
    const combats = this.combat.resolveCollisions(allUnits);

    if (combats.length > 0) {
      this.factions.alpha.units = this.combat.purgeDestroyed(this.factions.alpha.units);
      this.factions.omega.units = this.combat.purgeDestroyed(this.factions.omega.units);
    }
  }

  private advanceUnits(units: UnitInstance[], owner: FactionId, delta: number) {
    for (const unit of units) {
      const direction = owner === 'alpha' ? 1 : -1;
      unit.position += unit.blueprint.speed * delta * direction;
    }
  }

  public queueUnit(faction: FactionId, unitId: string): boolean {
    const blueprint = UNIT_BLUEPRINTS[unitId];
    const state = this.factions[faction];
    if (!blueprint || !blueprintAvailable(blueprint, state.builtStructures, state.tech.getTier())) {
      return false;
    }
    if (!state.economy.spend(blueprint.cost)) {
      return false;
    }
    state.production.enqueue(blueprint);
    return true;
  }

  public queueBuilding(faction: FactionId, buildingId: string): boolean {
    const blueprint = BUILDINGS[buildingId];
    const state = this.factions[faction];
    if (!blueprint || blueprint.tierRequired > state.tech.getTier()) {
      return false;
    }
    if (!state.economy.spend(blueprint.cost)) {
      return false;
    }
    if (state.builtStructures.has(buildingId)) {
      return false;
    }
    state.production.enqueue(blueprint);
    return true;
  }

  public advanceTech(faction: FactionId, tier: TechnologyTier): boolean {
    const state = this.factions[faction];
    const unlock = state.tech.canAdvance(tier);
    if (!unlock || !state.economy.spend(unlock.cost)) {
      return false;
    }
    state.tech.advance(unlock);
    return true;
  }

  public snapshot(): Record<FactionId, FactionState> {
    return {
      alpha: this.cloneFactionState(this.factions.alpha),
      omega: this.cloneFactionState(this.factions.omega)
    };
  }

  public getAvailability(faction: FactionId): ActionAvailability {
    const state = this.factions[faction];
    const resources = state.economy.snapshot();
    const tier = state.tech.getTier();

    const units = Object.values(UNIT_BLUEPRINTS).map((blueprint) => {
      const unlocked = blueprintAvailable(blueprint, state.builtStructures, tier);
      return {
        id: blueprint.id,
        name: blueprint.name,
        cost: blueprint.cost,
        available: unlocked && resources.credits >= blueprint.cost
      };
    });

    const buildings = Object.values(BUILDINGS).map((building) => {
      const unlocked = building.tierRequired <= tier && !state.builtStructures.has(building.id);
      return {
        id: building.id,
        name: building.name,
        cost: building.cost,
        available: unlocked && resources.credits >= building.cost
      };
    });

    const tech = TECH_TREE.map((unlock) => ({
      tier: unlock.tier,
      cost: unlock.cost,
      available: unlock.tier > tier && resources.credits >= unlock.cost
    }));

    return { units, buildings, tech };
  }

  private cloneFactionState(state: FactionState): FactionState {
    return {
      ...state,
      economy: state.economy,
      production: state.production,
      tech: state.tech,
      builtStructures: new Set(state.builtStructures),
      units: state.units.map((unit) => ({ ...unit, blueprint: unit.blueprint })),
      queueSnapshot: state.queueSnapshot.map((item) => ({ ...item })),
      resources: { ...state.resources }
    };
  }
}
