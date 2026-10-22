# Pwn Fast Reference

Use this only to classify the pwn lane, then switch to `pwn-general` for exploitation.

## 빠른 triage

1. `file`, mitigations, loader/libc와 아키텍처를 고정한다.
2. 한 번 실행해 실제 I/O 상태를 확인한다.
3. 입력 길이, 포맷, index, pointer, allocation/free 흐름을 추적한다.
4. 최소 crash, leak, read, write, UAF 중 하나를 재현한다.

## 우선순위

- No Canary: BOF와 saved return control 확인
- Canary: format/OOB/echo 등 leak 먼저
- PIE: base leak 또는 non-PIE direct target 먼저
- Full RELRO: GOT overwrite 집착 금지
- seccomp: 실제 허용 syscall을 확인한 뒤 ORW/SROP 판단
- heap: UAF/double free/overlap/size corruption 증거가 있을 때만 깊게 진입

## 지금 바로 볼 것

- `win`, `flag`, `system`, `puts`, `printf`, `read`, `gets`, `fgets`, `malloc`, `free`
- 메뉴형이면 create/edit/show/delete와 index 검증
- 입력 길이와 저장 위치, echo/leak 가능성
- 원격과 로컬의 loader/libc/transport 차이

## 최소 증거

- 정확한 crash/control offset 또는 lifetime state
- 반복 가능한 leak/read/write 하나
- 선택한 trigger와 보호기법 호환성
- 원본 target의 최종 exploit 로그

## 막히면

1. direct win/logic 경로를 다시 확인한다.
2. crash 대신 leak, leak 대신 partial overwrite/OOB를 구분한다.
3. heap이면 더 싼 stack/format/integer 경로가 없는지 확인한다.
