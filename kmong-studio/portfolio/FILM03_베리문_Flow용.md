# FILM 03 「BERRY MOON」 v2 — SNS 숏폼 CF · Google Flow 전용

> **가상 브랜드:** BERRY MOON (딸기 케이크 카페) · **9:16 · 15초 · 24fps · 5컷**
> **로그라인:** 오늘 밤 달이 이상하다. 하늘에 뜬 건 **거대한 딸기**. 그 달은 매일 밤, 한 카페의 케이크 위로 내려앉는다.
> **한 줄 구조:** 이상한 달(훅) → 달이 뜨는 곳(궁금증) → 달이 케이크에 내려앉음(마법) → 케이크(제품) → 달을 들고 집에 가는 사람(여운·CTA)

---

## v1에서 v2로 바꾼 이유

| v1 문제 | 원인 | v2 해결 |
|---|---|---|
| 이야기가 없음 (굴러옴 → 크림 → 카페 → 케이크) | 장면마다 새 사건, 주인공·이유 없음 | **"딸기 달"** 하나로 처음부터 끝까지 관통. 브랜드명(BERRY MOON)이 곧 이야기 |
| 전환이 뚝뚝 끊김 | 컷 사이에 공통 모양·움직임 없음 | 모든 컷을 **동그라미(달·창·케이크)** 로 이어 붙이는 매치 컷 + 줌/푸시인 방향 통일 |
| AI 티 (공중부양·뒤집힘·크림 물리) | 거대 물체를 **움직이게** 하고, 유체(크림 홍수)를 시킴 | 거대 딸기는 **하늘에 가만히** 떠 있음. 움직이는 건 **카메라**와 **작은 딸기 한 알**뿐 |
| 현실감 부족 | 낮/저녁 시간대가 섞이고, 연출된 행인 | 전부 **블루아워(해 진 직후)** 한 시간대. 거리 컷은 **실제 폰 영상** 문법(틸트업·디지털 줌·흔들림) |
| 사람 얼굴·손 어색함 | 반응 연기, 손 클로즈업 | 사람은 **실루엣·뒷모습만**, 손 없음 |

**AI 티를 줄이는 5원칙 (이 시트 전체에 적용)**
1. 한 컷에 **동작 하나**만
2. 큰 물체는 **정지**, 움직임은 카메라가 담당
3. **한 시간대·한 조명**으로 통일 (블루아워 + 카페 따뜻한 빛)
4. 사람은 뒷모습·실루엣, 손·얼굴 클로즈업 금지
5. 영상은 10초로 나와도 **가장 좋은 2~4초만** 사용

---

## 0. 설정

| 항목 | 값 |
|---|---|
| 비율 | **9:16** (이미지·영상 모두) |
| 모델 | 이미지 Nano Banana 2 · 영상 Omni 1.1 Flash (최종 컷만 상위 품질) |
| 대화 | **컷마다 새 대화**(✎)에서 생성 — 이전 컷 맥락이 섞이지 않게 |
| 거절 방지 | 사람을 "똑같이 유지"하라고 하지 않기, `fake` 단어 쓰지 않기 |

### 꼬리말 A — 거리(폰 영상) 컷: #1 · #2 · #5
```
Realistic smartphone video, vertical 9:16, handheld with natural micro-shake and phone auto-exposure, real blue-hour city light, true-to-life scale and lighting so the giant strawberry looks like it is really hanging in the sky. No text, no letters, no logos, no readable signs, no watermark. Audio: sound effects only as described, no music, no dialogue.
```

### 꼬리말 B — 카페 안 · 제품 컷: #3 · #4
```
High-end food commercial, macro lens, shallow depth of field, warm cozy cafe light, glossy textures, appetizing, vertical 9:16 framing. No text, no letters, no logos, no watermark. Audio: sound effects only as described, no music, no dialogue.
```

### 이미지 꼬리말 (이미지 만들 때 전부)
```
Vertical 9:16 photorealistic image, realistic light, realistic textures, ultra detailed. No text, no letters, no logos, no readable signs, no watermark.
```

---

## 1. 재료 이미지

| 재료 | 상태 | 쓰는 컷 |
|---|---|---|
| **S1 딸기** (분홍 배경) | ✅ 있음 | #1 · #3 · #5 |
| **S4 카페** (분홍 문 · 보름달 창 · 초승달 네온, 해 질 녘) | ✅ 있음 — **#2 첫 프레임으로 그대로 사용** | #1 · #2 · #5 |
| **S2 케이크 조각** | ✅ 있음 | #4 |
| **S5 홀케이크** (새로 만들기) | ⏳ | #3 |
| S3 골목 (낮) | v2에서는 안 씀 (시간대가 달라서) | — |

