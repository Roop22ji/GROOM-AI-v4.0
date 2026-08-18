from .engine import create_game_project, write_game

THREE_CDN = "https://cdn.jsdelivr.net/npm/three@0.179.1/build/three.module.js"

def temple_run_template():
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Groom Game</title>
<style>
html,body {{ margin:0; width:100%; height:100%; overflow:hidden; background:#111; }}
#hud {{ position:fixed; top:12px; left:12px; z-index:5; color:white;
font:700 20px Arial,sans-serif; text-shadow:0 2px 3px #000; }}
#help {{ position:fixed; bottom:12px; left:12px; z-index:5; color:white;
font:14px Arial,sans-serif; opacity:.85; }}
</style>
</head>
<body>
<div id="hud">Score: <span id="score">0</span></div>
<div id="help">A/D or ←/→ to move · Space to jump · R to restart</div>
<script type="module" src="./game.js"></script>
</body>
</html>"""

    js = f"""import * as THREE from "{THREE_CDN}";

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 500);
camera.position.set(0, 4.5, 8);
camera.lookAt(0, 1, -20);

const renderer = new THREE.WebGLRenderer({{antialias:true}});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff, 0x555555, 2));
const sun = new THREE.DirectionalLight(0xffffff, 2);
sun.position.set(5, 10, 5);
scene.add(sun);

const road = new THREE.Mesh(
  new THREE.BoxGeometry(9, 0.3, 180),
  new THREE.MeshStandardMaterial({{color:0x333333}})
);
road.position.set(0, -0.15, -70);
scene.add(road);

const player = new THREE.Mesh(
  new THREE.BoxGeometry(1.1, 1.8, 1.1),
  new THREE.MeshStandardMaterial({{color:0x3366ff}})
);
player.position.set(0, 0.9, 3);
scene.add(player);

const obstacles = [], coins = [];
const lanes = [-2.5, 0, 2.5];

function addObstacle(z) {{
  const o = new THREE.Mesh(
    new THREE.BoxGeometry(1.6,1.5,1.5),
    new THREE.MeshStandardMaterial({{color:0xff5533}})
  );
  o.position.set(lanes[Math.floor(Math.random()*3)], 0.75, z);
  scene.add(o); obstacles.push(o);
}}

function addCoin(z) {{
  const c = new THREE.Mesh(
    new THREE.TorusGeometry(0.35,0.1,12,24),
    new THREE.MeshStandardMaterial({{color:0xffd21f, emissive:0x553300}})
  );
  c.position.set(lanes[Math.floor(Math.random()*3)], 1.3, z);
  c.rotation.x = Math.PI/2;
  scene.add(c); coins.push(c);
}}

for (let z=-15; z>-150; z-=12) {{ addObstacle(z); addCoin(z-5); }}

let lane=1, targetX=0, yVelocity=0, score=0, running=true;
const clock = new THREE.Clock();

function hit(a,b,d=1.25) {{ return a.position.distanceTo(b.position)<d; }}
function restart() {{ location.reload(); }}

addEventListener("keydown", e => {{
  if (e.key==="ArrowLeft" || e.key.toLowerCase()==="a") lane=Math.max(0,lane-1);
  if (e.key==="ArrowRight" || e.key.toLowerCase()==="d") lane=Math.min(2,lane+1);
  if (e.code==="Space" && player.position.y<=0.91) yVelocity=10;
  if (e.key.toLowerCase()==="r") restart();
}});

function animate() {{
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.05);

  if (running) {{
    targetX=lanes[lane];
    player.position.x += (targetX-player.position.x)*Math.min(1,dt*10);
    yVelocity-=25*dt;
    player.position.y+=yVelocity*dt;
    if(player.position.y<0.9) {{ player.position.y=0.9; yVelocity=0; }}

    const speed=13*dt;
    for(const o of obstacles) {{
      o.position.z+=speed;
      if(hit(player,o)) {{
        running=false;
        document.getElementById("help").textContent="Game Over · Press R to restart";
      }}
    }}
    for(const c of coins) {{
      c.position.z+=speed; c.rotation.z+=dt*6;
      if(c.visible && hit(player,c,1.1)) {{
        c.visible=false; score+=10;
      }}
    }}
    score+=dt;
    document.getElementById("score").textContent=Math.floor(score);
    camera.position.x+=(player.position.x-camera.position.x)*dt*4;
    camera.lookAt(player.position.x,1,-20);
  }}
  renderer.render(scene,camera);
}}

addEventListener("resize",()=>{{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
}});
animate();
"""

    return html, js

def generate_temple_run():
    project=create_game_project("temple_run")
    html,js=temple_run_template()
    write_game(project,html,js)
    return project
