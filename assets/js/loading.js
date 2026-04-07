// loading.js: muestra y oculta el spinner de carga global
window.showLoadingSpinner = function(msg = 'Carregant dades...') {
  let overlay = document.getElementById('spinnerOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'spinnerOverlay';
    overlay.className = 'spinner-overlay';
    overlay.innerHTML = `
      <div class="spinner-content">
        <div class="lds-dual-ring"></div>
        <div class="spinner-msg">${msg}</div>
      </div>
    `;
    document.body.appendChild(overlay);
  } else {
    overlay.querySelector('.spinner-msg').textContent = msg;
    overlay.style.display = 'flex';
  }
};

window.hideLoadingSpinner = function() {
  const overlay = document.getElementById('spinnerOverlay');
  if (overlay) overlay.style.display = 'none';
};
