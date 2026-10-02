# FILM 04 · 05 — 가상 모델 「HARU(하루)」 캠페인 · Google Flow 전용

> 한 명의 가상 모델 **하루**로 두 편을 만든다 → "우리 브랜드 전속 모델로 패션·뷰티 다 돌릴 수 있다"를 증명
> - **FILM 04 「SEASON NOTE」** 패션 쇼핑몰 **ONDO(온도)** 사계절 룩북 · 아웃핏 트랜지션 · 9:16 · 약 16초
> - **FILM 05 「GRWM」** 뷰티 브랜드 **MULGYUL(물결)** 수분 앰플 · 같이 준비해요 브이로그 · 9:16 · 약 15초
> 브랜드·모델 모두 가상. 실존 인물과 닮으면 폐기.

---

## 0. 지금까지 배운 것 (이번엔 처음부터 적용)

| 문제 | 규칙 |
|---|---|
| 장면 점프 | 영상 프롬프트 첫 줄 `Animate the attached image… One continuous shot with no cuts` |
| 사람이 캐릭터 같음 | 이미지에 `candid, natural skin texture, not a 3D render, not a video game` + 필요하면 **편집 모드로 질감 추가** |
| Flow 거절 ("복제할 수 없는 요청") | 영상에서 사람을 "똑같이 복제/유지하라"고 길게 쓰지 않기 → `the same woman from the first frame` 정도로만 |
| 얼굴 변형 | **첫 프레임은 항상 정면 얼굴이 보이는 이미지**, 영상 동작은 **작고 느리게**, 말하는 입 모양 금지(자막·내레이션으로 대체) |
| 손가락 | 손은 **천천히, 한 동작만**. 손이 이상하면 그 컷은 손 없는 버전으로 |
| 첨부 실수 | 이미지와 프롬프트는 **같은 컷 번호끼리**, 첨부 썸네일에 ▶ 표시 있으면 영상 |
| 컷마다 | **새 대화(✎)** 에서 생성 |

### 이미지 꼬리말
```
Candid realistic photo, natural skin texture with fine pores, natural light, real fabric texture, not a 3D render, not a video game, not overly retouched. Vertical 9:16 photorealistic image. No text, no letters, no logos, no watermark.
```
### 영상 꼬리말 (FILM 04 · 패션)
```
Realistic fashion lookbook video shot on a cinema camera, vertical 9:16, natural motion, real fabric movement, natural skin texture, not a 3D render. No text, no letters, no logos, no watermark. Audio: sound effects only as described, no music, no dialogue.
```
### 영상 꼬리말 (FILM 05 · 브이로그)
```
Realistic smartphone vlog video, vertical 9:16, handheld with slight natural shake, soft morning window light, natural skin texture, not a 3D render. No text, no letters, no logos, no watermark. Audio: sound effects only as described, no music, no dialogue.
```

---

## 1. 하루(HARU) 기준 이미지 — 제일 먼저 (두 편 공통)

**H1 정면 얼굴** (Nano Banana 2 · 첨부 없음 · 9:16)
```
Portrait photo of a fictional Korean woman in her early twenties named Haru: shoulder-length dark brown hair with soft layers and light see-through bangs, warm brown eyes, natural fresh makeup with a soft coral lip, a small beauty mark just below her left eye, clear dewy skin, a warm friendly smile showing a little of her teeth, small silver hoop earrings, plain white crew-neck t-shirt. Front-facing head-and-shoulders shot, soft even studio light, plain light grey background.
```
+ 이미지 꼬리말
- 합격: 자연스러운 피부결, **왼쪽 눈 아래 점**(얼굴 식별 포인트), 연예인·실존 인물과 닮지 않음
- 캐릭터 같으면 편집 모드: `Edit this image. Keep her face, hair and pose exactly the same. Make her look like a real person photographed with a camera: natural skin texture with fine pores and slight unevenness, individual hair strands, real fabric texture. No text.`

**H2 전신** (첨부: H1 · 9:16)
```
Use the attached image as the reference for the woman: the same face, hair, beauty mark and earrings.
Full-body photo of the same woman standing naturally in a bright white photo studio, plain white t-shirt tucked into straight-leg light blue jeans and white sneakers, relaxed pose with one hand in her pocket, slight smile, slim natural body proportions, soft shadow on the white floor.
```
+ 이미지 꼬리말

