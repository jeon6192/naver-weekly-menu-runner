"""비공개 실행 출력은 숨기고 고정된 결과 필드만 공개한다."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

STATUSES = {'prepared', 'already_attempted', 'smtp_accepted', 'smtp_rejected',
            'uncertain', 'failed_before_data', 'failed', 'waiting_for_menu'}
ERROR_CODES = {'CONFIG', 'STATE', 'COLLECTION', 'NUTRITION', 'RENDER', 'RUNTIME',
               'DEPENDENCIES', 'SUMMARY'}
PREVIOUS_STATUSES = {'attempted', 'smtp_accepted', 'smtp_rejected', 'uncertain',
                     'failed_before_data'}
NUTRITION_ERRORS = {'NETWORK', 'INCOMPLETE', 'JSON', 'REPEATED_MENU', 'MENU_COVERAGE',
                    'MENU_ORDER', 'ENERGY', 'VALIDATION', 'HTTP_400', 'HTTP_401',
                    'HTTP_403', 'HTTP_404', 'HTTP_429', 'HTTP_500', 'HTTP_503', 'HTTP_OTHER',
                    'RESPONSE_SIZE', 'MENU_NAME', 'DAYS', 'NUMBER', 'NOTE', 'CACHE', 'KEY_MISSING'}


def main():
    parser = argparse.ArgumentParser(description='공개 로그에는 상태와 개수만 남긴다.')
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--send', action='store_true')
    parser.add_argument('--design-comparison', action='store_true')
    parser.add_argument('--design-final', action='store_true')
    parser.add_argument('--design-mobile', action='store_true')
    args = parser.parse_args()
    source = args.source.resolve()
    expected = os.environ.get('SOURCE_SHA', '')
    if re.fullmatch(r'[a-fA-F0-9]{40}', expected) is None:
        raise ValueError('SOURCE_VERSION')
    environment = os.environ.copy()
    # 읽기 토큰은 본체 다운로드에만 필요하다.
    for name in ('SOURCE_READ_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN', 'WEEKLY_MENU_LIVE_TEST'):
        environment.pop(name, None)
    environment['PYTHONUTF8'] = '1'
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=source,
                          env=environment, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=30)
    if head.returncode or head.stdout.strip().lower() != expected.lower():
        raise ValueError('SOURCE_VERSION')
    output = source / 'artifacts' / 'cloud-run'
    summary_path = output / 'public-summary.json'
    output.mkdir(parents=True, exist_ok=True)
    # 같은 작업 내 재실행에서 이전 결과를 현재 성공으로 오인하지 않는다.
    if summary_path.exists():
        summary_path.unlink()
    command = [sys.executable, '-m', 'weekly_menu.cloud', '--output', str(output),
               '--summary', str(summary_path)]
    if args.send:
        command.append('--send')
    if args.design_comparison:
        command.append('--design-comparison')
    if args.design_final:
        command.append('--design-final')
    if args.design_mobile:
        command.append('--design-mobile')
    result = subprocess.run(command, cwd=source, env=environment,
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace', timeout=600)
    if not summary_path.is_file() or summary_path.stat().st_size > 8192:
        raise ValueError('SUMMARY_MISSING')
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    if (not isinstance(summary, dict) or not isinstance(summary.get('status'), str)
            or summary['status'] not in STATUSES):
        raise ValueError('SUMMARY_INVALID')
    public = {'status': summary['status']}
    for name in ('menu_count', 'nutrient_count'):
        if name in summary:
            if type(summary[name]) is not int or not 0 <= summary[name] <= 2000:
                raise ValueError('SUMMARY_INVALID')
            public[name] = summary[name]
    for name in ('analysis_reused', 'sending_enabled', 'content_changed'):
        if name in summary:
            if type(summary[name]) is not bool:
                raise ValueError('SUMMARY_INVALID')
            public[name] = summary[name]
    if 'error_code' in summary:
        if not isinstance(summary['error_code'], str) or summary['error_code'] not in ERROR_CODES:
            raise ValueError('SUMMARY_INVALID')
        public['error_code'] = summary['error_code']
    if 'previous_status' in summary:
        if (not isinstance(summary['previous_status'], str)
                or summary['previous_status'] not in PREVIOUS_STATUSES):
            raise ValueError('SUMMARY_INVALID')
        public['previous_status'] = summary['previous_status']
    if 'nutrition_error' in summary:
        if (not isinstance(summary['nutrition_error'], str)
                or summary['nutrition_error'] not in NUTRITION_ERRORS):
            raise ValueError('SUMMARY_INVALID')
        public['nutrition_error'] = summary['nutrition_error']
    print(json.dumps(public, ensure_ascii=False, sort_keys=True))
    failed = summary['status'] in {'failed', 'smtp_rejected', 'uncertain', 'failed_before_data'}
    if summary['status'] == 'already_attempted':
        failed = summary.get('previous_status') != 'smtp_accepted'
    return 1 if result.returncode or failed else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired):
        # 원시 예외·경로·외부 응답·비공개 프로그램 출력을 공개하지 않는다.
        print('{"status":"failed","error_code":"LAUNCHER"}')
        raise SystemExit(1) from None
