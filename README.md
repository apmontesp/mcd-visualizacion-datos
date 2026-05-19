# Evaluación 1 – Laboratorio de Comunicación Basada en Evidencia

**Asignatura:** Visualización de Datos  
**Dataset:** Proyectos gubernamentales Colombia 2023–2024 (500 registros)

---

## Descripción

Aplicación Streamlit que desarrolla los dos primeros retos de la Evaluación 1, aplicando los principios de la Unidad 1: eficiencia cognitiva, leyes Gestalt y jerarquía visual.

| Reto | Objetivo | Técnica principal |
|------|----------|-------------------|
| 📏 Reto 1 – Jerarquía | Ingeniería de la Atención | Color selectivo + Data-to-Ink Ratio |
| ⚖️ Reto 2 – Contraste | Detección de Anomalías | Figura/Fondo + umbral estadístico |

---

## Estructura del repositorio

```
├── app.py                          # App principal Streamlit
├── dataset_evaluacion_unidad1.csv  # Dataset (fuente: profesor del curso)
├── requirements.txt                # Dependencias Python
└── README.md
```

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py
```

---

## Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub (asegúrate de incluir el CSV).
2. Entra a [share.streamlit.io](https://share.streamlit.io) y conecta tu cuenta de GitHub.
3. Selecciona el repositorio y apunta el **Main file path** a `app.py`.
4. Haz clic en **Deploy** — Streamlit instala las dependencias automáticamente.

---

## Dataset

- **Origen:** Proporcionado por el docente (basado en fuentes abiertas Gov.co)
- **Registros:** 500 proyectos
- **Período:** Enero 2023 – Mayo 2024
- **Variables:** `ID_Proyecto`, `Fecha_Inicio`, `Region`, `Departamento`, `Categoria`, `Estado`, `Presupuesto_USD`, `Poblacion_Beneficiada`, `Nivel_Impacto`

---

## Decisiones de diseño

### Reto 1 – Jerarquía
- **Tipo de gráfico:** Barras horizontales — óptimo para comparar categorías nominales.
- **Ordenación:** Descendente por presupuesto total para crear jerarquía visual inmediata.
- **Color:** Verde intenso para *Medio Ambiente* (categoría dominante con $270M), gris para el resto. El color actúa como atributo pre-atentivo, no como decoración.
- **Ruido eliminado:** Sin espinas top/right/left, sin leyenda redundante, cuadrícula tenue.

### Reto 2 – Contraste
- **Tipo de gráfico:** Barras temporales mensuales para detectar cambios discretos.
- **Figura/Fondo (Gestalt):** Barras grises = contexto histórico normal; barras rojas = anomalías que superan el umbral estadístico (media + 1σ = 22.1%).
- **Anomalía detectada:** Octubre 2023 y Enero 2024 alcanzan el 24.2% de proyectos retrasados, el doble del mínimo registrado (5.9% en Abril 2023).
- **Anotación integrada:** El insight se explica directamente en el gráfico, sin texto externo.