**H3 반측면** (첨부: H1 · 9:16) — 고개를 돌리는 컷의 기준
```
Use the attached image as the reference for the woman: the same face, hair, beauty mark and earrings.
Head-and-shoulders photo of the same woman turned three-quarters to the left, looking softly past the camera with a gentle smile, plain white t-shirt, soft studio light, plain light grey background.
```
+ 이미지 꼬리말

> H1·H2·H3는 **PC 폴더에 저장**. 이후 모든 컷에 H1(얼굴) + H2(체형)를 첨부합니다.

---

# FILM 04 「SEASON NOTE」 — ONDO 사계절 룩북 (9:16 · 약 16초)

**로그라인:** 하얀 스튜디오의 하루가 한 바퀴 돌 때마다 계절이 바뀐다. 봄 → 여름 → 가을 → 겨울 → 다시 스튜디오. *ONDO — 계절이 바뀌어도, 너의 온도.*
**전환 원리:** 각 컷은 **정면 포즈 → 한 바퀴 회전**으로 끝남. 편집에서 **회전 중간(뒷모습·모션블러)** 에 다음 계절 컷으로 넘기고 4프레임 휘감기 블러를 얹는다 → "돌았더니 계절이 바뀐" 느낌.

| 시간 | 컷 | 자막 |
|---|---|---|
| 0:00–0:02.5 | S0 스튜디오, 카메라 보고 웃다가 회전 | 이번 시즌 코디, 한 번에 보여줄게 |
| 0:02.5–0:05 | S1 봄 · 벚꽃길 | SPRING · 트렌치 + 플리츠 스커트 |
| 0:05–0:07.5 | S2 여름 · 바닷가 산책로 | SUMMER · 린넨 셔츠 원피스 |
| 0:07.5–0:10 | S3 가을 · 은행나무길 | AUTUMN · 니트 + 와이드 슬랙스 |
| 0:10–0:12.5 | S4 겨울 · 눈 내리는 밤거리 | WINTER · 롱 울코트 + 머플러 |
| 0:12.5–0:16 | S5 스튜디오로 돌아와 멈춤 + 로고 | ONDO · 계절이 바뀌어도, 너의 온도 |

### 컷별 이미지 (모두 첨부: H1 → H2 · Nano Banana 2 · 9:16)
공통 앞문장:
```
Use the first attached image as the reference for the woman's face, hair, beauty mark and earrings, and the second attached image as the reference for her body proportions.
```
- **S0 스튜디오**
```
Full-body photo of the same woman in the bright white studio wearing the white t-shirt and light blue jeans, facing the camera with a playful smile, one hand lifting slightly as if about to spin, soft studio light, soft shadow on the floor.
```
- **S1 봄**
```
Full-body photo of the same woman on a quiet street lined with blooming cherry blossom trees on a sunny spring afternoon, wearing a light beige trench coat over a cream knit top and a pale pink pleated midi skirt with white loafers, facing the camera with a soft smile, a few petals drifting in the air, warm natural sunlight.
```
- **S2 여름**
```
Full-body photo of the same woman on a wooden seaside boardwalk on a bright summer day, wearing a white linen button-down shirt dress with rolled sleeves, a woven straw bag and flat leather sandals, facing the camera with a bright smile, blue sea and sky behind her, strong natural sunlight and soft breeze in her hair.
```
- **S3 가을**
```
Full-body photo of the same woman on an avenue of golden ginkgo trees in autumn, yellow leaves covering the ground, wearing a chunky oatmeal knit sweater, wide brown wool trousers and dark loafers, holding a small leather shoulder bag, facing the camera with a calm smile, warm late-afternoon light.
```
- **S4 겨울**
```
Full-body photo of the same woman on a snowy city street at night with warm string lights and glowing shop windows behind her, wearing a long camel wool coat, a cream cable-knit muffler and black ankle boots, facing the camera with a gentle smile, soft snowflakes falling, warm bokeh lights.
```
- **S5 스튜디오 엔딩** (S0과 같은 스튜디오, 겨울 코트 그대로 입은 채 정면 · 로고 들어갈 위쪽 여백)
```
Full-body photo of the same woman back in the bright white studio, wearing the long camel wool coat and cream muffler, standing still and facing the camera with a confident smile, plenty of empty white space above her head for a logo.
```
+ 각 이미지에 이미지 꼬리말

