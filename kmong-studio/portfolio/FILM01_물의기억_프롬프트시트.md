# FILM 01 「물의 기억 (MEMORY OF WATER)」 — 제작용 프롬프트 시트

> 가상 브랜드 **AURÉA** 빙하수 세럼 · **45초 · 16:9 · 24fps · 4K 마스터** · 10컷
> 로그라인: *물방울 하나가 1만 년을 거슬러 올라, 마침내 당신의 피부에 닿는다.*
> 이 문서만 보고 위에서부터 순서대로 복사→붙여넣기 하면 완성되도록 만들었습니다.

---

## 0. 작업 순서 (총 약 13시간)

| 단계 | 할 일 | 툴 | 시간 |
|---|---|---|---|
| ① | 레퍼런스 3장 생성 (제품 · 모델 · 무드) | Midjourney 또는 Google 이미지 모델 | 1h |
| ② | 컷별 **첫 프레임** 10장 생성 → 베스트 선택 | 같은 툴 + ①을 레퍼런스로 첨부 | 2h |
| ③ | 첫 프레임 → 영상 생성 (Image-to-Video), 컷당 4~8회 | Veo / Kling | 5h |
| ④ | 편집 · 트랜지션 · 색보정 | Premiere / DaVinci | 3h |
| ⑤ | BGM · SFX · 내레이션 · 타이틀 | Suno · ElevenLabs · After Effects | 2h |

**규칙 3가지**
1. 모든 이미지 프롬프트 끝에 **[공통 접미사]**를 붙이세요.
2. 영상 툴에서 생성된 오디오는 **음소거**하세요. 최종 사운드는 ⑤에서 따로 입힙니다.
3. 병에 **글자·로고를 생성하지 마세요.** 로고는 ④ 편집에서 합성합니다.

---

## 1. 공통 설정

### [공통 접미사] — 모든 이미지 프롬프트 끝에
```
, shot on ARRI Alexa 65 with anamorphic lens, subtle 35mm film grain, high-end luxury skincare commercial, physically accurate lighting, color palette of glacier cyan #BFE9F2, deep navy #0A1A2F and champagne gold #D9B77E, ultra detailed, no text, no logo, no watermark --ar 16:9 --style raw --s 150
```
> Midjourney가 아닌 툴을 쓰면 `--` 파라미터만 지우고 넣으세요.

### [세계관 문장] — 영상 프롬프트 맨 앞에 붙이면 톤이 통일됨
```
A luxury skincare film about a single drop of ancient glacier water traveling ten thousand years to reach human skin. Palette: glacier cyan, deep navy, champagne gold. Backlit, rim-lit, water caustics, slow and reverent pacing.
```

### [네거티브] — 입력칸이 있으면 넣고, 없으면 재생성 기준으로 사용
```
text, letters, logo, watermark, distorted hands, extra fingers, warped face, flicker, morphing bottle shape, jitter, cartoon, CGI look, oversaturated, lens dirt
```

---

## 2. 레퍼런스 3장 (제일 먼저)

### REF-A 제품 (AURÉA 병) — 이후 #8 #9 #10에 **이미지 레퍼런스로 첨부**
```
product reference sheet of one luxury serum bottle shown twice side by side, front view and three-quarter view: a slim cylindrical frosted glass bottle with softly rounded shoulders, filled with pale icy blue liquid, topped with a polished champagne gold dropper cap with a ribbed collar, no label, no text, seamless light grey studio background, large softbox key light from the left, clean reflections, high-end product photography, ultra sharp
```
+ 공통 접미사
> 고르는 기준: 병 실루엣이 단순하고 금색 캡이 선명한 것. 이 한 장이 모든 제품 컷의 기준입니다.

### REF-B 모델 (가상 인물) — 이후 #7 #8에 **캐릭터 레퍼런스로 첨부**
```
character reference sheet of a fictional Korean woman in her late 20s, three views side by side: front, three-quarter, profile, calm serene expression, dewy luminous glass skin, minimal natural makeup, straight dark hair tied in a low loose bun with a few face-framing strands, small gold stud earrings, ivory silk camisole, soft even beauty lighting, neutral grey background
```
+ 공통 접미사
> 실존 인물과 닮은 결과가 나오면 폐기하고 다시 생성하세요. (초상권)

