import html
import json
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Hello World Motion Lab")
st.caption("Type a name, choose its style, and add a looping weather or celebration effect.")

# Controls
with st.sidebar:
    st.header("Customize your app")
    name = st.text_input("Your name or message", value="Hello World", max_chars=80)

    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana",
         "Trebuchet MS", "Impact", "Comic Sans MS", "monospace", "serif"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=110, value=56, step=2)

    background = st.selectbox(
        "Background",
        ["Midnight", "Light", "Ocean", "Sunset", "Forest", "Lavender", "Rose", "Custom dark"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
    )
    speed = st.select_slider(
        "Animation speed",
        options=["Slow", "Normal", "Fast"],
        value="Normal",
        help="Controls how quickly the animation moves.",
    )
    bold = st.checkbox("Bold text", value=True)
    italic = st.checkbox("Italic text", value=False)

themes = {
    "Midnight": ("#101426", "#ffffff"),
    "Light": ("#f7f8fc", "#171923"),
    "Ocean": ("#063b56", "#f2fbff"),
    "Sunset": ("#3b174f", "#fff5e8"),
    "Forest": ("#12372a", "#f1fff4"),
    "Lavender": ("#e9e2ff", "#2d2052"),
    "Rose": ("#4b172c", "#fff0f5"),
    "Custom dark": ("#050505", "#ffffff"),
}
bg_color, text_color = themes[background]
font_css = json.dumps(font_family)
escaped_name = html.escape(name or "Hello World")
display_name = escaped_name if name else "Hello World"

mode_css = {
    "Slow": {"duration": 14, "particle_duration": 8},
    "Normal": {"duration": 8, "particle_duration": 5},
    "Fast": {"duration": 4, "particle_duration": 2.8},
}[speed]

# A deterministic particle field is created inside the embedded HTML. CSS animations
# run continuously in the browser, so Streamlit does not need a sleep/rerun loop.
rng = random.Random(2026)
particles = []
particle_count = 70 if effect in ("Rain", "Snow", "Hail", "Confetti", "Wind gust") else 28
for i in range(particle_count):
    left = rng.randint(0, 100)
    delay = round(rng.uniform(-mode_css["particle_duration"], 0), 2)
    duration = round(rng.uniform(mode_css["particle_duration"] * 0.65, mode_css["particle_duration"] * 1.5), 2)
    size = rng.randint(7, 17)
    drift = rng.randint(-90, 90)
    symbol = {
        "Rain": "💧",
        "Snow": "❄",
        "Hail": "●",
        "Confetti": rng.choice(["●", "✦", "◆", "★", "🎉"]),
        "Wind gust": rng.choice(["〰", "﹏", "🍃", "➜"]),
        "Tornado": "〰",
        "None": "",
    }.get(effect, "❄")
    particles.append(
        f'<span class="particle p{i}" style="left:{left}%;--delay:{delay}s;'
        f'--duration:{duration}s;--size:{size}px;--drift:{drift}px">{symbol}</span>'
    )

effect_class = {
    "None": "effect-none",
    "Rain": "effect-rain",
    "Snow": "effect-snow",
    "Hail": "effect-hail",
    "Wind gust": "effect-wind",
    "Confetti": "effect-confetti",
    "Tornado": "effect-tornado",
}[effect]

if name_mode == "Ticker Tape":
    name_markup = f'<div class="ticker"><span>{display_name}</span></div>'
elif name_mode == "Repeated":
    name_markup = '<div class="repeated">' + "".join(
        f'<div>{display_name}</div>' for _ in range(6)
    ) + '</div>'
else:
    name_markup = f'<div class="center-name">{display_name}</div>'

weight = "700" if bold else "400"
font_style = "italic" if italic else "normal"

# Tornado has a rotating funnel; other effects use moving particles.
tornado_markup = '<div class="tornado">🌪️</div>' if effect == "Tornado" else ""

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; }}
.stage {{
  position: relative; width: 100%; height: 620px; overflow: hidden;
  background: {bg_color}; color: {text_color}; border-radius: 18px;
  font-family: {json.loads(font_css)}, sans-serif;
}}
.particle-layer {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }}
.particle {{ position:absolute; top:-40px; display:block; opacity:.82; font-size:var(--size);
  animation: fall var(--duration) linear var(--delay) infinite; will-change:transform; }}
