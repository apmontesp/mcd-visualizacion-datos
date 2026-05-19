# Pregunta 5 - Distribucion Regional del Presupuesto por Nivel de Impacto
# Requiere: pandas, matplotlib, numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

df = pd.read_csv("dataset_evaluacion_unidad1.csv")
df["Presupuesto_M"] = df["Presupuesto_USD"] / 1_000_000

reg_imp = (
    df.groupby(["Region", "Nivel_Impacto"])["Presupuesto_M"]
    .sum()
    .unstack(fill_value=0)
)

COLORES = {"Alto": "#15803d", "Medio": "#ca8a04", "Bajo": "#dc2626"}
niveles = [n for n in ["Alto", "Medio", "Bajo"] if n in reg_imp.columns]
x       = np.arange(len(reg_imp.index))
w       = 0.25

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for i, nivel in enumerate(niveles):
    ax.bar(x + i * w, reg_imp[nivel], width=w,
           color=COLORES[nivel], label=f"Impacto {nivel}")

ax.set_xticks(x + w)
ax.set_xticklabels(reg_imp.index, fontsize=9)
ax.set_xlabel("Region geografica", fontsize=10, color="#6b7280")
ax.set_ylabel("Presupuesto total (USD millones)", fontsize=10, color="#6b7280")
ax.set_title("Distribucion Regional del Presupuesto por Nivel de Impacto",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

ax.legend(frameon=False, fontsize=9)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#e5e7eb")
ax.grid(axis="y", color="#f3f4f6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("pregunta_5_region_impacto.png", dpi=150, bbox_inches="tight")
plt.show()