### REF-C 무드 (스타일 레퍼런스)
```
moody cinematic still of glacier ice interior with turquoise light caustics, a single glowing droplet at the center, deep navy shadows, champagne gold highlights, luxurious and reverent atmosphere
```
+ 공통 접미사 → Midjourney라면 이후 모든 컷에 `--sref [이 이미지 URL]` 추가

---

## 3. 컷별 프롬프트

> 형식: **🖼 첫 프레임**(이미지 툴) → **🎬 영상**(Image-to-Video) → **✂️ 편집 메모**
> 영상은 8초 이하로 생성하고, 표의 길이만큼 잘라 씁니다.

### #1 · 0:00–0:03 · 역중력 물방울 【1.5초 훅】 · 추천 툴: Veo

🖼 첫 프레임
```
extreme macro photograph of a single perfectly spherical crystal-clear water droplet suspended in pure black void, thin icy cyan rim light tracing its edge, inside the droplet a tiny inverted reflection of a vast blue glacier is visible, microscopic surface ripples, razor thin depth of field
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Extreme macro, locked-off camera. In pure darkness, a single water droplet falls UPWARD against gravity in ultra slow motion, drifting from the bottom of the frame toward the top. Its surface wobbles gently. An icy cyan rim light glints across it, and a tiny glacier reflection shimmers inside. Nothing else moves. Silent, hypnotic, 24fps.
```
✂️ 편집: 0.5초부터 사용. **첫 프레임부터 물방울이 움직이고 있어야** 훅이 됩니다. 역방향이 안 나오면 정방향으로 떨어지는 영상을 생성한 뒤 **편집에서 역재생**하세요 (가장 확실한 방법).

---

### #2 · 0:03–0:07 · 물방울 속 빙하로 진입 · 추천 툴: Kling (시작/끝 프레임)

🖼 시작 프레임 = #1의 마지막 프레임 캡처
🖼 끝 프레임
```
epic aerial view flying low over an immense blue glacier canyon at dawn, towering walls of translucent turquoise ice, soft golden sunrise haze drifting through the canyon, sense of vast ancient scale
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] The camera pushes steadily into the floating water droplet. The glacier reflected inside grows larger and larger until the camera passes through the droplet's surface in one seamless move and emerges flying low over an immense blue glacier canyon at dawn, golden haze drifting between the ice walls. One continuous camera move, no cuts.
```
✂️ 편집: 물방울 표면을 통과하는 순간에 **화이트 플래시 2프레임 + 저음 "훙"** SFX. 이음새가 어색하면 루마 페이드로 가립니다.

---

### #3 · 0:07–0:11 · 빙하 속에 갇힌 물 · 추천 툴: Veo

🖼 첫 프레임
```
inside a glacier, a small pocket of ancient liquid water trapped between layers of translucent blue ice crystals, sunlight refracting through the ice into shifting turquoise caustic patterns, a single droplet at the center glowing faintly champagne gold, tiny air bubbles frozen in the ice, sense of deep ancient time
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Slow lateral tracking shot gliding through translucent glacier ice. Turquoise light caustics ripple and shift across the ice layers. At the center, the trapped droplet slowly melts free and begins to glow soft gold. Micro bubbles rise past the lens. Majestic, meditative, very slow.
```
✂️ 편집: 화면 하단 중앙에 자막 `10,000 YEARS AGO` (Pretendard Light, 자간 +40%, 흰색 70%) 1.5초 페이드 인·아웃.

---

### #4 · 0:11–0:15 · 폭포 다이브 · 추천 툴: Kling

🖼 첫 프레임
```
top of a glacial meltwater waterfall seen from directly above the edge, turquoise water plunging down into a misty valley far below, small rainbows in the spray, early morning light, dramatic vertical depth
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] FPV drone shot: the camera tips over the edge of the glacial waterfall and dives straight down alongside the falling water, fast yet perfectly smooth, spray and mist rushing past the lens, rainbows flashing in the spray, plunging toward a turquoise pool far below.
```
✂️ 편집: 영상 속도를 **110~120%**로 올리고, 끝부분 모션 블러 구간에서 다음 컷으로 스위시 트랜지션.

---

### #5 · 0:15–0:19 · 이끼 숲의 이슬 · 추천 툴: Veo

