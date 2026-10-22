---
name: rev-ctf-fastpath
description: Solve simple, single-artifact reversing CTF challenges by tracing success or compare conditions, recovering the minimum transform, and producing a verified input, solver, decryptor, or patch. Use for ordinary ELF/PE/.NET/script and small VM or obfuscation tasks; use rev-final-fastpath for packed, staged, large-corpus, oracle, mobile, or complex hybrid work, and rev-game-hacking for game engines.
metadata:
  domain: ctf
  layer: rev
  subcategory: general-reversing
  language: ko
---

# Rev CTF Fastpath

## 목표

전체 프로그램이 아니라 성공 조건에 필요한 데이터 흐름만 복원한다. 승인된 CTF, 워게임, crackme에서 정확한 입력, 작은 solver/decryptor, 또는 설명 가능한 최소 patch를 원본으로 검증한다.

로컬 실행은 `ctf-wsl-toolchain`을 따른다.

## 초기 triage

1. 형식, 아키텍처, 보호기법, sidecar를 확인한다.
2. `flag|correct|wrong|success|win|key|usage` 문자열과 compare/output import를 찾는다.
3. 안전하면 한 번 실행해 입력 개수, 길이, 출력 패턴을 확인한다.
4. 성공/실패 문자열 xref 또는 `strcmp`/`memcmp`/직접 비교 호출자를 고른다.
5. 성공 조건을 한 문장으로 쓴다.

기존 `solve.py`, writeup, decompiler output, dump가 있으면 먼저 읽고 재작업하지 않는다.

## 증거 기반 solve cycle

### 앵커와 slice

- 성공 출력 또는 최종 비교에서 역방향으로 추적한다.
- 입력 길이, 변환 순서, 기대값, 분기만 남긴다.
- UI, 초기화, 로깅, 프레임워크 코드는 제외한다.

### 가장 싼 lane

- 직접 상수/비교: compare 순서대로 바이트 추출
- 가역 변환: 작은 `forward()`를 먼저 맞춘 뒤 역연산
- managed/script: 가장 높은 수준의 코드에서 검증 함수 복원
- 작은 VM: 검증 경로에서 실행되는 opcode만 모델링
- packed/anti-debug: compare/decrypt/unpack 경계에서 dump

### 산출물

`solve.py`, 입력 파일, extractor, debugger hook, 또는 최소 patch를 만든다. 하드코딩한 값에는 출처를 주석으로 남기고 중간값을 assertion으로 검증한다.

### 원본 확인

후보를 untouched binary/checker/service에 넣어 성공을 확인한다. patch만 성공하면 원래 입력이나 상태를 계속 복원한다.

## Pivot 규칙

- success/compare 앵커 없이 같은 정적 영역을 반복해서 읽고 있다면 입력→출력 경계 동적 추적으로 전환한다.
- 비교 대상이 숨겨졌으면 compare 직전 두 operand를 dump한다.
- 역연산이 불명확하면 한 round 또는 한 known sample의 forward model부터 맞춘다.
- packing/loader가 시끄러우면 post-decrypt/post-unpack stage를 dump하고 대상을 바꾼다.
- VM/난독화/다단계/대규모 corpus가 확인되면 `rev-final-fastpath`로 전환한다.
- Unity/Unreal/Godot 또는 게임 상태가 핵심이면 `rev-game-hacking`으로 전환한다.
- 경과 시간만으로 유효한 lane을 버리지 않는다. 새 중간값, 더 좁은 slice, 검증된 변환이 계속 생기면 깊게 진행한다.

## 유형별 기준

### Native ELF / PE

비교 호출자, 길이 check, `.rodata` 상수, index permutation을 우선한다. 필요할 때만 debugger로 compare 직전 레지스터/버퍼를 확인한다.

### .NET / Java

디컴파일러의 검증 함수와 문자열 복호화 루틴을 먼저 읽는다. UI/boilerplate를 제외한다.

### Python / JS / Lua

검증 로직을 직접 읽고 역함수나 작은 brute-force를 작성한다. import/anti-debug는 검증 경로에 영향을 줄 때만 우회한다.

### Small VM

dispatch loop, operand grammar, 최종 compare를 고정한다. 전체 ISA가 아니라 실제 검증 trace에 필요한 opcode만 구현한다.

### Packed / Obfuscated

정적 분석을 확장하기 전에 runtime dump, API hook, compare tracing 중 가장 좁은 관찰 경계를 고른다.

## 정확성 규칙

- width, signedness, overflow, endianness, permutation, RNG 소비 순서를 보존한다.
- brute force는 남은 미지수의 범위와 종료 조건을 먼저 계산한다.
- decompiler 표현을 그대로 믿지 말고 한 known intermediate로 forward model을 확인한다.
- 원본 artifact를 보존하고 patch/dump는 별도 파일로 만든다.
- 네트워크 endpoint는 사용자가 승인한 범위만 접속한다.

## 완료 계약

1. 성공 predicate와 핵심 slice
2. 확인된 변환/상수/상태 관계
3. 선택한 lane과 버린 가설
4. 재현 가능한 `input` / `script` / `decrypt` / `hook` / `patch`
5. 원본 검증 결과 또는 정확한 blocker와 다음 단일 probe

근거 없는 정답, 패치 화면만의 성공, 검증하지 않은 solver 출력은 완료가 아니다.
