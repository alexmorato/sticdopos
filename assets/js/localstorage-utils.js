// localstorage-utils.js

// Claves usadas en localStorage
const LS_KEYS = {
  TEMAS: 'sTICdOpos_temas',
  TIPO_PREGUNTA: 'sTICdOpos_tipoPregunta',
  DIFICULTAT: 'sTICdOpos_dificultat',
  ORIGIN: 'sTICdOpos_origin',
  FITXER: 'sTICdOpos_fitxer',
  PREGUNTA_POSITION: 'sTICdOpos_preguntaPosition',
  PREGUNTES_BARREJADES: 'sTICdOpos_preguntesBarrejades',
  ANSWERS: 'sTICdOpos_answers',
  CRONOMETRO: 'sTICdOpos_cronometro',
  PREGUNTES: 'sTICdOpos_preguntes',
  ESTUDIO_WIP: 'sTICdOpos_estudioWip',
  ESTUDIO_WIP_CONTINUE: 'sTICdOpos_estudioWipContinue',
  HISTORIAL_FALLOS: 'sTICdOpos_historialFallos',
  HISTORIAL_CONTESTADES: 'sTICdOpos_historialContestades',
  REPASAR_FALLOS: 'sTICdOpos_repasarFallos',
  JSON_COPYPASTE: 'sTICdOpos_jsonCopypaste', //lo quiero eliminar
  USER_NAME: 'sTICdOpos_userName',
  USER_PASS: 'sTICdOpos_userPass',
  INTERACCIONES_API: 'sTICdOpos_apiInteracciones',
  FIREBASE_SITE_ID: 'sTICdOpos_firebaseSiteId',
  ADMIN_DEBUG: 'sTICdOpos_debugadm'
};

// Método para borrar el estado guardado de estudio
function borrarEstudioEnProgreso() {
  localStorage.removeItem(LS_KEYS.PREGUNTES_BARREJADES);
  localStorage.removeItem(LS_KEYS.ANSWERS);
  localStorage.removeItem(LS_KEYS.CRONOMETRO);
  localStorage.removeItem(LS_KEYS.PREGUNTA_POSITION);
  localStorage.removeItem(LS_KEYS.REPASAR_FALLOS);
}
