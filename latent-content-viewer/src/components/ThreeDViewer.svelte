<script>
  import * as THREE from 'three';
  import { OrbitControls } from 'three-stdlib';
  import { onMount, createEventDispatcher } from 'svelte';
  import Popup from './Popup.svelte';
  import { colors } from '../colors.js';

  let container;
  const dispatch = createEventDispatcher();
  let spheres = [];
  let links = [];

  let data = null;
  let selectedNode = null;
  let crosshair = null;
  let scene, controls, camera, renderer;
  let popupData = null;
  let nodeScreenPos = { x: 0, y: 0 };

  let rotationSpeed = 0.01;
  let isPanning = false;
  let isDragging = false;
  let initialTouch = { x: 0, y: 0 };
  const touchThreshold = 100;
  const tapThreshold = 50;

  async function fetchData() {
    const response = await fetch('/nodes.json');
    const data = await response.json();
    return data;
  }

  function createSphere(position, color, id) {
    const geometry = new THREE.SphereGeometry(0.1, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(...position);
    sphere.userData = { id, defaultColor: color };
    return sphere;
  }

  function createLine(start, end) {
    const material = new THREE.LineBasicMaterial({ color: colors.color8 });
    const points = [new THREE.Vector3(...start), new THREE.Vector3(...end)];
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    return new THREE.Line(geometry, material);
  }

  function calculateCenterOfMass(positions) {
    const center = positions.reduce((acc, pos) => {
      acc[0] += pos[0];
      acc[1] += pos[1];
      acc[2] += pos[2];
      return acc;
    }, [0, 0, 0]).map(coord => coord / positions.length);
    return center;
  }

  function createCrosshair() {
    const geometry = new THREE.TetrahedronGeometry(0.2);
    const material = new THREE.MeshBasicMaterial({ color: colors.color5, wireframe: true });
    return new THREE.Mesh(geometry, material);
  }

  function updateNodeScreenPos(node) {
    if (node) {
      const vector = new THREE.Vector3().copy(node.position);
      vector.project(camera);
      nodeScreenPos = {
        x: (vector.x + 1) / 2 * window.innerWidth,
        y: -(vector.y - 1) / 2 * window.innerHeight
      };
    }
  }

  function selectNode(node) {
    if (selectedNode) {
      scene.remove(crosshair);
      popupData = null;
      if (history.state && history.state.id === selectedNode.userData.id) {
        history.pushState(null, '', window.location.pathname);
      }
    }
    selectedNode = node;
    if (node) {
      crosshair.position.copy(node.position);
      crosshair.rotation.set(
        Math.random() * Math.PI * 2,
        Math.random() * Math.PI * 2,
        Math.random() * Math.PI * 2
      );
      scene.add(crosshair);
      popupData = data[node.userData.id];
      updateNodeScreenPos(node);
    }
  }

  function onBackgroundClick() {
    if (!isPanning && !isDragging) {
      selectNode(null);
    }
  }

  function onKeyPress(event) {
    if (event.key === 'q') {
      selectNode(null);
    }
  }

  function onMouseDown(event) {
    isPanning = false;
    isDragging = false;
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
  }

  function onMouseMove(event) {
    isPanning = true;
    if (!isDragging) {
      event.preventDefault();
    }
    isDragging = true;
  }

  function onMouseUp(event) {
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    isPanning = false;
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    let nodeId = urlParams.get('node');
    const defaultNodeId = 'main.md';

    data = await fetchData();

    scene = new THREE.Scene();
    scene.background = new THREE.Color(colors.background);
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;

    const positions = [];
    const sphereMap = {};

    Object.keys(data).forEach((key) => {
      const item = data[key];
      const position = item.embedding;
      positions.push(position);
      const color = item.filetype === 'markdown' ? colors.color3 : colors.color4;
      const sphere = createSphere(position, color, key);
      scene.add(sphere);
      spheres.push(sphere);
      sphereMap[key] = sphere;
    });

    Object.keys(data).forEach((key) => {
      const item = data[key];
      if (item.metadata.links) {
        item.metadata.links.forEach(link => {
          const target = link.split('|')[0];
          if (sphereMap[target]) {
            links.push(createLine(item.embedding, data[target].embedding));
          }
        });
      }
    });

    links.forEach(line => scene.add(line));

    const centerOfMass = calculateCenterOfMass(positions);
    controls.target.set(...centerOfMass);
    camera.position.set(centerOfMass[0], centerOfMass[1], centerOfMass[2]+5);
    controls.update();

    crosshair = createCrosshair();

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    function onMouseClick(event) {
      if (isDragging) return;

      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(spheres);

      if (intersects.length > 0) {
        const id = intersects[0].object.userData.id;
        selectNode(intersects[0].object);
        history.pushState({ id, cameraPosition: camera.position.toArray(), targetPosition: controls.target.toArray() }, '', `?node=${id}`);
        dispatch('click', { id });
      } else {
        onBackgroundClick();
      }
    }

    function onTouchStart(event) {
      if (event.touches.length === 1) {
        isPanning = false;
        isDragging = false;
        initialTouch = { x: event.touches[0].clientX, y: event.touches[0].clientY };
        window.addEventListener('touchmove', onTouchMove);
        window.addEventListener('touchend', onTouchEnd);
      }
    }

    function onTouchMove(event) {
      isPanning = true;
      if (!isDragging) {
        event.preventDefault();
      }
      isDragging = true;
    }

    function onTouchEnd(event) {
      event.preventDefault();
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
    
      if (!isPanning && event.changedTouches.length === 1) {
        const touch = event.changedTouches[0];
        mouse.x = (touch.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(touch.clientY / window.innerHeight) * 2 + 1;
    
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(spheres);
    
        if (intersects.length > 0) {
          const id = intersects[0].object.userData.id;
          selectNode(intersects[0].object);
          history.pushState({ id, cameraPosition: camera.position.toArray(), targetPosition: controls.target.toArray() }, '', `?node=${id}`);
          dispatch('click', { id });
        } else {
          onBackgroundClick();
        }
      }
      isPanning = false;
    }
    
    window.addEventListener('mousedown', onMouseDown);
    window.addEventListener('click', onMouseClick);
    window.addEventListener('keypress', onKeyPress);
    window.addEventListener('touchstart', onTouchStart);

    const animate = function () {
      requestAnimationFrame(animate);
      controls.update();
      if (selectedNode) {
        updateNodeScreenPos(selectedNode);
        crosshair.rotation.x += rotationSpeed;
        crosshair.rotation.y += rotationSpeed;
      }
      renderer.render(scene, camera);
    };

    animate();

    function onWindowResize() {
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
    }

    window.addEventListener('resize', onWindowResize, false);

    window.addEventListener('popstate', (event) => {
      const state = event.state;
      if (state) {
        const { id, cameraPosition, targetPosition } = state;
        camera.position.fromArray(cameraPosition);
        controls.target.fromArray(targetPosition);
        controls.update();
        if (sphereMap[id]) {
          selectNode(sphereMap[id]);
        }
      } else {
        selectNode(null);
      }
    });

    window.addEventListener('selectnode', (event) => {
      const { id } = event.detail;
      if (sphereMap[id]) {
        selectNode(sphereMap[id]);
        history.pushState({ id, cameraPosition: camera.position.toArray(), targetPosition: controls.target.toArray() }, '', `?node=${id}`);
      }
    });

    if (!nodeId && sphereMap[defaultNodeId]) {
      nodeId = defaultNodeId;
    }

    if (nodeId && sphereMap[nodeId]) {
      const state = history.state;
      if (state) {
        const { cameraPosition, targetPosition } = state;
        camera.position.fromArray(cameraPosition);
        controls.target.fromArray(targetPosition);
        controls.update();
      }
      selectNode(sphereMap[nodeId]);
    }

    return () => {
      window.removeEventListener('resize', onWindowResize);
      window.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('click', onMouseClick);
      window.removeEventListener('keypress', onKeyPress);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('touchstart', onTouchStart);
      window.removeEventListener('touchmove', onTouchMove);
      window.removeEventListener('touchend', onTouchEnd);
    };
  });
</script>

<style>
  .no-select {
    user-select: none;
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
  }
</style>

<div bind:this={container} class="w-full h-screen no-select"></div>

<Popup nodeData={popupData} nodeScreenPos={nodeScreenPos} closePopup={() => selectNode(null)} />
