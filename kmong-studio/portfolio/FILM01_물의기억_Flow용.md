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

**ING-B 가상 모델** — 기준 인물: Flow에서 생성한 "빙하 전망 창가, 샴페인 실크 로브" 이미지의 여성
- **방법 A (추천):** 그 이미지를 첨부하고 아래 프롬프트 → 얼굴이 가장 비슷하게 유지됨
```
Use the attached image as the reference for the woman's face: keep her facial features, face shape, skin tone and hair color exactly the same. Ignore the bottle, the robe and the background.
Beauty portrait of this same fictional woman in her early 30s, calm serene expression with a faint soft smile, dewy luminous glass skin, minimal natural makeup, softly defined brows, long dark brown hair with soft natural waves, loosely tied in a low bun with a few face-framing strands, small gold stud earrings, ivory champagne silk camisole. Soft even beauty lighting, neutral grey background, front-facing medium close-up. She must be clearly recognizable as the same woman.
```
- **방법 B (첨부 없이):** 첨부 문장 두 줄을 빼고 `Beauty portrait of a fictional woman…`으로 시작
+ 이미지 꼬리말
> 기준 이미지는 반드시 **우리가 AI로 생성한 이미지**여야 합니다. 실제 사진·연예인 사진은 첨부 금지. 결과가 실존 인물과 닮았으면 폐기하고 다시 생성하세요.

**ING-C 무드**
```
Inside glacier ice, turquoise light caustics rippling across translucent ice layers, a single glowing droplet at the center, deep navy shadows and champagne gold highlights, luxurious and reverent atmosphere.
```
+ 이미지 꼬리말

---

### 재료 이미지는 어디에 쓰나 (사용처 표)

재료 3장은 **영상에 그대로 나오는 장면이 아니라, 뒤 컷들의 "기준 사진"**입니다. 한 번 만들어 저장해 두고, 해당 컷을 만들 때마다 **첨부**합니다.

| 재료 | 쓰는 컷 | 쓰는 방법 |
|---|---|---|
| **ING-C 무드** (빙하 속) | **#3** | 첫 프레임으로 그대로 쓰거나 재료로 첨부 |
| | #4 · #5 · #6 | 첫 프레임 이미지를 만들 때 **톤 참고용으로 첨부** → 컷끼리 색감이 맞음 |
| **ING-B 모델** (여성) | **#7** | 재료로 첨부 (얼굴 고정) |
| | #8 | 손끝이 나오니 함께 첨부하면 피부 톤이 맞음 (선택) |
| **ING-A 병** (AURÉA) | **#8** · **#9** | 재료로 첨부 또는 첫 프레임 이미지 생성 시 참고로 첨부 (병 모양 고정) |
| | #10 | 엔드 타이틀 뒤 배경에 병을 쓸 경우 |
| (없음) | #1 · #2 | 물방울 컷은 재료 없이 **첫/끝 프레임 이미지**로 진행 (#1 = 작은 물방울, #2 = 큰 물방울 → 빙하 협곡) |

**에이전트형 Flow에서 첨부하는 법:** 입력창 **+** → 재료 이미지 선택 → 프롬프트 맨 앞에 한 줄 추가
```
Use the attached image as the reference for the [bottle / woman / color and mood]. Keep it exactly the same.
```
(병이면 `bottle`, 모델이면 `woman`, 무드면 `color and mood`)

## 2. 컷별 Flow 프롬프트

> 각 컷마다 **모드 · 넣을 이미지 · 프롬프트** 순서입니다. 프롬프트 끝에는 **공통 꼬리말**을 붙이세요.

### #1 · 0:00–0:03 · 물방울 훅
- **모드:** Frames to Video (첫 프레임만)
- **첫 프레임 이미지:** **작은 물방울 + 검은 여백이 넓은 이미지** (Nano Banana 2, "Extreme macro of a single liquid water droplet floating in the center of a pure black frame…"로 뽑은 것). 여백이 넓어야 떨어지는 공간과 9:16 크롭 여유가 생깁니다.
  - 새로 뽑을 때 프롬프트:
