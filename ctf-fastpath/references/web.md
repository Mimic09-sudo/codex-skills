# Web Fast Reference

## 빠른 triage

1. 루트 응답과 헤더
2. 로그인/회원가입/업로드/다운로드 유무
3. JS와 숨은 API
4. 인증 전후 차이
5. 성공/실패 요청 비교

기록할 것:

- 상태 코드
- 주요 엔드포인트
- 쿠키 / 세션 특성
- 역할 차이
- 입력 지점

## 입력 지점 체크

- query
- form body
- JSON body
- multipart
- file name
- Host 헤더
- path parameter
- template parameter

## 우선순위

### 인증/권한

- IDOR
- role flag
- admin-only route 노출
- auth check race 또는 누락

### 파일 처리

- upload 후 실행 가능 여부
- download path traversal
- content-type 신뢰 여부

### 서버사이드 실행

- SSTI
- command injection
- deserialization
- SSRF

### 데이터 접근

- SQLi
- NoSQL injection
- GraphQL introspection / overfetch

## 요청 diff 규칙

항상 최소 두 개를 비교한다: 인증 전/후, 성공/실패, 일반/관리자, 정상/제어 입력.

비교 포인트는 상태 코드, body 필드, redirect, 쿠키 변화, 응답 시간이다.

## 증거 저장

- raw request와 response
- 성공/실패 payload
- 권한 변화 전후 응답

## 막히면

1. JS와 source map을 다시 확인한다.
2. 같은 기능의 다른 content-type 또는 HTTP method를 비교한다.
3. 숨은 파라미터와 인증된 라우트 목록을 확인한다.
