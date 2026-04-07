# 🤖 **Diferencia entre UiPath y UC4 (Automic/Automation Anywhere)**

## 🎯 **RESUMEN RÁPIDO**

| **Aspecto** | **UiPath** | **UC4 (ahora Automic/Automation Anywhere)** |
|------------|------------|---------------------------------------------|
| **Tipo principal** | **RPA puro** (automatización de interfaz) | **Orquestador de trabajos** (job scheduler) |
| **Enfoque** | Automatizar lo que hace un humano en su PC | Automatizar flujos de trabajos entre sistemas |
| **Metáfora** | "Robot de escritorio" que imita a una persona | "Conductor de orquesta" que coordina sistemas |
| **Nivel** | **Front-end** (interactúa con aplicaciones) | **Back-end** (integra sistemas a nivel de API/scripts) |

---

## 🔍 **EXPLICACIÓN DETALLADA**

### **🎨 UiPath (RPA)**
- **Funciona**: Capturando pantalla, moviendo mouse, tecleando
- **Para**: Procesos donde NO hay APIs disponibles (legacy systems, mainframe, SAP GUI)
- **Ejemplo**: Un robot que:
  1. Abre SAP
  2. Navega por menús
  3. Copia datos de pantalla
  4. Los pega en Excel
  5. Envía email con adjunto

### **⚙️ UC4/Automic (Orquestación)**
- **Funciona**: Ejecutando scripts, llamando APIs, transfiriendo ficheros
- **Para**: Integrar sistemas modernos que TIENE APIs
- **Ejemplo**: Un flujo que:
  1. Llama API REST de sistema A para obtener datos
  2. Transforma datos con script Python
  3. Sube fichero vía SFTP a servidor B
  4. Ejecuta stored procedure en base de datos
  5. Notifica vía webhook

---

## 🏗️ **COMPARATIVA TÉCNICA**

| **Característica** | **UiPath** | **UC4/Automic** |
|-------------------|------------|-----------------|
| **Interacción UI** | ✅ Excelente (su especialidad) | ⚠️ Limitada/no es su foco |
| **Integración APIs** | ✅ Sí (pero no principal) | ✅ **Excelente** (especialidad) |
| **Programación** | Low-code/visual (arrastrar actividades) | Más scripting/código |
| **Escalabilidad** | ✅ Buena (con Orchestrator) | ✅ **Muy buena** (diseñado para IT) |
| **Para procesos negocio** | ✅ **Ideal** (usuarios de negocio) | ✅ Ideal (equipos IT) |
| **Coste** | Alto (licencias por robot) | Muy alto (enterprise) |

---

## 🏛️ **EN CONTEXTO AYUNTAMIENTO**

### **📋 Cuándo usar UiPath:**
- **Digitalización de procesos en papel/formularios**
- **Migración datos entre sistemas legacy sin APIs**
- **Automatización de tareas repetitivas de oficina**
- **Procesos donde usuarios interactúan manualmente hoy**

### **📋 Cuándo usar UC4/Automic:**
- **Orquestación de backups nocturnos entre sistemas**
- **Flujos ETL (Extracción-Transformación-Carga) de datos**
- **Integración entre bases de datos y sistemas modernos**
- **Programación de jobs batch complejos en servidores**

---

## 🤝 **COMPLEMENTARIEDAD**

**No son rivales, son COMPLEMENTARIOS:**

```mermaid
graph LR
    A[Sistema Legacy sin API] -->|UiPath| B[Extrae datos vía UI]
    B --> C[Fichero intermedio]
    C -->|UC4/Automic| D[Procesa y carga a BD]
    D --> E[Sistema Moderno]
```

**Ejemplo real en Ayuntamiento:**
1. **UiPath**: Extrae datos de aplicación antigua de padrón (sin API)
2. **UC4**: Transforma datos, valida, y carga en nueva base de datos SQL
3. **Ambos**: Coordinados para proceso completo

---

## 🎯 **EN UNA FRASE**

**UiPath automatiza lo que haría un funcionario en su ordenador, mientras que UC4/Automic automatiza lo que haría un administrador de sistemas entre servidores.**