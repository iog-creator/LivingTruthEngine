# Nexus Wars 3D Tug-of-War

A standalone Three.js-powered prototype for a Nexus Wars-inspired 3D tug-of-war strategy game. Players expand an economy, construct tech buildings, and queue units that march down shared lanes in an automated battle. Rock–paper–scissors counter systems, technology tiers, and strategic defensive structures create a layered multiplayer experience.

## Features

- **Three Lane Tug-of-War** – Units automatically push across three ground lanes toward the opponent nexus.
- **Economy & Tech Tiers** – Resource income, technology unlocks, and upgrade trees gate advanced units.
- **Rock–Paper–Scissors Combat** – Infantry, artillery, and air/flying classes interact via counter multipliers.
- **Defenses and Super Weapons** – Build mid-game shields and cannons before escalating to late-game weapons.
- **Headless Simulation** – Deterministic systems layer on top of the render loop so balancing can run independently from visuals.

## Project Structure

```
projects/nexus-wars-3d/
├── CHANGELOG.md
├── LICENSE
├── README.md
├── index.html
├── package-lock.json
├── package.json
├── src/
│   ├── game/
│   │   ├── systems/      # Simulation subsystems (economy, combat, tech)
│   │   ├── Game.ts       # High-level orchestration of rendering + simulation
│   │   ├── Simulation.ts # Deterministic simulation core
│   │   ├── types.ts      # Shared type definitions
│   │   └── world.ts      # Helpers for building the Three.js scene
│   └── main.ts           # Application entry point
├── tsconfig.json
└── vite.config.ts
```

## Getting Started

```bash
npm install
npm run dev
```

- Visit `http://localhost:5173/` to preview the prototype.
- Use the HUD buttons to queue unit batches, construct buildings, and trigger technology upgrades.
- The simulation automatically ticks even if the render loop is paused, enabling deterministic testing hooks.

## Roadmap

- Integrate authoritative multiplayer networking.
- Balance economy pacing with AI-driven sparring partners.
- Expand defensive tiers and add super weapon build chains for late game escalation.
- Replace primitive geometry with authored 3D assets and animations.
- Write automated combat scenario tests using the simulation core.

## License

Released under the MIT License. See [LICENSE](./LICENSE).