**S5 홀케이크 (Nano Banana 2 · 첨부: S2 케이크 → 케이크 크림·스펀지 질감 기준)**
```
Use the attached image as the reference for the cream, sponge and strawberries.
Overhead view of a whole round strawberry cream cake on a white cake stand on a pale pink marble counter: a perfectly smooth white cream top like the surface of a full moon, a neat ring of piped cream swirls with sliced strawberries around the edge, the very center left empty and smooth. Warm cozy cafe light from the side, soft shadows.
```
+ 이미지 꼬리말 · 합격: **위에서 본 완벽한 원**, 가운데가 비어 있음, 딸기는 가장자리에만

---

## 2. 컷별 프롬프트

### #1 · 0:00–0:04 · 훅: "오늘 달, 이상하지 않아?" (틸트업 + 줌)
한 번의 생성으로 **틸트업 → 줌인**까지 연결되는 핵심 컷. 거대 딸기는 하늘에 **정지**.

- **① 첫 프레임 (첨부: S4 카페 → S1 딸기)**
```
Use the first attached image as the reference for the red-brick street and cafe style, and the second attached image as the reference for the strawberry.
Smartphone photo at blue hour on a cobblestone street lined with red-brick buildings and warm glowing windows: three passersby seen from behind have stopped in the middle of the street and are looking up at the sky, one holding up a phone. At the very top of the frame, just above the rooftops, the lower part of a giant glowing strawberry is visible in the deep blue sky, like a huge full moon rising, soft pink glow around it.
```
+ 이미지 꼬리말 · 합격: 사람은 뒷모습, 딸기가 **하늘 위쪽에 일부만** 보여서 "뭐지?" 하게 만듦

