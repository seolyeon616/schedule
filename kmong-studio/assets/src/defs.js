// Shared SVG defs (gradients, filters, symbols) + small render helpers.
// Every artboard in index.html uses <use href="#..."> against these symbols.

const DEFS = `
<svg width="0" height="0" style="position:absolute">
<defs>
  <linearGradient id="gGold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff3cf"/><stop offset=".38" stop-color="#efcd8a"/>
    <stop offset=".62" stop-color="#b98840"/><stop offset=".86" stop-color="#f6dc9f"/><stop offset="1" stop-color="#c79a52"/>
  </linearGradient>
  <linearGradient id="gGoldH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8a5f2a"/><stop offset=".35" stop-color="#f6dc9f"/>
    <stop offset=".55" stop-color="#fff3cf"/><stop offset="1" stop-color="#9c6d31"/>
  </linearGradient>
  <linearGradient id="gEbony" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#030202"/><stop offset=".3" stop-color="#231911"/>
    <stop offset=".46" stop-color="#4b3625"/><stop offset=".62" stop-color="#1c140e"/><stop offset="1" stop-color="#030202"/>
  </linearGradient>
  <radialGradient id="gFlash" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#fffaf0" stop-opacity="1"/><stop offset=".18" stop-color="#ffe3a6" stop-opacity=".85"/>
    <stop offset=".5" stop-color="#e6a94c" stop-opacity=".25"/><stop offset="1" stop-color="#e6a94c" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gNavy" cx=".5" cy=".35" r=".8">
    <stop offset="0" stop-color="#1d3d66"/><stop offset=".55" stop-color="#0a1629"/><stop offset="1" stop-color="#03060c"/>
  </radialGradient>
  <linearGradient id="gWater" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#10284a"/><stop offset="1" stop-color="#01040a"/>
  </linearGradient>
  <linearGradient id="gGlass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#9fd6e6" stop-opacity=".35"/><stop offset=".5" stop-color="#d8f3fa" stop-opacity=".18"/>
    <stop offset="1" stop-color="#6bb1c8" stop-opacity=".45"/>
  </linearGradient>
  <linearGradient id="gNight" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#140c26"/><stop offset=".45" stop-color="#2a1430"/><stop offset=".47" stop-color="#0b0a12"/><stop offset="1" stop-color="#030305"/>
  </linearGradient>
  <linearGradient id="gTrailR" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff5a44" stop-opacity=".2"/><stop offset="1" stop-color="#ff3b2a" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="gTrailW" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff1c8" stop-opacity=".25"/><stop offset="1" stop-color="#fffaf0" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="gMoonSky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0c1a38"/><stop offset=".7" stop-color="#050a18"/><stop offset="1" stop-color="#020308"/>
  </linearGradient>
  <linearGradient id="gWarm" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffe0a0"/><stop offset="1" stop-color="#c77e2c"/>
  </linearGradient>
  <linearGradient id="gMist" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#9fb4d6" stop-opacity="0"/><stop offset=".5" stop-color="#9fb4d6" stop-opacity=".16"/><stop offset="1" stop-color="#9fb4d6" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="gIce" cx=".5" cy=".4" r=".6">
    <stop offset="0" stop-color="#e8fbff"/><stop offset=".5" stop-color="#7fd0e6"/><stop offset="1" stop-color="#0d3a55"/>
  </radialGradient>

  <filter id="fGlow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fGlowBig" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="fBlur4"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="fBlur1"><feGaussianBlur stdDeviation="1.1"/></filter>

  <!-- 도깨비 방망이 : ebony body, gold inlay, film-sprocket studs -->
  <symbol id="club" viewBox="0 0 200 620">
    <path d="M64 400 C54 310 34 210 34 118 C34 54 62 28 100 28 C138 28 166 54 166 118 C166 210 146 310 136 400 Z" fill="url(#gEbony)"/>
    <path d="M74 392 C62 300 50 210 50 130 C50 84 66 56 84 46 C74 74 68 110 68 152 C68 240 76 320 84 392 Z" fill="#fff" opacity=".09"/>
    <path d="M64 400 C54 310 34 210 34 118 C34 54 62 28 100 28 C138 28 166 54 166 118 C166 210 146 310 136 400" fill="none" stroke="url(#gGold)" stroke-width="2" opacity=".9"/>
    <g fill="none" stroke="url(#gGold)" stroke-width="1.3" opacity=".55">
      <path d="M44 170 C60 158 74 180 90 168"/><path d="M110 168 C126 156 140 178 156 166"/>
      <path d="M52 280 C64 270 76 288 90 278"/><path d="M110 278 C124 268 136 286 148 276"/>
      <path d="M66 360 C78 350 88 368 98 358"/><path d="M102 358 C114 348 124 366 136 356"/>
    </g>
    <g fill="url(#gGold)" filter="url(#fGlow)">
      <rect x="91" y="70" width="18" height="24" rx="4.5"/><rect x="91" y="112" width="18" height="24" rx="4.5"/>
      <rect x="91" y="154" width="18" height="24" rx="4.5"/><rect x="91" y="196" width="18" height="24" rx="4.5"/>
      <rect x="91" y="238" width="18" height="24" rx="4.5"/><rect x="91" y="280" width="18" height="24" rx="4.5"/>
      <rect x="91" y="322" width="18" height="24" rx="4.5"/><rect x="91" y="364" width="18" height="20" rx="4.5"/>
      <rect x="52" y="96" width="14" height="18" rx="4"/><rect x="134" y="96" width="14" height="18" rx="4"/>
      <rect x="50" y="200" width="14" height="18" rx="4"/><rect x="136" y="200" width="14" height="18" rx="4"/>
      <rect x="56" y="304" width="12" height="16" rx="4"/><rect x="132" y="304" width="12" height="16" rx="4"/>
    </g>
    <rect x="56" y="396" width="88" height="16" rx="4" fill="url(#gGoldH)"/>
    <path d="M76 412 L83 588 Q100 602 117 588 L124 412 Z" fill="url(#gEbony)"/>
    <g fill="url(#gGoldH)" opacity=".92">
      <rect x="78" y="438" width="44" height="5" rx="2"/><rect x="79" y="466" width="42" height="5" rx="2"/>
      <rect x="80" y="494" width="40" height="5" rx="2"/><rect x="81" y="522" width="38" height="5" rx="2"/>
      <rect x="82" y="550" width="36" height="5" rx="2"/>
    </g>
    <ellipse cx="100" cy="592" rx="19" ry="7" fill="url(#gGoldH)"/>
  </symbol>

  <!-- small logo mark -->
  <symbol id="mark" viewBox="0 0 40 40">
    <g transform="rotate(-35 20 20)">
      <path d="M15 27 C14 20 13 12 14 8 C15 4 17.5 3 20 3 C22.5 3 25 4 26 8 C27 12 26 20 25 27 Z" fill="url(#gGold)"/>
      <g fill="#0a0a0c"><rect x="18.5" y="7" width="3" height="4" rx="1"/><rect x="18.5" y="13" width="3" height="4" rx="1"/><rect x="18.5" y="19" width="3" height="4" rx="1"/></g>
      <rect x="17.5" y="27" width="5" height="10" rx="1.5" fill="url(#gGold)"/>
    </g>
  </symbol>

  <!-- SCENE: perfume rising through still water -->
  <symbol id="scPerfume" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice">
    <rect width="320" height="180" fill="url(#gNavy)"/>
    <polygon points="160,0 60,130 260,130" fill="#cfe9ff" opacity=".05"/>
    <polygon points="160,0 120,130 200,130" fill="#fff4d6" opacity=".05"/>
    <rect y="128" width="320" height="52" fill="url(#gWater)"/>
    <g fill="none" stroke="#e6c07a">
      <ellipse cx="160" cy="131" rx="30" ry="4.5" opacity=".7"/><ellipse cx="160" cy="133" rx="58" ry="8.5" opacity=".42"/>
      <ellipse cx="160" cy="136" rx="92" ry="14" opacity=".24"/><ellipse cx="160" cy="140" rx="135" ry="21" opacity=".12"/>
    </g>
    <g opacity=".16" transform="translate(0,262) scale(1,-1)">
      <rect x="140" y="64" width="40" height="66" rx="7" fill="#9fd6e6"/>
    </g>
    <g filter="url(#fGlow)">
      <rect x="140" y="64" width="40" height="66" rx="7" fill="url(#gGlass)" stroke="url(#gGold)" stroke-width="1.1"/>
      <rect x="144" y="92" width="32" height="34" rx="5" fill="#8fd3ea" opacity=".35"/>
      <rect x="153" y="52" width="14" height="13" fill="url(#gGlass)" stroke="url(#gGold)" stroke-width=".8"/>
      <rect x="149" y="36" width="22" height="17" rx="3" fill="url(#gGold)"/>
      <rect x="144" y="70" width="4" height="54" rx="2" fill="#fff" opacity=".5"/>
    </g>
    <g fill="#f3b7c0" opacity=".75">
      <ellipse cx="112" cy="70" rx="4" ry="2" transform="rotate(-30 112 70)"/><ellipse cx="206" cy="52" rx="3.5" ry="1.8" transform="rotate(20 206 52)"/>
      <ellipse cx="226" cy="92" rx="3" ry="1.6" transform="rotate(-10 226 92)"/><ellipse cx="96" cy="104" rx="2.6" ry="1.4" transform="rotate(40 96 104)"/>
      <ellipse cx="190" cy="24" rx="2.4" ry="1.2" transform="rotate(-50 190 24)"/>
    </g>
  </symbol>

  <!-- SCENE: rainy night highway light trails -->
  <symbol id="scRoad" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice">
    <rect width="320" height="180" fill="url(#gNight)"/>
    <ellipse cx="160" cy="84" rx="120" ry="16" fill="#ff9a4a" opacity=".22" filter="url(#fBlur4)"/>
    <g opacity=".85">
      <circle cx="40" cy="78" r="2" fill="#ffcf7a"/><circle cx="62" cy="74" r="1.4" fill="#8ad7ff"/><circle cx="90" cy="80" r="2.2" fill="#ff7a6a"/>
      <circle cx="118" cy="76" r="1.3" fill="#fff"/><circle cx="210" cy="77" r="1.8" fill="#8ad7ff"/><circle cx="236" cy="80" r="2.4" fill="#ffcf7a"/>
      <circle cx="262" cy="73" r="1.4" fill="#fff"/><circle cx="290" cy="79" r="2" fill="#ff7a6a"/>
    </g>
    <polygon points="-20,180 340,180 172,85 148,85" fill="#07070b"/>
    <path d="M160 88 L160 180" stroke="#f4efe6" stroke-width="1.2" stroke-dasharray="6 9" opacity=".35"/>
    <g fill="none" stroke-linecap="round" filter="url(#fGlow)">
      <path d="M152 86 C120 110 70 140 -10 176" stroke="url(#gTrailR)" stroke-width="3"/>
      <path d="M154 87 C128 114 90 150 30 186" stroke="url(#gTrailR)" stroke-width="2"/>
      <path d="M168 86 C200 110 250 140 330 176" stroke="url(#gTrailW)" stroke-width="3.2"/>
      <path d="M166 87 C192 114 230 150 290 186" stroke="url(#gTrailW)" stroke-width="2"/>
    </g>
    <g id="rain" stroke="#cfe3ff" stroke-width=".6" opacity=".35"></g>
  </symbol>

  <!-- SCENE: hanok under full moon, ink-wash mountains -->
  <symbol id="scHanok" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice">
    <rect width="320" height="180" fill="url(#gMoonSky)"/>
    <circle cx="222" cy="56" r="78" fill="#f7e9c4" opacity=".05"/>
    <circle cx="222" cy="56" r="48" fill="#f7e9c4" opacity=".1"/>
    <circle cx="222" cy="56" r="30" fill="#f8f1dc" filter="url(#fGlow)"/>
    <circle cx="214" cy="50" r="6" fill="#e8dcc0" opacity=".5"/><circle cx="230" cy="64" r="4" fill="#e8dcc0" opacity=".4"/>
    <path d="M0 112 C40 76 66 92 98 72 C128 52 158 88 196 82 C236 74 268 98 320 86 L320 180 L0 180Z" fill="#1a2944" opacity=".85"/>
    <rect y="92" width="320" height="30" fill="url(#gMist)"/>
    <path d="M0 132 C50 104 90 118 130 104 C170 92 210 122 250 112 C280 104 300 116 320 110 L320 180 L0 180Z" fill="#0e172a"/>
    <path d="M150 34 l8 4 l8 -4 M160 28 l5 2.5 l5 -2.5" fill="none" stroke="#f4efe6" stroke-width="1" opacity=".7"/>
    <path d="M14 140 Q58 134 100 124 L220 124 Q262 134 306 140 Q312 136 318 128 L306 146 L14 146 L2 128 Q8 136 14 140Z" fill="#020204"/>
    <rect x="58" y="146" width="204" height="40" fill="#050507"/>
    <g fill="url(#gWarm)" filter="url(#fGlow)" opacity=".95">
      <rect x="74" y="152" width="30" height="24"/><rect x="114" y="152" width="30" height="24"/>
      <rect x="176" y="152" width="30" height="24"/><rect x="216" y="152" width="30" height="24"/>
    </g>
    <g stroke="#3a2512" stroke-width=".8">
      <path d="M89 152v24M74 164h30M129 152v24M114 164h30M191 152v24M176 164h30M231 152v24M216 164h30"/>
    </g>
  </symbol>

  <!-- SCENE: glacier droplet (물의 기억) -->
  <symbol id="scDrop" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice">
    <rect width="320" height="180" fill="#020306"/>
    <circle cx="160" cy="92" r="70" fill="#7fd0e6" opacity=".06"/>
    <path d="M160 30 C176 62 196 82 196 108 C196 130 180 146 160 146 C140 146 124 130 124 108 C124 82 144 62 160 30Z" fill="url(#gIce)" opacity=".9"/>
    <g opacity=".85">
      <path d="M130 122 L146 94 L156 108 L168 84 L190 122Z" fill="#eafcff" opacity=".7"/>
      <path d="M130 122 L146 94 L150 122Z" fill="#9fdcef" opacity=".6"/>
    </g>
    <path d="M160 30 C176 62 196 82 196 108 C196 130 180 146 160 146 C140 146 124 130 124 108 C124 82 144 62 160 30Z" fill="none" stroke="#bff3ff" stroke-width="1.2" filter="url(#fGlow)"/>
    <ellipse cx="146" cy="84" rx="5" ry="12" fill="#fff" opacity=".45" transform="rotate(20 146 84)"/>
  </symbol>
</defs>
</svg>`;

