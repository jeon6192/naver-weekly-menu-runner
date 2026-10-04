# 여러 AI에서 같은 프로젝트 규칙 사용

프로젝트 규칙은 루트 `AGENTS.md`가 정본이다. `agents-config`의 공통 정본과 AI별 얇은 진입 파일 구조를 따랐다. 프로젝트 규칙을 바꿀 때는 `AGENTS.md`를 수정하고 AI별 파일에 같은 내용을 복제하지 않는다.

## 지원 진입점

| AI 도구 | 저장소에서 연결하는 파일 |
| --- | --- |
| Codex | `AGENTS.md` 직접 읽기 |
| Claude Code | `CLAUDE.md`의 `@AGENTS.md` 가져오기 |
| Gemini CLI | `GEMINI.md`의 `@./AGENTS.md` 가져오기 |
| Kimi Code | `AGENTS.md` 직접 읽기 |
| Qwen Code | `QWEN.md`의 `@AGENTS.md` 가져오기, AGENTS 직접 읽기도 지원 |
| agy 대화형 | 프로젝트 `AGENTS.md`와 `GEMINI.md`를 읽는 경로 |
| agy 비대화형 `-p` | 규칙 본문을 프롬프트에 주입하는 래퍼 또는 명시적 주입 필요 |

파일 기반 지침을 지원하지 않는 다른 AI에는 프로젝트 `AGENTS.md`의 내용을 첫 지시로 전달한다. 저장소를 읽을 수 있는 AI에는 해당 파일을 먼저 읽게 한다. AI 이름만 바꿨다고 지침 적재가 자동 보장되는 것은 아니다.

## 시작과 확인

1. 해당 저장소 루트에서 AI를 시작한다. 프로그램 설치·계정 로그인은 해당 환경에 별도로 준비한다.
2. 새 세션에서 지침을 읽는다. 기존 세션은 다시 시작하거나 그 AI가 지원하는 지침 새로고침을 사용한다.
3. 첫 작업에서 읽은 지침 파일과 저장소 역할, 공개 범위·발송 기록 보존 규칙을 짧게 확인한다. 키·주소·기록 내용을 출력하지 않는다.

Codex는 현재 실행의 지침 파일을 확인하고, Claude는 `/context`, Gemini CLI·Qwen은 해당 도구의 `/memory`로 읽힌 내용을 확인할 수 있다. Kimi는 프로젝트 AGENTS의 주요 규칙을 요약하게 한다. 이 확인도 AI를 실제 실행하면 사용량이 발생할 수 있으므로 필요한 세션에서만 한다.

agy `-p`는 `agents-config`의 지침 주입 래퍼가 활성화돼 있으면 저장소 루트 `AGENTS.md`가 주입된다. 래퍼가 없거나 `AGY_NO_RULES=1`이면 자동 적재를 가정하지 않고 규칙 본문을 프롬프트에 직접 넣는다. 이 저장소는 전역 래퍼 설치·로그인·모델 설정을 변경하지 않는다.

## 확인 범위

파일 존재·상대 import 연결·공개 원본과 실행 저장소의 일치는 모델 호출 없이 확인할 수 있다. 각 AI의 실제 자동 발견과 적용은 그 도구의 버전·세션·설정에 따라 별도로 확인한다. 문서에서는 자동 적재를 실측했다고 표시하지 않는다.

참고 정본은 `agents-config`의 `common.md`, `stubs/`, `bin/agy-wrapper.ps1`이며 개인정보·공급자 전용 OMC 설정을 프로젝트에 복사하지 않는다. 지원 방식은 2026-10-04에 공식 문서와 정본 구현을 함께 확인했다.

[Codex 공식 지침](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Claude 메모리](https://code.claude.com/docs/en/memory) · [Gemini 컨텍스트](https://geminicli.com/docs/cli/gemini-md/) · [Kimi 시작](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html) · [Qwen 메모리](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/)
