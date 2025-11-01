import { BuildingBlueprint, TechnologyTier } from '../types';

export interface TechUnlock {
  tier: TechnologyTier;
  buildings: string[];
  cost: number;
}

export class TechSystem {
  private tier: TechnologyTier = TechnologyTier.I;
  private unlockedBuildings = new Set<string>();

  constructor(private readonly techTree: TechUnlock[]) {}

  public getTier(): TechnologyTier {
    return this.tier;
  }

  public canAdvance(nextTier: TechnologyTier): TechUnlock | null {
    if (nextTier <= this.tier) {
      return null;
    }
    return this.techTree.find((unlock) => unlock.tier === nextTier) ?? null;
  }

  public advance(unlock: TechUnlock) {
    this.tier = unlock.tier;
    unlock.buildings.forEach((id) => this.unlockedBuildings.add(id));
  }

  public isBuildingUnlocked(building: BuildingBlueprint): boolean {
    return building.tierRequired <= this.tier && (!building.unlocksUnits || building.unlocksUnits.every((id) => this.unlockedBuildings.has(id) || this.tier >= building.tierRequired));
  }
}
