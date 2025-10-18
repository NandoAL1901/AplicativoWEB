const video = document.getElementById('camera');
const outputText = document.getElementById('outputText');

let stream = null;

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: 640, height: 480 },
      audio: false
    });

    video.srcObject = stream;
    video.play();

    console.log("✅ Cámara activada correctamente.");

    // Iniciar predicciones cada 5 segundos
    setInterval(() => {
      captureFrameAndPredict();
    }, 5000);

  } catch (error) {
    console.error("❌ No se pudo iniciar la cámara:", error);
    outputText.classList.remove("alert-info");
    outputText.classList.add("alert-danger");
    outputText.innerHTML = `
      <strong>Error:</strong> No se pudo acceder a la cámara.<br>
      Asegúrate de cerrar otras apps y usar http://localhost<br>
      <code>${error.message}</code>
    `;
  }
}

function captureFrameAndPredict() {
  if (!stream) return;

  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0);

  const imageData = canvas.toDataURL('image/jpeg');

  fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageData })
  })
  .then(response => response.json())
  .then(data => {
    outputText.innerHTML = `Signo Predicho: <strong>${data.label}</strong> (Confianza: ${(data.confidence * 100).toFixed(2)}%)`;
  })
  .catch(error => {
    console.error("❌ Error al predecir:", error);
    outputText.innerHTML = '❌ Error en la predicción';
  });
}

// Inicia la cámara tan pronto cargue la página
window.addEventListener("DOMContentLoaded", startCamera);
