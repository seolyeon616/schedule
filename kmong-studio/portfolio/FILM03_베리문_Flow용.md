# FILM 03 「BERRY MOON」 — SNS 숏폼 CF (FOOH / CGI) · Google Flow 전용

> **가상 브랜드:** BERRY MOON (딸기 케이크 전문 카페) · **9:16 · 15초 · 24fps · 7컷**
> **로그라인:** 평범한 오후, 골목으로 **거대한 딸기**가 굴러온다. 생크림이 파도처럼 골목을 채우고, 해 질 녘 그 딸기가 **달처럼 떠오른다.** — *BERRY MOON*
> **보여주는 것:** 첫 1.5초 훅 · 요즘 가장 반응 좋은 FOOH(가짜 옥외 광고) CGI 연출 · 제품 매크로 · 9:16 네이티브 화질
> 실제 지명·간판·브랜드 로고는 쓰지 않습니다 (가상의 붉은 벽돌 골목).

---

## 0. 먼저 알아둘 것

| 항목 | 방법 |
|---|---|
| 비율 | Flow 설정에서 **9:16** (이미지도 영상도 전부 세로로 생성 → 화질 손실 없음) |
| 모델 | 이미지 **Nano Banana 2** · 영상 **Omni 1.1 Flash** (테스트) → 최종 컷만 상위 품질 |
| FOOH 느낌의 핵심 | **"휴대폰으로 실제로 찍은 것 같은"** 화면: 핸드헬드 흔들림, 자연광, 평범한 행인. 거대한 딸기만 비현실적이어야 진짜처럼 보임 |
| 딸기 모양 고정 | 딸기가 나오는 컷은 **ING-S1(딸기)** 첨부 |
| 사람 | 행인은 **뒷모습·멀리** 위주. 얼굴 클로즈업 X |
| ⚠️ Flow 거절 방지 | "복제할 수 없는 요청"이 뜨면: ① 사람을 `Keep ... exactly the same`으로 고정하라고 하지 말고 `passersby ... with minimal movement`로만 표현 ② `fake` 단어 빼기 ③ 사람 웃음·말소리 요청 빼기 ④ 새 대화에서 다시. 그래도 안 되면 사람 없이 이미지를 다시 생성 |
| 글자 | 자막·로고·간판 글씨는 **전부 편집에서** (AI에게 글자 생성 금지) |

### 영상 꼬리말 A — FOOH 컷용 (#1–#4, #7)
```
Photorealistic CGI street commercial, shot on a smartphone, handheld with subtle natural shake, natural daylight, realistic scale and shadows so the giant object looks truly present in the street, vertical 9:16 framing. No text, no letters, no logos, no readable signs, no watermark. Audio: sound effects only as described, no music, no dialogue.
```

### 영상 꼬리말 B — 제품 컷용 (#5, #6)
```
High-end food commercial, macro lens, shallow depth of field, soft warm window light, glossy textures, appetizing, vertical 9:16 framing. No text, no letters, no logos, no watermark. Audio: sound effects only as described, no music, no dialogue.
```

### 이미지 꼬리말 (이미지 만들 때 전부)
```
Vertical 9:16 photorealistic image, natural light, realistic textures, ultra detailed. No text, no letters, no logos, no readable signs, no watermark.
```

---

## 1. 재료(참조) 이미지 4장 — 제일 먼저

**ING-S1 딸기 (히어로)** — 모든 거대 딸기 컷의 기준
```
A single perfect giant strawberry, deep glossy red, evenly spaced golden seeds, fresh bright green leafy calyx on top, tiny water droplets on its surface, isolated on a seamless light pink studio background, soft studio light, centered, product photography.
```
+ 이미지 꼬리말 · 합격: 딸기 1개, 모양이 예쁘고 반짝임, 꼭지 초록이 선명

