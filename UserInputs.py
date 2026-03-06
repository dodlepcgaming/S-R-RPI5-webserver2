const inputState = {
  MovementK: '0'
};

window.addEventListener("keydown", (e) => {
  if (e.key === "ArrowUp")    inputState.MovementK = '1';
  if (e.key === "ArrowDown")  inputState.MovementK = '2';
  if (e.key === "ArrowLeft")  inputState.MovementK = '3';
  if (e.key === "ArrowRight") inputState.MovementK = '4';
});

window.addEventListener("keyup", (e) => {
  if (e.key === "ArrowUp")    inputState.MovementK = '0';
  if (e.key === "ArrowDown")  inputState.MovementK = '0';
  if (e.key === "ArrowLeft")  inputState.MovementK = '0';
  if (e.key === "ArrowRight") inputState.MovementK = '0';
});

const gamepadInfo = document.getElementById("gamepad-info");
const ball = document.getElementById("RVRBody");
let start;
let MovementC;

window.addEventListener("gamepadconnected", (e) => {
  const gp = navigator.getGamepads()[e.gamepad.index];
  gamepadInfo.textContent = `Gamepad connected at index ${gp.index}: ${gp.id}. It has ${gp.buttons.length} buttons and ${gp.axes.length} axes.`;
  RVRMovement();
});

window.addEventListener("gamepaddisconnected", (e) => {
  gamepadInfo.textContent = "Waiting for gamepad.";
});

function RVRMovement() {
  const gamepads = navigator.getGamepads();
  if (!gamepads) {
    return;
  }

  const gp = gamepads[0];
  if (gp.buttons[0].pressed) {
    MovementC = '1';
  }
  if (gp.buttons[1].pressed) {
    MovementC = '2';
  }
  if (gp.buttons[2].pressed) {
    MovementC = '3';
  }
  if (gp.buttons[3].pressed) {
    MovementC = '4';
  }
}