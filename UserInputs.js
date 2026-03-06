const inputState = {
  MovementK: '0'
};

let MovementC = '0';
const gamepadInfo = document.getElementById("gamepad-info");

// --- 1. Keyboard Logic ---
window.addEventListener("keydown", (e) => {
  let oldMove = inputState.MovementK;
  if (e.key === "ArrowUp")    inputState.MovementK = '1';
  else if (e.key === "ArrowDown")  inputState.MovementK = '2';
  else if (e.key === "ArrowLeft")  inputState.MovementK = '3';
  else if (e.key === "ArrowRight") inputState.MovementK = '4';
  
  // Only send if the state actually changed (prevents key-repeat spam)
  if (oldMove !== inputState.MovementK) sendMovement();
});

window.addEventListener("keyup", (e) => {
  inputState.MovementK = '0';
  sendMovement();
});

// --- 2. Gamepad Logic ---
window.addEventListener("gamepadconnected", (e) => {
  const gp = navigator.getGamepads()[e.gamepad.index];
  gamepadInfo.textContent = `Connected: ${gp.id}`;
  requestAnimationFrame(updateGamepadLoop);
});

window.addEventListener("gamepaddisconnected", () => {
  gamepadInfo.textContent = "Waiting for gamepad...";
});

function updateGamepadLoop() {
  const gamepads = navigator.getGamepads();
  if (!gamepads[0]) return;

  const gp = gamepads[0];
  let prevMovement = MovementC;

  // Standard D-Pad mapping
  if (gp.buttons[12].pressed)      MovementC = '1'; // Up
  else if (gp.buttons[13].pressed) MovementC = '2'; // Down
  else if (gp.buttons[14].pressed) MovementC = '3'; // Left
  else if (gp.buttons[15].pressed) MovementC = '4'; // Right
  // Standard Face Button mapping (A, B, X, Y)
  else if (gp.buttons[0].pressed)  MovementC = '1'; 
  else if (gp.buttons[1].pressed)  MovementC = '2';
  else if (gp.buttons[2].pressed)  MovementC = '3';
  else if (gp.buttons[3].pressed)  MovementC = '4';
  else                             MovementC = '0';

  if (prevMovement !== MovementC) {
      sendMovement();
  }

  requestAnimationFrame(updateGamepadLoop);
}

// --- 3. Communication Bridge ---
function sendMovement() {
    // Priority: Gamepad takes precedence over Keyboard
    let activeMovement = (MovementC !== '0') ? MovementC : inputState.MovementK;
    
    if (typeof ws !== 'undefined' && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ "command": activeMovement }));
    }
}