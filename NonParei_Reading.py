import json
import matplotlib.pyplot as plt
import numpy as np
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

JSON_FILE1 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy18-[Nonpareil on dataset 183 (T1)_ Curves object (JSON)].json"
JSON_FILE2 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy14-[Nonpareil on dataset 188 (T2)_ Curves object (JSON)].json"
JSON_FILE3 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy16-[Nonpareil on dataset 189 (T3)_ Curves object (JSON)].json"
JSON_FILE4 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy8-[Nonpareil on dataset 198 (T5)_ Curves object (JSON)].json"
JSON_FILE5 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy10-[Nonpareil on dataset 199 (T6)_ Curves object (JSON)].json"
JSON_FILE7 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy6-[Nonpareil on dataset 213 (T8)_ Curves object (JSON)].json"
JSON_FILE6 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy12-[Nonpareil on dataset 200 (T7)_ Curves object (JSON)].json"
JSON_FILE8 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy20-[Nonpareil on dataset 152 (T9)_ Curves object (JSON)].json"
JSON_FILE9 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy1-[Nonpareil on dataset 218 (T10)_ Curves object (JSON)].json"
JSON_FILE10 = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/Data/NonParei/Galaxy222-[Nonpareil on dataset 219 (T12)_ Curves object (JSON)].json"

JSON_FILES = [
    JSON_FILE1,
    JSON_FILE2,
    JSON_FILE3,
    JSON_FILE4,
    JSON_FILE5,
    JSON_FILE6,
    JSON_FILE7,
    JSON_FILE8,
    JSON_FILE9,
    JSON_FILE10
]

OUTPUT_DIR = "/home/bm-003/Desktop/UniversidadDeChile/ProyectoAnillo/Tapetes_Gorbea/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# CREAR FIGURA
# ============================================================

fig, ax = plt.subplots(figsize=(12, 8))

colors = plt.cm.tab20(np.linspace(0, 1, 20))
sample_counter = 0

print("Cargando archivos JSON...\n")

# ============================================================
# LEER TODOS LOS JSON Y GRAFICAR
# ============================================================

summary_data = []

for json_file in JSON_FILES:

    if json_file == "":
        continue

    print(f"Leyendo: {os.path.basename(json_file)}")

    with open(json_file, "r") as f:
        data = json.load(f)

    for sample_name, sample_data in data.items():

        x_obs = np.array(sample_data.get("x.obs", []))
        x_adj = np.array(sample_data.get("x.adj", []))
        x_model = np.array(sample_data.get("x.model", []))

        y_cov = np.array(sample_data.get("y.cov", []))
        y_model = np.array(sample_data.get("y.model", []))

        label = sample_data.get("label", sample_name)

        color = colors[sample_counter % len(colors)]

        L = sample_data.get("L", "N/A")
        diversity = sample_data.get("diversity", "N/A")

        print(f"  Muestra: {label}")
        print(f"     Sequencing effort: {x_obs[0]:.0f} - {x_obs[-1]:.0e} bp")
        print(f"     Coverage: {y_cov[0]:.2f} - {y_cov[-1]:.2f}")
        print(f"     L: {L}")
        print(f"     Diversity: {diversity}")
        print()

        # Curva observada
        if len(x_adj) > 0 and len(y_cov) > 0:
            ax.plot(
                x_adj,
                y_cov,
                "o-",
                color=color,
                linewidth=2,
                markersize=6,
                alpha=0.8,
                label=label,
            )

        # Curva del modelo
        if len(x_model) > 0 and len(y_model) > 0:
            ax.plot(
                x_model,
                y_model,
                "-",
                color=color,
                linewidth=1.5,
                alpha=0.5,
            )

        summary_data.append((os.path.basename(json_file), sample_name, sample_data))

        sample_counter += 1

# ============================================================
# FORMATO DEL GRÁFICO
# ============================================================