- **② 영상**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same street and the same strawberry throughout.
The handheld phone camera slowly tilts up from the passersby to the sky, revealing the whole giant glowing strawberry hanging perfectly still above the rooftops like a full moon, its green leaves on top. Then the phone zooms in on it with a slight digital-zoom shake until the strawberry fills most of the frame, its golden seeds glowing softly like craters. The strawberry never moves or changes shape; only the camera moves.
Audio: quiet evening city ambience, a few amazed murmurs in the distance, a soft rising airy tone as the camera zooms in.
```
+ 꼬리말 A · **사용 구간:** 틸트업 시작 ~ 딸기가 화면을 채우는 순간 (약 4초)

### #2 · 0:04–0:06 · 달이 뜨는 곳 (보름달 창으로 푸시인)
**#1 끝(화면을 채운 둥근 딸기) → #2 첫 장면(둥근 보름달 창)** 동그라미 매치 컷.

- **① 첫 프레임:** **S4 카페 이미지를 그대로** 사용 (새로 만들 필요 없음)
- **② 영상**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same cafe throughout.
Slow, steady push-in toward the glowing round moon window above the pink door. The warm light inside flickers softly and a faint pink glow from above washes over the red bricks, as if the strawberry moon is shining on the cafe. The door stays closed and the pink crescent neon glows gently.
Audio: a soft evening breeze, a distant cafe door bell chime.
```
+ 꼬리말 A · **사용 구간:** 2초 (창이 화면을 채워 갈 때 → #3으로)

### #3 · 0:06–0:09 · 달이 케이크에 내려앉는다 (이 광고의 마법)
**#2 끝(둥근 창) → #3 첫 장면(위에서 본 둥근 홀케이크)** 동그라미 매치 컷. 하늘의 딸기 달이 **작은 딸기 한 알**이 되어 케이크 한가운데로 떨어진다. 손 없음.

- **① 첫 프레임 (첨부: S5 홀케이크 → S1 딸기)**
```
Use the first attached image as the reference for the cake and the second attached image as the reference for the strawberry.
Overhead close-up of the whole round cream cake on the pink marble counter, its smooth white top like a full moon, the center empty. A single glossy strawberry with green leaves is falling from above toward the center of the cake, softly glowing pink, captured mid-air.
```
+ 이미지 꼬리말
- **② 영상**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same cake throughout.
The glossy strawberry drops in slow motion and lands softly right in the center of the cake, sinking slightly into the cream with a gentle bounce, staying upright with its leaves on top. A faint pink glow fades away as it settles, and a puff of powdered sugar rises. The overhead camera slowly rotates a few degrees. The cake keeps exactly the same round shape.
Audio: a soft creamy plop, a tiny magical shimmer, warm cafe ambience.
```
+ 꼬리말 B · **사용 구간:** 떨어지기 시작 ~ 가루가 피어오르는 순간 (약 3초)

### #4 · 0:09–0:11.5 · 제품: 케이크 단면
- **① 첫 프레임:** **S2 케이크 조각** 그대로 사용 (또는 아래로 새로 생성)
```
Use the attached image as the reference for the cake. Keep it exactly the same.
Macro close-up at table height of the strawberry cream shortcake slice on the white plate, its three soft sponge layers, silky cream and juicy strawberry slices in sharp focus, a silver fork resting beside it, warm cafe light, the glowing round window softly blurred behind.
```
+ 이미지 꼬리말
- **② 영상**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same cake throughout.
Very slow macro slide along the side of the cake slice, revealing its soft sponge layers, silky cream and juicy strawberry slices. The strawberries on top glisten and a few grains of powdered sugar drift down in the warm light. The cake keeps exactly the same shape and layers.
Audio: quiet cafe ambience, a faint cup clink.
```
+ 꼬리말 B · **사용 구간:** 2.5초

### #5 · 0:11.5–0:15 · 엔딩: 달을 들고 집에 간다
- **① 첫 프레임 (첨부: S4 카페 → S1 딸기)**
```
Use the first attached image as the reference for the cafe and the second attached image as the reference for the strawberry.
Wider smartphone photo at blue hour: the red-brick cafe with its glowing round moon window and pink door on a quiet cobblestone street, and high above its rooftop the giant glowing strawberry hangs in the deep blue sky like a full moon, a few stars around it. A customer seen from behind is walking away from the cafe down the street, holding a small pink cake box. Plenty of empty sky space at the top of the frame.
```
+ 이미지 꼬리말
- **② 영상**
```
Animate the attached image, using it as the first frame. One continuous shot with no cuts, the same cafe, street and strawberry throughout.
The customer walks slowly away down the street holding the pink cake box, seen from behind. The camera stays almost still with a slight handheld sway. The giant strawberry hangs perfectly still in the sky, glowing softly, and a few stars twinkle. The cafe window glows warmly.
Audio: footsteps on cobblestones, a soft evening breeze, a gentle closing chime.
```
+ 꼬리말 A · **사용 구간:** 3.5초 · 하늘 여백에 로고

---

## 3. 편집

### 타임라인 (15초)
| 시간 | 컷 | 전환 | 자막 (위쪽 18~24%) |
|---|---|---|---|
| 0:00–0:04 | #1 틸트업 → 딸기 달 줌인 | — | 0.2s **오늘 달… 좀 이상하지 않아?** |
| 0:04–0:06 | #2 보름달 창 푸시인 | **둥근 딸기 → 둥근 창** 매치 컷 | **이 달이 뜨는 곳이 있다** |
| 0:06–0:09 | #3 딸기가 케이크에 내려앉음 | **둥근 창 → 둥근 케이크** 매치 컷 | **매일 밤, 딸기 한 알이 내려앉는 케이크** |
| 0:09–0:11.5 | #4 케이크 단면 | 착지 "톡"에 맞춰 컷 | (작게) **딸기 생크림 케이크** |
| 0:11.5–0:15 | #5 달을 들고 집에 가는 손님 | 부드럽게 컷 | 로고 **BERRY MOON** + `매일 밤 11시까지` |

- 컷은 **동작이 끝나는 순간이 아니라 "동그라미가 화면을 채운 순간"**에 넘긴다 → 끊김 없이 흐름
- #1→#2, #2→#3 전환에 **0.2초 화이트/핑크 플래시 없이** 순수 하드컷 (매치 컷이 알아서 이어줌)
- 색: 거리 컷은 블루(차가움) · 카페 안은 따뜻한 골드 → 마지막에 둘이 한 화면(파란 하늘 + 따뜻한 창)

### 자막·로고
- 자막: **Pretendard Bold**, 흰색 + 부드러운 그림자, 핵심 단어 하나만 딸기색 `#E8475F`
- 로고: 둥근 세리프 `BERRY MOON` + 초승달 심볼, #5 하늘 여백에 천천히 페이드 인
- 아래 20%는 인스타·쇼츠 UI 자리라 비움

### 사운드
- 흐름: 조용한 밤거리 → (줌) 공기가 멈추는 듯한 상승 톤 → 카페 종소리 → **"톡" 착지 = 비트 드롭** → 따뜻한 BGM → 엔딩 차임
- **BGM Suno Style:** `dreamy lo-fi bossa nova, soft nylon guitar, warm rhodes, gentle brushed drums, night city mood, sweet and cozy, 92 bpm, instrumental, dessert cafe commercial`
- 드럼은 **#3 "톡"에서 시작** (그 전엔 기타·패드만)

---

## 4. QC
- [ ] 첫 1.5초 안에 "하늘에 뭔가 있다"가 보인다
- [ ] 거대 딸기가 **한 번도 움직이거나 모양이 바뀌지 않는다**
- [ ] 모든 거리 컷이 같은 블루아워 시간대다
- [ ] 동그라미 매치 컷 2곳(#1→#2, #2→#3)이 자연스럽게 이어진다
- [ ] 사람 얼굴·손이 클로즈업으로 나오지 않는다
- [ ] 간판·창문 어디에도 AI 글자가 없다
- [ ] 소리 끄고 봐도 "달 → 카페 → 케이크" 이야기가 이해된다
