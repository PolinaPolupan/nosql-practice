import time
import redis
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

CACHE_TTL = 30
PAGE_KEY = "heavy_page"

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)

TEMPLATES_DIR = Path("templates")
HEAVY_TEMPLATE = (TEMPLATES_DIR / "heavy_page.html").read_text(encoding="utf-8")
STATS_TEMPLATE = (TEMPLATES_DIR / "stats.html").read_text(encoding="utf-8")


def build_heavy_html() -> tuple[str, float]:
    start = time.perf_counter()

    rows = []
    for i in range(12000):
        val = (i * i) % 9973
        rows.append(f"<tr><td>{i}</td><td>Item {i}</td><td>{val}</td></tr>")

    time.sleep(1)
    render_ms = (time.perf_counter() - start) * 1000

    html = (
        HEAVY_TEMPLATE
        .replace("{{ROWS}}", "".join(rows))
        .replace("{{RENDER_MS}}", f"{render_ms:.1f}")
    )
    return html, render_ms


@app.get("/", response_class=HTMLResponse)
def heavy_cached_page():
    req_start = time.perf_counter()
    cached = r.get(PAGE_KEY)

    if cached:
        total_ms = (time.perf_counter() - req_start) * 1000
        body = (
            cached
            .replace("{{CACHE_STATUS}}", '<span class="status status-hit">HIT</span>')
            .replace("{{TOTAL_MS}}", f"{total_ms:.2f}")
        )
        return HTMLResponse(content=body)

    html, _ = build_heavy_html()
    r.setex(PAGE_KEY, CACHE_TTL, html)

    total_ms = (time.perf_counter() - req_start) * 1000
    body = (
        html
        .replace("{{CACHE_STATUS}}", '<span class="status status-miss">MISS</span>')
        .replace("{{TOTAL_MS}}", f"{total_ms:.2f}")
    )
    return HTMLResponse(content=body)


@app.get("/invalidate")
def invalidate():
    r.delete(PAGE_KEY)
    return {"status": "ok", "message": "Page cache cleared"}


@app.get("/stats", response_class=HTMLResponse)
def stats():
    info = r.info()
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total * 100) if total else 0

    html = (
        STATS_TEMPLATE
        .replace("{{HITS}}", str(hits))
        .replace("{{MISSES}}", str(misses))
        .replace("{{HIT_RATIO}}", f"{hit_ratio:.1f}")
        .replace("{{DBSIZE}}", str(r.dbsize()))
    )
    return HTMLResponse(content=html)