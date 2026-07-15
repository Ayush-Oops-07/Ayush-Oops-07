import html, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 480, 376
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 100
LINE_H = 20.5

BG="#0d1117"; BG2="#111722"; FRAME="#30363d"; MUTED="#7d8590"
INK="#c9d1d9"; KEY="#ffa657"; SECTION="#58a6ff"; GREEN="#3fb950"; ACCENT="#22d3ee"

ROWS = [
    ("host",),
    ("kv","Now",   "MCA @ Graphic Era University, Dehradun"),
    ("kv","Prev",  "Cloud Intern @ Pinnacle Labs"),
    ("kv","Also",  "AI & Cloud Intern @ AICTE + Edunet"),
    ("kv","Edu",   "BCA CGPA: 8.01 · C.V. Raman Global Univ"),
    ("gap",),
    ("sec","Stack"),
    ("kv","Cloud",  "AWS (EC2, S3, IAM), Oracle OCI, GCP"),
    ("kv","DevOps", "Docker, K8s, Jenkins, Terraform, Ansible"),
    ("kv","AI Ops", "Copilot, Claude AI, LangChain, Bedrock"),
    ("kv","Backend","Flask, Django, Node.js, MySQL, MongoDB"),
    ("gap",),
    ("sec","Highlights"),
    ("bul","Oracle OCI DevOps Professional (2025)"),
    ("bul","2 Live Production Deployments on AWS EC2"),
    ("bul","AI-Augmented DevOps Practitioner"),
]

def esc(s): return html.escape(s)

def rise(inner, i):
    if STATIC: return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2+4}" fill="{MUTED}" font-size="12" text-anchor="middle">ayush@github: ~$ neofetch</text>')

y = TITLEBAR_H + 30
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap": y += LINE_H * 0.5; continue
    if kind == "host":
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">'
                 f'<tspan fill="{GREEN}">ayush</tspan><tspan fill="{MUTED}">@</tspan>'
                 f'<tspan fill="{ACCENT}">github</tspan></text>'
                 f'<line x1="{KEY_X+114}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">&#8212; {title}</text>'
                 f'<line x1="{KEY_X+12+len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    else: continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f: f.write(svg)
print("wrote", OUT, len(svg), "bytes")
