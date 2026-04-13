import json
import sys
from pathlib import Path
from typing import Dict, Any, List

from rich.console import Console
from rich.markdown import Markdown

from analyzers.cacheability import analyze_cache_breaker
from analyzers.context_bloat import analyze_context_bloat
from analyzers.models import AuditResult, WasteDetection

console = Console()


def load_input(file_path: str) -> Dict[str, Any]:
    """Carga JSON de prompt o trace y normaliza formatos."""
    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]Error: Archivo no encontrado: {file_path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        console.print(f"[red]Error: El archivo no es JSON válido: {file_path}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error al leer el archivo: {e}")
        sys.exit(1)

    if isinstance(data, dict):
        if "messages" in data or "tools" in data:
            return data
        if isinstance(data.get("input"), dict):
            input_data = data["input"]
            if "messages" in input_data or "tools" in input_data:
                return input_data

    console.print("[red]Error: Formato no soportado.")
    console.print("Se esperaba JSON con 'messages'/'tools' en la raíz o dentro de un objeto 'input'.")
    sys.exit(1)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        console.print("[red]Uso: llm-waste-audit scan <archivo.json> [--markdown]")
        console.print("Ejemplo: llm-waste-audit scan examples/langfuse/sample_trace.json")
        sys.exit(1)

    file_path = sys.argv[2]
    export_md = "--markdown" in sys.argv

    data = load_input(file_path)

    w2_detections: List[WasteDetection] = analyze_cache_breaker(data)
    w1_detections: List[WasteDetection] = analyze_context_bloat(data)
    all_detections = w1_detections + w2_detections

    cache_score = 100
    for det in w2_detections:
        if det.waste_class == "W2":
            cache_score -= int(det.confidence * 28)
    cache_score = max(0, min(100, cache_score))

    bloat_score = 0
    for det in w1_detections:
        if det.waste_class == "W1":
            bloat_score += int(det.confidence * 25)
    bloat_score = min(100, bloat_score)

    total_savings = sum((d.potential_savings_percent or 0) for d in all_detections)
    avg_savings = round(total_savings / len(all_detections)) if all_detections else 0
    savings_range = f"{max(15, avg_savings-15)}–{min(80, avg_savings+15)}%" if all_detections else "0%"

    result = AuditResult(
        cacheability_score=cache_score,
        context_bloat_score=bloat_score,
        flagged_wastes=all_detections,
        total_estimated_savings=savings_range,
        report="Reporte generado por llm-waste-audit v0.1"
    )

    console.print(Markdown("# LLM Waste Audit Report\n"))
    console.print(f"[bold]Cacheability Score:[/bold] {result.cacheability_score}/100 (higher is better)")
    console.print(f"[bold]Context Bloat Score:[/bold] {result.context_bloat_score}/100 (higher is worse)")
    console.print(f"[bold]Estimated savings potential:[/bold] {result.total_estimated_savings}\n")

    if result.flagged_wastes:
        console.print("### Waste detectado:")
        for w in result.flagged_wastes:
            console.print(f"• **[ {w.waste_class} ]** — {w.description}")
            console.print(f"  → Ahorro estimado: ~{w.potential_savings_percent}%")
            console.print(f"  → Sugerencia: {w.suggestion}\n")
    else:
        console.print("[green]¡No se detectó desperdicio claro en W1 o W2!")

    if export_md:
        md_path = Path("waste_report.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# LLM Waste Audit Report\n\n")
            f.write(f"**Cacheability Score:** {result.cacheability_score}/100 (higher is better)  \n")
            f.write(f"**Context Bloat Score:** {result.context_bloat_score}/100 (higher is worse)  \n")
            f.write(f"**Estimated savings potential:** {result.total_estimated_savings}\n\n")

            if result.flagged_wastes:
                f.write("## Detected Waste\n\n")
                for w in result.flagged_wastes:
                    f.write(f"### {w.waste_class}\n")
                    f.write(f"- **Description:** {w.description}\n")
                    f.write(f"- **Confidence:** {w.confidence:.2f}\n")
                    if w.potential_savings_percent is not None:
                        f.write(f"- **Potential savings:** ~{w.potential_savings_percent}%\n")
                    f.write(f"- **Suggestion:** {w.suggestion}\n\n")
            else:
                f.write("No clear W1 or W2 waste detected.\n")

        console.print(f"[green]→ Reporte Markdown guardado en: {md_path}")


if __name__ == "__main__":
    main()
