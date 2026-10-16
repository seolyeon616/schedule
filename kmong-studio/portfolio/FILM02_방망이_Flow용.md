# FILM 02 「방망이 (THE CLUB)」 — Google Flow 전용 프롬프트 시트

> 뚝딱컷 브랜드 필름 · **50초 · 16:9 · 24fps** · 10컷 (방망이 컷 + 7개 세계 + 몽타주 + 엔드)
> 로그라인: *금빛 도깨비 방망이가 "뚝딱" 칠 때마다 광고 한 편이 태어난다. 마지막 "뚝딱"에 나오는 건 당신의 브랜드.*
> Flow(Veo 3.1) 기능 기준입니다. 메뉴 이름은 업데이트에 따라 조금 다를 수 있습니다.

---

## 0. 먼저 알아둘 것

| 항목 | 방법 |
|---|---|
| 비율 | Flow 설정에서 **16:9** |
| 모델 | 테스트는 **Fast**, 최종 컷만 **Quality** |
| 방망이 모양 고정 | 방망이가 나오는 컷(#0, #1, #8, #9)은 **ING-CLUB을 재료로 넣거나 첫 프레임으로** 사용 |
| "뚝딱" 소리 | Veo가 타격음을 만들어 주지만, **최종 "뚝딱" 사운드 로고는 따로 제작**해 모든 전환에 똑같이 사용 (아래 4번) |
| 손 | 방망이를 쥔 손은 **절대 보여주지 않기**. 방망이는 스스로 떠서 움직임 |
| 글자 | 자막 `〇〇 나와라`와 로고는 **전부 편집에서** 넣기 |

### 공통 꼬리말 (모든 영상 프롬프트 끝에)
```
Cinematic high-end commercial, shot on a large-format cinema camera with anamorphic lens, subtle film grain, dramatic contrast, rich blacks with champagne gold highlights. No text, no letters, no logos, no watermark, no human hands. Audio: sound effects only as described, no music, no dialogue.
```

### 이미지 꼬리말 (Flow에서 이미지 만들 때)
```
Cinematic 16:9 still frame, high-end commercial photography, anamorphic lens look, subtle film grain, rich blacks, champagne gold highlights, ultra detailed. No text, no letters, no logos, no watermark, no human hands.
```

---

## 1. 재료(Ingredients) 이미지 — 제일 먼저

**ING-CLUB 방망이 (가장 중요 — 마음에 들 때까지 여러 장 뽑기)**
```
A sleek modern Korean dokkaebi magic club floating upright in darkness: a smooth polished dark ebony wood body that widens toward a rounded blunt head, traditional cloud patterns inlaid in thin gold leaf, and instead of spikes it has rows of small glowing golden rectangular studs shaped like film sprocket holes. A slender handle wrapped with thin gold bands and a gold end cap. Dramatic rim light tracing its silhouette, pure black background, luxury prop design, centered.
```
+ 이미지 꼬리말
> 고르는 기준: ① 칼·야구방망이처럼 보이지 않고 **머리가 둥글고 두툼할 것** ② 금색 스프로킷 돌기가 선명할 것.

**ING-SHOCK 충격파 소스 (모든 세계 전환에 재사용)**
- 모드: Text to Video
```
Low-angle close-up on a glossy pure black floor. A ring-shaped shockwave of golden light bursts outward from the center in slow motion, sparks and fine golden dust lifting into the air, then fading. Pure black background. Audio: a deep wooden knock impact followed by a bright metallic ring and a sub-bass boom.
```
+ 공통 꼬리말
> 이 클립 하나를 편집에서 **모든 "뚝딱" 순간에 겹쳐** 씁니다 (Screen/Add 블렌드).

**ING-MODEL 패션 모델 (가상 인물, #4용)**
```
Full-body fashion portrait of a fictional East Asian female model in her 20s, sharp elegant features, sleek dark hair pulled back, wearing a long flowing crimson silk gown, standing still with a calm powerful expression, neutral studio background.
```
+ 이미지 꼬리말
> 실존 인물과 닮았으면 폐기.

---

## 2. 컷별 Flow 프롬프트

### #0 · 0:00–0:05 · 금가루가 방망이가 된다 【훅】
- **모드:** Ingredients to Video (재료: ING-CLUB)
```
In total darkness, drifting golden dust particles slowly swirl together and form the floating ebony dokkaebi club from the reference, its golden studs lighting up one by one. It hovers in the center, rotating very slowly, a thin rim light tracing its silhouette. Slow push-in. Silent, mysterious, luxurious. Audio: a faint shimmering whisper of gold dust, then silence.
```
+ 공통 꼬리말
- **편집:** 마지막 1초에 방망이가 아래로 내려치는 동작은 #1 첫 부분과 이어 붙입니다.

### #1 · 0:05–0:10 · 뚝딱 → 버거 나와라 (F&B)
- **1-a 타격 (방망이)** · Ingredients to Video (ING-CLUB)
```
The floating ebony dokkaebi club from the reference swings down on its own and strikes a glossy black floor with its rounded head. At the impact a ring of golden light bursts outward across the floor, sparks flying. Low angle, slow motion. Audio: a sharp wooden knock and bright metallic ring.
```
- **1-b 세계** · Frames to Video (첫 프레임 이미지 먼저 생성)
  - 첫 프레임:
```
A gourmet burger assembling itself in mid-air above a black plate: brioche bun, crisp lettuce, tomato slices, glossy beef patty with cheddar melting and dripping, each ingredient floating in sequence, sesame seeds suspended, charcoal background, warm key light.
```
  - 영상:
```
Ultra high-speed slow motion: burger ingredients fall from above one by one and stack perfectly in mid-air — bun, lettuce, tomato, patty with cheddar melting and dripping, top bun with sesame seeds bouncing. Warm key light, charcoal background. The camera tilts up with the stack. Audio: juicy sizzle, soft landing thuds.
```
- **편집 자막:** `버거 나와라`

### #2 · 0:10–0:15 · 자동차 나와라 (모빌리티)
- **모드:** Text to Video 또는 Frames to Video
```
A sleek unbranded silver concept car slices through heavy rain on a coastal highway at night, water spraying in wide arcs, headlights streaking, wet asphalt mirroring city lights. Fast low tracking shot alongside the car. The car has no logo, no badge and no text. Audio: a smooth powerful electric motor whoosh, heavy rain and tire spray.
```
- **편집 자막:** `자동차 나와라` · 실존 차 브랜드와 닮았으면 재생성.

### #3 · 0:15–0:20 · 향기 나와라 (뷰티)
- **모드:** Frames to Video
  - 첫 프레임:
```
A perfectly still water surface in a dark navy space, champagne gold backlight, the very top of a crystal perfume bottle just breaking through the surface, rose petals floating above.
```
  - 영상:
```
Macro crane-up: a crystal perfume bottle rises slowly up through the perfectly still water surface, sending concentric ripples outward, while rose petals float upward around it in reverse gravity. Champagne gold backlight, deep navy background. The bottle has no label. Audio: a gentle water emergence, delicate glassy shimmer.
```
- **편집 자막:** `향기 나와라`

### #4 · 0:20–0:25 · 바람 나와라 (패션)
- **모드:** Ingredients to Video (재료: ING-MODEL)
```
A towering wall of sandstorm parts in the middle to reveal the model from the reference standing on a golden sand dune at sunset. Her long crimson silk gown streams dozens of meters into the wind like liquid fire. Aerial shot slowly descending toward her. Her face stays consistent. Epic, high fashion. Audio: roaring desert wind easing into a soft silk flutter.
```
- **편집 자막:** `바람 나와라`

### #5 · 0:25–0:30 · 집 나와라 (공간/부동산)
- **모드:** Text to Video
```
On an empty plot of land at dusk, glowing golden lines of light draw and construct a minimalist modern house in seconds — walls, large glass windows, flat roof — then warm interior lights switch on one by one. Slow orbit around the house. Architectural visualization, magical realism. Audio: soft rising construction chimes, a final warm click as the lights turn on.
```
- **편집 자막:** `집 나와라`

### #6 · 0:30–0:35 · 미래 나와라 (테크)
- **모드:** Text to Video
```
FPV flight at high speed through a futuristic city built from flowing streams of light data and translucent holographic skyscrapers, cyan and violet palette with gold accents, smooth banking turns, sense of wonder. Audio: an airy digital whoosh with soft electronic pulses.
```
- **편집 자막:** `미래 나와라`

### #7 · 0:35–0:41 · 달 나와라 (K-컬처)
- **모드:** Frames to Video
  - 첫 프레임:
```
A traditional Korean hanok at night under a giant full moon, paper lattice doors glowing warmly from inside, curved tiled eaves silhouetted against the moonlit sky, mist in the distant mountains, poetic and elegant.
```
  - 영상:
```
The hanok's paper lattice doors slide open under the giant full moon. Beyond them, a traditional ink-wash landscape painting comes alive: mist flows between the mountains and a white crane glides across. The camera glides forward through the doors into the painting. Audio: a single gayageum pluck, soft night insects, flowing mist.
```
- **편집 자막:** `달 나와라` · 가야금 한 음이 이 영상의 한국적 정체성 포인트.

### #8 · 0:41–0:45 · 뚝딱뚝딱뚝딱 몽타주
- **8-a 연속 타격** · Ingredients to Video (ING-CLUB)
```
The floating ebony dokkaebi club from the reference strikes the glossy black floor three times in rapid rhythm, each hit sending out a brighter ring of golden light, sparks building up. Locked-off low angle. Audio: three accelerating wooden knocks with metallic rings.
```
- **편집:** 세 번 타격 사이에 #1~#7의 가장 강한 장면을 **0.3초씩** 끼움 → 4프레임 블랙 → 정적

### #9 · 0:45–0:50 · 당신의 브랜드, 나와라 【엔드】
- **9-a 마지막 타격** · Ingredients to Video (ING-CLUB)
```
The floating ebony dokkaebi club from the reference rises slowly, pauses, then strikes the black floor one final time. A massive golden shockwave floods the entire frame with warm light, then golden dust drifts slowly in the dark. Audio: one deep definitive wooden knock, bright ring, long shimmering tail.
```
- **편집:** 금가루가 모여 로고 `뚝딱컷` → `촬영 없이, 방송급 광고를 뚝딱.`
  - 첫 카피 `당신의 브랜드, 나와라.` (Pretendard Black, 흰색) → 로고 (골드) → 슬로건

---

## 3. 편집 리듬표 (약 5초마다 "뚝딱")

```
0:05 뚝딱 → 버거   0:10 뚝딱 → 자동차   0:15 뚝딱 → 향수
0:20 뚝딱 → 사막   0:25 뚝딱 → 집       0:30 뚝딱 → 미래
0:35 뚝딱 → 한옥   0:41 뚝딱뚝딱뚝딱   0:45 마지막 뚝딱 → 로고
```
- 전환 방법: 각 세계 컷 끝 → **ING-SHOCK 충격파 겹치기 + 원형 와이프** → 다음 세계
- 자막 `〇〇 나와라`: 각 세계 시작 0.2초 후 등장, 1.5초 유지, 하단 중앙, Noto Serif KR Bold

## 4. 사운드

**"뚝딱" 사운드 로고 (1초, 한 번 만들어 모든 전환·모든 납품물 엔드카드에 사용)**
- ElevenLabs 등 효과음 생성 툴에서 레이어 3개를 따로 만들어 겹치기:
```
1) a single hollow wooden knock like a temple block, dry and close
2) a bright short metallic bell ring with a shimmering tail
3) a deep cinematic sub-bass boom, short
```
> Veo가 만든 타격음은 참고용. 최종은 이 사운드 로고로 통일해야 브랜드가 각인됩니다.

**BGM (Suno 등 상업 이용 플랜)**
```
modern Korean fusion cinematic trailer, 50 seconds, instrumental. Deep taiko and wooden percussion hits landing every 5 seconds on the transitions, subtle gayageum plucks, dark ambient synth pads, each section shifting texture (sizzle, engine, water, wind, construction, digital, traditional), a rapid triple hit build at 41 seconds, then total silence, then a final golden shimmering resolve.
```

## 5. QC 체크
- [ ] 방망이 모양이 모든 컷에서 같다 (특히 머리 모양·금색 돌기)
- [ ] 손이 한 번도 안 보인다
- [ ] 자동차·향수병에 실존 브랜드 흔적이 없다
- [ ] 화면에 AI가 만든 글자가 없다
- [ ] "뚝딱" 소리가 모든 전환에서 같은 소리다
- [ ] 첫 5초 안에 방망이가 완성되어 보인다

## 6. 쇼케이스용 파생물
| 산출물 | 구성 |
|---|---|
| 9:16 숏폼 20초 | #0(2s) → 뚝딱 → #1(2s) → 뚝딱 → #3(2s) → 뚝딱 → #7(3s) → #8 → #9. 세이프존 상단 14% · 하단 20% |
| 인스타 시리즈 「〇〇 나와라 뚝딱」 | #1~#7을 각각 7초 숏폼으로 따로 올리기 (첫 게시물 7개 확보) |
| 키비주얼 | #0 방망이 완성 프레임, #9 충격파 프레임 → 크몽 썸네일 실사 교체용 |
