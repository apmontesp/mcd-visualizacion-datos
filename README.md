# Evaluación 1 – Laboratorio de Comunicación Basada en Evidencia

**Asignatura:** Visualización de Datos
**Dataset:** Proyectos gubernamentales Colombia 2023-2024 (500 registros)

---

## Descripción

Aplicación Streamlit interactiva que desarrolla los dos primeros retos de la Evaluación 1, aplicando los principios de la Unidad 1: eficiencia cognitiva, leyes Gestalt y jerarquía visual.

La app incluye un panel de filtros globales (Region, Categoria, Estado, Nivel de Impacto) que actualiza en tiempo real todos los análisis y KPIs. Cada visualización está construida con Plotly, permitiendo explorar los datos mediante tooltips al pasar el cursor sobre cada elemento. Se incluye además un botón de descarga del codigo Python (matplotlib) correspondiente a cada grafica.

| Pregunta | Objetivo | Tecnica principal |
|----------|----------|-------------------|
| 1 – Jerarquía de Inversión | Identificar la categoría dominante por presupuesto | Barras horizontales con color selectivo |
| 2 – Alertas Temporales | Detectar periodos con tasa de retraso anómala | Barras temporales con umbral estadístico |
| 3 – Eficiencia de Inversión | Relacionar presupuesto con alcance poblacional | Dispersion con cuadrantes de riesgo |
| 4 – Composición del Portafolio | Comparar estados de ejecución por categoría | Barras apiladas normalizadas |
| 5 – Capital Territorial | Cruzar inversión regional con nivel de impacto | Barras agrupadas |

---

## Estructura del repositorio

```
app.py                          # Aplicación principal Streamlit
dataset_evaluacion_unidad1.csv  # Dataset (fuente: docente del curso)
requirements.txt                # Dependencias Python
README.md
```

---

## Instalación local

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/mcd-visualizacion-datos.git
cd mcd-visualizacion-datos

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicacion
streamlit run app.py
```

---

## Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub asegurándote de incluir el archivo CSV.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io) y conecta tu cuenta de GitHub.
3. Selecciona el repositorio y establece el **Main file path** en `app.py`.
4. Haz clic en **Deploy**. Streamlit Cloud instala las dependencias del `requirements.txt` automaticamente.

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

## Decisiones de diseño

Todas las visualizaciones aplican los siguientes principios:

- **Fondo blanco** con ejes descritos y unidades explicitas en todos los graficos.
- **Tooltips interactivos** para revelar valores exactos al pasar el cursor, evitando etiquetas estaticas que saturan la vista.
- **Color como herramienta de enfasis**, no de decoracion. Cada gama cromatica tiene una funcion semantica definida (verde = eficiencia/alto impacto, rojo = alerta/bajo impacto, gris = contexto neutral).
- **Data-to-Ink Ratio maximizado**: sin espinas decorativas, cuadricula minima y leyendas externas al area de datos cuando son necesarias.
- **Leyes Gestalt aplicadas**: ordenacion logica (Pregunta 1), figura/fondo (Pregunta 2) y proximidad (Preguntas 4 y 5).
