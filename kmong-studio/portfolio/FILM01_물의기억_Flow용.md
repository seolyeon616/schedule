# FILM 01 「물의 기억」 — Google Flow 전용 프롬프트 시트

> 원본 시트(`FILM01_물의기억_프롬프트시트.md`)를 **Google Flow(Veo 3.1)** 기능에 맞춰 다시 쓴 버전입니다.
> 기능 이름과 옵션은 Flow 업데이트에 따라 바뀔 수 있습니다. 화면에 보이는 이름 기준으로 맞춰 쓰세요.

---

## 0. Flow에서 달라지는 점

| 원본 시트 | Flow에서는 |
|---|---|
| `--ar 16:9 --style raw --s 150` | **지우세요.** 비율은 Flow 설정에서 **16:9** 선택 |
| `--sref` (스타일 레퍼런스) | **Ingredients**(재료 이미지)로 대체 |
| 네거티브 프롬프트 칸 | 없음 → 프롬프트 안에 **긍정문으로** 씀 (예: "The bottle has no label or text") |
| 영상 툴 오디오는 음소거 | Veo는 **효과음을 같이 만들어 줌** → 효과음은 살리고 **음악·대사는 빼라고** 지시 |
| Kling의 시작/끝 프레임 | **Frames to Video** (첫 프레임 + 끝 프레임) |
| 캐릭터 레퍼런스 첨부 | **Ingredients to Video** (인물·제품 이미지를 재료로) |
| 역재생 | Flow에선 불가 → **편집 프로그램에서** 역재생 |

**모델 선택:** 테스트는 **Fast**(크레딧 절약), 최종 컷만 **Quality**로 다시 생성.
**클립 길이:** 한 번에 약 8초 → 필요한 부분만 편집에서 잘라 씀.

### Flow용 공통 꼬리말 (모든 영상 프롬프트 끝에 붙이기)
```
Cinematic luxury skincare commercial, shot on a large-format cinema camera with anamorphic lens, subtle film grain, color palette of glacier cyan, deep navy and champagne gold, backlit with rim light. No text, no letters, no logos, no watermark on screen. Audio: sound effects only as described, no music, no dialogue.
```

### Flow용 이미지 꼬리말 (Flow 안에서 이미지를 만들 때)
```
Cinematic 16:9 still frame, high-end luxury skincare commercial, anamorphic lens look, subtle film grain, glacier cyan, deep navy and champagne gold palette, physically accurate lighting, ultra detailed. No text, no letters, no logos, no watermark.
```

---

## 1. 재료(Ingredients) 이미지 3장 — 제일 먼저

Flow의 이미지 생성(또는 Gemini 앱)에서 만들고 **저장해 두세요.** 이후 컷에서 계속 재사용합니다.

**ING-A 제품 (AURÉA 병)**
```
A single luxury serum bottle on a seamless light grey studio background: a slim cylindrical frosted glass bottle with softly rounded shoulders, filled with pale icy blue liquid, topped with a polished champagne gold dropper cap with a ribbed collar. The bottle has no label and no text. Large softbox light from the left, clean reflections, high-end product photography, centered, ultra sharp.
```
+ 이미지 꼬리말

**ING-B 가상 모델**
```
Portrait of a fictional Korean woman in her late 20s, calm serene expression, dewy luminous glass skin, minimal natural makeup, straight dark hair tied in a low loose bun with a few face-framing strands, small gold stud earrings, ivory silk camisole, soft even beauty lighting, neutral grey background, front-facing medium close-up.
```
+ 이미지 꼬리말
> 실존 인물과 닮았으면 폐기하고 다시 생성하세요.

**ING-C 무드**
```
Inside glacier ice, turquoise light caustics rippling across translucent ice layers, a single glowing droplet at the center, deep navy shadows and champagne gold highlights, luxurious and reverent atmosphere.
```
+ 이미지 꼬리말

---

## 2. 컷별 Flow 프롬프트

> 각 컷마다 **모드 · 넣을 이미지 · 프롬프트** 순서입니다. 프롬프트 끝에는 **공통 꼬리말**을 붙이세요.

