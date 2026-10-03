# 주간 식단 공개 실행 설정

집 PC가 꺼져 있어도 비공개 식단 프로그램을 GitHub의 표준 Ubuntu runner에서 실행하는 설정이다. 이 디렉터리의 파일만 별도 공개 저장소의 루트에 복사한다. 본체 소스·과거 Git 이력·SQL·인증·메일·발송 DB는 공개 저장소에 복사하지 않는다.

2026-10-04에 실제 준비·게시·발송·예약 실행을 허용받았고 [공개 실행 저장소](https://github.com/jeon6192/naver-weekly-menu-runner)에 launcher 5개 파일만 독립 이력으로 게시했다. 최초 공개 SHA는 `77a9204909b2d3af94dde7888534181123615f91`, 확인한 기본 브랜치는 `codex/weekly-menu-runner`다. 본체 작업 브랜치의 검증 SHA는 `cbecab4c2279ea28c744db6e946938fab39d8ce4`이며 커밋·push와 해당 SHA의 로컬 launcher 검증을 완료했다. Variables 5개와 URL Secret 등록을 완료했으며 나머지 인증 연결·dispatch·예약·실제 발송은 아직 남아 있다. Windows 로컬 의존성·Chromium 설치, 기존 테스트 65개 통과·5개 생략·하위 검증 63개 통과, YAML 2개 파싱, 공개 샘플 34개 메뉴·136개 영양값·원문 캡처 재생성을 확인했다. 이 결과는 GitHub의 실제 실행 성공을 의미하지 않는다.

신규 통합 14개·HTTP 경계 82개는 오프라인으로 통과했다. Supabase Free·Seoul·Healthy 프로젝트의 SQL 적용 후 카탈로그 표 3개·RLS 3개·보호 트리거 2개, 익명·일반 사용자 표/함수 권한 0개, 서비스 역할 최소 표 권한 3개와 전체 계약 일치를 확인했다. 합성 행을 이용한 9개 검증으로 순차 고유 시도·최종 상태·분석 불변·금지 수정/삭제·최초 관측 시각 보존을 확인하고 명시적으로 ROLLBACK했다. 실제 운영 행은 조회·변경하지 않았다. 동시 세션과 REST 인증은 미검증이다.

공개 저장소 Variables 5개와 `SUPABASE_URL` Secret을 등록했다. `ENABLE_DELIVERY`·`WEEKLY_MENU_HISTORY_RECONCILED`·`GEMINI_FREE_TIER_CONFIRMED`는 모두 `false`다. 나머지 `SOURCE_READ_TOKEN`·`SUPABASE_SERVICE_ROLE_KEY`·`GEMINI_API_KEY`·`SMTP_PASSWORD` 설정은 브라우저의 새 접근 권한·인증 규칙에 따라 사용자 직접 처리 요청 중이다. 해당 Gemini 프로젝트가 Free이며 v2 인계 이후 추가 시도가 없다는 확인도 요청했다. 실제 모델 API·SMTP·클라우드 CI는 0건이고 예약은 꺼져 있다. 프로젝트 ID·URL·인증 값은 공개 문서에 넣지 않는다.

## 실행 범위

`validate.yml`은 수동으로 기존 테스트와 공개 샘플 재생성을 검증한다. `operate.yml`도 수동 실행만 정의한다. 기본 `send=false` 실행은 원문 수집·필요한 Gemini 분석·비공개 원격 기록·미리보기 생성까지 진행하며 메일을 발송하지 않는다. 따라서 기본 실행도 외부 요청과 원격 데이터 기록을 한다. 실행 허용과 실제 외부 실행 성공을 구분한다.

`send=true`와 `ENABLE_DELIVERY=true`가 함께 지정된 경우에만 발송 명령을 전달한다. 실제 발송은 취소할 수 없다. 발송 전에 영구 시도를 기록하며 같은 기간의 수정·실패·불확실 기록을 자동 재발송하지 않는다. SMTP 수락은 실제 수신·화면 검수의 완료가 아니다.

## 준비할 설정

실행 저장소의 Settings → Secrets and variables → Actions에서 아래 이름을 준비한다. 값은 채팅·README·공개 로그에 넣지 않는다. Secrets와 Variables의 화면 값을 포함한 스크린샷도 공유하지 않는다.

| 위치 | 이름 | 조건 |
| --- | --- | --- |
| Variables | `SOURCE_REPOSITORY` | 현재 비공개 본체 `jeon6192/naver-blog-bot`만 허용한다 |
| Variables | `SOURCE_SHA` | 신규 구현과 검증이 포함돼 원격 본체에 존재하는 검토된 40자리 commit SHA다. 로컬 미커밋 변경이나 기존 인계 SHA를 새 구현으로 표시하지 않는다 |
| Secrets | `SOURCE_READ_TOKEN` | 본체 저장소 하나의 Contents 읽기 권한만 가진 별도 인증이다. checkout 후 Git 인증에 보관하지 않는다 |
| Secrets | `GEMINI_API_KEY` | 무료 프로젝트의 키다. 무료 요금표가 있다는 것만으로 이 키의 프로젝트가 무료라고 판단하지 않는다 |
| Secrets | `SUPABASE_URL` | 전용 비공개 기록 프로젝트 주소다 |
| Secrets | `SUPABASE_SERVICE_ROLE_KEY` | 기록 프로젝트의 서버 전용 키다. 공개·브라우저에 노출하지 않는다 |
| Secrets | `SMTP_PASSWORD` | 실제 발송이 승인된 경우에만 준비하는 외부 앱 인증이다 |
| Secrets | `SMTP_USER`, `SMTP_SENDER` | 로그인과 발신 주소다. Variables에 두면 단계의 env 로그에 공개될 수 있어 Secrets로 등록한다 |
| Variables | `GEMINI_FREE_TIER_CONFIRMED` | 해당 키의 프로젝트가 무료 등급임을 직접 확인한 뒤 `true`로 설정한다 |
| Variables | `WEEKLY_MENU_HISTORY_RECONCILED` | 기존 PC별 시도 기록과 원격 상태를 대조·보존한 뒤 `true`로 설정한다. 새 DB가 비어 있다는 이유로 완료 처리하지 않는다 |
| Variables | `ENABLE_DELIVERY` | 기본은 미설정 또는 `false`다. 미발송 검증·기존 시도 대조·인증 준비 후 첫 1회 발송 전에 `true`로 설정한다. 실제 수신 검수 후 예약을 활성화한다 |

`SOURCE_SHA`가 바뀌면 검증부터 다시 수행한다. 본체 기본 브랜치에 병합할 필요는 없지만 원격에 해당 SHA가 있어야 checkout할 수 있다. 검증한 본체 SHA는 이미 작업 브랜치에 게시돼 있다. 워크플로와 wrapper는 모두 같은 `SOURCE_SHA`를 확인한다.

Supabase는 전용 프로젝트에 비공개 본체의 `weekly_menu/sql/` SQL을 적용해야 한다. 익명·일반 사용자에게 기록 테이블을 공개하지 않는다. 기록 준비 검사 실패, 네트워크 오류, 원자적 발송 기록 실패 시 SMTP를 시작하지 않는다. 서비스 키는 서버 작업 전용이며 높은 권한을 가지므로 다른 앱의 데이터를 함께 넣지 않는다.

## 준비와 확인 순서

1. 본체의 신규 코드·검증 결과를 확인한다. 실제 실행은 허용받았으며 운영자 계정의 GitHub 공개 표준 runner 사용 가능 여부와 Gemini 무료 프로젝트 여부를 확인한다.
2. 별도 공개 저장소에는 이 디렉터리의 파일만 게시했고 남은 인증·설정을 등록한다. 후속 게시 전에도 파일 목록·diff·비밀값 포함 여부를 확인한다. 기존 저장소의 공개 전환은 하지 않는다.
3. Actions → 주간 식단 검증 → Run workflow로 고정 SHA의 기존 테스트와 공개 샘플을 확인한다. 단계 실패 시 다음으로 넘어가지 않는다. 테스트 통과 개수와 34개 메뉴·136개 영양값·원문 PNG가 로그에 표시돼야 한다.
4. 원격 기록 SQL을 적용하고, Actions → 주간 식단 처리에서 `send=false`로 실행한다. `prepared` 상태·메뉴 개수·영양값 개수를 확인한다. 발송 전에는 기존 시도 기록 대조도 완료해야 한다. 미리보기와 개인 산출물은 공개 artifact로 업로드하지 않는다. 받은메일 검수와 별도로 비공개 환경에서 확인한다.
5. 실제 발송 승인 이후에만 `ENABLE_DELIVERY=true`와 `send=true`로 한 번 실행한다. SMTP 수락 뒤 본인의 받은메일과 모바일 화면에서 전체 메뉴·영양·원문 캡처를 확인한다. 발송 기록을 삭제하거나 다른 라벨로 바꿔 재시도하지 않는다.
6. 검증된 운영 코드와 실제 수신 검수가 완료된 뒤 예약을 활성화한다. 아래 예약 예시는 권고이며 파일에는 아직 등록하지 않았다.

## 예약과 결과 판단

권고 확인 주기는 한국 시각 08:17·12:17·18:17 하루 3회다. UTC cron 예시는 `17 3,9,23 * * *`다. 정확한 시각에 실행된다는 보장은 없다. 실제 운영 승인·수신 검수가 끝나면 `operate.yml`의 `on` 아래 주석 처리한 `schedule` 두 줄을 활성화한다. 예약 이벤트는 발송 의도로 처리하지만 `ENABLE_DELIVERY=true`·기존 기록 대조 완료 조건을 함께 통과해야 한다. 지금은 주석 상태라 예약이 등록되지 않는다.

| 결과 | 의미와 후속 행동 |
| --- | --- |
| `prepared` | 원문·분석·미리보기 준비 상태다. 발송과 실제 수신 완료로 계산하지 않는다 |
| `waiting_for_menu` | 검증된 현재·다음 주 원문이 아직 없어 다음 확인을 기다린다. 원문 접근·파싱 실패를 이 상태로 대체하지 않는다 |
| `smtp_accepted` | SMTP가 수락했다. 실제 받은메일·모바일 검수를 별도로 확인한다 |
| `already_attempted` | 같은 주의 기존 시도가 있어 재발송하지 않았다. `previous_status`와 `content_changed`를 확인한다 |
| `uncertain`, `failed_before_data`, `smtp_rejected` | 원격 시도 기록을 보존한다. 같은 주를 자동 재시도하지 않는다 |
| `failed` | 설정·기록·수집·분석·렌더 단계가 실패했다. 공개 오류 코드를 기준으로 비공개 환경에서 진단한다 |

발송 실패·불확실 기존 시도는 재확인 작업에서도 실패로 표시한다. 공개 로그에는 고정 상태·개수·참/거짓·단계 코드만 남긴다. 원시 프로그램 출력과 traceback은 wrapper가 숨긴다. 원문·EML·DB·인증·비공개 소스를 artifact에 게시하지 않는다. 발송용 인증은 의존성 설치와 테스트가 끝난 처리 단계에만 전달한다. GitHub가 단계의 env 목록을 로그에 표시하므로 인증·프로젝트 주소·개인 이메일은 반드시 실제 Secrets 항목에 등록한다. Variables나 파일에서 전달한 민감값이 자동으로 가려질 거라고 가정하지 않는다.

## 중단과 복구

운영을 멈추려면 `ENABLE_DELIVERY=false`로 바꾸고 운영 workflow를 비활성화한다. 이미 SMTP에 제출한 메일은 되돌릴 수 없고, 중단된 발송의 영구 `attempted` 기록도 삭제하지 않는다. 원격 기록이 준비되지 않으면 발송을 중단하는 동작을 유지한다.

Supabase 무료 프로젝트는 1주 비활성 시 정지될 수 있고 자동 백업이 제공되지 않는다. 같은 키로 상태를 계속 확인하는 실행도 정지·삭제·인증 만료를 없앤다는 보장은 없다. 원격 기록을 비공개 위치에 정기 백업하고, 운영 전에 마지막 백업과 기존 모든 시도를 대조한다. 복원·확인 전에는 `WEEKLY_MENU_HISTORY_RECONCILED=false`와 `ENABLE_DELIVERY=false`를 유지한다. 운영 workflow 성공만으로 백업 완료를 판단하지 않는다.

## 근거와 검증 한계

공개 표준 runner 무료 정책은 [GitHub 요금 안내](https://docs.github.com/en/billing/concepts/product-billing/github-actions), 새 작업별 환경은 [hosted runner 안내](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners), 예약 지연·기본 브랜치·비활성 조건은 [예약 이벤트 안내](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)를 기준으로 한다. Actions와 본체 SHA 고정·최소권한·원시 로그 제한은 [보안 안내](https://docs.github.com/en/actions/reference/security/secure-use)를 따른다.

Gemini 무료 이용은 [공식 요금](https://ai.google.dev/gemini-api/docs/pricing#gemini-2.5-flash)과 실제 프로젝트의 [무료 등급·한도](https://ai.google.dev/gemini-api/docs/rate-limits)가 함께 맞아야 한다. Supabase 무료 정지·백업 제한은 [요금](https://supabase.com/pricing), 서버 키 권한은 [API 키 안내](https://supabase.com/docs/guides/getting-started/api-keys)를 확인한다.

현재 GitHub 실제 실행·클라우드 SMTP 연결·실제 v2 수신·예약·백업 복구는 미검증이다. 선언한 확인 변수는 운영자의 확인 표시이며 provider의 실제 권한·요금·연결 성공을 자동 증명하지 않는다.
