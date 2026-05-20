# Pregunta 4 - Composición del Portafolio por Estado de Ejecución
# Mapa de calor con escala de color semántica por estado
# (morado=Planeación, azul=Ejecución, rojo=Retrasado, verde=Finalizado)
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

# Colormaps semánticos por estado
ESTADO_CMAPS = {
    "En Planeación": mcolors.LinearSegmentedColormap.from_list("plan",  ["#faf5ff", "#c4b5fd", "#7c3aed"]),
    "En Ejecución":  mcolors.LinearSegmentedColormap.from_list("ejec",  ["#eff6ff", "#93c5fd", "#1d4ed8"]),
    "Retrasado":     mcolors.LinearSegmentedColormap.from_list("retr",  ["#fff1f2", "#fca5a5", "#dc2626"]),
    "Finalizado":    mcolors.LinearSegmentedColormap.from_list("final", ["#f0fdf4", "#86efac", "#15803d"]),
}
FALLBACK_CMAP = mcolors.LinearSegmentedColormap.from_list("fb", ["#f8fafc", "#6b7280"])

n_rows, n_cols = pivot.shape
cell_w = 1.0   # ancho de cada columna en coordenadas de imagen
gap    = 0.06  # separación entre columnas

fig, ax = plt.subplots(figsize=(10, 4.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for j, estado in enumerate(pivot.columns):
    col_vals = pivot.values[:, j].reshape(-1, 1)
    col_max  = float(col_vals.max()) or 1.0
    cmap_j   = ESTADO_CMAPS.get(estado, FALLBACK_CMAP)
    norm_j   = mcolors.Normalize(vmin=0, vmax=col_max)

    x_left  = j * (cell_w + gap) - 0.5
    x_right = x_left + cell_w
    ax.imshow(
        col_vals,
        aspect="auto",
        cmap=cmap_j,
        norm=norm_j,
        extent=[x_left, x_right, n_rows - 0.5, -0.5],
        interpolation="nearest",
    )

    for i in range(n_rows):
        v = pivot.values[i, j]
        text_color = "white" if v / col_max > 0.65 else "#111827"
        ax.text(
            j * (cell_w + gap), i,
            f"{v:.1f}%", ha="center", va="center",
            fontsize=10, fontweight="bold", color=text_color,
        )

x_ticks = [j * (cell_w + gap) for j in range(n_cols)]
ax.set_xticks(x_ticks)
ax.set_xticklabels(pivot.columns, fontsize=10, color="#374151")
ax.set_yticks(range(n_rows))
ax.set_yticklabels(pivot.index, fontsize=10, color="#374151")
ax.set_xlim(-0.5 * (cell_w + gap), n_cols * (cell_w + gap) - 0.5)

ax.set_title("Composición del Portafolio por Estado de Ejecución (%)",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.set_xlabel("Estado de ejecución", fontsize=10, color="#6b7280")
ax.set_ylabel("Categoría de proyecto", fontsize=10, color="#6b7280")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(which="both", bottom=False, left=False)
ax.xaxis.set_minor_locator(plt.NullLocator())
ax.yaxis.set_minor_locator(plt.NullLocator())

plt.tight_layout()
plt.savefig("pregunta_4_composicion.png", dpi=150, bbox_inches="tight")
plt.show()