ax.set_xlabel("Sequencing effort", fontsize=12, fontweight="bold")
ax.set_ylabel("Estimated average coverage", fontsize=12, fontweight="bold")
ax.set_title(
    "Nonpareil Curves",
    fontsize=14,
    fontweight="bold",
    bbox=dict(boxstyle="round", facecolor="#FFA500", alpha=0.8),
)

ax.set_xscale("log")

ax.grid(True, linestyle="--", alpha=0.3)

ax.set_xlim(1e6, 1e12)
ax.set_ylim(0, 1)

ax.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=8,
    framealpha=0.95,
)

plt.tight_layout()

# ============================================================
# GUARDAR FIGURAS
# ============================================================

png_file = os.path.join(OUTPUT_DIR, "Nonpareil_curves.png")
pdf_file = os.path.join(OUTPUT_DIR, "Nonpareil_curves.pdf")

plt.savefig(png_file, dpi=300, bbox_inches="tight")
plt.savefig(pdf_file, dpi=300, bbox_inches="tight")

print(f"\n✓ PNG guardado: {png_file}")
print(f"✓ PDF guardado: {pdf_file}")

# ============================================================
# GUARDAR RESUMEN
# ============================================================

summary_file = os.path.join(OUTPUT_DIR, "Nonpareil_summary.txt")

with open(summary_file, "w") as f:

    f.write("=" * 70 + "\n")
    f.write("NONPAREIL CURVES ANALYSIS SUMMARY\n")
    f.write("=" * 70 + "\n\n")

    for file_name, sample_name, sample_data in summary_data:

        x_obs = sample_data.get("x.obs", [])
        y_cov = sample_data.get("y.cov", [])

        f.write(f"Archivo: {file_name}\n")
        f.write(f"Muestra: {sample_data.get('label', sample_name)}\n")
        f.write("-" * 70 + "\n")
        f.write(f"File: {sample_data.get('file', 'N/A')}\n")
        f.write(f"Color: {sample_data.get('col', 'N/A')}\n")
        f.write(f"Sequencing effort: {x_obs[0]:.0f} - {x_obs[-1]:.0e} bp\n")
        f.write(f"Coverage: {y_cov[0]:.2f} - {y_cov[-1]:.2f}\n")
        f.write(f"Average read length (L): {sample_data.get('L', 'N/A')}\n")
        f.write(f"Adjusted read length (AL): {sample_data.get('AL', 'N/A')}\n")
        f.write(f"Total reads (R): {sample_data.get('R', 'N/A')}\n")
        f.write(f"Total base pairs (LR): {sample_data.get('LR', 'N/A')}\n")
        f.write(f"Diversity: {sample_data.get('diversity', 'N/A')}\n")
        f.write(f"Kappa: {sample_data.get('kappa', 'N/A')}\n")
        f.write(f"Completeness (C): {sample_data.get('C', 'N/A')}\n")
        f.write(f"Model R-squared: {sample_data.get('modelR', 'N/A')}\n")
        f.write(f"Consistent: {sample_data.get('consistent', 'N/A')}\n")
        f.write(f"Kernel: {sample_data.get('kernel', 'N/A')}\n")
        f.write(f"Version: {sample_data.get('version', 'N/A')}\n")
        f.write("\n")

print(f"Resumen guardado: {summary_file}")

# ============================================================
# GUARDAR JSON COMBINADO
# ============================================================

combined_json = {}

for json_file in JSON_FILES:

    if json_file == "":
        continue

    with open(json_file, "r") as f:
        data = json.load(f)

    combined_json.update(data)

json_output = os.path.join(OUTPUT_DIR, "Nonpareil_data.json")

with open(json_output, "w") as f:
    json.dump(combined_json, f, indent=2)

print(f"✓ JSON combinado guardado: {json_output}")

print("\n" + "=" * 70)
print("✓ Proceso completado exitosamente")
print("=" * 70)
print(f"\nSe procesaron {sample_counter} muestra(s).")
print(f"Archivos generados en: {OUTPUT_DIR}")

plt.show()