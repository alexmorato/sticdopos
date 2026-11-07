# Lector de preguntas TTS

## Objetivo

Crear un modo de juego a pantalla completa que cargue un JSON de preguntas, lea cada pregunta mediante el motor TTS del navegador y revele su respuesta cuando termine el tiempo para contestar. La experiencia debe mantener la paleta visual de sTIC d'Opos y adaptarse a escritorio y móvil.

Este documento define el comportamiento acordado antes de empezar la implementación.

## Archivos y entrada

- `leer_ask.html`: pantalla del juego.
- `leer_ask_config.html`: página de configuración abierta desde la opción Admin.
- La página del juego recibe `root`, `tema` y `fitxer` por query string. Ejemplo: `leer_ask.html?root=apunts_new&tema=T16&fitxer=T16-Cards_es.json`.
- `root` y `tema` identifican la ubicación del JSON; `fitxer` es su nombre. Las rutas publicadas deben evitar duplicar el prefijo `sticdopos`.
- La sección Ask de `leerrecursos.html` debe abrir el lector con estos parámetros, en vez de mostrar el JSON directamente.
- Una carga manual desde Admin tiene prioridad sobre el archivo de la URL durante la sesión actual.

## Formato de datos

El contrato formal está en [ask.schema.json](ask.schema.json), compatible con JSON Schema 2020-12. El lector carga un objeto JSON con esta estructura:

```json
{
  "name": "Tabla del 5",
  "description": "Práctica oral de la tabla de multiplicar del 5",
  "language": "es",
  "settings": {
    "default_answer_time_seconds": 7,
    "secs_with_tick": 5,
    "time_between_questions_seconds": 2,
    "aleatorio": false,
    "intro_phrase": "Empezamos la sesión de aprendizaje.",
    "question_prefix": "Nueva pregunta."
  },
  "questions": [
    { "que": "Cinco por uno", "ans": "cinco", "secs": 3 },
    { "que": "Cinco por dos", "ans": "diez" }
  ]
}
```

- `name` es el título preferido; si falta, se usa el nombre del archivo sin extensión.
- `description`, `language` y `settings` son opcionales. Si aparece `name` o `language`, debe ser texto no vacío.
- `settings.aleatorio` es opcional y debe ser booleano. Con `true`, las preguntas se mezclan una vez al cargar; con `false` o si se omite, se conserva su orden en el JSON.
- Si se vuelve desde Admin durante una sesión, se conserva la mezcla existente y se repite desde el inicio la pregunta actual.
- `questions` es obligatorio y debe ser un array no vacío. Cada elemento requiere `que` y `ans` como textos no vacíos.
- `secs` es opcional por pregunta y, si existe, debe ser numérico y no negativo. Tiene prioridad sobre la preferencia del panel Admin.
- `settings.default_answer_time_seconds` y `settings.time_between_questions_seconds`, si aparecen, deben ser números no negativos. Ambos aceptan cero.
- `settings.secs_with_tick` es opcional y debe ser un entero no negativo. Si vale `N`, se reproduce un sonido breve una vez al entrar en cada segundo visible desde `N` hasta `1` del tiempo para responder; `0` o la ausencia del campo desactiva los ticks.
- Si falta `secs`, se usa el tiempo predeterminado guardado en Admin; si no está configurado, se usa `settings.default_answer_time_seconds` y, en último lugar, 7 segundos.
- La pausa entre preguntas sigue la misma prioridad: preferencia guardada en Admin, `settings.time_between_questions_seconds` y, en último lugar, 2 segundos. Una pausa de cero segundos es válida.
- Las frases `intro_phrase` y `question_prefix` son opcionales y, si aparecen, deben ser texto.
- Se permiten propiedades adicionales en el objeto raíz, en `settings` y en cada pregunta para facilitar extensiones compatibles.
- No se calcula puntuación ni se intenta reconocer la respuesta hablada. El juego no anuncia automáticamente aciertos, errores o el fin de la sesión.

## Pantalla del juego

La página ocupa el viewport completo. La composición utiliza dimensiones porcentuales y unidades de viewport para mantener proporciones estables; no debe quedar una página de desplazamiento normal.

### Escritorio

- Franja superior compacta con el valor `name` del JSON.
- Debajo, una composición aproximada de 70 % de ancho para la columna de contenido y 30 % para el temporizador.
- La columna de contenido se divide verticalmente: aproximadamente 60 % para la pregunta y 40 % para la respuesta.
- La pregunta permanece visible durante toda su ronda.
- La respuesta permanece oculta hasta que termina el tiempo para contestar.
- El temporizador ocupa la altura del área de juego y muestra el estado actual además del tiempo restante.

Las proporciones son una guía inicial y deben ajustarse para que el texto largo no se recorte.

### Móvil

