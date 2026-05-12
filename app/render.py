from __future__ import annotations

import html
from pathlib import Path

from app.services.ledger_service import build_service

service = build_service()


def page_shell(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #09111d;
      --panel: #101d2f;
      --panel-2: #17263c;
      --line: #29486f;
      --ink: #f3ecde;
      --muted: #b5c2d7;
      --blue: #6db2ff;
      --pink: #f0bfd7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(54, 103, 164, 0.18), transparent 30%),
        linear-gradient(180deg, #08111c 0%, #0b1522 100%);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
    }}
    .frame {{
      width: 1440px;
      min-height: 920px;
      margin: 0 auto;
      padding: 48px;
    }}
    .shell {{
      background: rgba(13, 24, 39, 0.94);
      border: 1px solid var(--line);
      border-radius: 36px;
      padding: 34px 36px 36px;
    }}
    .eyebrow {{
      margin: 0 0 22px;
      font: 700 13px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.35em;
      text-transform: uppercase;
      color: var(--blue);
    }}
    h1 {{
      margin: 0;
      font-size: 70px;
      line-height: 1.02;
      max-width: 1180px;
      letter-spacing: -0.05em;
    }}
    p.lead {{
      margin: 24px 0 0;
      max-width: 1060px;
      color: var(--muted);
      font: 400 19px/1.55 "Segoe UI", sans-serif;
    }}
    .pills {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin: 22px 0 26px;
    }}
    .pill {{
      background: #1d2d45;
      border: 1px solid #335a8d;
      color: #f5f7fb;
      padding: 10px 16px;
      border-radius: 999px;
      font: 700 15px/1 "Segoe UI", sans-serif;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin: 8px 0 34px;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid #335885;
      border-radius: 24px;
      padding: 22px 22px 18px;
      min-height: 170px;
    }}
    .card h2 {{
      margin: 0 0 12px;
      color: #a8cbff;
      font: 700 12px/1.2 "Segoe UI", sans-serif;
      letter-spacing: 0.24em;
      text-transform: uppercase;
    }}
    .metric {{
      font-size: 58px;
      line-height: 1;
      margin: 0 0 10px;
    }}
    .card p, .card li, .table, .lane {{
      color: var(--muted);
      font: 400 18px/1.45 "Segoe UI", sans-serif;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1.25fr 0.85fr;
      gap: 18px;
    }}
    .table {{
      display: grid;
      gap: 12px;
    }}
    .row {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr 0.8fr 0.8fr;
      gap: 14px;
      align-items: center;
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
    }}
    .row strong {{
      color: var(--ink);
      display: block;
      font: 700 24px/1.1 Georgia, serif;
    }}
    .small {{
      font-size: 15px;
      color: #87a2c7;
    }}
    .lane {{
      padding: 16px 18px;
      background: #0c1728;
      border: 1px solid #223c5d;
      border-radius: 18px;
      margin-bottom: 12px;
    }}
    .lane strong {{
      display: block;
      color: var(--ink);
      font: 700 24px/1.15 Georgia, serif;
      margin-bottom: 6px;
    }}
    pre {{
      margin: 0;
      color: #d7e8ff;
      font: 16px/1.5 Consolas, monospace;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="frame">
    <div class="shell">
      <p class="eyebrow">{html.escape(eyebrow)}</p>
      {body}
    </div>
  </div>
</body>
</html>"""


def render_overview() -> str:
    summary = service.summary()
    events = service.events()[:3]
    rows = "".join(
        f"""
        <div class="row">
          <div>
            <strong>{html.escape(event['studentName'])}</strong>
            <div class="small">{html.escape(event['eventType'])}</div>
          </div>
          <div>{html.escape(event['ownerLane'])}</div>
          <div>{event['daysOpen']} days</div>
          <div>{event['closureScore']}</div>
        </div>
        """
        for event in events
    )
    body = f"""
      <h1>Keep the full intervention history visible so schools can see which support actions actually worked.</h1>
      <p class="lead">
        Learner Intervention Ledger records outreach attempts, owner-lane handoffs, resolution quality, and cycle time
        so student success teams can stop repeating stalled playbooks and double down on the ones that move risk down.
      </p>
      <div class="pills">
        <div class="pill">intervention history tracking</div>
        <div class="pill">lane handoff visibility</div>
        <div class="pill">closure quality scoring</div>
        <div class="pill">closed-loop outcome proof</div>
      </div>
      <div class="stats">
        <div class="card"><h2>interventions logged</h2><div class="metric">{summary['interventionCount']}</div><p>Each case keeps its channel, lane, and outcome history visible.</p></div>
        <div class="card"><h2>open cases</h2><div class="metric">{summary['openCaseCount']}</div><p>Active work still waiting on resolution or escalation.</p></div>
        <div class="card"><h2>strong resolutions</h2><div class="metric">{summary['strongResolutionCount']}</div><p>Cases that genuinely improved and can feed future playbooks.</p></div>
        <div class="card"><h2>avg. closure score</h2><div class="metric">{summary['averageClosureScore']}</div><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
      <div class="grid-2">
        <div class="card"><h2>active ledger</h2><div class="table">{rows}</div></div>
        <div class="card"><h2>lead recommendation</h2><p>{html.escape(summary['leadRecommendation'])}</p></div>
      </div>
    """
    return page_shell("Learner Intervention Ledger", "Learner Intervention Ledger", body)


def render_outcomes() -> str:
    breakdown = service.outcome_breakdown()
    lanes = service.lane_breakdown()
    lane_cards = "".join(
        f'<div class="lane"><strong>{html.escape(lane["ownerLane"])}</strong><div>{lane["count"]} interventions</div></div>'
        for lane in lanes
    )
    outcome_cards = "".join(
        f'<div class="lane"><strong>{html.escape(item["effectiveness"])}</strong><div>{item["count"]} cases in this resolution band</div></div>'
        for item in breakdown
    )
    body = f"""
      <h1>See which outreach patterns closed the loop and which ones just created more activity without resolution.</h1>
      <p class="lead">
        Outcome bands and lane counts make it easier to compare advising, faculty, finance, and care-team patterns instead of
        treating all intervention volume as success.
      </p>
      <div class="grid-2">
        <div class="card"><h2>outcome quality</h2>{outcome_cards}</div>
        <div class="card"><h2>owner lane load</h2>{lane_cards}</div>
      </div>
    """
    return page_shell("Outcome Quality", "Outcome Breakdown", body)


def render_evidence() -> str:
    event = service.intervention("int-4033") or service.events()[0]
    body = f"""
      <h1>The ledger preserves enough context to explain why a case stayed open, improved, or escalated again.</h1>
      <p class="lead">
        One intervention record can hold the lane, channel, response pattern, risk shift, closure quality, and next-best action
        without burying the student story in an opaque CRM timeline.
      </p>
      <div class="card">
        <h2>case evidence</h2>
        <pre>{html.escape(str(event))}</pre>
      </div>
    """
    return page_shell("Case Evidence", "Case Evidence", body)


def render_api_summary() -> str:
    payload = service.sample_payload()
    body = f"""
      <h1>The API turns intervention history into something dashboards, CRMs, and advising ops can actually consume.</h1>
      <p class="lead">
        Summary metrics and open-case extracts stay close together so higher-ed systems can reason about both workload and effectiveness.
      </p>
      <div class="card">
        <h2>sample payload</h2>
        <pre>{html.escape(str(payload))}</pre>
      </div>
    """
    return page_shell("API Summary", "API Summary", body)


def write_static_proof_pages(output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-outcomes.html": render_outcomes(),
        "03-evidence.html": render_evidence(),
        "04-api-summary.html": render_api_summary(),
    }
    written: list[Path] = []
    for name, contents in pages.items():
        path = output_dir / name
        path.write_text(contents, encoding="utf-8")
        written.append(path)
    return written
