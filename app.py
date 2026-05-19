"""
Evaluación 1 – Laboratorio de Comunicación Basada en Evidencia
Materia: Visualización de Datos
Dataset: Proyectos gubernamentales Colombia 2023-2024
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────
# Configuración global de la app
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Lab. Comunicación Basada en Evidencia",
    page_icon="📊",
    layout="wide",
)

# ─────────────────────────────────────────────
# Estilos globales
# ─────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f1117; }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.2rem !important; }
    .reto-badge {
        display: inline-block;
        background: #1a1a2e;
        color: #a78bfa;
        border: 1px solid #4c1d95;
        border-radius: 6px;
        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .justif-box {
        background: #0f1117;
        border-left: 3px solid #a78bfa;
        padding: 12px 16px;
        border-radius: 0 6px 6px 0;
        font-size: 0.88rem;
        color: #c4c4d4;
        margin-top: 1rem;
    }
    .justif-box b { color: #c4b5fd; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Carga de datos (cacheado)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent
    df = pd.read_csv(base / "dataset_evaluacion_unidad1.csv", parse_dates=["Fecha_Inicio"])
    df["YearMonth"] = df["Fecha_Inicio"].dt.to_period("M")
    return df

df = load_data()

# ─────────────────────────────────────────────
# Sidebar – navegación
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Evaluación 1")
    st.markdown("**Laboratorio de Comunicación**  \nBasada en Evidencia")
    st.markdown("---")
    pagina = st.radio(
        "Ir a:",
        ["🏠 Inicio", "📏 Reto 1 – Jerarquía", "⚖️ Reto 2 – Contraste"],
        index=0,
    )
    st.markdown("---")
    st.caption("Dataset: Proyectos Gov. Colombia\n500 proyectos · 2023–2024")

# ═══════════════════════════════════════════════════════════
# PÁGINA: INICIO
# ═══════════════════════════════════════════════════════════
if pagina == "🏠 Inicio":
    st.title("Laboratorio de Comunicación Basada en Evidencia")
    st.markdown("""
    Esta app presenta los dos primeros retos de la Evaluación 1 de la asignatura
    **Visualización de Datos**, aplicando los principios de la Unidad 1.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        #### 📏 Reto 1 – Jerarquía
        **Ingeniería de la Atención**
        Visualización donde la dominancia visual de una categoría
        estratégica es indiscutible. Se aplican:
        - Ordenación lógica de datos
        - Reducción de ruido (Data-to-Ink Ratio)
        - Color como herramienta de énfasis
        """)
    with col2:
        st.markdown("""
        #### ⚖️ Reto 2 – Contraste
        **Detección de Anomalías**
        Contraste de Figura y Fondo para que un punto de quiebre
        demande atención inmediata. Se aplican:
        - Datos históricos en tonos neutros
        - Alta vibrancia en la anomalía
        - Anotaciones integradas al gráfico
        """)

    st.markdown("---")
    st.subheader("Vista rápida del dataset")
    st.dataframe(df.drop(columns=["YearMonth"]).head(8), use_container_width=True)
    st.caption(f"Total: {len(df)} proyectos · Período: {df['Fecha_Inicio'].min().date()} → {df['Fecha_Inicio'].max().date()}")


# ═══════════════════════════════════════════════════════════
# PÁGINA: RETO 1 – JERARQUÍA
# ═══════════════════════════════════════════════════════════
elif pagina == "📏 Reto 1 – Jerarquía":

    st.markdown('<div class="reto-badge">RETO 1 · PONDERACIÓN 33%</div>', unsafe_allow_html=True)
    st.title("Jerarquía: Ingeniería de la Atención")
    st.markdown(
        "**Pregunta guía:** ¿Qué categoría de proyecto concentra el mayor volumen de inversión pública en Colombia?"
    )

    # ── Preparación de datos ──────────────────────────────
    cat_budget = (
        df.groupby("Categoria")["Presupuesto_USD"]
        .sum()
        .sort_values(ascending=True)   # ascending para barh (el mayor queda arriba)
        .reset_index()
    )
    cat_budget["Presupuesto_M"] = cat_budget["Presupuesto_USD"] / 1_000_000

    CATEGORIA_FOCO = "Medio Ambiente"
    COLOR_FOCO   = "#16a34a"   # verde intenso
    COLOR_NEUTRO = "#d1d5db"   # gris claro

    colors = [COLOR_FOCO if c == CATEGORIA_FOCO else COLOR_NEUTRO
              for c in cat_budget["Categoria"]]

    # ── Figura ───────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.barh(
        cat_budget["Categoria"],
        cat_budget["Presupuesto_M"],
        color=colors,
        height=0.55,
        zorder=3,
    )

    # Etiquetas de valor al final de cada barra
    for bar, val, cat in zip(bars, cat_budget["Presupuesto_M"], cat_budget["Categoria"]):
        peso = "bold" if cat == CATEGORIA_FOCO else "normal"
        color_txt = "#15803d" if cat == CATEGORIA_FOCO else "#6b7280"
        ax.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"${val:.0f}M",
            va="center", ha="left",
            fontsize=9, color=color_txt, fontweight=peso,
        )

    # Anotación de insight
    foco_val = cat_budget.loc[cat_budget["Categoria"] == CATEGORIA_FOCO, "Presupuesto_M"].values[0]
    ax.annotate(
        "  Mayor inversión\n  del portafolio",
        xy=(foco_val, cat_budget[cat_budget["Categoria"] == CATEGORIA_FOCO].index[0]),
        xytext=(foco_val - 60, cat_budget[cat_budget["Categoria"] == CATEGORIA_FOCO].index[0] + 0.55),
        fontsize=8.5, color="#15803d", fontweight="bold",
        arrowprops=dict(arrowstyle="-", color="#15803d", lw=1.2),
    )

    # Limpieza visual (Data-to-Ink Ratio)
    ax.set_xlabel("Presupuesto Total (USD millones)", fontsize=9, color="#374151")
    ax.set_title(
        "Presupuesto Total por Categoría de Proyecto",
        fontsize=13, fontweight="bold", color="#111827", pad=14,
    )
    ax.set_xlim(0, cat_budget["Presupuesto_M"].max() * 1.22)
    ax.tick_params(axis="y", labelsize=9.5, colors="#374151")
    ax.tick_params(axis="x", labelsize=8, colors="#9ca3af")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

    # Eliminar espinas innecesarias (Gestalt: simplicidad)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#e5e7eb")
    ax.grid(axis="x", color="#f3f4f6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # ── Justificación ─────────────────────────────────────
    st.markdown("""
    <div class="justif-box">
    <b>Eficiencia:</b> Gráfico de barras horizontales — tipo óptimo para comparar categorías nominales.
    El atributo pre-atentivo <b>color</b> dirige el ojo instantáneamente a <i>Medio Ambiente</i>
    sin necesidad de leer todas las etiquetas.<br><br>
    <b>Sintaxis (Gestalt):</b> Las barras se ordenan de mayor a menor presupuesto (de arriba hacia abajo),
    creando una jerarquía visual intuitiva. Las espinas laterales y superiores se eliminan para reducir
    la carga cognitiva (Ley de Simplicidad). La cuadrícula vertical tenue actúa como guía, no como decoración.<br><br>
    <b>Reducción de ruido:</b> Sin rellenos de fondo, sin bordes en barras, sin leyenda redundante —
    cada píxel tiene función informativa (Data-to-Ink Ratio maximizado).
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA: RETO 2 – CONTRASTE
# ═══════════════════════════════════════════════════════════
elif pagina == "⚖️ Reto 2 – Contraste":

    st.markdown('<div class="reto-badge">RETO 2 · PONDERACIÓN 33%</div>', unsafe_allow_html=True)
    st.title("Contraste: Detección de Anomalías")
    st.markdown(
        "**Pregunta guía:** ¿En qué momento del período aumenta de forma crítica la tasa de proyectos retrasados?"
    )

    # ── Preparación de datos ──────────────────────────────
    monthly_total     = df.groupby("YearMonth").size().rename("total")
    monthly_retrasado = df[df["Estado"] == "Retrasado"].groupby("YearMonth").size().rename("retrasados")
    monthly           = pd.concat([monthly_total, monthly_retrasado], axis=1).fillna(0)
    monthly["pct"]    = (monthly["retrasados"] / monthly["total"] * 100).round(1)
    monthly           = monthly.reset_index()
    monthly["label"]  = monthly["YearMonth"].dt.strftime("%b\n%Y").str.replace("\n", "\n")
    monthly["idx"]    = range(len(monthly))

    # Umbral de anomalía: media + 1 std
    media = monthly["pct"].mean()
    std   = monthly["pct"].std()
    umbral = media + std

    ANOMALIA_COLOR  = "#dc2626"   # rojo intenso
    NEUTRO_COLOR    = "#cbd5e1"   # gris azulado neutro
    UMBRAL_COLOR    = "#f97316"   # naranja para línea de umbral

    es_anomalia = monthly["pct"] >= umbral
    bar_colors  = [ANOMALIA_COLOR if a else NEUTRO_COLOR for a in es_anomalia]

    # ── Figura ───────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.bar(
        monthly["idx"],
        monthly["pct"],
        color=bar_colors,
        width=0.65,
        zorder=3,
    )

    # Línea de umbral (referencia estadística)
    ax.axhline(
        umbral, color=UMBRAL_COLOR, linewidth=1.5,
        linestyle="--", zorder=4,
        label=f"Umbral de alerta ({umbral:.1f}%)",
    )

    # Etiquetas de % en barras anómalas
    for bar, val, anom in zip(bars, monthly["pct"], es_anomalia):
        if anom:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.6,
                f"{val:.0f}%",
                ha="center", va="bottom",
                fontsize=8.5, color=ANOMALIA_COLOR, fontweight="bold",
            )

    # Anotación principal en el pico máximo
    pico_idx  = monthly["pct"].idxmax()
    pico_val  = monthly.loc[pico_idx, "pct"]
    pico_x    = monthly.loc[pico_idx, "idx"]
    pico_mes  = monthly.loc[pico_idx, "label"].replace("\n", " ")

    ax.annotate(
        f"⚠  Pico crítico: {pico_val:.0f}% de\n    proyectos retrasados",
        xy=(pico_x, pico_val),
        xytext=(pico_x - 4.5, pico_val + 4),
        fontsize=9, color=ANOMALIA_COLOR, fontweight="bold",
        arrowprops=dict(
            arrowstyle="-|>", color=ANOMALIA_COLOR,
            connectionstyle="arc3,rad=-0.2", lw=1.5,
        ),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ANOMALIA_COLOR, lw=1),
    )

    # Ejes y formato
    ax.set_xticks(monthly["idx"])
    ax.set_xticklabels(monthly["label"], fontsize=8, color="#374151")
    ax.set_ylabel("% Proyectos Retrasados", fontsize=9, color="#374151")
    ax.set_ylim(0, monthly["pct"].max() + 12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.tick_params(axis="y", labelsize=8, colors="#9ca3af")

    ax.set_title(
        "Tasa Mensual de Proyectos Retrasados — Alerta de Quiebre",
        fontsize=13, fontweight="bold", color="#111827", pad=14,
    )

    # Leyenda mínima
    patch_neutro   = mpatches.Patch(color=NEUTRO_COLOR, label="Tasa histórica normal")
    patch_anomalia = mpatches.Patch(color=ANOMALIA_COLOR, label="Tasa anómala (> umbral)")
    ax.legend(
        handles=[patch_neutro, patch_anomalia],
        loc="upper left", frameon=False,
        fontsize=8.5, labelcolor="#374151",
    )

    # Limpieza
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#e5e7eb")
    ax.spines["bottom"].set_color("#e5e7eb")
    ax.grid(axis="y", color="#f3f4f6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # ── Estadísticas de soporte ───────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasa promedio", f"{media:.1f}%", help="Promedio mensual del período")
    col2.metric("Umbral de alerta", f"{umbral:.1f}%", help="Media + 1 desviación estándar")
    col3.metric(
        "Meses en alerta",
        f"{es_anomalia.sum()} / {len(monthly)}",
        delta=f"{es_anomalia.sum()/len(monthly)*100:.0f}% del período",
        delta_color="inverse",
    )

    # ── Justificación ─────────────────────────────────────
    st.markdown("""
    <div class="justif-box">
    <b>Eficiencia:</b> Gráfico de barras temporales — ideal para detectar cambios discretos mes a mes.
    El atributo pre-atentivo <b>color</b> (rojo vs. gris) activa la detección de anomalías sin
    procesamiento consciente.<br><br>
    <b>Sintaxis (Gestalt – Figura/Fondo):</b> Las barras grises forman el "fondo" (contexto histórico),
    mientras que las barras rojas emergen como "figura" (anomalías). La línea de umbral punteada
    actúa como frontera cognitiva clara. La anotación integrada en el gráfico elimina la necesidad
    de un texto exterior.<br><br>
    <b>Contraste de alerta:</b> El rojo (#dc2626) frente al gris neutro (#cbd5e1) maximiza el
    contraste simultáneo, garantizando que los picos de Oct-2023 y Ene-2024 (24.2%) sean
    visualmente irresistibles. Los meses normales se perciben como ruido de fondo, no como información primaria.
    </div>
    """, unsafe_allow_html=True)
