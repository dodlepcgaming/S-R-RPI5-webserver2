const inputState = {
  MovementK: '0'
};

let MovementC = '0';
const gamepadInfo = document.getElementById("gamepad-info");

window.addEventListener("keydown", (e) => {
  let oldMove = inputState.MovementK;
  if (e.key === "ArrowUp")    inputState.MovementK = '1';
  if (e.key === "ArrowDown")  inputState.MovementK = '2';
  if (e.key === "ArrowLeft")  inputState.MovementK = '3';
  if (e.key === "ArrowRight") inputState.MovementK = '4';

  if (oldMove !== inputState.MovementK) {
      console.log("Keyboard Move Command:", inputState.MovementK);
      sendMovement();
  }
});

function sendMovement() {
    let activeMovement = (MovementC !== '0') ? MovementC : inputState.MovementK;
    
    if (typeof ws !== 'undefined' && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ "command": activeMovement }));
        console.log(">>> Sent to Pi:", activeMovement);
    } else {
        console.error("!!! WebSocket NOT CONNECTED. Check Pi script.");
    }
}

window.addEventListener("keyup", (e) => {
  inputState.MovementK = '0';
  sendMovement();
});

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

  if (gp.buttons[12].pressed)      MovementC = '1';
  else if (gp.buttons[13].pressed) MovementC = '2';
  else if (gp.buttons[14].pressed) MovementC = '3';
  else if (gp.buttons[15].pressed) MovementC = '4';

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

function sendMovement() {
    let activeMovement = (MovementC !== '0') ? MovementC : inputState.MovementK;
    
    if (typeof ws !== 'undefined' && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ "command": activeMovement }));
    }
}