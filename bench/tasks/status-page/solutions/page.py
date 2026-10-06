"""Public status page. Reference solution: validates the hidden checks, not a benchmark output."""
import re
import sys
from datetime import datetime, timezone
from html import escape

from app.status import STATES, load

LABELS = {"operational": "Operational", "degraded": "Degraded performance", "outage": "Major outage", "maintenance": "Under maintenance"}
SEVERITY = ["outage", "degraded", "maintenance", "operational"]

CSS = """
:root { --bg: #ffffff; --text: #1b1c1f; --ok: #2e9d67; --warn: #b8860b; --down: #d93f3f; --maint: #2f80ed; }
@media (prefers-color-scheme: dark) { :root { --bg: #0b0c0d; --text: #ececee; } }
body { margin: 0; padding: 24px 16px; background: var(--bg); color: var(--text); font-family: system-ui, sans-serif; }
header, footer, .banner, .empty, .services { max-width: 640px; margin: 0 auto 16px; }
.services { padding: 0; list-style: none; }
.service { display: flex; align-items: baseline; gap: 12px; padding: 12px 0; }
.dot { width: 10px; height: 10px; border-radius: 50%; flex: none; }
[data-state="operational"] .dot { background: var(--ok); }
[data-state="degraded"] .dot { background: var(--warn); }
[data-state="outage"] .dot { background: var(--down); animation: pulse 1.6s ease-in-out infinite; }
[data-state="maintenance"] .dot { background: var(--maint); }
@keyframes pulse { 50% { opacity: 0.35; } }
@media (prefers-reduced-motion: reduce) { [data-state="outage"] .dot { animation: none; } }
@media (max-width: 480px) { .service { flex-direction: column; gap: 4px; } }
a:focus-visible { outline: 2px solid var(--text); outline-offset: 2px; }
"""


def _service(service):
    name, state = escape(service["name"]), service["state"]
    url = service.get("url")
    if url:
        rel = ' rel="noopener"' if url.startswith(("http://", "https://")) else ""
        name = f'<a href="{escape(url)}"{rel}>{name}</a>'
    slug = re.sub(r"[^a-z0-9]+", "-", service["name"].lower()).strip("-")
    parts = [f'<li class="service" id="service-{slug}" data-state="{state}">', '<span class="dot" aria-hidden="true"></span>',
             f"<h2>{name}</h2>", f'<span class="state">{LABELS[state]}</span>']
    if service.get("note"):
        parts.append(f'<p class="note">{escape(service["note"])}</p>')
    if service.get("uptime") is not None:
        parts.append(f'<span class="uptime">{service["uptime"]:.2f}% uptime</span>')
    return "".join(parts) + "</li>"


def render(services, generated_at):
    for service in services:
        if service["state"] not in STATES:
            raise ValueError(f"unknown state: {service['state']}")
    count = lambda *states: sum(service["state"] in states for service in services)
    total, attention, maintenance = len(services), count("degraded", "outage"), count("maintenance")
    if not services:
        title, body = "Status · no services", '<p class="empty">No services configured.</p>'
    else:
        title = f"Status · {count('operational')} of {total} operational"
        text = "All systems operational" if not attention else f"{attention} of {total} services need{'s' if attention == 1 else ''} attention"
        if maintenance:
            text += f" · {maintenance} under maintenance"
        kind = "down" if count("outage") else "warn" if count("degraded") else "ok"
        ordered = sorted(services, key=lambda service: (SEVERITY.index(service["state"]), service["name"].lower()))
        body = (f'<p class="banner banner--{kind}" role="status">{text}</p>'
                f'<main><ul class="services">{"".join(_service(service) for service in ordered)}</ul></main>')
    if not services:
        body = f"<main>{body}</main>"
    stamp = escape(generated_at)
    return (f'<!doctype html>\n<html lang="en">\n<head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>{CSS}</style></head>\n'
            f"<body><header><h1>System status</h1></header>{body}"
            f'<footer><time datetime="{stamp}">Updated {stamp}</time></footer></body>\n</html>\n')


if __name__ == "__main__":
    sys.stdout.write(render(load(sys.argv[1]), datetime.now(timezone.utc).isoformat()))