```
Extreme macro of a single liquid water droplet floating in the center of a pure black frame, the droplet small in the frame with lots of black empty space around it. Inside the droplet, a tiny reflection of a vast blue glacier. A thin icy cyan rim light traces its edge and a soft cyan glow surrounds it. A few tiny water beads float nearby.
```
- **영상 프롬프트 (에이전트형 Flow: + 로 첫 프레임 이미지 첨부 후):**
```
Use the attached image as the first frame. Keep the droplet, the glacier reflection inside it, the glow and the black background exactly the same.
Extreme macro, locked-off camera, the camera does not move. The water droplet falls slowly and straight down in ultra slow motion, staying sharp and in focus. It is liquid water, not a glass ball: its surface wobbles and ripples softly as it falls, and the glacier reflection inside it shimmers and bends. The soft cyan glow travels with it. Two or three tiny water beads drift slowly beside it. Pure black background, nothing else in the frame. Audio: a single soft crystalline water drip with a long airy reverb.
```
+ 공통 꼬리말
- **고르는 기준:** 물방울이 **하나**이고, 떨어지는 동안 **모양이 크게 찌그러지지 않고**, 화면 밖으로 너무 빨리 나가지 않는 것.
- **편집:** 떨어지는 영상을 **역재생** → "위로 떠오르는 물방울". 역재생하면 영상 끝이 첫 프레임(물방울 정중앙)이 되어 #2로 이어집니다.

### #2 · 0:03–0:07 · 물방울 속으로 → 빙하 협곡
- **모드:** Frames to Video (**첫 + 끝 프레임**)
- **첫 프레임:** **큰 물방울 이미지** (물방울 안에 빙하가 크게 보이는 것). #1 끝(작은 물방울)에서 한 단계 당겨 들어간 컷처럼 이어집니다. 이미지 없이 #1과 완벽히 맞추고 싶으면 #1 첫 프레임 이미지를 그대로 써도 됩니다.
- **끝 프레임:** **새벽 빙하 협곡 이미지** (물방울 속 빙하와 색·방향이 비슷할수록 넘어가는 장면이 자연스러움). 새로 뽑을 때:
```
Epic aerial view flying low over an immense blue glacier canyon at dawn, towering walls of translucent turquoise ice on both sides, soft golden sunrise haze drifting through the canyon, the canyon leading straight ahead toward the horizon.
```
+ 이미지 꼬리말
- **영상 프롬프트 (첫 프레임·끝 프레임 순서로 첨부 후):**
```
Use the first attached image as the first frame and the second attached image as the last frame.
The camera pushes steadily forward into the floating water droplet. The glacier reflected inside it grows larger and larger until the camera passes through the droplet's liquid surface in one seamless move, with a brief shimmer of water refraction, and emerges flying low over the immense blue glacier canyon at dawn, continuing forward. One continuous camera move, no cuts, no fade.
Audio: a deep whoosh passing through water, then vast cold wind.
```
+ 공통 꼬리말
- **실패하면:** 물방울이 사라지고 장면이 그냥 바뀌는(디졸브) 결과가 나오면 `The camera physically flies through the droplet like diving into water.`를 추가하세요.

### #3 · 0:07–0:11 · 빙하 속 갇힌 물
- **모드:** Ingredients to Video (재료: **ING-C**) — 또는 Frames to Video(첫 프레임 = ING-C)
- **영상 프롬프트:**
```
Slow lateral tracking shot gliding through translucent glacier ice. Turquoise light caustics ripple across the ice layers. At the center, a trapped droplet slowly melts free and begins to glow soft champagne gold. Tiny bubbles rise past the lens. Majestic, meditative, very slow. Audio: deep glacier ice creaking softly, cavernous and distant.
```
- **편집:** 자막 `10,000 YEARS AGO`는 편집에서 넣기.

