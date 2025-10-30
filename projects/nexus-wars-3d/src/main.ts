import { WebGLRenderer, PerspectiveCamera, Scene, Clock, Vector2 } from 'three';
import { Game } from './game/Game';

const app = document.getElementById('app');
if (!app) {
  throw new Error('Failed to find #app container');
}

const renderer = new WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
app.appendChild(renderer.domElement);

const camera = new PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 28, 42);
camera.lookAt(0, 0, 0);

const scene = new Scene();
const game = new Game(scene, camera, renderer);
const clock = new Clock();
const pointer = new Vector2();

function resize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener('resize', resize);
window.addEventListener('pointermove', (event) => {
  pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
  game.onPointerMove(pointer);
});

const hud = document.getElementById('hud');
if (!hud) {
  throw new Error('Failed to find #hud container');
}

game.mountHud(hud);

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  game.update(delta);
  renderer.render(scene, camera);
}

animate();
