#!/usr/bin/env python3
"""Live profile cards for SirAseef's README, regenerated every 6 hours by GitHub Actions.

Writes to --out (default: dist/):
  greeting.svg         time-aware greeting from Karachi (PKT) + current Karachi conditions
  heatflood-live.svg   "Live from HeatFlood Sentinel": current temperature, precipitation and
                       a 24-hour forecast sparkline for five Pakistani cities (Open-Meteo, keyless)
  github-activity.svg  public GitHub numbers, 30-day commit chart and latest repositories
  career-timeline.svg  animated career Gantt with the NOW line at generation time

Standard library only. If a source fails, the previous card is kept (copied back from the
`live` branch) instead of publishing an empty one.
"""
import argparse, datetime as dt, json, os, sys, urllib.request, urllib.parse
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import gen  # noqa: E402  (shared palette, frame, motif and chart helpers)
from gen import (BG, G1, G2, G3, INK, MUTED, LINE, PLAT, STEEL, CARD, CARD2,
                 frame, text, chip, esc, alpha_mark, orbit_ring, rule, head, lift, MONTHS)

PKT = dt.timezone(dt.timedelta(hours=5), "PKT")
USER = os.environ.get("GH_USER", "SirAseef")
REPO = os.environ.get("GITHUB_REPOSITORY", f"{USER}/{USER}")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
UA = {"User-Agent": f"{USER}-profile-live-cards"}

CITIES = [("Karachi", 24.8607, 67.0011), ("Lahore", 31.5204, 74.3587), ("Islamabad", 33.6844, 73.0479),
          ("Jacobabad", 28.2769, 68.4514), ("Sukkur", 27.7052, 68.8574)]
REGION = {"Karachi": "Sindh", "Lahore": "Punjab", "Islamabad": "Capital Territory", "Jacobabad": "Sindh", "Sukkur": "Sindh"}
WMO = {0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "fog",
       51: "light drizzle", 53: "drizzle", 55: "dense drizzle", 61: "light rain", 63: "rain", 65: "heavy rain",
       66: "freezing rain", 67: "freezing rain", 71: "light snow", 73: "snow", 75: "heavy snow", 80: "rain showers",
       81: "rain showers", 82: "violent showers", 95: "thunderstorm", 96: "thunderstorm, hail", 99: "thunderstorm, hail"}


