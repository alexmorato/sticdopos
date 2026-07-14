// localstorage-utils.js

// Claves usadas en localStorage
const LS_KEYS = {
  TEMAS: 'sTICdOpos_temas',
  TIPO_PREGUNTA: 'sTICdOpos_tipoPregunta',
  DIFICULTAT: 'sTICdOpos_dificultat',
  ORIGIN: 'sTICdOpos_origin',
  FITXER: 'sTICdOpos_fitxer',
  FITXERS_ESTUDIANT: 'sTICdOpos_fitxersEstudiant',
  PREGUNTA_POSITION: 'sTICdOpos_preguntaPosition',
  PREGUNTES_BARREJADES: 'sTICdOpos_preguntesBarrejades',
  ANSWERS: 'sTICdOpos_answers',
  CRONOMETRO: 'sTICdOpos_cronometro',
  PREGUNTES: 'sTICdOpos_preguntes',
  ESTUDIO_WIP: 'sTICdOpos_estudioWip',
  ESTUDIO_WIP_CONTINUE: 'sTICdOpos_estudioWipContinue',
  HISTORIAL_FALLOS: 'sTICdOpos_historialFallos',
  HISTORIAL_CONTESTADES: 'sTICdOpos_historialContestades',
  HISTORIAL_TESTS_INICIADOS: 'sTICdOpos_historialTestsIniciados',
  REPASAR_FALLOS: 'sTICdOpos_repasarFallos',
  JSON_COPYPASTE: 'sTICdOpos_jsonCopypaste', //lo quiero eliminar
  USER_NAME: 'sTICdOpos_userName',
  USER_PASS: 'sTICdOpos_userPass',
  INTERACCIONES_API: 'sTICdOpos_apiInteracciones',
  FIREBASE_SITE_ID: 'sTICdOpos_firebaseSiteId',
  ADMIN_DEBUG: 'sTICdOpos_debugadm',
  YOUTUBE_PAUSADO: 'sTICdOpos_youtubePausado',
  YOUTUBE_CONTINUE: 'sTICdOpos_youtubeContinue',
  IFRAME_URL: 'sTICdOpos_iframe_url',
  IFRAME_NAME: 'sTICdOpos_iframe_name',
  IFRAME_TEMA: 'sTICdOpos_iframe_tema',
  IFRAME_TYPE: 'sTICdOpos_iframe_type',
  IFRAME_ORIGIN: 'sTICdOpos_iframe_origin',
  IFRAME_NOTES: 'sTICdOpos_iframe_notes',
  DIAPOS_PAUSADO: 'sTICdOpos_diaposPausado',
  DIAPOS_CONTINUE: 'sTICdOpos_diaposContinue',
  MD_PAUSADO: 'sTICdOpos_mdPausado',
  MD_CONTINUE: 'sTICdOpos_mdContinue',
  TTS_RATE: 'sTICdOpos_tts_rate',
  TTS_PITCH: 'sTICdOpos_tts_pitch',
  TTS_LANG: 'sTICdOpos_tts_lang',
  TTS_VOICE: 'sTICdOpos_tts_voice',
  TTS_DOC_REF: 'sTICdOpos_tts_docRef',
  TTS_PROGRESS: 'sTICdOpos_tts_progress',
  TTS_COLLAPSED_CARDS: 'sTICdOpos_tts_collapsedCards'
};

const LS_SENSITIVE_KEYS = Object.freeze(
  [
    LS_KEYS.USER_PASS
  ]
    .filter((keyValue) => typeof keyValue === 'string' && keyValue.trim() !== '')
);

function isSensitiveLocalStorageKey(storageKey) {
  if (typeof storageKey !== 'string' || storageKey.trim() === '') return false;
  return LS_SENSITIVE_KEYS.includes(storageKey);
}



// Método para borrar el estado guardado de estudio
function borrarEstudioEnProgreso() {
  localStorage.removeItem(LS_KEYS.PREGUNTES_BARREJADES);
  localStorage.removeItem(LS_KEYS.ANSWERS);
  localStorage.removeItem(LS_KEYS.CRONOMETRO);
  localStorage.removeItem(LS_KEYS.PREGUNTA_POSITION);
  localStorage.removeItem(LS_KEYS.REPASAR_FALLOS);
  localStorage.removeItem(LS_KEYS.FITXERS_ESTUDIANT);
}

function obtenerHistorialTestsIniciados() {
  try {
    const data = JSON.parse(localStorage.getItem(LS_KEYS.HISTORIAL_TESTS_INICIADOS) || '{}');
    if (!data || typeof data !== 'object' || Array.isArray(data)) return {};
    return data;
  } catch (e) {
    return {};
  }
}

function obtenerHitsTestIniciado(fileName) {
  if (!fileName) return 0;
  const historial = obtenerHistorialTestsIniciados();
  const rawValue = historial[fileName];
  const count = Number(rawValue);
  return Number.isFinite(count) && count > 0 ? Math.floor(count) : 0;
}

function registrarInicioTests(fileNames) {
  if (!Array.isArray(fileNames) || fileNames.length === 0) return;

  const historial = obtenerHistorialTestsIniciados();
  const filesUnicos = [...new Set(fileNames.filter(Boolean))];

  filesUnicos.forEach(fileName => {
    const current = Number(historial[fileName]);
    const currentSafe = Number.isFinite(current) && current > 0 ? Math.floor(current) : 0;
    historial[fileName] = currentSafe + 1;
  });

  localStorage.setItem(LS_KEYS.HISTORIAL_TESTS_INICIADOS, JSON.stringify(historial));
}
