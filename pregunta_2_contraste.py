# Pregunta 2 - Alertas Temporales de Retraso
# Requiere: pandas, matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv("dataset_evaluacion_unidad1.csv", parse_dates=["Fecha_Inicio"])
df["YearMonth"] = df["Fecha_Inicio"].dt.to_period("M")

monthly_total     = df.groupby("YearMonth").size().rename("total")
monthly_retrasado = df[df["Estado"] == "Retrasado"].groupby("YearMonth").size().rename("retrasados")
monthly           = pd.concat([monthly_total, monthly_retrasado], axis=1).fillna(0).reset_index()
monthly["pct"]    = (monthly["retrasados"] / monthly["total"] * 100).round(1)
monthly["label"]  = monthly["YearMonth"].dt.strftime("%b\n%Y")

media  = monthly["pct"].mean()
umbral = media + monthly["pct"].std()
colors = ["#dc2626" if v >= umbral else "#cbd5e1" for v in monthly["pct"]]

fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.bar(range(len(monthly)), monthly["pct"], color=colors, width=0.65, zorder=3)
ax.axhline(umbral, color="#f97316", linewidth=1.5, linestyle="--",
           label=f"Umbral de alerta ({umbral:.1f}%)")

ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["label"], fontsize=8, color="#374151")
ax.set_xlabel("Mes de inicio del proyecto", fontsize=10, color="#6b7280")
ax.set_ylabel("Porcentaje de proyectos retrasados (%)", fontsize=10, color="#6b7280")
ax.set_title("Tasa Mensual de Proyectos Retrasados — Identificacion de Periodos Criticos",
             fontsize=13, fontweight="bold", color="#111827", pad=14)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
ax.set_ylim(0, monthly["pct"].max() + 8)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
for spine in ["left", "bottom"]:
    ax.spines[spine].set_color("#e5e7eb")
ax.grid(axis="y", color="#f3f4f6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("pregunta_2_contraste.png", dpi=150, bbox_inches="tight")
plt.show()