### #4 · 0:11–0:15 · 폭포 다이브
- **모드:** Frames to Video (첫 프레임만) — 에이전트형 Flow에선 이미지를 "프롬프트에 추가"로 첨부
- **첫 프레임 이미지:** 폭포 가장자리 + 물보라 + 무지개 + 뒤쪽 설산 이미지
```
Top of a glacial meltwater waterfall seen from right above its edge, turquoise water plunging into a misty valley far below, small rainbows in the spray, early morning light.
```
+ 이미지 꼬리말
- **영상 프롬프트 (첨부 후):**
```
Use the attached image as the first frame. Keep the waterfall, the rocks, the rainbows and the morning light exactly the same.
FPV drone shot: the camera glides forward over the rocky edge of the waterfall, then tips over the edge and dives straight down alongside the falling turquoise water. Fast yet perfectly smooth and stable, no shaking. Spray and mist rush past the lens, the rainbows flash in the spray as the camera passes through them, and the misty valley floor opens up below. One continuous camera move, no cuts.
Audio: a powerful rushing waterfall roar swelling up, wind rushing past.
```
+ 공통 꼬리말
- **고르는 기준:** 카메라가 **가장자리를 넘어 아래로** 떨어지는 것 (옆으로만 흐르거나 멈춰 있으면 탈락), 무지개를 통과하는 순간이 있으면 최고.
- **실패하면:** 카메라가 안 내려가면 `The camera pitches down 90 degrees and falls with the water.`를 추가.

