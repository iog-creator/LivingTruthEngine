import { ResourceState, TechnologyTier } from '../types';

export interface EconomyConfig {
  baseIncomePerMinute: number;
  tierIncomeBonus: Record<TechnologyTier, number>;
}

export class EconomySystem {
  private resources: ResourceState = { credits: 0, incomePerMinute: 120 };
  private readonly config: EconomyConfig;

  constructor(config?: Partial<EconomyConfig>) {
    this.config = {
      baseIncomePerMinute: 120,
      tierIncomeBonus: {
        [TechnologyTier.I]: 0,
        [TechnologyTier.II]: 45,
        [TechnologyTier.III]: 120
      },
      ...config
    };

    this.resources = {
      credits: 200,
      incomePerMinute: this.config.baseIncomePerMinute
    };
  }

  public tick(delta: number, tier: TechnologyTier) {
    const bonus = this.config.tierIncomeBonus[tier] ?? 0;
    const incomePerSecond = (this.resources.incomePerMinute + bonus) / 60;
    this.resources.credits += incomePerSecond * delta;
  }

  public spend(amount: number): boolean {
    if (this.resources.credits < amount) {
      return false;
    }
    this.resources.credits -= amount;
    return true;
  }

  public addIncome(flat: number) {
    this.resources.incomePerMinute += flat;
  }

  public snapshot(): ResourceState {
    return {
      credits: Math.floor(this.resources.credits),
      incomePerMinute: Math.round(this.resources.incomePerMinute)
    };
  }
}