**고르는 기준(공통):** H1과 **같은 얼굴**(점 위치 포함), 정면, 손가락 자연스러움, 옷 디테일이 프롬프트대로.

### 컷별 영상 (첨부: 해당 컷 이미지 1장 · 새 대화 · Omni 1.1 Flash · 9:16)
- **S0 · S1 · S2 · S3 · S4 공통**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same place and the same woman from the first frame.
She smiles at the camera and shifts her weight naturally for a moment, then does one smooth, graceful full spin in place, her clothes and hair swinging naturally with the motion. The camera stays at the same distance with a very slight push-in. Natural, unhurried movement, no talking.
Audio: [계절 소리], soft fabric swish during the spin.
```
  - `[계절 소리]` → S0: `quiet studio room tone` · S1: `a light spring breeze, birds chirping` · S2: `gentle sea waves, seagulls far away` · S3: `dry leaves rustling underfoot` · S4: `soft snowfall hush, distant city chatter`
- **S5 엔딩**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same woman and studio from the first frame.
She finishes settling into place, adjusts her muffler with one hand slowly, then looks at the camera with a confident smile and holds the pose. The camera slowly pulls back a little. Natural, calm movement, no talking.
Audio: quiet studio room tone, soft fabric rustle.
```
+ 영상 꼬리말 (패션)

**거절되면:** 첫 줄의 `and the same woman from the first frame`을 지우고 다시.
**편집:** 각 컷 **정면 포즈 1.5초 + 회전 앞부분 0.8초**만 사용 → 회전 중간에 하드컷 + 휘감기 블러. 자막은 계절명 영문(Fraunces 계열) 크게 + 코디명 한글 작게.

---

# FILM 05 「GRWM」 — MULGYUL 수분 앰플 (9:16 · 약 15초)

**로그라인:** 출근 10분 전, 하루가 폰 카메라를 켜고 "같이 준비해요". 물결 수분 앰플 한 방울로 아침이 촉촉해진다.
**형식:** UGC 브이로그. 하루는 **말하지 않음**(입 모양 어색함 방지) → 화면 자막 + (선택) AI 내레이션.

**제품 기준 이미지 P1 (먼저 생성 · 첨부 없음)**
```
A single skincare ampoule bottle for a fictional brand: a slim clear glass dropper bottle with soft aqua-blue tinted glass, filled with clear watery serum with tiny floating bubbles, a frosted white dropper cap, no label and no text, standing on a pale wet stone surface with soft water ripples around it, bright clean morning light, minimal product photography.
```
+ 이미지 꼬리말 · 합격: 병 1개, 라벨·글자 없음

| 시간 | 컷 | 자막 (UGC 말투) |
|---|---|---|
| 0:00–0:02 | G1 침대 옆 창가, 폰 셀카 시점 손 흔들며 인사 | 출근 10분 전, 같이 준비해요 ☁️ |
| 0:02–0:04.5 | G2 화장대 위 앰플을 집어 듦 (손 + 제품) | 요즘 제 아침 1순위 |
| 0:04.5–0:07.5 | G3 스포이드로 손등에 한 방울 (매크로) | 물처럼 가볍게 스며들어요 |
| 0:07.5–0:10.5 | G4 볼에 톡톡, 거울 속 촉촉한 피부 | 바르자마자 물광 ✨ |
| 0:10.5–0:13 | G5 제품 히어로 (물결 위 앰플) | MULGYUL 수분 앰플 |
| 0:13–0:15 | G6 가방 들고 문 앞에서 윙크 | 오늘도 촉촉하게, 다녀올게요! |