document.body.insertAdjacentHTML("afterbegin", DEFS);

// seeded random so renders are deterministic
function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

// rain lines inside the road symbol
(() => {
  const g = document.getElementById("rain"); const r = rng(7); let h = "";
  for (let i = 0; i < 70; i++) { const x = r() * 340 - 10, y = r() * 170, l = 6 + r() * 10; h += `<line x1="${x}" y1="${y}" x2="${x - 2.5}" y2="${y + l}"/>`; }
  g.innerHTML = h;
})();

// gold sparks around a point; el must be position:relative/absolute
function sparks(el, cx, cy, n, spread, seed, up = 1) {
  const r = rng(seed); let h = "";
  for (let i = 0; i < n; i++) {
    const a = -Math.PI * (0.08 + r() * 0.84) * up, d = Math.pow(r(), 0.7) * spread;
    const x = cx + Math.cos(a) * d * 1.5, y = cy + Math.sin(a) * d;
    const s = 0.8 + r() * 2.6, o = 0.35 + r() * 0.65;
    h += `<div style="position:absolute;left:${x}px;top:${y}px;width:${s}px;height:${s}px;border-radius:50%;background:#ffe2a0;opacity:${o};box-shadow:0 0 ${4 + s * 3}px #f0b95c"></div>`;
  }
  el.insertAdjacentHTML("beforeend", h);
}

