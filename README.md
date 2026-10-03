# 주간 식단 공개 실행 설정

현재 실행 본체는 `9373a103f0f26e7849e39c3ac1efbc228b3bf3db`, 공개 실행 코드는 `4d7f0940c8624d80928217aeffc45f6d2b90203b`다. 사용자 요청의 [디자인 비교 B 발송](https://github.com/jeon6192/naver-weekly-menu-runner/actions/runs/37142227656)은 2026-10-04 02:55 KST 성공했고 실제 수신·34개 메뉴·136개 영양값·원문 이미지 로드를 확인했다. 아래 이전 발송·예약 SHA는 실행 이력이다.

집 PC가 꺼져 있어도 비공개 식단 프로그램을 GitHub 표준 Ubuntu runner에서 실행한다. 이 디렉터리의 파일만 공개 저장소에 둔다. 본체 소스·과거 Git 이력·SQL·인증·메일·발송 DB는 공개하지 않는다.

[공개 실행 저장소](https://github.com/jeon6192/naver-weekly-menu-runner)의 기본 브랜치는 `codex/weekly-menu-runner`다. 실제 발송 본체 runtime은 `529b1efe5be0adfdb87cf00edd776aeaba63dabd`이며 공개 `23f86f4`는 이전 게시 이력이다. 현재 예약 실행 본체는 `843f74606827b97dbd538ee310148294af4fb2c8`, 공개 설정은 `8a21eac150974f182002a4e5614b0c4f4041fd57`로 게시했다. 실제 발송 디자인 SHA `529b1efe5be0adfdb87cf00edd776aeaba63dabd`와 구분한다. launcher 5개 파일·Secrets 5개·Variables 5개를 준비했다.

[실제 발송 37139886669](https://github.com/jeon6192/naver-weekly-menu-runner/actions/runs/37139886669)이 2026-10-04 02:16 KST `smtp_accepted`로 성공하고 본인 한 명의 받은메일 도착을 확인했다. CC/BCC는 없다. 무료 `gemini-3.5-flash-lite` 저장 분석을 재사용했고 원문 이미지 1개·요일/상시 표 4개·34행·기준량 34개·영양값 136개를 확인했다. PC 미리보기는 6열·390px 미리보기는 3+2이며 실제 NAVER WORKS 웹 받은메일에서는 style 제한으로 모바일 기본 구성이 표시된다. 물리 휴대폰 앱 검수는 아직 하지 않았다.

수신 확인 후 한국 시각 08:17·12:17·18:17 예약을 활성 설정했고 첫 cron 실행은 미관측이다. [중복 확인 실행 37140304338](https://github.com/jeon6192/naver-weekly-menu-runner/actions/runs/37140304338)이 `already_attempted`·`previous_status=smtp_accepted`로 성공했다. 메뉴 34개를 확인하고 신규 영양 분석·SMTP 진입 전에 중단했으며 추가 메일은 0건이다. 백업 복구는 미확인이다. 관련 기존 표시 테스트 13개·하위 검증 13개만 1회 확인했고 새 테스트 추가·전체 테스트 반복은 하지 않았다. 이전 CI 37137927627의 69개 통과·1개 생략은 이전 코드 이력이다. 프로젝트 식별자·주소·인증 값은 공개 문서에 넣지 않는다.

## 실행 범위

`validate.yml`은 수동으로 기존 테스트와 공개 샘플 재생성을 검증한다. `operate.yml`은 수동 실행과 하루 3회 예약을 정의한다. 기본 `send=false` 실행은 원문 수집·필요한 Gemini 분석·비공개 원격 기록·미리보기 생성까지 진행하며 메일을 발송하지 않는다. 따라서 기본 실행도 외부 요청과 원격 데이터 기록을 한다. 실행 허용과 실제 외부 실행 성공을 구분한다.

`send=true`와 `ENABLE_DELIVERY=true`가 함께 지정된 경우에만 발송 명령을 전달한다. 실제 발송은 취소할 수 없다. 발송 전에 영구 시도를 기록하며 같은 기간의 수정·실패·불확실 기록을 자동 재발송하지 않는다. SMTP 수락은 실제 수신·화면 검수의 완료가 아니다.

수동 실행의 `요청한 디자인 비교 B 1회`는 사용자에게 승인된 비교 목적에만 사용한다. `design_comparison=true`와 발송 체크가 함께 있어야 실제 비교 메일을 보낸다. 기존 `per-menu-v2` 기록을 변경하지 않고 고정 비교 목적 `compact-b-20261004`를 따로 기록하며 같은 목적을 재발송하지 않는다. 예약에서는 비교 옵션을 사용하지 않고 기존 A 디자인을 유지한다. 요청받은 긴 안내 두 문구는 A·B 모두 삭제했다.

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

`SOURCE_SHA`가 바뀌면 변경 범위의 점검과 미발송 처리를 확인한다. 전체 테스트는 필요한 변경에만 `validate.yml`로 수동 실행하고 `operate.yml`에서 반복하지 않는다. 본체 기본 브랜치에 병합할 필요는 없지만 원격에 해당 SHA가 있어야 checkout할 수 있다. 검증한 본체 SHA는 이미 작업 브랜치에 게시돼 있다. 워크플로와 wrapper는 모두 같은 `SOURCE_SHA`를 확인한다.

Supabase는 전용 프로젝트에 비공개 본체의 `weekly_menu/sql/` SQL을 적용해야 한다. 익명·일반 사용자에게 기록 테이블을 공개하지 않는다. 기록 준비 검사 실패, 네트워크 오류, 원자적 발송 기록 실패 시 SMTP를 시작하지 않는다. 서비스 키는 서버 작업 전용이며 높은 권한을 가지므로 다른 앱의 데이터를 함께 넣지 않는다.

## 준비와 확인 순서

1. 본체의 신규 코드·검증 결과를 확인한다. 실제 실행은 허용받았으며 운영자 계정의 GitHub 공개 표준 runner 사용 가능 여부와 Gemini 무료 프로젝트 여부를 확인한다.
2. 별도 공개 저장소에는 이 디렉터리의 파일만 게시했고 인증·설정 등록을 완료했다. 후속 게시 전에도 파일 목록·diff·비밀값 포함 여부를 확인한다. 기존 저장소의 공개 전환은 하지 않는다.
3. 변경 부분을 점검한다. 전체 테스트가 필요한 변경에만 Actions → 주간 식단 검증을 수동 실행한다. 운영 실행은 준비 검사를 통과한 고정 SHA를 사용한다.
4. 원격 SQL 적용과 실제 `send=false` 운영 성공을 확인했다. 디자인 적용과 실제 1회 수신까지 완료했으며 변경 후 필요한 확인은 Actions → 주간 식단 처리에서 진행한다. `prepared` 상태·메뉴 개수·영양값 개수를 확인한다. 발송 전에는 기존 시도 기록 대조도 완료해야 한다. 미리보기와 개인 산출물은 공개 artifact로 업로드하지 않는다. 받은메일 검수와 별도로 비공개 환경에서 확인한다.
5. 실제 v2 1회 발송과 웹 받은메일 확인을 완료했다. 물리 휴대폰 앱 검수는 별도로 남아 있다. 발송 기록을 삭제하거나 다른 라벨로 바꿔 재시도하지 않는다.
6. 실제 수신 확인 후 아래 예약을 활성 설정했다. 실제 중복 차단은 확인했고 첫 cron 실행은 별도로 확인한다.

## 예약과 결과 판단

한국 시각 08:17·12:17·18:17 하루 3회로 활성 설정했다. UTC cron은 `17 3,9,23 * * *`다. 첫 cron 실행은 아직 관측하지 않았고 정확한 실행 시각은 보장하지 않는다. 예약 이벤트는 발송 의도로 처리하지만 `ENABLE_DELIVERY=true`·기존 기록 대조 완료 조건과 원격 중복 차단을 함께 통과해야 한다.

| 결과 | 의미와 후속 행동 |
| --- | --- |
| `prepared` | 원문·분석·미리보기 준비 상태다. 발송과 실제 수신 완료로 계산하지 않는다 |
| `waiting_for_menu` | 검증된 현재·다음 주 원문이 아직 없어 다음 확인을 기다린다. 원문 접근·파싱 실패를 이 상태로 대체하지 않는다 |
| `smtp_accepted` | SMTP가 수락했다. 실제 받은메일·모바일 검수를 별도로 확인한다 |
| `already_attempted` | 같은 주의 기존 시도가 있어 재발송하지 않았다. `previous_status`와 `content_changed`를 확인한다 |
| `uncertain`, `failed_before_data`, `smtp_rejected` | 원격 시도 기록을 보존한다. 같은 주를 자동 재시도하지 않는다 |
| `failed` | 설정·기록·수집·분석·렌더 단계가 실패했다. 공개 오류 코드를 기준으로 비공개 환경에서 진단한다 |

발송 실패·불확실 기존 시도는 재확인 작업에서도 실패로 표시한다. 공개 로그에는 고정 상태·개수·참/거짓·단계 코드만 남긴다. 원시 프로그램 출력과 traceback은 wrapper가 숨긴다. 원문·EML·DB·인증·비공개 소스를 artifact에 게시하지 않는다. 발송용 인증은 의존성 준비가 끝난 처리 단계에만 전달한다. GitHub가 단계의 env 목록을 로그에 표시하므로 인증·프로젝트 주소·개인 이메일은 반드시 실제 Secrets 항목에 등록한다. Variables나 파일에서 전달한 민감값이 자동으로 가려질 거라고 가정하지 않는다.

## 중단과 복구

운영을 멈추려면 `ENABLE_DELIVERY=false`로 바꾸고 운영 workflow를 비활성화한다. 이미 SMTP에 제출한 메일은 되돌릴 수 없고, 중단된 발송의 영구 `attempted` 기록도 삭제하지 않는다. 원격 기록이 준비되지 않으면 발송을 중단하는 동작을 유지한다.

Supabase 무료 프로젝트는 1주 비활성 시 정지될 수 있고 자동 백업이 제공되지 않는다. 같은 키로 상태를 계속 확인하는 실행도 정지·삭제·인증 만료를 없앤다는 보장은 없다. 원격 기록을 비공개 위치에 정기 백업하고, 운영 전에 마지막 백업과 기존 모든 시도를 대조한다. 복원·확인 전에는 `WEEKLY_MENU_HISTORY_RECONCILED=false`와 `ENABLE_DELIVERY=false`를 유지한다. 운영 workflow 성공만으로 백업 완료를 판단하지 않는다.

## 근거와 검증 한계

공개 표준 runner 무료 정책은 [GitHub 요금 안내](https://docs.github.com/en/billing/concepts/product-billing/github-actions), 새 작업별 환경은 [hosted runner 안내](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners), 예약 지연·기본 브랜치·비활성 조건은 [예약 이벤트 안내](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)를 기준으로 한다. Actions와 본체 SHA 고정·최소권한·원시 로그 제한은 [보안 안내](https://docs.github.com/en/actions/reference/security/secure-use)를 따른다.

Gemini 무료 이용은 [공식 요금](https://ai.google.dev/gemini-api/docs/pricing)과 실제 프로젝트의 [무료 등급·한도](https://ai.google.dev/gemini-api/docs/rate-limits)가 함께 맞아야 한다. Supabase 무료 정지·백업 제한은 [요금](https://supabase.com/pricing), 서버 키 권한은 [API 키 안내](https://supabase.com/docs/guides/getting-started/api-keys)를 확인한다.

실제 GitHub 발송·받은메일 도착까지 확인했다. 첫 cron 실행·물리 휴대폰 앱·백업 복구는 아직 미확인이다. 선언한 확인 변수는 운영자의 확인 표시이며 provider의 실제 권한·요금·연결 성공을 자동 증명하지 않는다.
