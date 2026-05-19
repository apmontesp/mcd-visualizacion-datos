# Pregunta 4 - Composicion del Portafolio por Estado de Ejecucion
# Requiere: pandas, matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

df = pd.read_csv("dataset_evaluacion_unidad1.csv")

estado_cat = (
    df.groupby(["Categoria", "Estado"])
    .size()
    .unstack(fill_value=0)
)
estado_pct = estado_cat.div(estado_cat.sum(axis=1), axis=0) * 100

COLORES = {
    "En Planeación": "#7c3aed",
    "En Ejecución":  "#1d4ed8",
    "Retrasado":     "#dc2626",
    "Finalizado":    "#15803d",
}
orden = ["En Planeación", "En Ejecución", "Retrasado", "Finalizado"]
cols  = [c for c in orden if c in estado_pct.columns]

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bottom = [0.0] * len(estado_pct)
for col in cols:
    vals = estado_pct[col].values
    ax.bar(estado_pct.index, vals, bottom=bottom,
           color=COLORES[col], label=col, width=0.6)
    bottom = [b + v for b, v in zip(bottom, vals)]

ax.set_xlabel("Categoria de proyecto", fontsize=10, color="#6b7280")
ax.set_ylabel("Participacion por estado (%)", fontsize=10, color="#6b7280")
ax.set_title("Composicion del Portafolio: Estado de Ejecucion por Categoria",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

patches = [mpatches.Patch(color=COLORES[c], label=c) for c in cols]
ax.legend(handles=patches, loc="upper right", frameon=False, fontsize=9)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#e5e7eb")
ax.grid(axis="y", color="#f3f4f6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("pregunta_4_composicion.png", dpi=150, bbox_inches="tight")
plt.show()
