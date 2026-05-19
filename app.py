"""
Evaluación 1 – Laboratorio de Comunicación Basada en Evidencia
Materia: Visualización de Datos
Dataset: Proyectos Gubernamentales Colombia 2023-2024
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# ── Configuración ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Evaluación 1 – Visualización de Datos", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #f8fafc; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .section-num {
        display: inline-block; background: #111827; color: white;
        font-size: 0.72rem; font-weight: 700; border-radius: 4px;
        padding: 2px 10px; letter-spacing: 0.06em; margin-bottom: 4px;
    }
    .context-box {
        background: #f9fafb; border-left: 3px solid #d1d5db;
        padding: 10px 14px; border-radius: 0 6px 6px 0;
        font-size: 0.87rem; color: #374151; margin-bottom: 8px;
    }
    .arg-box {
        background: #f0fdf4; border-left: 3px solid #16a34a;
        padding: 12px 14px; border-radius: 0 6px 6px 0;
        font-size: 0.84rem; color: #374151; line-height: 1.55;
    }
    .arg-box b { color: #15803d; }
    h2 { font-size: 1.12rem !important; margin-top: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Constantes de diseño ──────────────────────────────────────────────────────
C_FOCO, C_NEUTRO, C_ALERTA = "#16a34a", "#cbd5e1", "#dc2626"
ESTADO_COLORS  = {"En Planeacion":"#7c3aed","En Ejecución":"#1d4ed8","Retrasado":"#dc2626","Finalizado":"#15803d"}
IMPACTO_COLORS = {"Alto":"#15803d","Medio":"#ca8a04","Bajo":"#dc2626"}

def layout(title="", xt="", yt="", legend=False, h=420):
    return dict(
        title=dict(text=title, font=dict(size=13, color="#111827", family="Arial"), x=0, xanchor="left"),
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=11, color="#374151"),
        xaxis=dict(title=dict(text=xt, font=dict(size=11, color="#6b7280")),
                   showgrid=True, gridcolor="#f3f4f6", linecolor="#d1d5db",
                   showline=True, zeroline=False, tickfont=dict(size=10, color="#6b7280")),
        yaxis=dict(title=dict(text=yt, font=dict(size=11, color="#6b7280")),
                   showgrid=False, linecolor="#d1d5db", showline=True,
                   zeroline=False, tickfont=dict(size=10, color="#374151")),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10), bgcolor="rgba(255,255,255,0.85)",
                    bordercolor="#e5e7eb", borderwidth=1),
        hoverlabel=dict(bgcolor="white", bordercolor="#d1d5db", font_size=12, font_family="Arial"),
        margin=dict(l=10, r=20, t=60, b=10), height=h,
    )

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    p = Path(__file__).parent / "dataset_evaluacion_unidad1.csv"
    if not p.exists():
        st.error("No se encontro 'dataset_evaluacion_unidad1.csv'. Incluyelo en la raiz del repositorio.")
        st.stop()
    df = pd.read_csv(p, parse_dates=["Fecha_Inicio"])
    df["YearMonth"]     = df["Fecha_Inicio"].dt.to_period("M")
    df["Presupuesto_M"] = df["Presupuesto_USD"] / 1_000_000
    return df

def read_code(filename):
    p = Path(__file__).parent / "codigo" / filename
    return p.read_text(encoding="utf-8") if p.exists() else "# Archivo no encontrado"

df = load_data()

# ── Sidebar – Panel de Control ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Panel de Control")
    st.markdown("Ajusta los filtros para explorar el portafolio. Todos los análisis responden en tiempo real.")
    st.markdown("---")
    regiones   = st.multiselect("Region",            sorted(df["Region"].unique()),           default=sorted(df["Region"].unique()))
    categorias = st.multiselect("Categoria",          sorted(df["Categoria"].unique()),         default=sorted(df["Categoria"].unique()))
    estados    = st.multiselect("Estado",             sorted(df["Estado"].unique()),            default=sorted(df["Estado"].unique()))
    impactos   = st.multiselect("Nivel de Impacto",   sorted(df["Nivel_Impacto"].unique()),     default=sorted(df["Nivel_Impacto"].unique()))
    st.markdown("---")
    st.caption("Dataset: Proyectos Gov. Colombia\n500 proyectos · 2023-2024")

df_f = df[df["Region"].isin(regiones) & df["Categoria"].isin(categorias) &
          df["Estado"].isin(estados)   & df["Nivel_Impacto"].isin(impactos)].copy()

if df_f.empty:
    st.warning("La combinacion de filtros no arroja resultados. Ajusta los parametros del panel lateral.")
    st.stop()

# ── Encabezado y KPIs ─────────────────────────────────────────────────────────
st.title("Laboratorio de Comunicación Basada en Evidencia")
st.markdown("Evaluación 1  ·  Materia: Visualización de Datos")
st.markdown("---")

n_ret, pct_ret = len(df_f[df_f["Estado"]=="Retrasado"]), len(df_f[df_f["Estado"]=="Retrasado"])/len(df_f)*100
c1,c2,c3,c4 = st.columns(4)
c1.metric("Proyectos en análisis",  f"{len(df_f):,}")
c2.metric("Presupuesto total",       f"USD {df_f['Presupuesto_USD'].sum()/1e6:.1f}M")
c3.metric("Población beneficiada",   f"{df_f['Poblacion_Beneficiada'].sum():,.0f}")
c4.metric("Tasa de retraso",         f"{pct_ret:.1f}%",
          delta=f"{n_ret} proyectos retrasados", delta_color="inverse")
st.markdown("---")

# ── Helper ────────────────────────────────────────────────────────────────────
def render_q(num, title, context, fig, arg, code_file, key):
    st.markdown(f'<div class="section-num">PREGUNTA {num}</div>', unsafe_allow_html=True)
    st.subheader(title)
    st.markdown(f'<div class="context-box"><b>Contexto del análisis:</b> {context}</div>', unsafe_allow_html=True)
    cf, ca = st.columns([3, 1])
    with cf:
        st.plotly_chart(fig, use_container_width=True, key=f"fig_{key}")
    with ca:
        st.markdown(f'<div class="arg-box"><b>Argumentación Visual</b><br><br>{arg}</div>', unsafe_allow_html=True)
    st.download_button("Descargar codigo Python de esta grafica",
                       data=read_code(code_file), file_name=code_file,
                       mime="text/plain", key=f"dl_{key}")
    st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════════
# PREGUNTA 1 – Jerarquía de Inversión por Categoría
# ════════════════════════════════════════════════════════════════════════════════
cat = df_f.groupby("Categoria")["Presupuesto_M"].sum().sort_values(ascending=True).reset_index()
cat["pct"]   = (cat["Presupuesto_M"] / cat["Presupuesto_M"].sum() * 100).round(1)
cat["color"] = cat["Categoria"].apply(lambda c: C_FOCO if c == cat.iloc[-1]["Categoria"] else C_NEUTRO)

fig1 = go.Figure(go.Bar(
    x=cat["Presupuesto_M"], y=cat["Categoria"], orientation="h",
    marker_color=cat["color"],
    customdata=np.stack([cat["pct"], cat["Presupuesto_M"]], axis=-1),
    hovertemplate="<b>%{y}</b><br>Presupuesto: USD %{customdata[1]:.1f}M<br>Participacion: %{customdata[0]:.1f}%<extra></extra>",
))
l1 = layout("Presupuesto Total Asignado por Categoria de Proyecto",
            xt="Presupuesto total (USD millones)", yt="Categoria de proyecto", h=370)
l1["xaxis"]["tickprefix"] = "$"; l1["xaxis"]["ticksuffix"] = "M"
fig1.update_layout(**l1)

render_q(1, "Jerarquía de Inversión: ¿Qué categoría concentra el mayor presupuesto del portafolio?",
         "¿Existe una categoría que absorbe desproporcionadamente el capital disponible, o la inversión está distribuida de forma equilibrada entre todas las categorías?",
         fig1,
         "<b>Eficiencia:</b> Las barras horizontales son óptimas para categorías nominales. El color verde actúa como atributo pre-atentivo: dirige la atención a la categoría dominante antes de que el lector procese conscientemente los valores.<br><br>"
         "<b>Sintaxis (Gestalt):</b> La ordenación descendente crea jerarquía visual inmediata. La supresión de espinas laterales y la cuadrícula tenue maximizan el Data-to-Ink Ratio.<br><br>"
         "<b>Interacción:</b> Al pasar el cursor se despliegan el presupuesto exacto y la participación porcentual en el portafolio.",
         "pregunta_1_jerarquia.py", "q1")

# ════════════════════════════════════════════════════════════════════════════════
# PREGUNTA 2 – Alertas Temporales de Retraso
# ════════════════════════════════════════════════════════════════════════════════
m_tot = df_f.groupby("YearMonth").size().rename("total")
m_ret = df_f[df_f["Estado"]=="Retrasado"].groupby("YearMonth").size().rename("retrasados")
mon   = pd.concat([m_tot, m_ret], axis=1).fillna(0).reset_index()
mon["pct"]   = (mon["retrasados"] / mon["total"] * 100).round(1)
mon["label"] = mon["YearMonth"].dt.strftime("%b %Y")
umbral       = mon["pct"].mean() + mon["pct"].std()
mon["color"] = mon["pct"].apply(lambda v: C_ALERTA if v >= umbral else C_NEUTRO)

fig2 = go.Figure(go.Bar(
    x=mon["label"], y=mon["pct"], marker_color=mon["color"],
    customdata=np.stack([mon["retrasados"].astype(int), mon["total"].astype(int)], axis=-1),
    hovertemplate="<b>%{x}</b><br>Tasa de retraso: %{y:.1f}%<br>Retrasados: %{customdata[0]}<br>Total del mes: %{customdata[1]}<extra></extra>",
))
fig2.add_hline(y=umbral, line_dash="dash", line_color="#f97316", line_width=1.5,
               annotation_text=f"Umbral de alerta  {umbral:.1f}%",
               annotation_position="top right",
               annotation_font=dict(size=10, color="#f97316"))
l2 = layout("Tasa Mensual de Proyectos Retrasados — Identificacion de Periodos Criticos",
            xt="Mes de inicio del proyecto", yt="Porcentaje de proyectos retrasados (%)", h=400)
l2["yaxis"]["ticksuffix"] = "%"
fig2.update_layout(**l2)

render_q(2, "Alertas Temporales: ¿En qué periodos se dispara la tasa de retraso?",
         "¿Existen meses donde la concentración de proyectos retrasados supera un umbral estadísticamente significativo, revelando un patrón sistémico y no aleatorio?",
         fig2,
         "<b>Figura/Fondo (Gestalt):</b> Las barras grises forman el contexto histórico (fondo). Las barras rojas emergen como figura (anomalías) sin necesidad de buscarlas activamente.<br><br>"
         "<b>Umbral estadístico:</b> La línea punteada representa media + 1 desviación estándar como frontera cognitiva entre normalidad y alerta.<br><br>"
         "<b>Interacción:</b> Al pasar el cursor se despliegan la tasa exacta, los proyectos retrasados y el total de proyectos del mes.",
         "pregunta_2_contraste.py", "q2")

# ════════════════════════════════════════════════════════════════════════════════
# PREGUNTA 3 – Eficiencia de Inversión: Presupuesto vs Población Beneficiada
# ════════════════════════════════════════════════════════════════════════════════
med_p   = df_f["Presupuesto_M"].median()
med_pob = df_f["Poblacion_Beneficiada"].median()

fig3 = go.Figure()
fig3.add_shape(type="rect", x0=med_p, y0=0,
               x1=df_f["Presupuesto_M"].max()*1.12, y1=med_pob,
               fillcolor="rgba(220,38,38,0.05)", line_width=0, layer="below")
fig3.add_annotation(x=df_f["Presupuesto_M"].max()*1.08, y=med_pob*0.12,
                    text="ZONA CRITICA<br>Alto gasto · Bajo alcance",
                    showarrow=False, font=dict(size=9, color="#dc2626"), xanchor="right")
for nivel, color in IMPACTO_COLORS.items():
    s = df_f[df_f["Nivel_Impacto"]==nivel]
    if s.empty: continue
    fig3.add_trace(go.Scatter(
        x=s["Presupuesto_M"], y=s["Poblacion_Beneficiada"], mode="markers",
        name=f"Impacto {nivel}",
        marker=dict(color=color, size=7, opacity=0.72, line=dict(width=0.5, color="white")),
        customdata=np.stack([s["ID_Proyecto"], s["Departamento"], s["Categoria"],
                             s["Estado"], s["Presupuesto_M"].round(2),
                             s["Poblacion_Beneficiada"].astype(int)], axis=-1),
        hovertemplate="<b>%{customdata[0]}</b>  ·  %{customdata[1]}<br>"
                      "Categoría: %{customdata[2]}  |  Estado: %{customdata[3]}<br>"
                      "Presupuesto: USD %{customdata[4]}M<br>"
                      "Poblacion beneficiada: %{customdata[5]:,}<extra></extra>",
    ))
fig3.add_vline(x=med_p,   line_dash="dot", line_color="#9ca3af", line_width=1)
fig3.add_hline(y=med_pob, line_dash="dot", line_color="#9ca3af", line_width=1)
l3 = layout("Eficiencia de Inversion: Presupuesto Asignado vs. Poblacion Beneficiada",
            xt="Presupuesto asignado (USD millones)", yt="Poblacion beneficiada (personas)",
            legend=True, h=460)
l3["xaxis"]["tickprefix"] = "$"; l3["xaxis"]["ticksuffix"] = "M"
l3["yaxis"]["tickformat"] = ",.0f"
fig3.update_layout(**l3)

render_q(3, "Eficiencia de Inversión: ¿A mayor presupuesto, mayor alcance poblacional?",
         "¿La magnitud del presupuesto asignado garantiza proporcionalmente un mayor número de personas beneficiadas, o existen proyectos que consumen recursos sin retorno equivalente en alcance?",
         fig3,
         "<b>Cuadrantes de riesgo:</b> Las líneas de mediana dividen el espacio en cuatro zonas. El cuadrante inferior derecho (sombreado) identifica proyectos con gasto superior al típico pero alcance poblacional inferior al esperado.<br><br>"
         "<b>Doble codificación:</b> La posición x/y comunica las dos métricas cuantitativas. El color codifica el nivel de impacto declarado, permitiendo verificar coherencia entre eficiencia e impacto reportado.<br><br>"
         "<b>Interacción:</b> El cursor revela el proyecto, departamento, categoría, estado y cifras exactas de cada punto.",
         "pregunta_3_eficiencia.py", "q3")

# ════════════════════════════════════════════════════════════════════════════════
# PREGUNTA 4 – Composición del Portafolio por Estado de Ejecución
# ════════════════════════════════════════════════════════════════════════════════
ec   = df_f.groupby(["Categoria","Estado"]).size().reset_index(name="count")
tot  = df_f.groupby("Categoria").size().rename("total").reset_index()
ec   = ec.merge(tot, on="Categoria")
ec["pct"] = (ec["count"] / ec["total"] * 100).round(1)

fig4 = go.Figure()
for est in ["En Planeacion","En Ejecucion","Retrasado","Finalizado"]:
    s   = ec[ec["Estado"]==est]
    ac  = pd.DataFrame({"Categoria": sorted(df_f["Categoria"].unique())})
    s   = ac.merge(s, on="Categoria", how="left").fillna({"pct":0,"count":0,"Estado":est,"total":0})
    fig4.add_trace(go.Bar(
        name=est, x=s["Categoria"], y=s["pct"],
        marker_color=ESTADO_COLORS.get(est,"#94a3b8"),
        customdata=np.stack([s["count"].astype(int), s["pct"], s["total"].astype(int)], axis=-1),
        hovertemplate="<b>"+est+"</b>  ·  %{x}<br>Participacion: %{customdata[1]:.1f}%<br>Proyectos: %{customdata[0]}<br>Total categoria: %{customdata[2]}<extra></extra>",
    ))
l4 = layout("Composicion del Portafolio: Estado de Ejecucion por Categoria (%)",
            xt="Categoria de proyecto", yt="Participacion por estado (%)", legend=True, h=420)
l4["barmode"] = "stack"
l4["yaxis"]["ticksuffix"] = "%"
fig4.update_layout(**l4)

render_q(4,
    "Composicion del Portafolio: Que categorias concentran mas proyectos retrasados?",
    "Existe alguna categoria donde la proporcion de proyectos retrasados o en planeacion "
    "es desproporcionadamente alta, senalando un problema estructural en esa area?",
    fig4,
    "<b>Barras apiladas normalizadas:</b> Al llevar cada categoria al 100%, la comparacion de "
    "proporciones es directa e imparcial independientemente del volumen total.<br><br>"
    "<b>Color como semaforo:</b> El rojo (Retrasado) actua como senal de alerta dentro de la "
    "composicion. El lector identifica la categoria mas comprometida sin realizar calculos.<br><br>"
    "<b>Interaccion:</b> El cursor revela la participacion exacta, el numero de proyectos en ese "
    "estado y el total de la categoria.",
    "pregunta_4_composicion.py", "q4")

# =============================================================================
# PREGUNTA 5 - Distribucion Regional del Presupuesto por Nivel de Impacto
# =============================================================================
ri = df_f.groupby(["Region","Nivel_Impacto"]).agg(
    Presupuesto_M=("Presupuesto_M","sum"), Proyectos=("ID_Proyecto","count")
).reset_index()

fig5 = go.Figure()
for nivel in ["Alto","Medio","Bajo"]:
    s  = ri[ri["Nivel_Impacto"]==nivel]
    ar = pd.DataFrame({"Region": sorted(df_f["Region"].unique())})
    s  = ar.merge(s, on="Region", how="left").fillna({"Presupuesto_M":0,"Proyectos":0,"Nivel_Impacto":nivel})
    fig5.add_trace(go.Bar(
        name="Impacto "+nivel, x=s["Region"], y=s["Presupuesto_M"],
        marker_color=IMPACTO_COLORS[nivel],
        customdata=np.stack([s["Proyectos"].astype(int), s["Presupuesto_M"].round(1)], axis=-1),
        hovertemplate="<b>Impacto "+nivel+"</b>  ·  %{x}<br>Presupuesto: USD %{customdata[1]:.1f}M<br>Proyectos: %{customdata[0]}<extra></extra>",
    ))
l5 = layout("Distribucion Regional del Presupuesto por Nivel de Impacto",
            xt="Region geografica", yt="Presupuesto total (USD millones)", legend=True, h=420)
l5["barmode"] = "group"
l5["yaxis"]["tickprefix"] = "$"
l5["yaxis"]["ticksuffix"] = "M"
fig5.update_layout(**l5)

render_q(5,
    "Capital Territorial: Que regiones combinan alta inversion con bajo impacto?",
    "La distribucion geografica del presupuesto guarda coherencia con el nivel de impacto "
    "reportado, o existen regiones donde el capital invertido no se traduce en resultados de alto impacto?",
    fig5,
    "<b>Barras agrupadas:</b> Permite comparar el volumen de inversion y su distribucion por "
    "nivel de impacto dentro de cada region sin perder la nocion del total.<br><br>"
    "<b>Color como senal de eficiencia:</b> El verde (Alto impacto) indica inversion eficiente; "
    "el rojo (Bajo impacto) senala capital en riesgo.<br><br>"
    "<b>Interaccion:</b> El cursor muestra el nivel de impacto, la region, el presupuesto exacto "
    "y el numero de proyectos asociados.",
    "pregunta_5_region_impacto.py", "q5")
