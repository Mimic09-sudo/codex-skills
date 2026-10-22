---
name: ctf-fastpath
description: Classify an authorized CTF challenge, route it to the narrowest rev/pwn/web/crypto/forensics/misc workflow, and drive evidence toward a reproducible input, solver, exploit, patch, decryptor, or recovery procedure. Use when the category or cheapest solve lane is not yet clear; switch to a specialist after classification.
metadata:
  domain: ctf
  layer: general
  subcategory: multi-category
  language: ko
---

# CTF Fastpath

## 역할

문제를 넓게 분석하는 스킬이 아니라, 가장 싼 성공 경로를 빠르게 고르고 전문 스킬로 넘기는 라우터다. 분류가 끝나면 선택된 분야만 깊게 본다.

승인된 CTF, 워게임, 로컬 챌린지 범위에서만 사용한다. 로컬 도구 실행은 `ctf-wsl-toolchain`을 따른다.

## 초기 분류

1. 문제 설명, 규칙, flag 형식, 제공 파일과 접속 정보를 확인한다.
2. `rg --files`, `file`, 헤더/메타데이터, 한 번의 안전한 실행 또는 루트 응답으로 입력·출력 형태를 고정한다.
3. flag에 가장 가까운 앵커 하나를 찾는다.
4. 대표 분야 하나와 첫 검증 하나를 선택한다.

| 증거 | 우선 분야 | 첫 검증 |
|---|---|---|
| 네이티브 크래시, 길이/포인터/수명 제어 | pwn | 보호기법과 최소 crash/leak |
| 비교, 성공 분기, 변환, VM, 패킹 | rev | success/compare xref 또는 런타임 dump |
| HTTP 라우트, 인증, 업로드, 템플릿 | web | 정상/변형 raw request diff |
| 암호문, nonce, oracle, 수식 | crypto | 인코딩 분리와 작은 forward model |
| PCAP, 메모리, 디스크, 로그 | forensics | 인벤토리·타임라인·고신호 artifact |
| 규칙/스테고/자동화/혼합 | misc | 최소 재현과 작은 solver |

파일 종류가 아니라 성공 조건을 기준으로 분류한다. 웹에서 받은 바이너리는 `web → rev`, 서비스 메모리 취약점은 `pwn`, PCAP에서 추출한 암호문은 `forensics → crypto`처럼 주 경로를 하나만 먼저 잡는다.

## 전문 스킬 라우팅

- `pwn`: [pwn 빠른 참조](references/pwn.md)를 읽고 `pwn-general`로 전환한다.
- 단순 단일 바이너리 `rev`: `rev-ctf-fastpath`로 전환한다.
- 복합/패킹/VM/대규모/다단계 `rev`: `rev-final-fastpath`로 전환한다.
- 게임/엔진 `rev`: `rev-game-hacking`으로 전환한다.
- `web`: [web 빠른 참조](references/web.md)를 읽는다.

존재하지 않는 전문 스킬을 가정하지 않는다. 전문 스킬이 없으면 이 스킬의 공통 계약으로 계속 진행한다.

## 증거 기반 solve cycle

### 성공 조건 고정

- `flag`, `correct`, `success`, `win`, 응답 차이, 출력 파일, 검증 함수 등 성공 앵커를 한 문장으로 쓴다.
- 입력 표면과 출력/검증 표면을 하나씩 고른다.

### 가장 싼 구분 가설

- 가설은 하나만 세운다.
- 함수, 엔드포인트, 파일, 주소, 필드 단위의 검증을 실행한다.
- 성공과 실패 샘플 또는 원본과 변형 샘플을 비교한다.

### 산출물 시작

설명보다 먼저 `solve.py`, `exploit.py`, raw request, patch, decryptor, extractor 중 하나를 만든다. 중간값과 실패 조건을 assertion으로 남긴다.

### 원본 검증 또는 분기

- 원본 artifact/service/checker로 후보를 검증한다.
- 실패하면 틀린 불변식 하나를 적고 다음으로 싼 가설로 바꾼다.
- 복잡한 문제는 성공 조건과 primitive/관계가 계속 좁혀지는 동안 충분히 깊게 판다. 경과 시간만으로 중단하거나 lane을 바꾸지 않는다.

## 분야별 초점

### Rev

문자열 → 비교/성공 분기 → 입력 변환 → 필요한 상수 순으로 역추적한다. 전체 함수나 VM 명령어를 모두 이해하지 않는다.

### Pwn

`file`, mitigations, loader/libc, 실제 I/O를 고정한 뒤 crash/leak/read/write/lifetime primitive를 증명한다. 이름 붙은 기법을 먼저 고르지 않는다.

### Web

루트/헤더, JS/API, 인증 전후, 정상/변형 요청을 비교한다. 승인 범위 밖 호스트를 스캔하지 않는다.

### Crypto

인코딩과 암호를 분리하고 작은 forward model을 만든다. 키/nonce 재사용, RNG, 모듈러 역연산, oracle을 증거 순으로 본다.

### Forensics

파일 인벤토리와 시간축부터 고정한다. 전체 덤프를 무작정 문자열 검색하지 말고 계정·세션·전송·삭제 흔적을 좁힌다.

### Misc

반복 규칙, 작은 brute-force 범위, 상태 전이, 스테고 채널을 찾고 즉시 자동화한다.

## 막힘 규칙

1. 현재 가설이 실패한 관찰을 한 줄로 남긴다.
2. 다음 가설은 최대 세 개만 만든다.
3. 가장 싼 구분 실험 하나를 실행한다.
4. 같은 입력·도구·추측을 근거 없이 반복하지 않는다.

반복된 깊은 분석이 새 앵커, 검증 가능한 관계, 후보 artifact를 만들지 못하면 정적↔동적, 원본↔추출 stage, 직접 분석↔oracle/patch/dump처럼 관찰 경계를 바꾼다. 새 증거가 쌓이는 경로는 시간 때문에 버리지 않는다.

## 완료 계약

- 문제 분류와 성공 조건
- 확정된 사실과 버린 가설
- 선택한 solve lane과 가장 싼 이유
- 재현 가능한 `input` / `script` / `exploit` / `patch` / `decrypt` / `recover`
- 원본 검증 결과 또는 정확한 blocker와 다음 단일 probe

검증 없는 자동화 결과, 패치로 보인 성공 화면, 설명만 있는 분석은 solve가 아니다.
