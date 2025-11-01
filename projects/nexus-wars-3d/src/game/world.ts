import {
  Scene,
  AmbientLight,
  DirectionalLight,
  GridHelper,
  Mesh,
  MeshStandardMaterial,
  PlaneGeometry,
  Color,
  PerspectiveCamera,
  Group
} from 'three';

export interface WorldLayers {
  battlefield: Mesh;
  lanes: Group;
}

export function createWorld(scene: Scene, camera: PerspectiveCamera): WorldLayers {
  const ambient = new AmbientLight(0xaabbd1, 0.6);
  scene.add(ambient);

  const sun = new DirectionalLight(0xffffff, 0.9);
  sun.position.set(-20, 30, 25);
  scene.add(sun);

  const grid = new GridHelper(80, 20, new Color('#2ec4ff'), new Color('#152238'));
  grid.position.y = 0.02;
  scene.add(grid);

  const planeGeometry = new PlaneGeometry(80, 120);
  const planeMaterial = new MeshStandardMaterial({
    color: new Color('#0b1224'),
    metalness: 0.05,
    roughness: 0.8
  });
  const battlefield = new Mesh(planeGeometry, planeMaterial);
  battlefield.rotation.x = -Math.PI / 2;
  scene.add(battlefield);

  const lanes = new Group();
  const laneMaterial = new MeshStandardMaterial({ color: new Color('#1d2f4d') });
  for (let i = 0; i < 3; i++) {
    const lane = new Mesh(new PlaneGeometry(16, 120), laneMaterial);
    lane.position.x = (i - 1) * 18;
    lane.rotation.x = -Math.PI / 2;
    lane.position.y = 0.01;
    lanes.add(lane);
  }
  scene.add(lanes);

  camera.position.set(0, 28, 42);
  camera.lookAt(0, 0, 0);

  return { battlefield, lanes };
}