🖼 첫 프레임
```
macro shot of a single dew droplet resting on the central vein of a vibrant green fern leaf in an ancient mossy forest, golden dawn light rays streaming through the canopy behind, creamy bokeh, the droplet acting as a tiny lens reflecting the forest
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Macro follow shot. The dew droplet rolls slowly along the vein of the fern leaf, catching and bending the golden dawn light. The leaf sways slightly in a gentle breeze. At the tip of the leaf the droplet swells, detaches and falls out of frame. Calm, fresh, alive.
```
✂️ 편집: 물방울이 잎 끝에서 떨어지는 순간 = 다음 컷 시작 (**액션 매치 컷**).

---

### #6 · 0:19–0:23 · 도시의 빗방울 · 추천 툴: Runway 또는 Veo

🖼 첫 프레임
```
close up of raindrops on a large floor to ceiling window at night, behind the glass the blurred neon lights of a modern Seoul skyline in cyan and warm amber bokeh, rain streaks running down the glass, moody premium atmosphere, shallow depth of field focused on the droplets
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] A single water droplet falls from above and splashes onto the window glass in slow motion. Then a slow rack focus pulls from the droplets on the glass to the blurred neon city lights behind, cyan and amber bokeh shimmering through the rain streaks. Quiet, urban, cinematic.
```
✂️ 편집: 도심 앰비언스를 아주 작게 깔아 "현재"로 넘어왔다는 걸 소리로도 알립니다.

---

### #7 · 0:23–0:29 · 창가의 여인 · 추천 툴: Veo (REF-B 첨부 필수)

🖼 첫 프레임
```
[REF-B woman] standing beside a rain-streaked floor to ceiling window at blue hour, eyes gently closed, rippling water-light caustics from the rainy window sliding across her cheek and neck, dewy glass skin, ivory silk camisole, soft cool window light with a warm gold rim light from behind, serene and intimate, medium close up
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Slow orbit from left to right around the woman standing by the rainy window. Rippling water-light caustics glide across her cheek and neck. She slowly opens her eyes, and a faint, calm smile appears. Minimal movement, intimate, luxurious. Her face stays consistent throughout.
```
✂️ 편집: **얼굴이 변형되면 무조건 재생성.** 눈 뜨는 순간이 훅 B 소재이니 가장 아름다운 1초를 표시해 두세요.

---

### #8 · 0:29–0:35 · 세럼 한 방울 【수미상관】 · 추천 툴: Veo (REF-A · REF-B 첨부)

🖼 첫 프레임
```
extreme macro of the champagne gold glass dropper from the reference bottle, a single drop of pale icy blue serum swelling at its tip above the woman's fingertip, inside the droplet a tiny reflection of a blue glacier is clearly visible, black background, champagne gold rim light
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Extreme macro. A drop of pale icy blue serum slowly swells at the tip of a glass dropper, a tiny glacier shimmering inside it exactly like the opening shot. It detaches and falls in slow motion onto a fingertip, spreading into a thin luminous film with a soft shimmer.
```
✂️ 편집: #1과 **같은 구도·같은 크기**로 맞춰 배치 → 관객이 "처음 그 물방울이다"라고 알아채게. 내레이션이 여기서 딱 한 줄 들어갑니다 (아래 5번).

---

### #9 · 0:35–0:41 · 제품 히어로 · 추천 툴: Kling (REF-A 첨부 필수)

🖼 첫 프레임
```
the reference serum bottle standing perfectly upright on a thin sheet of perfectly still water, beneath the water surface the faint glowing silhouette of a glacier is visible like a memory from another world, concentric ripples spreading from the base of the bottle, low angle, deep navy background, champagne gold rim light, hero product shot
```
+ 공통 접미사

🎬 영상
```
[세계관 문장] Low-angle slow arc of about 30 degrees around the serum bottle standing on still water. Concentric ripples spread gently from its base. Beneath the surface, the faint glacier silhouette glows and fades. A champagne gold rim light slides along the glass edge. The bottle shape never changes. Hero product shot.
```
✂️ 편집: 병 형태가 1프레임이라도 변하면 재생성. **로고 `AURÉA`는 AE에서 병에 트래킹 합성**합니다 (Mocha 또는 Planar Tracker).

---

### #10 · 0:41–0:45 · 엔드 타이틀 · After Effects

- 배경: 블랙 → #9 마지막 프레임을 20%로 깔아도 좋음
- 연출: 물방울 하나가 화면 중앙에 떨어져 잉크처럼 번지며 로고가 드러남
  (Turbulent Displace + Liquid 매트, 또는 아래 소스를 생성해 루마 매트로 사용)
