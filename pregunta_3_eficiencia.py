# Pregunta 3 - Eficiencia de Inversion: Presupuesto vs. Poblacion Beneficiada
# Requiere: pandas, matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv("dataset_evaluacion_unidad1.csv")
df["Presupuesto_M"] = df["Presupuesto_USD"] / 1_000_000

med_p   = df["Presupuesto_M"].median()
med_pob = df["Poblacion_Beneficiada"].median()

COLORES = {"Alto": "#15803d", "Medio": "#ca8a04", "Bajo": "#dc2626"}

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.axhspan(0, med_pob, xmin=0.5, alpha=0.05, color="#dc2626")
ax.text(df["Presupuesto_M"].max() * 0.97, med_pob * 0.08,
        "ZONA CRITICA  Alto gasto / Bajo alcance",
        ha="right", fontsize=8, color="#dc2626")

for nivel, color in COLORES.items():
    mask = df["Nivel_Impacto"] == nivel
    ax.scatter(df[mask]["Presupuesto_M"], df[mask]["Poblacion_Beneficiada"],
               color=color, alpha=0.7, s=40, label=f"Impacto {nivel}",
               edgecolors="white", linewidths=0.5)

ax.axvline(med_p,   color="#9ca3af", linewidth=1, linestyle=":")
ax.axhline(med_pob, color="#9ca3af", linewidth=1, linestyle=":")

ax.set_xlabel("Presupuesto asignado (USD millones)", fontsize=10, color="#6b7280")
ax.set_ylabel("Poblacion beneficiada (personas)", fontsize=10, color="#6b7280")
ax.set_title("Eficiencia de Inversion: Presupuesto Asignado vs. Poblacion Beneficiada",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

ax.legend(frameon=False, fontsize=9)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#e5e7eb")
ax.grid(color="#f3f4f6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("pregunta_3_eficiencia.png", dpi=150, bbox_inches="tight")
plt.show()