def get_json(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def stamp(now):
    return f"{now:%H:%M} PKT · {now.day} {MONTHS[now.month-1]} {now.year}"


# ------------------------------------------------------------------ data: Open-Meteo
def fetch_weather():
    q = {"latitude": ",".join(str(c[1]) for c in CITIES), "longitude": ",".join(str(c[2]) for c in CITIES),
         "current": "temperature_2m,precipitation,relative_humidity_2m,weather_code",
         "hourly": "temperature_2m,precipitation", "forecast_days": 2, "timezone": "Asia/Karachi"}
    qs = urllib.parse.urlencode(q)
    errs = []
    # primary: the public forecast API; second host serves the same model archive if the first is rate-limited
    for host in ("api.open-meteo.com", "historical-forecast-api.open-meteo.com"):
        try:
            d = get_json(f"https://{host}/v1/forecast?{qs}")
            if isinstance(d, dict) and d.get("error"):
                raise RuntimeError(d.get("reason"))
            if not isinstance(d, list) or len(d) != len(CITIES):
                raise RuntimeError("unexpected response shape")
            return d, host
        except Exception as e:  # noqa: BLE001
            errs.append(f"{host}: {e}")
    raise RuntimeError("; ".join(errs))


def next24(city):
    cur = city["current"]["time"][:13]  # 'YYYY-MM-DDTHH'
    times = city["hourly"]["time"]
    i0 = next((i for i, t in enumerate(times) if t[:13] == cur), 0)
    t = city["hourly"]["temperature_2m"][i0:i0 + 24]
    p = city["hourly"]["precipitation"][i0:i0 + 24]
    return [x for x in t if x is not None], [x or 0 for x in p], times[i0:i0 + 24]


# ------------------------------------------------------------------ data: GitHub
def gh(path):
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    return get_json(f"https://api.github.com{path}", h)


def fetch_github(now):
    user = gh(f"/users/{USER}")
    repos = gh(f"/users/{USER}/repos?per_page=100&sort=pushed")
    since = (now - dt.timedelta(days=30)).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    days = Counter()
    for r in repos:
        if r.get("fork"):
            continue
        for page in range(1, 6):
            try:
                cs = gh(f"/repos/{r['full_name']}/commits?author={USER}&since={since}&per_page=100&page={page}")
            except Exception:  # empty repos return 409
                break
            for c in cs:
                ts = c["commit"]["author"]["date"]
                d = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(PKT).date()
                days[d] += 1
            if len(cs) < 100:
                break
    return user, repos, days


# ------------------------------------------------------------------ cards
def greeting_card(now, karachi=None):
    W, H = 1200, 150
    h = now.hour
    if 5 <= h < 12:
        g, tint = "Good morning from Karachi", G2
    elif 12 <= h < 17:
        g, tint = "Good afternoon from Karachi", G1
    elif 17 <= h < 21:
        g, tint = "Good evening from Karachi", G3
    else:
        g, tint = "Good night from Karachi", PLAT
    b = []
    b.append(f'<circle cx="110" cy="75" r="90" fill="{tint}" opacity=".10" filter="url(#soft)"/>')
    b.append(orbit_ring(110, 75, 58, dur=160, ticks=48, major=4))
    b.append(alpha_mark(110, 75, .55, node=True))
    b.append(gen.shine_text(210, 70, g, 34, 800, width=640, glow=False))
    wd = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][now.weekday()]
    b.append(text(212, 102, f"{wd} · {now.day} {MONTHS[now.month-1]} {now.year}  ·  thanks for stopping by.", 15.5, INK, 500))
    if karachi:
        b.append(f'<text x="1160" y="66" class="t" font-size="30" font-weight="800" fill="url(#gold)" text-anchor="end">{karachi["t"]:.0f}°C</text>')
        b.append(text(1160, 92, f"Karachi now · {karachi['desc']}", 13, PLAT, 600, "end"))
    b.append(f'<text x="1160" y="124" class="m" font-size="11" fill="{MUTED}" text-anchor="end" letter-spacing="1">UPDATED {stamp(now)} · EVERY 6 H</text>')
    b.append(rule(212, 760, 126))
    return lift(frame(W, H, "gr", "".join(b)))


def sparkline(x, y, w, h, temps, precs, k):
    lo, hi = min(temps), max(temps)
    span = max(hi - lo, 1)
    n = len(temps)
    px = lambda i: x + w * i / (n - 1)
    py = lambda v: y + h - 6 - (h - 14) * (v - lo) / span
    o = []
    pmax = max(max(precs), 1.0)
    bwid = w / n * .6
    for i, p in enumerate(precs):
        if p > 0:
            bh = max(2, (h - 10) * .55 * p / pmax)
            o.append(f'<rect x="{px(i)-bwid/2:.1f}" y="{y+h-bh:.1f}" width="{bwid:.1f}" height="{bh:.1f}" rx="1" fill="{STEEL}" opacity=".75"/>')
    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(temps))
    o.append(f'<polygon points="{x:.1f},{y+h} {pts} {x+w:.1f},{y+h}" fill="url(#spk)" opacity=".5"/>')
    plen = sum(((px(i+1)-px(i))**2 + (py(temps[i+1])-py(temps[i]))**2) ** .5 for i in range(n - 1))
    o.append(f'<polyline points="{pts}" fill="none" stroke="url(#goldH)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" '
             f'stroke-dasharray="{plen:.0f}" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="{plen:.0f};0;0;{-plen:.0f}" keyTimes="0;.25;.9;1" dur="14s" begin="-{14-k*.4:.1f}s" repeatCount="indefinite"/></polyline>')
    imax = temps.index(hi)
    o.append(f'<circle cx="{px(imax):.1f}" cy="{py(hi):.1f}" r="3.2" fill="#FFF3C4" filter="url(#glow)"/>')
    o.append(f'<circle cx="{px(0):.1f}" cy="{py(temps[0]):.1f}" r="3" fill="{G2}" class="pulse"/>')
    return "".join(o)


