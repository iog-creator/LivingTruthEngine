import { CombatResult, UnitClass, UnitInstance } from '../types';

const COUNTER_DEFAULT = 1;

export class CombatSystem {
  public engage(attacker: UnitInstance, defender: UnitInstance): CombatResult {
    const counterMultiplier = attacker.blueprint.counterMultipliers[defender.blueprint.unitClass] ?? COUNTER_DEFAULT;
    const damage = attacker.blueprint.damage * counterMultiplier;
    defender.health -= damage;

    return {
      attacker,
      defender,
      damageDealt: damage,
      defenderRemaining: Math.max(0, defender.health)
    };
  }

  public resolveCollisions(units: UnitInstance[]): CombatResult[] {
    const results: CombatResult[] = [];
    const groupedByLane = new Map<number, UnitInstance[]>();

    for (const unit of units) {
      const laneUnits = groupedByLane.get(unit.lane) ?? [];
      laneUnits.push(unit);
      groupedByLane.set(unit.lane, laneUnits);
    }

    for (const laneUnits of groupedByLane.values()) {
      laneUnits.sort((a, b) => a.position - b.position);
      for (let i = 0; i < laneUnits.length - 1; i++) {
        const current = laneUnits[i];
        const next = laneUnits[i + 1];
        if (current.owner !== next.owner && Math.abs(current.position - next.position) < 1.5) {
          const resultA = this.engage(current, next);
          results.push(resultA);
          if (next.health > 0) {
            const resultB = this.engage(next, current);
            results.push(resultB);
          }
        }
      }
    }

    return results;
  }

  public purgeDestroyed(units: UnitInstance[]): UnitInstance[] {
    return units.filter((unit) => unit.health > 0);
  }
}
