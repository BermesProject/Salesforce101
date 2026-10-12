#!/usr/bin/env python3
"""아이웨어 상대 시각을 변환합니다. Salesforce 접속이나 DML은 수행하지 않습니다."""
import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

DAY2 = Path(__file__).resolve().parents[1]
OFFSETS = {
    'Received_Offset_Hours': 'Received_At__c',
    'Due_Offset_Hours': 'Response_Due_At__c',
    'First_Response_Offset_Hours': 'First_Response_At__c',
}


def prepare(anchor):
    base = datetime.fromisoformat(anchor.replace('Z', '+00:00'))
    if base.tzinfo is None or base.utcoffset() is None:
        raise ValueError('기준 시각에 +09:00 또는 Z처럼 시간대를 포함해 주세요.')
    records = []
    with (DAY2 / 'Eyewear/Data/consultation-templates.csv').open(encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            record = {k: (v if v != '' else None) for k, v in row.items() if k not in OFFSETS}
            if row['Needs_Manager__c'] not in ('true', 'false'):
                raise ValueError('매니저 도움 필요 값은 true 또는 false여야 합니다.')
            record['Needs_Manager__c'] = row['Needs_Manager__c'] == 'true'
            for source, target in OFFSETS.items():
                value = row[source]
                record[target] = None if value == '' else (
                    base + timedelta(hours=float(value))
                ).astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
            records.append(record)
    return {'anchor': base.isoformat(), 'object': 'Luxury_Client_Consultation__c',
            'lookupCodesResolved': False, 'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--anchor', required=True, help='실행 시각과 시간대를 입력해 주세요.')
    parser.add_argument('--output', required=True, type=Path, help='저장소 밖 새 JSON 파일 경로입니다.')
    args = parser.parse_args()
    destination = args.output.expanduser().resolve()
    repo = DAY2.parent
    if destination == repo or repo in destination.parents:
        parser.error('실행별 파일은 저장소 밖에 저장해 주세요.')
    try:
        payload = prepare(args.anchor)
        with destination.open('x', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write('\n')
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print('상담 10건의 시각을 준비했습니다. 직원 코드 연결과 org 등록은 아직 수행하지 않았습니다.')


if __name__ == '__main__':
    main()
