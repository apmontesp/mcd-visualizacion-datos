# Pregunta 1 - Jerarquia de Inversion por Categoria
# Requiere: pandas, matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv("dataset_evaluacion_unidad1.csv")
df["Presupuesto_M"] = df["Presupuesto_USD"] / 1_000_000

cat_data = (
    df.groupby("Categoria")["Presupuesto_M"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)
top_cat  = cat_data.iloc[-1]["Categoria"]
C_FOCO   = "#16a34a"
C_NEUTRO = "#cbd5e1"
colors   = [C_FOCO if c == top_cat else C_NEUTRO for c in cat_data["Categoria"]]

fig, ax = plt.subplots(figsize=(9, 4.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.barh(cat_data["Categoria"], cat_data["Presupuesto_M"], color=colors, height=0.55)
ax.set_xlabel("Presupuesto total (USD millones)", fontsize=10, color="#6b7280")
ax.set_ylabel("Categoria de proyecto", fontsize=10, color="#6b7280")
ax.set_title("Presupuesto Total Asignado por Categoria de Proyecto",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#e5e7eb")
ax.grid(axis="x", color="#f3f4f6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
ax.tick_params(axis="y", labelsize=9.5, colors="#374151")
ax.tick_params(axis="x", labelsize=8, colors="#9ca3af")

plt.tight_layout()
plt.savefig("pregunta_1_jerarquia.png", dpi=150, bbox_inches="tight")
plt.show()