**ING-S2 케이크 (제품)** — #5·#6의 제품 기준
```
A slice of strawberry cream shortcake on a small white ceramic plate: three layers of fluffy vanilla sponge and silky whipped cream with sliced strawberries inside, topped with a swirl of cream and two whole glossy strawberries, a light dusting of powdered sugar, on a pale pink marble table, soft window light, close-up food photography.
```
+ 이미지 꼬리말 · 합격: 단면 층이 깔끔, 크림이 매끈, 딸기가 선명

**ING-S3 골목 (배경)** — #1–#4의 거리 기준
```
A charming narrow red-brick alley in Seoul on a sunny spring afternoon, converted brick warehouses with large black steel-framed windows, small potted plants, a few pedestrians walking away in the distance, warm natural light, eye-level smartphone photo. Shop signs are blank with no writing.
```
+ 이미지 꼬리말 · 합격: 간판에 글자 없음, 골목이 앞으로 뻗어 있음

**ING-S4 카페 외관** — #4·#7의 가게 기준
```
The facade of a small cozy dessert cafe in a red-brick building: a large round moon-shaped window glowing with warm light, pale pink door, a small round blank pink neon sign shaped like a crescent moon with no letters, potted strawberry plants by the door, late afternoon light.
```
+ 이미지 꼬리말 · 합격: 동그란 창과 초승달 네온이 보이고 글자 없음

### 재료 사용처
| 재료 | 쓰는 컷 |
|---|---|
| ING-S1 딸기 | #1 · #2 · #3 · #7 |
| ING-S2 케이크 | #5 · #6 |
| ING-S3 골목 | #1 · #2 · #3 |
| ING-S4 카페 | #4 · #7 |

첨부 한 줄 (프롬프트 맨 앞):
```
Use the attached image as the reference for the [strawberry / cake / alley / cafe]. Keep it exactly the same.
```

---

## 2. 컷별 프롬프트 (각 컷: ① 첫 프레임 이미지 → ② 영상)

### #1 · 0:00–0:02 · 훅: 골목으로 굴러오는 거대 딸기
- **① 이미지 (첨부: ING-S3 → ING-S1)**
```
Use the first attached image as the reference for the alley and the second attached image as the reference for the strawberry.
Eye-level smartphone photo in the red-brick alley: a giant strawberry the size of a small car is rolling around the corner at the far end of the alley toward the camera, two pedestrians in the distance turning to look at it. Realistic scale, contact shadow on the pavement.
```
- **② 영상 (첨부: ①결과)** — v2: 1차 결과의 문제(장면 점프·공중부양·딸기 뒤집힘·크기 변화)를 막는 버전
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts: the same alley, the same buildings and the same strawberry from the first frame to the last.
The giant strawberry hops toward the camera in two slow, heavy bounces, like a huge soft ball. It always stays upright with its green leaves on top, never tumbling, spinning or flipping over. Each time it lands it touches the cobblestones, squashes slightly and casts a clear shadow; it never floats. Its size, shape and seed pattern stay exactly the same. The two passersby step aside to the edges of the alley, staying seen from behind. The camera stays in place at eye level with only a small natural handheld shake.
Audio: two deep soft thuds of the landing strawberry, street ambience.
```
+ 꼬리말 A · **편집:** 두 번째 착지 "쿵"까지 약 2초만 사용 → #2로 하드컷
- **그래도 튀면 (대안 B, 가장 안정적):** 딸기를 움직이지 말고 카메라만 움직이기
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same alley throughout.
The giant strawberry stays still in the alley. The handheld camera walks slowly toward it with natural footsteps, the strawberry growing larger in the frame, glossy and perfectly still, casting a shadow on the cobblestones. The two passersby stop and look up at it, seen from behind.
Audio: footsteps on cobblestones, street ambience, a low curious hum of the crowd.
```