// perspective shockwave rings on the floor
function shock(el, cx, cy, w, h, seed = 1) {
  const svg = `<svg class="abs" style="left:${cx - w / 2}px;top:${cy - h / 2}px;overflow:visible" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
    <ellipse cx="${w / 2}" cy="${h / 2}" rx="${w * 0.5}" ry="${h * 0.5}" fill="none" stroke="#e6c07a" stroke-width="1" opacity=".18"/>
    <ellipse cx="${w / 2}" cy="${h / 2}" rx="${w * 0.36}" ry="${h * 0.36}" fill="none" stroke="#f6d89a" stroke-width="1.6" opacity=".38" filter="url(#fGlow)"/>
    <ellipse cx="${w / 2}" cy="${h / 2}" rx="${w * 0.22}" ry="${h * 0.22}" fill="none" stroke="#fff0c8" stroke-width="2.4" opacity=".75" filter="url(#fGlowBig)"/>
    <ellipse cx="${w / 2}" cy="${h / 2}" rx="${w * 0.2}" ry="${h * 0.9}" fill="url(#gFlash)" opacity=".9"/>
    <ellipse cx="${w / 2}" cy="${h / 2}" rx="${w * 0.07}" ry="${h * 0.16}" fill="#fffaf0" filter="url(#fGlowBig)"/>
  </svg>`;
  el.insertAdjacentHTML("beforeend", svg);
}

