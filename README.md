# 주간 식단 공개 실행 설정

집 PC가 꺼져 있어도 GitHub 표준 Ubuntu 서버가 비공개 본체를 가져와 주간 식단을 수집·정리·메일로 전달한다. 이 공개 저장소에는 실행 설정만 둔다. 본체·SQL·인증·메일·발송 기록은 공개하지 않는다.

## 현재 운영

- 본체는 비공개 `jeon6192/naver-blog-bot`의 `c1af6be55a387eb9b4e21aa23cf50a4d7ebfbc0f`를 사용한다.
- 실제 블로그 `cbob0803`의 주간 글만 처리하며 메뉴별 가상 1회분 영양을 Free Gemini로 추정한다.
- 기존 운영 수신자 4명의 주소는 `WEEKLY_MENU_RECIPIENTS` Secret에 보관한다. 공개 로그에는 개수만 표시한다.
- 매일 한국 시각 08:17·12:17·16:17에 확인하고, 같은 주 운영 메일은 1회만 보낸다.
- [마지막 본인 확인](https://github.com/jeon6192/naver-weekly-menu-runner/actions/runs/37177491392)은 2026-10-04 13:37 KST에 성공했다. 수신자 1명·메뉴 34개·영양값 136개이며 사용자가 실제 수신을 확인한다.
- [이전 예약 실행](https://github.com/jeon6192/naver-weekly-menu-runner/actions/runs/37171925891)은 성공했다. 새 4명 운영 예약의 첫 전달은 아직 미관측이다.

## 예약 근거

[공개 RSS](https://rss.blog.naver.com/cbob0803.xml)에서 일일 10개를 제외한 주간 4개를 실제 원문 표까지 확인했다. 게시 KST는 2026-09-14 월 10:53, 09-17 목 15:10, 09-22 화 15:09, 10-02 금 14:43이다. 요일은 불규칙하고 4개 중 3개가 오후여서 매일 오전·정오·오후에 확인한다. 확정된 게시 규칙으로 보지 않는다. UTC 예약은 `17 3,7,23 * * *`이며 GitHub 상황에 따라 지연될 수 있다.

## 필요한 설정

| 위치 | 이름 | 용도 |
| --- | --- | --- |
| Secrets | `SOURCE_READ_TOKEN` | 비공개 본체 하나의 Contents 읽기 전용 |
| Secrets | `GEMINI_API_KEY` | 확인된 무료 프로젝트 키 |
| Secrets | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | 비공개 발송 기록 서버 설정 |
| Secrets | `SMTP_PASSWORD` | NAVER WORKS 외부 앱 비밀번호 |
| Secrets | `WEEKLY_MENU_RECIPIENTS` | 기존 운영 수신자 목록, 쉼표로 구분 |
| Secrets | `SMTP_USER`, `SMTP_SENDER` | 필요할 때 로그인·발신 주소 지정 |
| Variables | `SOURCE_REPOSITORY`, `SOURCE_SHA` | 본체 저장소와 검토된 40자리 버전 |
| Variables | `GEMINI_FREE_TIER_CONFIRMED` | 해당 키의 무료 프로젝트 확인 후 `true` |
| Variables | `WEEKLY_MENU_HISTORY_RECONCILED` | 기존 발송 이력 보존·대조 후 `true` |
| Variables | `ENABLE_DELIVERY` | 운영 전달 활성화 `true`, 중단 `false` |

## 수동 실행과 결과

GitHub Actions → 주간 식단 처리 → Run workflow에서 기본 실행은 발송하지 않는다. 운영 발송 체크만 켜면 지정된 운영 목록에 전달한다. 디자인 확인 옵션을 함께 선택하면 본인 1명에게만 보낸다. 이번 마지막 확인 목적 `styled-a-release-20261004`는 이미 성공했으며 같은 목적을 다시 보내지 않는다. 디자인 옵션은 한 종류만 선택한다.

`prepared`는 준비만 완료, `smtp_accepted`는 SMTP 수락, `already_attempted`는 같은 주의 시도 기록으로 발송 차단, `waiting_for_menu`는 검증된 현주/차주 식단이 아직 없는 상태다. 실제 받은메일 도착은 수신자가 확인한다. `failed_before_data`, `smtp_rejected`, `uncertain`은 기록을 보존하고 자동 재시도하지 않는다. 일부 수신자 거절도 같은 운영 건을 자동 재발송하지 않는다.

## 중단·복구

`ENABLE_DELIVERY=false`와 workflow 비활성화로 중단한다. 이미 제출한 메일은 취소할 수 없다. 기존 기록을 삭제하거나 라벨·새 DB로 바꿔 재발송하지 않는다. Supabase 상태 표는 비공개로 백업하고 복구 시 전체 시도를 대조하기 전 발송을 켜지 않는다. 무료 프로젝트 휴면과 인증 만료도 기록을 초기화하는 방식으로 복구하지 않는다.

공개에는 이 디렉터리의 5개 파일만 복사한다. 프리뷰·EML·원문·SQL·기록 DB·비공개 소스·과거 Git 이력을 artifact나 로그에 올리지 않는다. 필요한 변경에만 수동 검증을 실행하며 운영마다 전체 테스트를 반복하지 않는다.

[GitHub 실행 서버](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) · [예약 이벤트](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) · [Gemini 무료 요금](https://ai.google.dev/gemini-api/docs/pricing)
