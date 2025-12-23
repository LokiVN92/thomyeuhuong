let running = false;
let interval;

const num = document.getElementById("number");
const spin = document.getElementById("spin");
const win = document.getElementById("win");

function weightedRandom(min, max) {
  let split = 1400000;
  let r = Math.random();
  if (r < 0.98) {
    let t = Math.random() ** 2.5;
    return Math.floor(min + t * (Math.min(split, max) - min));
  }
  let t = Math.random() ** 4;
  return Math.floor(split + t * (max - split));
}

function start() {
  if (running) return;
  running = true;
  spin.currentTime = 0;
  spin.play();

  interval = setInterval(() => {
    num.innerText = (Math.random() * 1000000 + 1000000).toFixed(0);
  }, 60);
}

function stop() {
  if (!running) return;
  running = false;
  clearInterval(interval);
  spin.pause();

  let result = weightedRandom(1000000, 2000000);
  num.innerText = result.toLocaleString();

  win.currentTime = 0;
  win.play();

  sendToSheet(result);
}

/* ===== GOOGLE SHEET ===== */
function sendToSheet(result) {
  fetch("https://script.google.com/macros/s/AKfycbzQ0LdUuAsGhU2slQ_FyQuqKdgg-fcXCre8bAFXMQ7DyA3ndgs6-3B2Aijuo9C-BRFG/exec", {
    method: "POST",
    body: JSON.stringify({
      result: result,
      time: new Date().toLocaleString()
    })
  });
}

/* ===== SETTINGS ===== */
document.getElementById("bgInput").onchange = e => {
  document.body.style.backgroundImage =
    `url(${URL.createObjectURL(e.target.files[0])})`;
};

document.getElementById("spinInput").onchange = e => {
  spin.src = URL.createObjectURL(e.target.files[0]);
};

document.getElementById("winInput").onchange = e => {
  win.src = URL.createObjectURL(e.target.files[0]);
};