### #1 · 0:00–0:03 · 물방울 훅
- **모드:** Frames to Video (첫 프레임만)
- **첫 프레임 이미지** (Flow 이미지 생성):
```
Extreme macro of a single perfectly spherical crystal-clear water droplet suspended in pure black darkness, a thin icy cyan rim light tracing its edge, a tiny reflection of a vast blue glacier visible inside the droplet.
```
- **영상 프롬프트:**
```
Extreme macro, locked-off camera. In pure darkness, a single crystal-clear water droplet falls slowly downward in ultra slow motion, its surface wobbling gently. An icy cyan rim light glints across it, and a tiny glacier reflection shimmers inside. Nothing else moves. Audio: a single soft crystalline water drip with a long airy reverb.
```
- **편집:** 떨어지는 영상을 **역재생** → "위로 떨어지는 물방울" 완성. (Veo에 역중력을 바로 시키는 것보다 훨씬 안정적)

### #2 · 0:03–0:07 · 물방울 속으로 → 빙하 협곡
- **모드:** Frames to Video (**첫 + 끝 프레임**)
- **첫 프레임:** #1 영상의 한 장면 캡처 (물방울이 화면 중앙에 크게 있는 프레임)
- **끝 프레임 이미지:**
```
Epic aerial view flying low over an immense blue glacier canyon at dawn, towering walls of translucent turquoise ice, soft golden sunrise haze drifting through the canyon.
```
- **영상 프롬프트:**
```
The camera pushes steadily into the floating water droplet. The glacier reflected inside grows larger until the camera passes through the droplet's surface in one seamless move and emerges flying low over an immense blue glacier canyon at dawn. One continuous camera move, no cuts. Audio: a deep whoosh passing through water, then vast cold wind.
```

### #3 · 0:07–0:11 · 빙하 속 갇힌 물
- **모드:** Ingredients to Video (재료: **ING-C**) — 또는 Frames to Video(첫 프레임 = ING-C)
- **영상 프롬프트:**
```
Slow lateral tracking shot gliding through translucent glacier ice. Turquoise light caustics ripple across the ice layers. At the center, a trapped droplet slowly melts free and begins to glow soft champagne gold. Tiny bubbles rise past the lens. Majestic, meditative, very slow. Audio: deep glacier ice creaking softly, cavernous and distant.
```
- **편집:** 자막 `10,000 YEARS AGO`는 편집에서 넣기.

### #4 · 0:11–0:15 · 폭포 다이브
- **모드:** Text to Video (재료 없이) 또는 Frames to Video
- **첫 프레임 이미지 (선택):**
```
Top of a glacial meltwater waterfall seen from right above its edge, turquoise water plunging into a misty valley far below, small rainbows in the spray, early morning light.
```
- **영상 프롬프트:**
```
FPV drone shot: the camera tips over the edge of a glacial waterfall and dives straight down alongside the falling turquoise water, fast yet perfectly smooth, spray and mist rushing past the lens, rainbows flashing in the spray. Audio: a powerful rushing waterfall roar swelling up.
```

### #5 · 0:15–0:19 · 이끼 숲의 이슬
- **모드:** Frames to Video (첫 프레임)
- **첫 프레임 이미지:**
```
Macro shot of a single dew droplet resting on the central vein of a vibrant green fern leaf in an ancient mossy forest, golden dawn light rays streaming through the canopy behind, creamy bokeh.
```
- **영상 프롬프트:**
```
Macro follow shot. The dew droplet rolls slowly along the vein of the fern leaf, catching the golden dawn light. The leaf sways slightly in a gentle breeze. At the tip of the leaf the droplet swells, detaches and falls out of frame. Audio: soft forest dawn ambience, distant birds, one tiny drip.
```

### #6 · 0:19–0:23 · 도시 유리창
- **모드:** Frames to Video (첫 프레임)
- **첫 프레임 이미지:**
```
Close-up of raindrops on a large floor-to-ceiling window at night, behind the glass the blurred neon lights of a modern Seoul skyline in cyan and warm amber bokeh, rain streaks running down the glass, shallow depth of field on the droplets.
```
- **영상 프롬프트:**
```
A single water droplet falls from above and splashes onto the window glass in slow motion. Then a slow rack focus pulls from the droplets on the glass to the blurred neon city lights behind, cyan and amber bokeh shimmering through the rain. Audio: rain tapping on glass, muffled city ambience at night.
```

