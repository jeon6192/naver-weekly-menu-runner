"""기존 테스트와 공개 샘플을 검증하고 공개 로그에는 집계만 남긴다."""

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

def run_stage(label, command, source, timeout, environment):
    try:
        result = subprocess.run(command, cwd=source, env=environment,
                                capture_output=True, text=True, encoding='utf-8',
                                errors='replace', timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError(f'{label}: 실행 또는 제한 시간 확인에 실패했다.') from None
    if result.returncode:
        raise ValueError(f'{label}: 실패했다. 비공개 본체의 원시 출력은 공개하지 않는다.')
    print(f'{label}: 통과했다.')
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description='AI·SMTP 호출 없는 클라우드 검증')
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    expected = os.environ.get('SOURCE_SHA', '')
    if re.fullmatch(r'[a-fA-F0-9]{40}', expected) is None:
        raise ValueError('본체의 검증된 40자리 SHA를 준비해야 한다.')
    environment = os.environ.copy()
    # 라이브 테스트와 인증 설정을 검증 자식 프로세스에 전달하지 않는다.
    for name in ['WEEKLY_MENU_LIVE_TEST', 'GEMINI_API_KEY', 'EMAIL_PASSWORD',
                 'SMTP_PASSWORD', 'SOURCE_READ_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN',
                 'SUPABASE_URL', 'SUPABASE_SERVICE_ROLE_KEY', 'SMTP_USER',
                 'SMTP_SENDER']:
        environment.pop(name, None)
    environment['PYTEST_ADDOPTS'] = ''
    environment['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    environment['PYTHONUTF8'] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    head = run_stage('본체 버전 확인', ['git', 'rev-parse', 'HEAD'], source, 30, environment)
    if head.strip().lower() != expected.lower():
        raise ValueError('검토한 본체 버전과 다르다. 검증을 중단한다.')
    output = run_stage('기존 테스트', [sys.executable, '-m', 'pytest', '-q', '--tb=no', 'tests'],
                       source, 600, environment)
    passed = re.search(r'\b(\d+) passed\b', output)
    skipped = re.search(r'\b(\d+) skipped\b', output)
    if not passed:
        raise ValueError('테스트 통과 개수를 확인하지 못했다.')
    print(f'테스트 집계: {passed.group(1)}개 통과, {skipped.group(1) if skipped else 0}개 생략.')
    run_stage('공개 샘플 재생성', [sys.executable, 'tools/replay_public_example.py',
                                  '--output', 'artifacts/cloud-fixture'], source, 180, environment)
    fixture = source / 'artifacts' / 'cloud-fixture'
    menu = json.loads((fixture / 'menu.json').read_text(encoding='utf-8'))
    nutrition = json.loads((fixture / 'nutrition.json').read_text(encoding='utf-8'))
    if len(menu['days']) != len(nutrition['days']):
        raise ValueError('샘플 날짜 개수가 다르다.')
    foods = []
    for day, estimate in zip(menu['days'], nutrition['days'], strict=True):
        if (day['date'] != estimate['date'] or day['weekday'] != estimate['weekday']
                or day['menus'] != [food['menu_name'] for food in estimate['items']]):
            raise ValueError('샘플의 날짜·메뉴·순서가 원문과 다르다.')
        foods.extend(estimate['items'])
    if menu['always_available'] != [food['menu_name'] for food in nutrition['always_available']]:
        raise ValueError('상시 제공 메뉴가 원문과 다르다.')
    foods.extend(nutrition['always_available'])
    nutrients = ('kcal', 'carbs_g', 'protein_g', 'fat_g')
    if len(foods) != 34 or any(isinstance(food[key], bool)
                             or not isinstance(food[key], (int, float))
                             or not math.isfinite(food[key]) or food[key] < 0
                             for food in foods for key in nutrients):
        raise ValueError('공개 샘플의 메뉴 개수 또는 영양값이 다르다.')
    if not (fixture / 'source-menu.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('재생성한 원문 캡처 PNG를 확인하지 못했다.')
    print('샘플 집계: 메뉴 34개, 영양값 136개, 원문 캡처 PNG 생성 확인.')
    print('검증을 완료했다. AI 요청·SMTP 인증·메일 발송은 실행하지 않았다.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError):
        print('검증에 실패했다. 비공개 데이터와 원시 오류는 공개 로그에 출력하지 않는다.')
        raise SystemExit(1) from None