### #2 · 0:02–0:04 · 쿵! 크림이 터진다
- **① 이미지 (첨부: ING-S3 → ING-S1)**
```
Use the first attached image as the reference for the alley and the second attached image as the reference for the strawberry.
Low-angle smartphone photo: the giant strawberry has stopped in the middle of the alley and landed on a huge soft mound of fresh whipped cream, cream starting to splash outward, a few loose strawberries flying in the air.
```
- **② 영상**
```
Animate the attached image, using it as the first frame.
The giant strawberry sinks softly into the mound of whipped cream and a thick wave of silky white cream bursts outward in slow motion, fresh strawberries tumbling through the air. The handheld camera shakes slightly from the impact.
Audio: a deep soft whump, a creamy splash, strawberries landing with light thuds.
```
+ 꼬리말 A

### #3 · 0:04–0:06 · 생크림 파도가 골목을 채운다 (탑뷰)
- **① 이미지 (첨부: ING-S3)**
```
Use the attached image as the reference for the alley.
High-angle view from a rooftop looking down the red-brick alley: a gentle river of glossy white whipped cream flows through the alley, whole strawberries bobbing on its surface like boats, pedestrians standing safely on doorsteps, smiling and taking photos from a distance.
```
- **② 영상**
```
Use the attached image as the first frame.
The camera slowly tilts down as the soft river of whipped cream flows gently down the alley, strawberries drifting and turning on the surface, the cream forming smooth glossy swirls around the corners of the brick buildings.
Audio: soft creamy flowing sounds, street ambience.
```
+ 꼬리말 A

### #4 · 0:06–0:09 · 크림이 카페 앞에 도착
- **① 이미지 (첨부: ING-S4)**
```
Use the attached image as the reference for the cafe.
Smartphone photo at street level: the river of whipped cream reaches the cafe with the round moon-shaped window and gently stops right at its pink door, forming a perfect smooth swirl like the top of a cake, a single strawberry resting on top of the swirl.
```
- **② 영상**
```
Use the attached image as the first frame. Keep the cafe exactly the same.
The whipped cream slides gently to a stop at the pink cafe door and curls into a perfect glossy swirl, a single strawberry rolling to rest on top. The warm light in the round window glows a little brighter.
Audio: a soft creamy settle, a small cafe door bell chime.
```
+ 꼬리말 A · **편집:** 크림 소용돌이 → #5 케이크 크림 소용돌이로 **매치 컷**

### #5 · 0:09–0:11 · 제품: 케이크 단면
- **① 이미지 (첨부: ING-S2)**
```
Use the attached image as the reference for the cake.
Extreme close-up of the strawberry cream shortcake slice on the white plate, a silver dessert fork slowly cutting down through the layers, glossy strawberries and silky cream in sharp focus.
```
- **② 영상**
```
Use the attached image as the first frame. Keep the cake exactly the same.
Slow macro push-in as the silver fork presses down through the soft sponge and cream layers, revealing juicy strawberry slices inside, a strawberry on top wobbling gently. Soft warm window light.
Audio: a soft fork sinking into sponge, a tiny ceramic clink.
```
+ 꼬리말 B

### #6 · 0:11–0:13 · 한 입 (손만)
- **① 이미지 (첨부: ING-S2)**
```
Use the attached image as the reference for the cake.
Close-up of a hand lifting a forkful of the strawberry cream cake toward the camera, a whole glossy strawberry on top, the cafe's round moon-shaped window softly blurred in the warm background.
```
- **② 영상**
```
Use the attached image as the first frame. Keep the cake exactly the same.
The hand slowly lifts the forkful of strawberry cream cake toward the camera, the cream soft and glossy, a crumb falling in slow motion, warm light flaring through the round window behind.
Audio: a soft happy exhale, gentle cafe ambience.
```
+ 꼬리말 B · **주의:** 손가락 수·모양 확인 (이상하면 재생성)