Las tres áreas se apilan para conservar el orden pregunta, temporizador y respuesta, con tamaños adaptados a la altura disponible. Deben seguir siendo legibles sin solaparse; el contenido largo puede reducir tipografía o permitir desplazamiento dentro de su propia zona.

### Estilo

Reutilizar los colores actuales de la aplicación: fondo `#0b1020`, superficies `#141a2a`, bordes `#27304a`, texto claro y acento verde `#6ae0a7` / `#2aebad`. El temporizador puede enfatizar la urgencia con el rojo ya presente en la aplicación cuando quede poco tiempo.

## Ciclo de una ronda

1. Al iniciar, se lee `intro_phrase` si existe.
2. Se muestra la pregunta y se lee `question_prefix` si existe, seguido del texto `que`.
3. La cuenta para responder empieza cuando termina la locución de la pregunta. Así la lectura no consume el tiempo de respuesta.
4. Durante la cuenta, la pregunta sigue visible y la respuesta sigue oculta.
5. Al llegar a cero, se muestra `ans` y se lee mediante TTS.
6. El temporizador muestra la pausa configurada en `time_between_questions_seconds`.
7. Al terminar la pausa, se avanza automáticamente a la siguiente pregunta.
8. Al acabar la última pregunta, se muestra el estado de sesión completada y se ofrece reiniciar.

La cuenta debe seguir siendo visible en las fases de respuesta y pausa, con una etiqueta que identifique la fase. No se mostrarán mensajes de acierto o error mientras no haya puntuación.

## Menú y controles

El botón hamburguesa reutiliza el estilo del resto de la aplicación y contiene:

- **Atrás**: regresar a la página anterior; si no hay historial, volver a `leerrecursos.html`.
- **Pantalla completa**: activar o salir del modo fullscreen y reflejar el estado actual.
- **Menú**: ir a `index.html`.
- **Admin**: abrir `leer_ask_config.html`.
- **Pausa / continuar**: detener o reanudar tanto el TTS como el temporizador.
- **Saltar**: detener la locución y pasar de forma segura a la siguiente pregunta.
- **Reiniciar**: volver a la primera pregunta y comenzar una nueva sesión.

En el final de la sesión debe haber una acción visible para reiniciarla. Las acciones de salto, reinicio y navegación deben cancelar la locución y los temporizadores pendientes para evitar que una ronda anterior siga activa.

## Configuración Admin

La página `leer_ask_config.html` permite ajustar las preferencias del lector:

- Idioma predeterminado.
- Voz disponible para el idioma seleccionado.
- Velocidad TTS.
- Tono TTS.
- Texto de prueba editable y botón para escucharlo con los parámetros seleccionados.
- Tiempo de respuesta predeterminado.
- Tiempo entre preguntas.
- Pegar un JSON manual en el textarea o cargarlo desde un archivo.
- Restaurar valores predeterminados y volver al juego.

Las preferencias se guardan en `localStorage`. El idioma definido en `language` por el JSON prevalece siempre sobre la preferencia local; el lector usa una voz compatible con ese idioma y, si no hay ninguna disponible, conserva el código de idioma del JSON para que el navegador elija la voz. Al abrir Admin desde un juego con idioma definido, el selector queda fijado a ese idioma. La lista de voces se actualiza cuando el navegador notifica que están disponibles. Admin se abre en la misma pestaña para compartir el JSON temporal; al volver, la ronda activa se repite desde el comienzo de la pregunta actual.

El JSON manual se valida antes de aceptarse y se conserva en `sessionStorage` durante la navegación actual. Al abrir Admin, el JSON manual activo se muestra en el textarea para editarlo o sustituirlo. Al recargar el lector con F5, se elimina el override manual y se vuelve a descargar el JSON de la URL con una marca temporal y caché desactivada. La configuración es local al navegador y no constituye una zona protegida por permisos de administrador.

## Validación y estados de error

La interfaz debe informar de forma clara si falta algún parámetro, falla la carga, el JSON no es válido, no contiene preguntas utilizables o el navegador no ofrece `SpeechSynthesis`. La carga manual debe indicar por qué se rechaza un archivo inválido.

El temporizador y el estado de TTS deben permanecer sincronizados al pausar, reanudar, saltar, reiniciar, cambiar de página o finalizar la sesión. Debe comprobarse en un navegador de escritorio y en una ventana móvil.

## Decisiones cerradas

- La pregunta se lee antes de iniciar el tiempo de respuesta.
- La respuesta se revela al terminar el tiempo y el juego avanza automáticamente tras la pausa.
- No hay puntuación ni reconocimiento de voz por ahora.
- Se incluirán controles para pausar, saltar y reiniciar.
- La voz se selecciona según el idioma del JSON, con una alternativa si no existe una coincidencia.
- El diseño usa pregunta arriba, respuesta abajo y temporizador a la derecha en escritorio; en móvil las zonas se apilan.