### #5 · 0:15–0:19 · 이끼 숲의 이슬
- **모드:** 2단계 — ① 첫 프레임 **이미지** 만들기(ING-C를 톤 참고로 첨부) → ② 그 이미지를 첨부해 **영상** 만들기
- **① 첫 프레임 이미지 (이미지 모델, ING-C 첨부 후):**
```
Use the attached image only as a reference for color grading and lighting mood: deep navy shadows, glowing cyan highlights and warm champagne gold light. Do not copy its ice, its composition or its droplet shape.
Macro shot of a single dew droplet resting on the central vein of a vibrant green fern leaf in an ancient mossy forest, golden dawn light rays streaming through the canopy behind, creamy bokeh. The droplet sits in the center of the frame and a tiny reflection of the forest is visible inside it.
```
+ 이미지 꼬리말
- **고르는 기준:** 이슬방울 **하나**, 잎맥 위, 뒤에 금빛 빛줄기. 초록이 너무 형광이면 탈락 (전체 톤이 #3·#4와 이어져야 함)
- **② 영상 프롬프트 (①에서 고른 이미지를 첨부 후):**
```
Use the attached image as the first frame. Keep the fern leaf, the dew droplet, the forest and the golden light exactly the same.
Macro follow shot, slow and gentle. The dew droplet rolls slowly along the vein of the fern leaf toward its tip, catching the golden dawn light, the forest reflection inside it shimmering. The leaf sways slightly in a gentle breeze and dust particles float in the light rays. At the tip of the leaf the droplet swells, detaches and falls out of frame in slow motion.
Audio: soft forest dawn ambience, distant birds, one tiny drip.
```
+ 공통 꼬리말
- **편집:** #4 폭포 굉음을 끊고 조용한 숲 소리로 전환. 방울이 떨어지는 순간 → #6으로 컷.

### #6 · 0:19–0:23 · 도시 유리창
- **모드:** 2단계 — ① 첫 프레임 **이미지**(ING-C를 톤 참고로 첨부) → ② 그 이미지를 첨부해 **영상**
- **① 첫 프레임 이미지 (Nano Banana 2, ING-C 첨부 후):**
```
Use the attached image only as a reference for color grading and lighting mood: deep navy shadows, glowing cyan highlights and warm champagne gold light. Do not copy its ice, its composition or its droplet shape.
Close-up of raindrops on a large floor-to-ceiling window at night, behind the glass the blurred lights of a modern city skyline in cyan and warm amber bokeh, rain streaks running down the glass, shallow depth of field with the droplets on the glass in sharp focus. No readable signs or text in the city lights.
```
+ 이미지 꼬리말
- **고르는 기준:** 유리 위 물방울이 선명하고, 뒤 도시 불빛은 **글자·간판이 안 읽히게** 동그란 빛망울로만 보이는 것. 이 이미지는 **#7 배경 참고로도 쓰니 저장**해 두세요.
- **② 영상 프롬프트 (①에서 고른 이미지만 첨부, 모델 Omni 1.1 Flash):**
```
Use the attached image as the first frame. Keep the window, the raindrops and the city lights exactly the same.
Locked-off close-up. A single water droplet falls from above and splashes onto the window glass in slow motion, sending tiny beads sliding down the glass. Then a slow rack focus pulls from the droplets on the glass to the blurred city lights behind, cyan and amber bokeh shimmering through the rain.
Audio: rain tapping on glass, muffled city ambience at night.
```
+ 공통 꼬리말
- **편집:** #5 방울이 떨어지는 순간 → #6 물방울이 유리에 부딪히는 순간으로 **"떨어짐 → 부딪힘" 매치 컷**.

### #7 · 0:23–0:29 · 창가의 여인
- **모드:** 3단계 — ① ING-B(가상 모델) 만들기 → ② 첫 프레임 **이미지**(ING-B + #6 이미지 첨부) → ③ 그 이미지로 **영상**
- **① ING-B (Nano Banana 2, 첨부 없음):** 위 1장의 ING-B 프롬프트 + 이미지 꼬리말. 실존 인물과 닮았으면 폐기. #8에서도 쓰니 저장.
- **② 첫 프레임 이미지 (Nano Banana 2, 첨부 2장: ING-B → #6 첫 프레임 이미지 순서):**
```
Use the first attached image as the reference for the woman: keep her face, hairstyle, earrings and ivory silk camisole exactly the same. Use the second attached image as the reference for the rainy night window and the blurred city lights behind it.
Medium close-up of the woman standing beside the rain-streaked floor-to-ceiling window at blue hour, three-quarter profile facing the window, eyes gently closed, serene expression. Soft rippling water-light caustics from the rainy glass fall across her cheek and neck. Cool blue window light on her face with a warm champagne gold rim light from behind. The city lights are soft cyan and amber bokeh with no readable signs.
```
+ 이미지 꼬리말
- **고르는 기준:** 얼굴이 ING-B와 같은 사람, 눈 감은 상태, 얼굴에 물빛 무늬, 손가락·귀걸이 이상 없음.
- **③ 영상 프롬프트 (②에서 고른 이미지만 첨부, Omni 1.1 Flash):**
```
Use the attached image as the first frame. Keep the woman's face, hair and outfit exactly the same throughout.
Slow gentle orbit from left to right around her. Rippling water-light caustics from the rainy window glide slowly across her cheek and neck. After a moment she slowly opens her eyes, and a faint calm smile appears. Minimal, graceful movement, no talking, no hand gestures. Soft cool window light with a warm gold rim light from behind.
Audio: very soft rain on glass, quiet room tone.
```
+ 공통 꼬리말
- **실제 사용 버전 (첫 프레임에 큰 물방울이 얼굴 옆에 뜬 결과일 때):**
```
Use the attached image as the first frame. Keep the woman's face, hair, earrings and camisole exactly the same throughout.
Very slow push-in toward her face, the camera barely moves. The large teardrop-shaped raindrop on the window glass beside her face slowly slides down the glass, leaving a thin glistening trail. Soft rippling water-light caustics drift gently across her cheek and neck. After a moment she slowly opens her eyes and gazes calmly toward the window, and a faint serene smile appears. Minimal, graceful movement, no talking, no hand gestures. Cool blue window light with a warm champagne gold rim light from behind.
Audio: very soft rain on glass, quiet room tone.
```
+ 공통 꼬리말
- **실패하면:** 얼굴이 바뀌면 orbit(회전)을 빼고 `Very slow push-in, the camera barely moves.`로 교체.

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