### 이미지 (첨부: H1 → (필요 시 P1) · Nano Banana 2 · 9:16)
- **G1** (첨부 H1)
```
Use the attached image as the reference for the woman's face, hair, beauty mark and earrings.
Selfie-angle smartphone photo of the same woman sitting on the edge of her bed by a sunny window in the morning, wearing a soft oversized cream cardigan over a white camisole, hair slightly tousled, smiling at the camera and lifting one hand in a small wave, cozy bedroom with white linen and a plant behind her, soft morning sunlight.
```
- **G2** (첨부 H1 → P1)
```
Use the first attached image as the reference for the woman and the second attached image as the reference for the ampoule bottle.
Smartphone photo at a small white vanity table by the window: the same woman, seen from the chest up and slightly to the side, picks up the aqua-blue glass ampoule bottle with one hand and looks at it with a pleased smile, a round mirror and a few minimal skincare items on the table, soft morning light.
```
- **G3** (첨부 P1) — 손 매크로, 얼굴 없음
```
Use the attached image as the reference for the ampoule bottle and dropper.
Macro close-up of the frosted white dropper releasing a single clear drop of watery serum onto the back of a woman's hand, the drop glistening in soft morning light, the aqua glass bottle softly blurred in the background, natural skin texture, relaxed hand with five natural fingers.
```
- **G4** (첨부 H1)
```
Use the attached image as the reference for the woman's face, hair, beauty mark and earrings.
Close-up photo of the same woman in front of a round mirror in morning light, gently patting her cheek with her fingertips, eyes softly closed with a content smile, her skin looking fresh, dewy and glowing, natural skin texture, cream cardigan.
```
- **G5** (첨부 P1)
```
Use the attached image as the reference for the ampoule bottle.
Hero product shot of the same aqua-blue glass ampoule bottle standing in a few millimetres of clear still water on pale stone, soft concentric ripples around its base, bright clean morning light with soft caustic reflections, plenty of empty space above for a logo.
```
- **G6** (첨부 H1)
```
Use the attached image as the reference for the woman's face, hair, beauty mark and earrings.
Smartphone photo of the same woman at her apartment front door in the morning, dressed for work in a light blue shirt and beige trousers with a tote bag on her shoulder, turning back toward the camera with a playful wink and a smile, soft daylight from the doorway.
```
+ 각 이미지에 이미지 꼬리말

### 영상 (첨부: 해당 컷 이미지 1장 · 새 대화 · Omni 1.1 Flash · 9:16)
- **G1**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same room and the same woman from the first frame.
Filmed like a phone selfie video: she gives a small friendly wave at the camera and smiles, then tucks her hair behind her ear. Slight natural handheld shake. She does not talk.
Audio: soft morning room tone, birds outside the window.
```
- **G2**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts.
She lifts the aqua-blue ampoule bottle slowly toward the camera to show it, tilting it gently so the light catches the glass, with a pleased smile. Her hand and fingers stay natural and relaxed. She does not talk.
Audio: a soft glass clink, morning room tone.
```
- **G3**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts.
Macro: a single clear drop of serum slowly falls from the dropper onto the back of the hand and spreads into a thin glistening film. The hand stays still. Soft morning light.
Audio: a tiny delicate liquid drop.
```
- **G4**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same woman from the first frame.
She gently pats her cheek two times with her fingertips, eyes softly closed, then opens her eyes and smiles at her reflection. Her skin catches the morning light with a fresh dewy glow. Slow, calm movement. She does not talk.
Audio: soft patting sounds, a quiet happy exhale.
```
- **G5**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same bottle throughout.
Soft concentric ripples spread slowly from the base of the ampoule bottle across the clear water, light caustics shimmering on the stone. The camera pushes in very slightly. The bottle never changes shape.
Audio: a soft water droplet, a gentle shimmer.
```
- **G6**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same woman from the first frame.
She adjusts the tote bag on her shoulder, looks back at the camera with a playful wink and a smile, then turns toward the open door. Natural, light movement. She does not talk.
Audio: keys jingling, a door opening, morning street sounds outside.
```
+ 영상 꼬리말 (브이로그)

**편집:** UGC 자막(둥근 굵은 고딕 + 흰 말풍선 박스), 컷 템포 빠르게(2~3초), BGM은 가벼운 로파이. 원하면 AI 여성 보이스로 자막을 읽는 내레이션 추가 (입 모양이 안 보이므로 자연스러움).

---

## 2. QC (두 편 공통)
- [ ] 모든 컷의 얼굴이 H1과 같은 사람 (특히 **왼쪽 눈 아래 점**)
- [ ] 손가락 5개, 자연스러운 손 모양
- [ ] 말하는 입 모양 없음
- [ ] 옷·제품에 AI 글자 없음
- [ ] 캐릭터처럼 매끈한 피부 X → 편집 모드로 질감 보강
- [ ] 각 영상은 가장 좋은 2~3초만 사용