### #7 · 0:23–0:29 · 창가의 여인
- **모드:** **Ingredients to Video** (재료: **ING-B** 인물 + #6 첫 프레임을 배경으로)
- **영상 프롬프트:**
```
The woman from the reference stands beside a rain-streaked floor-to-ceiling window at blue hour, eyes gently closed. Slow orbit from left to right around her. Rippling water-light caustics from the rainy window glide across her cheek and neck. She slowly opens her eyes and a faint calm smile appears. Soft cool window light with a warm gold rim light from behind. Her face stays exactly the same throughout. Audio: very soft rain on glass, quiet room tone.
```
- **팁:** 얼굴이 흔들리면 Ingredients 대신 **Flow 이미지로 첫 프레임을 먼저 만든 뒤**(ING-B 참고) Frames to Video로 가세요. 얼굴 유지가 더 안정적입니다.

### #8 · 0:29–0:35 · 세럼 한 방울 (첫 컷과 짝)
- **모드:** Ingredients to Video (재료: **ING-A** 병) — 또는 첫 프레임 방식
- **첫 프레임 이미지 (첫 프레임 방식일 때):**
```
Extreme macro of a champagne gold glass dropper, a single drop of pale icy blue serum swelling at its tip above a woman's fingertip, inside the droplet a tiny reflection of a blue glacier is visible, black background, champagne gold rim light.
```
- **영상 프롬프트:**
```
Extreme macro. A drop of pale icy blue serum slowly swells at the tip of the champagne gold glass dropper, a tiny glacier shimmering inside it. It detaches and falls in slow motion onto a fingertip, spreading into a thin luminous film with a soft shimmer. Audio: a delicate liquid drop landing softly, gentle shimmering reverb.
```
- **편집:** #1과 같은 크기·같은 위치에 배치. 내레이션 "1만 년을 기다린, 한 방울."은 ElevenLabs 등에서 따로 녹음 (Veo 대사는 한국어 품질이 들쭉날쭉함).

### #9 · 0:35–0:41 · 제품 히어로
- **모드:** **Frames to Video** (첫 프레임 = 아래 이미지. 병 모양 고정에 가장 안정적)
- **첫 프레임 이미지** (ING-A를 참고 이미지로 넣고 생성):
```
The same serum bottle from the reference standing perfectly upright on a thin sheet of perfectly still water, beneath the water surface the faint glowing silhouette of a glacier is visible, concentric ripples spreading from the base, low angle, deep navy background, champagne gold rim light, hero product shot. The bottle has no label and no text.
```
- **영상 프롬프트:**
```
Low-angle slow arc of about 30 degrees around the serum bottle standing on still water. Concentric ripples spread gently from its base. Beneath the surface, the faint glacier silhouette glows and fades. A champagne gold rim light slides along the glass edge. The bottle's shape stays exactly the same. Audio: a soft low resonant water tone.
```
- **편집:** 로고 `AURÉA`는 편집에서 병에 붙임.

### #10 · 0:41–0:45 · 엔드 타이틀
- **모드:** Text to Video (배경 소스용)
```
Top-down view: a single drop of water falls onto a perfectly black glossy surface in slow motion and spreads into one clean circular ripple. Pure black background, minimal. Audio: a soft water drop impact with a gentle shimmering chime.
```
- **편집:** 파문 위로 `당신의 피부에 닿기까지, 1만 년.` → `AURÉA` 타이틀 (원본 시트 #10 참고).

---

## 3. Flow에서 편하게 하는 요령

- **Scenebuilder**에 10컷을 순서대로 놓고 흐름을 먼저 확인한 뒤, 컷별로 다운로드해 편집 프로그램에서 마무리하세요.
- 컷이 짧으면 **Extend**로 이어서 늘리기 (특히 #3, #9).
- 마음에 드는 컷의 **프롬프트는 그대로 두고 여러 번 생성** → 베스트 선택. 한 번에 한 가지만 바꿔 가며 수정.
- 음악(BGM)은 Flow가 아니라 원본 시트 4번 프롬프트로 따로 만드세요. Veo가 만든 효과음은 편집에서 음악 밑에 깔면 됩니다.
- 세로 숏폼 버전은 16:9 영상을 잘라도 되지만, Veo 3.1은 **9:16 생성도 지원**하니 #1·#8·#9는 9:16으로 한 번씩 더 뽑으면 화질이 좋습니다.