def weather_card(data, host, now):
    W = 1200; RH = 72; Y0 = 150
    H = Y0 + RH * len(CITIES) + 70
    b = []
    b.append(f'<circle cx="62" cy="52" r="7" fill="#FF4D4D"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    b.append(text(80, 58, "LIVE FROM HEATFLOOD SENTINEL", 14, G1, 800, extra='letter-spacing="3"'))
    b.append(text(48, 86, f"Current conditions and the next 24 hours across five cities · refreshed every 6 hours · updated {stamp(now)}", 13.5, MUTED, 400, extra='font-style="italic"'))
    b.append(alpha_mark(1140, 56, .3, node=True))
    cols = [(48, "CITY"), (300, "NOW"), (420, "HUMIDITY"), (540, "RAIN NOW"), (668, "NEXT 24 H  ·  °C RANGE"), (858, "NEXT 24 H  ·  TEMPERATURE / RAIN")]
    for x, lab in cols:
        b.append(text(x, Y0 - 18, lab, 10.5, PLAT, 700, cls="m", extra='letter-spacing="1.5" fill-opacity=".7"'))
    b.append(f'<line x1="40" y1="{Y0-8}" x2="1160" y2="{Y0-8}" stroke="{LINE}"/>')
    for k, ((name, lat, lon), c) in enumerate(zip(CITIES, data)):
        y = Y0 + k * RH
        if k % 2 == 0:
            b.append(f'<rect x="32" y="{y}" width="1136" height="{RH}" rx="10" fill="#FFFFFF" fill-opacity=".022"/>')
        cur = c["current"]
        temps, precs, _ = next24(c)
        b.append(text(48, y + 32, name, 18, "#FFFFFF", 700))
        b.append(text(48, y + 52, REGION.get(name, "Pakistan"), 11.5, MUTED, 400))
        t = cur["temperature_2m"]
        tc = G3 if t >= 40 else (G2 if t >= 30 else PLAT)
        b.append(f'<text x="300" y="{y+44}" class="t" font-size="26" font-weight="800" fill="{tc}">{t:.1f}<tspan font-size="14" font-weight="600" fill="{PLAT}"> °C</tspan></text>')
        b.append(text(420, y + 43, f"{cur.get('relative_humidity_2m', 0):.0f}%", 17, INK, 600))
        b.append(text(540, y + 43, f"{cur['precipitation']:.1f} mm", 17, STEEL if cur['precipitation'] > 0 else INK, 600))
        desc = WMO.get(cur.get("weather_code"), "")
        b.append(text(540, y + 60, desc, 11, MUTED, 400))
        if temps:
            b.append(text(668, y + 36, f"{min(temps):.0f}° – {max(temps):.0f}°", 17, INK, 600))
            tot = sum(precs)
            b.append(text(668, y + 56, f"rain {tot:.1f} mm" if tot > 0 else "no rain expected", 11.5, STEEL if tot > 0 else MUTED, 500))
            b.append(sparkline(858, y + 10, 290, RH - 18, temps, precs, k))
    # scanning line across sparklines
    yb = Y0 + RH * len(CITIES)
    b.append(f'<line x1="858" y1="{Y0}" x2="858" y2="{yb}" stroke="#FFF3C4" stroke-opacity=".25"><animateTransform attributeName="transform" type="translate" values="0 0;290 0;290 0" keyTimes="0;.6;1" dur="10s" repeatCount="indefinite"/></line>')
    b.append(f'<line x1="40" y1="{yb+14}" x2="1160" y2="{yb+14}" stroke="{LINE}"/>')
    b.append(text(48, yb + 42, "Weather data by Open-Meteo.com (CC BY 4.0) · hourly model forecast, Asia/Karachi time", 12, MUTED, 400))
    b.append(text(1152, yb + 42, "MS thesis · NED UET", 12, MUTED, 400, "end", extra='font-style="italic"'))
    extra = f'<linearGradient id="spk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{G1}" stop-opacity=".55"/><stop offset="1" stop-color="{G1}" stop-opacity="0"/></linearGradient>'
    return lift(frame(W, H, "wx", "".join(b), extra))


def github_card(user, repos, days, now):
    W, H = 1200, 400
    b = []
    b.append(head(48, 56, "LIVE GITHUB ACTIVITY", f"Public data for @{USER} from the GitHub API · updated {stamp(now)}"))
    b.append(alpha_mark(1140, 56, .3, node=True))
    total30 = sum(days.values())
    since = dt.datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")).astimezone(PKT)
    last_push = max((r.get("pushed_at") or "" for r in repos), default="")
    tiles = [("PUBLIC REPOS", str(user.get("public_repos", 0))), ("FOLLOWERS", str(user.get("followers", 0))),
             ("COMMITS · 30 DAYS", str(total30)), ("ON GITHUB SINCE", f"{MONTHS[since.month-1]} {since.year}")]
    for i, (lab, val) in enumerate(tiles):
        x = 48 + (i % 2) * 196; y = 110 + (i // 2) * 104
        b.append(f'<rect x="{x}" y="{y}" width="184" height="92" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".35"/>')
        b.append(f'<rect x="{x+14}" y="{y}" width="156" height="3" rx="1.5" fill="url(#goldH)"/>')
        b.append(text(x + 18, y + 30, lab, 10.5, PLAT, 700, cls="m", extra='letter-spacing="1.2" fill-opacity=".8"'))
        b.append(f'<text x="{x+18}" y="{y+72}" class="t" font-size="{30 if len(val) < 6 else 24}" font-weight="800" fill="url(#gold)">{esc(val)}</text>')
    # 30-day commit bars
    cx0, cy0, cw, ch = 470, 120, 420, 150
    b.append(f'<rect x="{cx0-20}" y="{cy0-12}" width="{cw+40}" height="{ch+86}" rx="14" fill="{CARD}" stroke="{G1}" stroke-opacity=".25"/>')
    b.append(text(cx0, cy0 + 12, "COMMITS PER DAY · LAST 30 DAYS · PUBLIC REPOS", 10.5, PLAT, 700, cls="m", extra='letter-spacing="1" fill-opacity=".8"'))
    today = now.date()
    seq = [days.get(today - dt.timedelta(days=29 - i), 0) for i in range(30)]
    mx = max(max(seq), 1)
    bw = cw / 30
    base = cy0 + ch + 20
    b.append(f'<line x1="{cx0}" y1="{base}" x2="{cx0+cw}" y2="{base}" stroke="{LINE}"/>')
    for i, v in enumerate(seq):
        x = cx0 + i * bw + bw * .18
        hgt = 0 if v == 0 else max(3, (ch - 20) * v / mx)
        if v == 0:
            b.append(f'<rect x="{x:.1f}" y="{base-2}" width="{bw*.64:.1f}" height="2" fill="{PLAT}" opacity=".18"/>')
            continue
        an = (f'<animate attributeName="height" values="0;{hgt:.1f};{hgt:.1f};0" keyTimes="0;.15;.9;1" dur="14s" begin="-{14-i*.05:.2f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="{base};{base-hgt:.1f};{base-hgt:.1f};{base}" keyTimes="0;.15;.9;1" dur="14s" begin="-{14-i*.05:.2f}s" repeatCount="indefinite"/>')
        b.append(f'<rect x="{x:.1f}" y="{base-hgt:.1f}" width="{bw*.64:.1f}" height="{hgt:.1f}" rx="2" fill="url(#gold)">{an}</rect>')
    imax = seq.index(max(seq))
    if max(seq) > 0:
        b.append(text(cx0 + imax * bw + bw / 2, base - (ch - 20) - 8, f"{max(seq)}", 11, G2, 700, "middle", cls="m"))
    d0 = today - dt.timedelta(days=29)
    b.append(text(cx0, base + 18, f"{d0.day} {MONTHS[d0.month-1]}", 11, MUTED, 500, cls="m"))
    b.append(text(cx0 + cw, base + 18, f"{today.day} {MONTHS[today.month-1]}", 11, MUTED, 500, "end", cls="m"))
    # latest repositories
    rx = 940
    b.append(text(rx, cy0 + 12, "LATEST REPOSITORIES", 10.5, PLAT, 700, cls="m", extra='letter-spacing="1" fill-opacity=".8"'))
    own = [r for r in repos if not r.get("fork")][:3]
    for i, r in enumerate(own):
        y = cy0 + 30 + i * 66
        b.append(f'<rect x="{rx}" y="{y}" width="212" height="56" rx="12" fill="{CARD}" stroke="{G1}" stroke-opacity=".3"/>')
        nm = r["name"] if len(r["name"]) <= 22 else r["name"][:21] + "…"
        b.append(text(rx + 14, y + 23, nm, 14, "#FFFFFF", 700))
        pd = dt.datetime.fromisoformat(r["pushed_at"].replace("Z", "+00:00")).astimezone(PKT)
        meta = f"updated {pd.day} {MONTHS[pd.month-1]} {pd.year}" + (f" · {r['language']}" if r.get("language") else "")
        b.append(text(rx + 14, y + 42, meta, 11, MUTED, 400))
    if not own:
        b.append(text(rx, cy0 + 56, "No public repositories yet.", 13, MUTED, 400))
    b.append(text(48, 370, "Counts are public data only; private work is not shown.", 12, MUTED, 400, extra='font-style="italic"'))
    return lift(frame(W, H, "gh", "".join(b)))


# ------------------------------------------------------------------ main
def keep_previous(out, name):
    """Copy last published card back from the live branch so a failed fetch never blanks it."""
    try:
        url = f"https://raw.githubusercontent.com/{REPO}/live/{name}"
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            open(os.path.join(out, name), "wb").write(r.read())
        print(f"kept previous {name}")
    except Exception as e:  # noqa: BLE001
        print(f"no previous {name}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    now = dt.datetime.now(PKT)
    status = {}
    karachi = None
    try:
        data, host = fetch_weather()
        open(os.path.join(a.out, "heatflood-live.svg"), "w").write(weather_card(data, host, now))
        cur = data[0]["current"]
        karachi = {"t": cur["temperature_2m"], "desc": WMO.get(cur.get("weather_code"), "live")}
        status["weather"] = f"ok via {host}"
    except Exception as e:  # noqa: BLE001
        status["weather"] = f"FAILED: {e}"
        keep_previous(a.out, "heatflood-live.svg")
    try:
        open(os.path.join(a.out, "github-activity.svg"), "w").write(github_card(*fetch_github(now), now))
        status["github"] = "ok"
    except Exception as e:  # noqa: BLE001
        status["github"] = f"FAILED: {e}"
        keep_previous(a.out, "github-activity.svg")
    open(os.path.join(a.out, "greeting.svg"), "w").write(greeting_card(now, karachi))
    open(os.path.join(a.out, "career-timeline.svg"), "w").write(lift(gen.career_timeline_svg(now)))
    status["generated_at"] = now.isoformat()
    open(os.path.join(a.out, "status.json"), "w").write(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