```
a single drop of water falling onto a perfectly black glossy surface in slow motion, spreading into a clean circular ripple, top-down view, pure black background, minimal
```
- 카피 순서:
  1. `당신의 피부에 닿기까지, 1만 년.` — Noto Serif KR Medium, 흰색
  2. `AURÉA` — 영문 세리프(Cormorant 계열), 샴페인 골드, 자간 +30%
  3. 작은 글씨 `Glacial Origin Serum`
- 마지막 0.5초: 화면 우하단에 작게 **뚝딱컷 로고 + "뚝딱" 사운드 로고**

---

## 4. BGM (Suno 등 상업 이용 플랜)

```
minimal cinematic ambient score for a luxury skincare commercial, 45 seconds, instrumental. 0-7s: near silence, a single crystalline glass tone and deep sub bass swell. 7-19s: slow sparse felt piano notes, glass harmonics, glacial ambience, a sense of ancient time. 19-29s: soft urban pulse enters, warm pads. 29-41s: emotional warm string swell rising to a gentle peak. 41-45s: everything resolves to one resonant piano note with long reverb tail. Elegant, restrained, no drums.
```
> 3~4개 생성 → **29초 지점에서 감정이 올라오는 곡**을 선택.

---

## 5. 효과음 (ElevenLabs Sound Effects 등) & 내레이션

| 컷 | 효과음 프롬프트 |
|---|---|
| #1 | `a single water droplet sound played in reverse, crystalline, close, with a very long airy reverb tail` |
| #2 | `deep cinematic whoosh passing through water surface, low sub boom, airy` |
| #3 | `deep glacier ice creaking and cracking, slow, cavernous, distant` |
| #4 | `rushing waterfall white noise swelling up then cutting, powerful mist` |
| #5 | `soft forest dawn ambience, distant birds, a tiny water drip` |
| #6 | `rain tapping on a large glass window, muffled city ambience at night` |
| #8 | `a single delicate liquid drop landing on skin, soft tick with shimmering reverb` |
| #10 | `soft water drop impact spreading into a gentle shimmering chime` |

**내레이션** (#8에서 한 줄만, 여성 · 낮은 톤 · 속삭이듯 · 천천히)
```
1만 년을 기다린, 한 방울.
```
> ElevenLabs 디렉션 예: Stability 낮게(감정 표현↑), Style 중간. 호흡이 들리도록 앞에 0.3초 여백.

---

## 6. 편집 & 컬러

- 컷 연결은 **물의 움직임으로만** 이어집니다: 역중력 → 통과 → 녹음 → 낙하 → 굴러감 → 튐 → 비침 → 떨어짐 → 파문
- 색: 앞 절반(과거)은 시안/네이비로 차갑게 → #7부터 골드 림라이트로 따뜻하게 → **온도 변화 = 시간이 흘러 "지금"에 닿았다는 신호**
- 블랙 레벨을 살짝 올린 필름 룩 + 그레인 3%
- 자막 세이프존: 하단 10% 안쪽

## 7. 캠페인 킷 (포트폴리오 쇼케이스용)

| 산출물 | 구성 |
|---|---|
| 9:16 숏폼 15초 | #1(2s) → #3(2s) → #7(3s) → #8(4s) → #9(2s) → #10(2s). 상단 14% · 하단 20% 비우기 |
| 훅 A | #1 역중력 물방울로 시작 |
| 훅 B | #7 모델이 눈 뜨는 순간으로 시작 |
| 훅 C | 검은 화면 + 자막 `1만 년 된 물을 바른다면?` 1초 → #1 |
| 키비주얼 스틸 | #3, #7, #9 첫 프레임 → 4K 업스케일 |

## 8. QC 체크 (하나라도 걸리면 재생성)
- [ ] #7·#8 얼굴·손가락 변형 없음 (1프레임씩 확인)
- [ ] #8·#9 병 모양이 REF-A와 동일
- [ ] 화면 어디에도 AI가 만든 글자 없음
- [ ] #1과 #8 물방울 크기·위치가 대응됨
- [ ] 컷 사이 밝기·색온도 점프 없음 (의도된 온도 변화 제외)
- [ ] 첫 1.5초 안에 역중력 물방울이 보임
- [ ] 오디오 피크 −1dB 이하, 내레이션 명료
