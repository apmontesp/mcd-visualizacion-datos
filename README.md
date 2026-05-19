# Evaluación 1 – Laboratorio de Comunicación Basada en Evidencia

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mcd-visualizacion-datos.streamlit.app/)

**Asignatura:** Visualización de Datos — Maestría en Ingeniería  
**Universidad:** EAFIT  
**Docente:** Mauricio Arias Correa  
**Estudiante:** Ana Montes-Pimienta

---

## Descripción

Aplicación Streamlit interactiva que desarrolla los dos primeros retos de la Evaluación 1, aplicando los principios de la Unidad 1: eficiencia cognitiva, leyes Gestalt y jerarquía visual.

La app incluye un panel de filtros globales (Region, Categoria, Estado, Nivel de Impacto) que actualiza en tiempo real todos los análisis y KPIs. Cada visualización está construida con Plotly, permitiendo explorar los datos mediante tooltips al pasar el cursor. Se incluye además un botón de descarga del codigo Python (matplotlib) para cada grafica.

| Pregunta | Objetivo | Tecnica principal |
|----------|----------|-------------------|
| 1 – Jerarquía de Inversión | Identificar la categoría dominante por presupuesto | Barras horizontales con color selectivo |
| 2 – Alertas Temporales | Detectar periodos con tasa de retraso anómala | Barras temporales con umbral estadístico |
| 3 – Eficiencia de Inversión | Relacionar presupuesto con alcance poblacional | Dispersion con cuadrantes de riesgo |
| 4 – Composición del Portafolio | Comparar estados de ejecución por categoría | Barras apiladas normalizadas |
| 5 – Capital Territorial | Cruzar inversión regional con nivel de impacto | Barras agrupadas |
| Análisis Geoespacial | Identificar focos de riesgo por departamento | Mapa de burbujas (carto-positron) |

---

## Estructura del repositorio

```
app.py                              # Aplicación principal Streamlit
dataset_evaluacion_unidad1.csv      # Dataset (fuente: docente del curso)
requirements.txt                    # Dependencias Python
README.md
codigo/
    pregunta_1_jerarquia.py         # Script matplotlib descargable — P1
    pregunta_2_contraste.py         # Script matplotlib descargable — P2
    pregunta_3_eficiencia.py        # Script matplotlib descargable — P3
    pregunta_4_composicion.py       # Script matplotlib descargable — P4
    pregunta_5_region_impacto.py    # Script matplotlib descargable — P5
```

---

## Instalación local

```bash
git clone https://github.com/amontes-pimienta/mcd-visualizacion-datos.git
cd mcd-visualizacion-datos
pip install -r requirements.txt
streamlit run app.py
```

---

## Despliegue

La aplicación está publicada en Streamlit Cloud:  
[https://mcd-visualizacion-datos.streamlit.app/](https://mcd-visualizacion-datos.streamlit.app/)

Para republicar después de un cambio, basta con hacer push a la rama `main` — Streamlit Cloud detecta el cambio y redespliega automáticamente.

---

## Dataset

| Campo | Descripción |
|-------|------------|
| ID_Proyecto | Identificador unico del proyecto |
| Fecha_Inicio | Fecha de inicio del proyecto |
| Region | Region geografica colombiana |
| Departamento | Departamento del proyecto |
| Categoria | Sector tematico (Educacion, Salud, etc.) |
| Estado | Estado operativo actual |
| Presupuesto_USD | Presupuesto asignado en dolares |
| Poblacion_Beneficiada | Numero de personas beneficiadas |
| Nivel_Impacto | Nivel declarado de impacto (Alto, Medio, Bajo) |

Origen: proporcionado por el docente, basado en fuentes abiertas de datos.gov.co.  
Periodo cubierto: enero 2023 – mayo 2024. Total: 500 proyectos.

---

## Principios de diseño aplicados

Todas las visualizaciones siguen los siguientes criterios:

- Fondo blanco con ejes descritos y unidades explicitas en todos los graficos.
- Tooltips interactivos para revelar valores exactos al pasar el cursor, evitando etiquetas estaticas que saturan la vista.
- Color como herramienta de enfasis, no de decoracion. Verde = eficiencia/alto impacto, Rojo = alerta/bajo impacto, Gris = contexto neutral.
- Data-to-Ink Ratio maximizado: sin espinas decorativas, cuadricula minima y leyendas externas al area de datos.
- Leyes Gestalt aplicadas: ordenacion logica (P1), figura/fondo (P2), cuadrantes de riesgo (P3), composicion apilada (P4), agrupacion regional (P5), doble codificacion espacial (mapa).
