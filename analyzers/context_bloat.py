from .models import WasteDetection


def analyze_context_bloat(prompt_data: dict) -> list[WasteDetection]:
    detections = []
    messages = prompt_data.get("messages", [])

    total_chars = sum(len(str(m.get("content", ""))) for m in messages)
    est_tokens = total_chars // 4

    if est_tokens > 4000:
        detections.append(WasteDetection(
            waste_class="W1",
            confidence=0.80 if est_tokens > 8000 else 0.60,
            description=f"Contexto estimado grande ({est_tokens} tokens) → probable bloat",
            potential_savings_percent=45 if est_tokens > 8000 else 30,
            suggestion="Reducir contexto innecesario. Usar summarization entre sesiones o retrieval más selectivo."
        ))

    contents = [str(m.get("content", ""))[:300] for m in messages]
    unique_ratio = len(set(contents)) / len(contents) if contents else 1
    if unique_ratio < 0.75:
        detections.append(WasteDetection(
            waste_class="W1",
            confidence=0.70,
            description="Alta repetición de bloques de contexto entre mensajes",
            potential_savings_percent=35,
            suggestion="Extraer bloques estáticos a un prefijo cacheable o implementar session memory."
        ))

    tools = prompt_data.get("tools") or []

    if len(tools) > 6:
        detections.append(WasteDetection(
            waste_class="W1",
            confidence=0.55,
            description="Tool definitions infladas por cantidad → contribuyen a context bloat",
            potential_savings_percent=25,
            suggestion="Optimizar o mover tools a un sistema de tool calling externo si es posible."
        ))

    if any(len(str(t)) > 500 for t in tools):
        detections.append(WasteDetection(
            waste_class="W1",
            confidence=0.65,
            description="Tool definitions largas → agregan contexto costoso en cada request",
            potential_savings_percent=20,
            suggestion="Reducir descripciones extensas o mantener tool schemas más compactos y estables."
        ))

    return detections
