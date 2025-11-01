import {
  Color,
  Mesh,
  MeshStandardMaterial,
  PerspectiveCamera,
  Scene,
  SphereGeometry,
  Vector2,
  WebGLRenderer
} from 'three';
import { Simulation, FactionState, ActionAvailability } from './Simulation';
import { createWorld } from './world';
import { FactionId, TechnologyTier, UnitInstance } from './types';

interface UnitVisual {
  mesh: Mesh;
  instance: UnitInstance;
}

export class Game {
  private readonly simulation = new Simulation();
  private readonly worldLayers;
  private readonly unitMeshes: Map<string, UnitVisual> = new Map();
  private readonly uiButtons: HTMLButtonElement[] = [];
  private hud?: HTMLElement;
  private availability: ActionAvailability | null = null;

  constructor(private readonly scene: Scene, private readonly camera: PerspectiveCamera, private readonly _renderer: WebGLRenderer) {
    this.worldLayers = createWorld(scene, camera);
  }

  public mountHud(element: HTMLElement) {
    this.hud = element;
    this.renderHud(this.simulation.snapshot().alpha);
  }

  public update(delta: number) {
    this.simulation.tick(delta);
    const snapshot = this.simulation.snapshot();
    this.availability = this.simulation.getAvailability('alpha');
    this.syncUnits(snapshot);
    if (this.hud) {
      this.renderHud(snapshot.alpha);
    }
  }

  public onPointerMove(_pointer: Vector2) {
    // Reserved for selecting units or lanes in future iterations
  }

  private syncUnits(snapshot: Record<FactionId, FactionState>) {
    const existing = new Set<string>();
    for (const faction of Object.values(snapshot)) {
      for (const unit of faction.units) {
        existing.add(unit.id);
        if (!this.unitMeshes.has(unit.id)) {
          this.createUnitMesh(unit);
        }
        const visual = this.unitMeshes.get(unit.id);
        if (visual) {
          this.updateUnitMesh(visual, unit);
        }
      }
    }

    for (const [id, visual] of Array.from(this.unitMeshes.entries())) {
      if (!existing.has(id)) {
        this.scene.remove(visual.mesh);
        this.unitMeshes.delete(id);
      }
    }
  }

  private createUnitMesh(unit: UnitInstance) {
    const geometry = new SphereGeometry(1.2, 20, 20);
    const material = new MeshStandardMaterial({
      color: unit.owner === 'alpha' ? new Color('#2ec4ff') : new Color('#ff595e'),
      emissive: unit.blueprint.tier === TechnologyTier.III ? new Color('#ffe066') : new Color('#0d1b2a'),
      emissiveIntensity: unit.blueprint.tier === TechnologyTier.III ? 0.6 : 0.2
    });
    const mesh = new Mesh(geometry, material);
    mesh.position.set(this.laneToX(unit.lane), 1.2, unit.position);
    this.scene.add(mesh);
    this.unitMeshes.set(unit.id, { mesh, instance: unit });
  }

  private updateUnitMesh(visual: UnitVisual, unit: UnitInstance) {
    visual.mesh.position.z = unit.position;
    visual.mesh.position.x = this.laneToX(unit.lane);
    visual.mesh.scale.setScalar(1 + unit.blueprint.tier * 0.25);
    visual.instance = unit;
  }

  private laneToX(lane: number) {
    return (lane - 1) * 18;
  }

  private renderHud(faction: FactionState) {
    if (!this.hud) {
      return;
    }
    this.hud.innerHTML = '';

    const resource = document.createElement('div');
    resource.className = 'resource';
    resource.textContent = `Credits: ${faction.resources.credits} | Income: ${faction.resources.incomePerMinute}/min | Tier ${faction.tech.getTier()}`;
    this.hud.appendChild(resource);

    const availability = this.availability ?? this.simulation.getAvailability('alpha');

    const queueList = document.createElement('div');
    queueList.textContent = `Queue: ${faction.queueSnapshot.map((item) => ('unitClass' in item.blueprint ? item.blueprint.name : item.blueprint.name)).join(', ') || 'Empty'}`;
    this.hud.appendChild(queueList);

    const structures = document.createElement('div');
    const structureNames = Array.from(faction.builtStructures).map((id) => availability.buildings.find((building) => building.id === id)?.name ?? id);
    structures.textContent = `Structures: ${structureNames.join(', ') || 'None'}`;
    this.hud.appendChild(structures);

    const controls = document.createElement('div');
    controls.style.display = 'grid';
    controls.style.gridTemplateColumns = 'repeat(2, minmax(0, 1fr))';
    controls.style.gap = '6px';
    this.hud.appendChild(controls);

    this.uiButtons.splice(0, this.uiButtons.length);

    availability.units.forEach(({ id, name, cost, available }) => {
      controls.appendChild(
        this.createButton(
          `${name} (${cost})`,
          () => this.simulation.queueUnit('alpha', id),
          available
        )
      );
    });

    availability.buildings.forEach(({ id, name, cost, available }) => {
      controls.appendChild(
        this.createButton(
          `${name} (${cost})`,
          () => this.simulation.queueBuilding('alpha', id),
          available
        )
      );
    });

    availability.tech.forEach(({ tier, cost, available }) => {
      controls.appendChild(
        this.createButton(
          `Research Tier ${tier} (${cost})`,
          () => this.simulation.advanceTech('alpha', tier),
          available
        )
      );
    });
  }

  private createButton(label: string, onClick: () => void, enabled: boolean) {
    const button = document.createElement('button');
    button.textContent = label;
    button.disabled = !enabled;
    button.addEventListener('click', () => {
      onClick();
      if (this.hud) {
        this.renderHud(this.simulation.snapshot().alpha);
      }
    });
    this.uiButtons.push(button);
    return button;
  }
}
