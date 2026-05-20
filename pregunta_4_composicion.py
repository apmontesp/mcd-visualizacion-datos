# Pregunta 4 - Composición del Portafolio por Estado de Ejecución
# Mapa de calor: categorías × estados, intensidad proporcional al porcentaje
# Requiere: pandas, matplotlib, numpy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

df = pd.read_csv("dataset_evaluacion_unidad1.csv")

ec = df.groupby(["Categoria", "Estado"]).size().reset_index(name="count")
tot = df.groupby("Categoria").size().rename("total").reset_index()
ec = ec.merge(tot, on="Categoria")
ec["pct"] = (ec["count"] / ec["total"] * 100).round(1)

estados_order = ["En Planeación", "En Ejecución", "Retrasado", "Finalizado"]
cats = sorted(df["Categoria"].unique())

pivot = ec.pivot_table(index="Categoria", columns="Estado", values="pct", fill_value=0)
pivot = pivot.reindex(
    index=cats,
    columns=[s for s in estados_order if s in pivot.columns],
    fill_value=0,
)

cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom", ["#f8fafc", "#fef9c3", "#fca5a5", "#dc2626"]
)

fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

im = ax.imshow(pivot.values, aspect="auto", cmap=cmap, vmin=0, vmax=55)

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns, fontsize=10, color="#374151")
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index, fontsize=10, color="#374151")

for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        v = pivot.values[i, j]
        color = "white" if v > 35 else "#111827"
        ax.text(j, i, f"{v:.1f}%", ha="center", va="center",
                fontsize=10, fontweight="bold", color=color)

cbar = plt.colorbar(im, ax=ax, pad=0.02, fraction=0.03)
cbar.ax.tick_params(labelsize=9)
cbar.set_label("% proyectos", fontsize=9, color="#6b7280")
cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

ax.set_title("Composición del Portafolio por Estado de Ejecución (%)",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.set_xlabel("Estado de ejecución", fontsize=10, color="#6b7280")
ax.set_ylabel("Categoría de proyecto", fontsize=10, color="#6b7280")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks(np.arange(-0.5, len(pivot.columns), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(pivot.index), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=2)
ax.tick_params(which="minor", bottom=False, left=False)

plt.tight_layout()
plt.savefig("pregunta_4_composicion.png", dpi=150, bbox_inches="tight")
plt.show()
