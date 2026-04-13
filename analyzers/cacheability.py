import re
from .models import WasteDetection


def analyze_cache_breaker(prompt_data: dict) -> list[WasteDetection]:
    detections = []
    messages = prompt_data.get("messages", []) if isinstance(prompt_data, dict) else []

    text = " ".join(str(m.get("content", "")) for m in messages[:4]).lower()

    if re.search(r"(timestamp|current.?time|date|now=|\d{4}-\d{2}-\d{2})", text):
        detections.append(WasteDetection(
            waste_class="W2",
            confidence=0.85,
            description="Elemento dinámico (timestamp, fecha, etc.) detectado en prefijo temprano → rompe prompt caching",
            potential_savings_percent=65,
            suggestion="Mover todo el contenido dinámico al final del prompt. Mantener 'Static first, dynamic last'."
        ))

    if re.search(r"(request.?id|session.?id|req-|sess-)", text):
        detections.append(WasteDetection(
            waste_class="W2",
            confidence=0.75,
            description="Request ID o Session ID en prefijo → invalida cache en cada llamada",
            potential_savings_percent=55,
            suggestion="Eliminar IDs del prefijo o moverlos al mensaje del usuario."
        ))

    tools = prompt_data.get("tools") or []
    if len(tools) > 4 or any(len(str(t)) > 800 for t in tools):
        detections.append(WasteDetection(
            waste_class="W2",
            confidence=0.60,
            description="Tool definitions numerosas o muy largas → riesgo alto de romper cache si varían ligeramente",
            potential_savings_percent=40,
            suggestion="Mantener tool schemas estables y colocarlas en la parte cacheable del prefijo."
        ))

    return detections
