"""Generate the light and dark profile banners for github.com/ln-bodicherla."""

import sys
from pathlib import Path

W, H = 1280, 340

THEMES = {
    "dark": dict(
        bg="#070707", glow1="rgba(255,255,255,0.13)", glow2="rgba(255,255,255,0.07)",
        window="#141414", window_op="0.86", border="rgba(255,255,255,0.10)",
        bar="#1b1b1b", dot="rgba(255,255,255,0.22)", text="#f2f2f2",
        dim="rgba(255,255,255,0.58)", faint="rgba(255,255,255,0.36)",
        chip="rgba(255,255,255,0.06)", chip_border="rgba(255,255,255,0.12)",
        menubar="rgba(255,255,255,0.04)", shadow="0.55",
    ),
    "light": dict(
        bg="#ececec", glow1="rgba(255,255,255,0.95)", glow2="rgba(255,255,255,0.7)",
        window="#ffffff", window_op="0.92", border="rgba(0,0,0,0.09)",
        bar="#f4f4f4", dot="rgba(0,0,0,0.18)", text="#111111",
        dim="rgba(0,0,0,0.60)", faint="rgba(0,0,0,0.40)",
        chip="rgba(0,0,0,0.035)", chip_border="rgba(0,0,0,0.10)",
        menubar="rgba(255,255,255,0.55)", shadow="0.16",
    ),
}

SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "'SF Mono', ui-monospace, 'JetBrains Mono', Menlo, Consolas, monospace"

CHIPS = ["Document AI", "LLMs & RAG", "AI agents & MCP", "MLOps", "Linux & macOS tools"]


def chips(t, x0, y):
    out, x = [], x0
    for label in CHIPS:
        w = int(len(label) * 7.6 + 30)
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="{t["chip"]}" stroke="{t["chip_border"]}"/>'
            f'<text x="{x + w / 2}" y="{y + 19.5}" text-anchor="middle" class="chip">{label.replace("&", "&amp;")}</text>'
        )
        x += w + 10
    return "\n    ".join(out)


def menu(t):
    out, x = [], 58
    for label in ["Work", "Projects", "Open source", "Contact"]:
        out.append(f'<text x="{x}" y="20" class="menu" style="font-weight:400">{label}</text>')
        x += int(len(label) * 6.9 + 22)
    return "\n    ".join(out)


def facts(t, x, y):
    rows = [("now", "Quantiphi"), ("before", "C3 AI · PwC · BCBS"), ("based", "Redwood City, CA")]
    out = []
    for i, (k, v) in enumerate(rows):
        yy = y + i * 24
        out.append(f'<text x="{x}" y="{yy}" class="mono">{k}</text>')
        out.append(f'<text x="{x + 76}" y="{yy}" class="mono" style="fill:{t["dim"]}">{v}</text>')
    return "\n    ".join(out)


def banner(name):
    t = THEMES[name]
    wx, wy, ww, wh = 64, 58, W - 128, 250
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="LN Bodicherla, Senior Machine Learning Engineer">
  <title>LN Bodicherla, Senior Machine Learning Engineer</title>
  <style>
    .name {{ font: 700 50px {SANS}; fill: {t["text"]}; letter-spacing: -1px; }}
    .role {{ font: 500 15px {SANS}; fill: {t["dim"]}; letter-spacing: 3.2px; }}
    .tag  {{ font: 400 19px {SANS}; fill: {t["dim"]}; }}
    .mono {{ font: 400 14px {MONO}; fill: {t["faint"]}; }}
    .menu {{ font: 600 13px {SANS}; fill: {t["dim"]}; }}
    .chip {{ font: 500 13px {SANS}; fill: {t["dim"]}; }}
    .win  {{ animation: rise 0.9s cubic-bezier(.2,.9,.3,1.1) both; }}
    .fade {{ animation: fade 1.2s ease-out 0.35s both; }}
    .cursor {{ animation: blink 1.1s steps(1) infinite; }}
    .drift {{ animation: drift 18s ease-in-out infinite alternate; }}
    @keyframes rise  {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade  {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes blink {{ 0%, 50% {{ opacity: 1; }} 50.01%, 100% {{ opacity: 0; }} }}
    @keyframes drift {{ from {{ transform: translate(-40px, -10px); }} to {{ transform: translate(60px, 20px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .win, .fade, .cursor, .drift {{ animation: none; }} }}
  </style>
  <defs>
    <radialGradient id="g1" cx="22%" cy="10%" r="60%"><stop offset="0" stop-color="{t["glow1"]}"/><stop offset="1" stop-color="{t["bg"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="85%" cy="100%" r="55%"><stop offset="0" stop-color="{t["glow2"]}"/><stop offset="1" stop-color="{t["bg"]}" stop-opacity="0"/></radialGradient>
    <filter id="shadow" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000" flood-opacity="{t["shadow"]}"/></filter>
    <clipPath id="round"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#round)">
    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
    <g class="drift"><rect x="-80" y="-60" width="{W + 160}" height="{H + 120}" fill="url(#g1)"/></g>
    <rect width="{W}" height="{H}" fill="url(#g2)"/>

    <!-- menu bar -->
    <rect width="{W}" height="30" fill="{t["menubar"]}"/>
    <text x="24" y="20" class="menu">LN</text>
    {menu(t)}
    <text x="{W - 24}" y="20" text-anchor="end" class="menu" style="font-weight:400">lnbodicherla.dev</text>

    <!-- window -->
    <g class="win" filter="url(#shadow)">
      <rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="14" fill="{t["window"]}" fill-opacity="{t["window_op"]}" stroke="{t["border"]}"/>
      <path d="M{wx + 14} {wy} h{ww - 28} a14 14 0 0 1 14 14 v20 h-{ww} v-20 a14 14 0 0 1 14 -14z" fill="{t["bar"]}"/>
      <line x1="{wx}" y1="{wy + 34}" x2="{wx + ww}" y2="{wy + 34}" stroke="{t["border"]}"/>
      <circle cx="{wx + 22}" cy="{wy + 17}" r="6" fill="{t["dot"]}"/>
      <circle cx="{wx + 42}" cy="{wy + 17}" r="6" fill="{t["dot"]}"/>
      <circle cx="{wx + 62}" cy="{wy + 17}" r="6" fill="{t["dot"]}"/>
      <text x="{wx + ww / 2}" y="{wy + 22}" text-anchor="middle" class="mono">~ / about</text>
    </g>

    <g class="fade">
      <text x="{wx + 44}" y="{wy + 76}" class="mono">$ whoami<tspan class="cursor"> ▍</tspan></text>
      <text x="{wx + 42}" y="{wy + 132}" class="name">Lakshmi Narasaiah Bodicherla</text>
      <text x="{wx + 44}" y="{wy + 164}" class="role">SENIOR MACHINE LEARNING ENGINEER</text>
      <text x="{wx + 44}" y="{wy + 194}" class="tag">Production document AI, LLM and agent systems. Desktop tools for Linux and macOS on the side.</text>
    {chips(t, wx + 44, wy + 208)}
    {facts(t, wx + ww - 300, wy + 76)}
    </g>
  </g>
</svg>
'''


out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for theme in THEMES:
    (out / f"banner-{theme}.svg").write_text(banner(theme))
print("written to", out)