// club placed so the head tip sits on (tx,ty), body rising at `deg` from vertical (+ = leaning right)
function club(el, tx, ty, height, deg) {
  const w = height * 200 / 620, tipX = w * 0.5, tipY = height * 28 / 620;
  el.insertAdjacentHTML("beforeend",
    `<svg class="abs" style="left:${tx - tipX}px;top:${ty - tipY}px;width:${w}px;height:${height}px;transform-origin:${tipX}px ${tipY}px;transform:rotate(${180 + deg}deg);filter:drop-shadow(0 0 16px rgba(240,190,100,.35)) drop-shadow(0 25px 30px rgba(0,0,0,.8))"><use href="#club"/></svg>`);
}

function frame(el, { x, y, w, h, rot = 0, scene, tag = "", rec = false, z = 1 }) {
  el.insertAdjacentHTML("beforeend",
    `<div class="frame" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;transform:rotate(${rot}deg);z-index:${z}">
      <svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice"><use href="#${scene}"/></svg>
      ${tag ? `<span class="tag">${tag}</span>` : ""}${rec ? `<span class="rec">REC</span>` : ""}
    </div>`);
}

function floorGlow(el, cx, cy, w, h) {
  el.insertAdjacentHTML("afterbegin",
    `<div class="abs" style="left:${cx - w / 2}px;top:${cy - h / 2}px;width:${w}px;height:${h}px;border-radius:50%;background:radial-gradient(ellipse at center, rgba(236,180,90,.42), rgba(236,180,90,.12) 40%, transparent 70%)"></div>`);
}
