import { BuildQueueItem, BuildingBlueprint, UnitBlueprint } from '../types';

export class ProductionSystem {
  private readonly queue: BuildQueueItem[] = [];

  constructor(private readonly onComplete: (blueprint: UnitBlueprint | BuildingBlueprint) => void) {}

  public enqueue(blueprint: UnitBlueprint | BuildingBlueprint) {
    this.queue.push({ blueprint, progress: 0 });
  }

  public remove(id: string) {
    const index = this.queue.findIndex((item) => 'id' in item.blueprint && item.blueprint.id === id);
    if (index >= 0) {
      this.queue.splice(index, 1);
    }
  }

  public tick(delta: number) {
    for (let i = 0; i < this.queue.length; i++) {
      const item = this.queue[i];
      item.progress += delta;
      const buildTime = item.blueprint.buildTime;
      if (item.progress >= buildTime) {
        this.onComplete(item.blueprint);
        this.queue.splice(i, 1);
        i--;
      }
    }
  }

  public snapshot(): BuildQueueItem[] {
    return this.queue.map((item) => ({ ...item }));
  }
}
