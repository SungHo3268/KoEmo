# KoEmo: Korean Emotional & Contextual Nuance Benchmark

한국어의 맥락 의존적 어휘 선택 능력을 평가하는 LLM 벤치마크

**데이터 제작 가이드라인**: [https://ko-bench.github.io/KoEmo/](https://ko-bench.github.io/KoEmo/)

## 연구 목적

한국어는 동일한 의미 범주 내에서도 맥락, 감정, 감각적 강도에 따라 상이한 단어를 선택해야 하는 풍부한 어휘 체계를 갖고 있다. 예를 들어 "뜨거운 국물"을 표현할 때, 단순한 온도 서술은 "뜨겁다", 추위 속에서의 긍정적 수용은 "뜨끈하다", 먹고 난 후의 개운함은 "시원하다"로 표현된다.

KoEmo는 이러한 **미묘한 어휘 선택의 차이를 LLM이 제대로 이해하고 있는지** 평가하는 벤치마크이다.

## 이론적 배경

### 어휘장 이론 (Lexical Field Theory, Trier 1931)
어휘는 고립적으로 존재하지 않고, 의미적으로 연관된 단어들의 장(field) 안에서 서로의 의미 경계를 규정한다. 같은 어휘장 내 단어들의 경계를 LLM이 제대로 인지하는지 직접 테스트한다.

### 평가어 이론 (Appraisal Theory, Martin & White 2005)
언어에서 태도(Attitude)를 감정(Affect), 판단(Judgement), 감상(Appreciation)의 세 축으로 분류한다. 한국어의 뉘앙스 차이가 이 "평가적 태도"의 미세한 차이에서 비롯된다.

### 한국어 감각어 분류 (채완 1986, 김광해 1993)
한국어 감각어를 오감 기반으로 체계적으로 분류하며, 특히 한국어의 상징어(음성상징어, 의태어, 의성어) 체계가 세계적으로 독보적으로 풍부하다는 점에 주목한다.

## 도메인 분류 체계

```
KoEmo
├── 1. 감각 표현 (Sensory)           ← 어휘장 이론 + 감각어 분류
│   ├── 1.1 시각 (Visual): 색상, 밝기, 크기/형태
│   ├── 1.2 미각 (Gustatory): 매운맛, 단맛, 짠맛, 쓴맛
│   ├── 1.3 촉각 (Tactile): 온도, 질감, 경도, 표면
│   ├── 1.4 청각 (Auditory): 소리 크기, 소리 질감
│   └── 1.5 후각 (Olfactory): 좋은 냄새, 나쁜 냄새
│
├── 2. 감정 표현 (Emotional)          ← Appraisal Theory (Affect)
│   ├── 2.1 긍정 감정: 기쁨, 편안함, 감동
│   ├── 2.2 부정 감정: 슬픔, 분노, 불안
│   └── 2.3 복합 감정: 아련함, 씁쓸함
│
├── 3. 판단 표현 (Judgement)          ← Appraisal Theory (Judgement)
│   ├── 3.1 사회적 관계: 친밀도, 예의, 배려
│   ├── 3.2 능력/성품 판단: 성실함, 영리함
│   └── 3.3 상황 판단: 적절성, 난이도
│
├── 4. 감상 표현 (Appreciation)       ← Appraisal Theory (Appreciation)
│   ├── 4.1 심미적 평가: 아름다움, 분위기
│   └── 4.2 가치 평가: 품질, 상태
│
└── 5. 상징 표현 (Symbolic/Ideophone) ← 한국어 고유 특성
    ├── 5.1 의태어: 움직임, 상태
    └── 5.2 의성어: 웃음, 울음
```

## 평가 형식

- **4지선다 객관식**: 상황/맥락이 주어지고, 가장 자연스러운 단어 1개를 선택
- **정답 체계**: 최적 정답 1개
- **도메인별 문항 수**: 대체로 균등하되 엄격히 강제하지 않음 (한국어 특성에 따른 자연스러운 불균형 허용)

## 데이터 형식

JSON Lines (.jsonl) 포맷. 각 문항의 스키마:

```json
{
  "id": "sensory_gustatory_001",
  "domain": "감각 표현",
  "category": "미각",
  "subcategory": "매운맛",
  "word_group": ["맵다", "얼큰하다", "알싸하다", "칼칼하다"],
  "scenario": "상황 설명 텍스트",
  "choices": ["맵다", "얼큰하다", "알싸하다", "칼칼하다"],
  "answer": "얼큰하다",
  "explanation": "정답 근거 설명"
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| id | string | 고유 식별자 (`{domain}_{category}_{번호}`) |
| domain | string | 상위 도메인 (5개 중 하나) |
| category | string | 중분류 |
| subcategory | string | 소분류 |
| word_group | list[str] | 해당 문항이 속한 유의어군 |
| scenario | string | 맥락/상황 설명 + 빈칸 |
| choices | list[str] | 4개의 선택지 |
| answer | string | 최적 정답 (1개) |
| explanation | string | 정답 근거 및 오답 단어들이 부적절한 이유 |

## 디렉토리 구조

```
KoEmo/
├── README.md
├── data/
│   ├── samples.jsonl          # 샘플 데이터
│   └── schema.json            # JSON 스키마 정의
└── word_samples               # 초기 아이디어 메모
```
