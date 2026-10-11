# Salesforce101

Claude와 함께 Salesforce Developer Edition에 DAY 1 실습 metadata를 설치하기 위한 교육 저장소입니다.

## 시작하기

1. 저장소를 clone합니다.
2. `Day1/` 디렉터리에서 Claude Code를 시작합니다.
3. `Day1/CLAUDE.md`의 안전 규칙에 따라 읽기 전용 점검과 dry-run부터 진행합니다.
4. 실제 배포는 사용자 승인 후에만 진행합니다.

```sh
cd Day1
claude
```

Claude에 전달할 첫 요청:

```text
CLAUDE.md와 catalog.json을 먼저 읽고 Flow / Custom App / Object / Field 명세를 내 Salesforce Developer Edition에 설치해 줘. 먼저 대상 org와 기존 구성요소를 읽기 전용으로 확인하고 dry-run까지만 진행해. 실제 배포 전에는 내 승인을 받아.
```

## 저장소 구조

- `Day1/Object/`
- `Day1/Field/`
- `Day1/Custom App/`
- `Day1/Flow/`

이 저장소는 Salesforce DX 프로젝트가 아닙니다. Claude가 저장소 외부의 임시 작업공간에서 설치 payload를 구성합니다.

## 사용 권리

이 저장소에는 오픈소스 라이선스가 없습니다. 저장소 열람 권한은 복제·수정·재배포·상업적 이용 권한을 자동으로 부여하지 않습니다. 수업 외 사용은 저장소 소유자에게 확인하세요.