@keyframes fall {{
  0% {{ transform: translate3d(0,-40px,0) rotate(0deg); opacity:0; }}
  10% {{ opacity:.9; }}
  90% {{ opacity:.9; }}
  100% {{ transform: translate3d(var(--drift),680px,0) rotate(360deg); opacity:0; }}
}}
.effect-rain .particle {{ color:#69c9ff; text-shadow:0 0 5px #65c7ff; }}
.effect-rain .particle {{ transform:scaleX(.6); }}
.effect-snow .particle {{ color:#fff; text-shadow:0 0 8px #bce8ff; }}
.effect-hail .particle {{ background:#d8f0ff; width:var(--size); height:var(--size); border-radius:50%;
  color:transparent; box-shadow:0 0 5px #fff; }}
.effect-confetti .particle {{ animation-name: confetti-fall; }}
@keyframes confetti-fall {{
  0% {{ transform:translate3d(0,-30px,0) rotate(0deg); opacity:0; }}
  10% {{ opacity:1; }}
  100% {{ transform:translate3d(var(--drift),680px,0) rotate(900deg); opacity:1; }}
}}
.effect-wind .particle {{ color:#a5e9c7; font-size:calc(var(--size) * 1.8); animation-name: gust; }}
@keyframes gust {{
  0% {{ transform:translate3d(-120px,80px,0) rotate(0deg); opacity:0; }}
  20% {{ opacity:.8; }}
  100% {{ transform:translate3d(1100px, -80px,0) rotate(30deg); opacity:0; }}
}}
.effect-tornado .particle {{ color:#b9c6d8; font-size:calc(var(--size) * 1.6); animation-name: swirl; }}
@keyframes swirl {{
  0% {{ transform:translate3d(-80px,100px,0) rotate(0deg); opacity:0; }}
  20% {{ opacity:.7; }}
  100% {{ transform:translate3d(80px,560px,0) rotate(720deg); opacity:0; }}
}}
.name-layer {{ position:relative; z-index:5; display:flex; align-items:center; justify-content:center;
  width:100%; height:100%; padding:24px; font-size:{font_size}px; font-weight:{weight};
  font-style:{font_style}; text-shadow:0 2px 14px rgba(0,0,0,.2); }}
.center-name {{ text-align:center; overflow-wrap:anywhere; }}
.ticker {{ width:100%; overflow:hidden; white-space:nowrap; }}
.ticker span {{ display:inline-block; padding-left:100%; animation: ticker {mode_css['duration']}s linear infinite; }}
@keyframes ticker {{ from {{ transform:translateX(0); }} to {{ transform:translateX(-200%); }} }}
.repeated {{ width:100%; text-align:center; line-height:1.3; overflow-wrap:anywhere; }}
.repeated div:nth-child(even) {{ opacity:.62; }}
.tornado {{ position:absolute; z-index:3; font-size:130px; left:50%; top:50%;
  transform:translate(-50%,-50%); opacity:.65; animation: spin 3s linear infinite; }}
@keyframes spin {{ from {{ transform:translate(-50%,-50%) rotate(0deg) scale(.8); }}
  50% {{ transform:translate(-50%,-50%) rotate(180deg) scale(1.15); }}
  to {{ transform:translate(-50%,-50%) rotate(360deg) scale(.8); }} }}
.status {{ position:absolute; z-index:8; bottom:12px; right:16px; font:12px Arial,sans-serif;
  opacity:.7; letter-spacing:.04em; }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker span, .tornado {{ animation-duration:30s !important; }}
}}
</style>
</head>
<body>
  <div class="stage {effect_class}">
    <div class="particle-layer">{''.join(particles)}</div>
    {tornado_markup}
    <div class="name-layer">{name_markup}</div>
    <div class="status">HELLO WORLD MOTION LAB · {html.escape(effect.upper())}</div>
  </div>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)

st.info(
    "Tip: The animation runs in the preview itself, so it loops continuously without repeatedly rerunning the Streamlit app."
)
st.caption("Built with Python, Streamlit, HTML, and CSS animations.")