### #7 · 0:13–0:15 · 엔딩: 딸기 달이 뜬다
- **① 이미지 (첨부: ING-S4 → ING-S1)**
```
Use the first attached image as the reference for the cafe and the second attached image as the reference for the strawberry.
Smartphone photo at dusk looking up at the red-brick cafe with its glowing round window: above the rooftop, the giant strawberry floats in the pink and violet twilight sky like a rising moon, softly glowing, a few first stars appearing. Empty sky space above for a logo.
```
- **② 영상**
```
Use the attached image as the first frame. Keep the cafe and the strawberry exactly the same.
The giant strawberry slowly rises above the rooftop into the twilight sky like a moon, glowing softly pink, the cafe window light warming below. The handheld camera slowly tilts up to follow it.
Audio: a gentle magical shimmer, evening street ambience fading.
```
+ 꼬리말 A · **편집:** 하늘 여백에 로고 `BERRY MOON`

---

## 3. 편집

### 타임라인 (15초)
| 시간 | 컷 | 자막 (한국어 · 영어 버전) |
|---|---|---|
| 0:00–0:02 | #1 굴러오는 딸기 | **오늘, 골목에 딸기가 굴러왔다** · *Something sweet is rolling in.* |
| 0:02–0:04 | #2 쿵! | (자막 없이 소리로) |
| 0:04–0:06 | #3 크림 강 | **생크림이 넘쳐흐르는 중** · *The street is overflowing.* |
| 0:06–0:09 | #4 카페 도착 | **그 끝엔,** · *And at the end of it,* |
| 0:09–0:11 | #5 케이크 단면 | **매일 아침 딸기로 굽는 케이크** · *Fresh strawberries, every morning.* |
| 0:11–0:13 | #6 한 입 | (자막 없음) |
| 0:13–0:15 | #7 딸기 달 | 로고 **BERRY MOON** + `STRAWBERRY CAKE CAFE` |

- 컷 전환은 전부 하드컷, **딸기가 부딪히는 순간·크림이 멈추는 순간에 맞춰** 끊기 (리듬이 핵심)
- #4 크림 소용돌이 → #5 케이크 크림 소용돌이: **매치 컷**
- 1:1·4:5 피드용이 필요하면 9:16에서 가운데 잘라 추가 납품 (옵션 상품으로 안내)

### 자막 스타일 (SNS 숏폼)
- 폰트: **Pretendard Bold** (한글) / 영어는 Pretendard SemiBold · 흰 글씨 + 부드러운 그림자, 딸기색 `#E8475F` 포인트 한 단어
- 위치: 화면 **위에서 18~24%** (아래 20%는 인스타·쇼츠 버튼 자리라 비움)
- 등장: 0.15초 살짝 튀어 오르는 팝 (명품 광고와 달리 **경쾌하게**)
- 로고: 둥근 세리프(예: **Fraunces** 또는 Cormorant) `BERRY MOON` + 초승달 심볼, 하늘 여백에

### 사운드
- **BGM:** 경쾌한 보사노바/시티팝 느낌, 110~120bpm, 0:02 "쿵"에 맞춰 드럼 인
  Suno Style: `playful bossa nova city pop, bright acoustic guitar, soft brushed drums, light bells, sweet and fun, 116 bpm, instrumental, cafe commercial`
- **효과음 강조 지점:** 0:02 쿵(저음) · 0:03 크림 스플래시 · 0:08 카페 종소리 · 0:14 반짝 효과음
- 내레이션 없음 (자막 + 소리로 충분). 원하면 마지막에 여성 목소리 한 줄 *"베리문."*

---

## 4. QC (하나라도 걸리면 재생성)
- [ ] 첫 1.5초 안에 거대 딸기가 보인다
- [ ] 딸기 모양·색이 #1·#2·#3·#7에서 같다 (ING-S1)
- [ ] 케이크가 #5·#6에서 같다 (ING-S2)
- [ ] 간판·창문·화면 어디에도 AI가 만든 글자가 없다
- [ ] 행인 얼굴이 뭉개지거나 이상하지 않다 (멀리·뒷모습)
- [ ] #6 손가락 모양 정상
- [ ] 거대 딸기에 **그림자와 바닥 접지**가 있다 (없으면 합성 티가 남)
- [ ] 휴대폰으로 소리 끄고 봐도 이야기가 이해된다
