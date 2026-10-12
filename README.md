# Salesforce101

교육생께서 Claude Code와 함께 Salesforce Developer Edition에 실습 환경을 준비하실 수 있도록 만든 저장소입니다.

## 시작하기

1. 저장소를 clone해 주세요. (`git clone https://github.com/BermesProject/Salesforce101.git`)
2. 첫날 수업은 [Day1 안내](Day1/README.md), 이어지는 세 주제 실습은 [Day2 안내](Day2/README.md)를 확인해 주세요.
3. 해당 디렉터리에서 Claude Code를 시작하고 `CLAUDE.md`에 따라 읽기 전용 점검과 dry-run부터 진행해 주세요.
4. 실제 배포는 대상과 변경 범위를 확인하고 승인하신 후 진행합니다.

```sh
cd Day1
claude
```

Claude에 전달할 첫 요청:

```text
CLAUDE.md와 catalog.json을 먼저 읽고 Flow / Custom App / Object / Field 명세를 제 Salesforce Developer Edition에 설치해 주세요. 먼저 대상 org와 기존 구성요소를 읽기 전용으로 확인하고 dry-run까지만 진행해 주세요. 실제 배포 전에는 제 승인을 받아 주세요.
```

## 저장소 구조

- `Day1/` — 기본 오브젝트·관계, Ohana Consulting 앱, Flow 구조 관찰과 기본 데이터입니다.
- `Day2/Common/` — 세 주제에서 함께 사용하는 Employee 오브젝트와 직원 6명입니다.
- `Day2/Game/` — 게임 마케팅 실적과 화면 Flow 입력 예제입니다.
- `Day2/Eyewear/` — 아이웨어 상담, 첫 응답 기한, 직원 간 이관 데이터입니다.
- `Day2/AI-Sales/` — AI 도입 평가, Prompt Builder·Agentforce 실습 데이터입니다.

Day 2에서는 Day 1 환경과 데이터를 보존하며 Cleanup을 실행하지 않습니다. [주제별 준비 데이터 목록](Day2/DATA_PLAN.md)을 먼저 확인해 주세요.

이 저장소는 Salesforce DX 프로젝트가 아닙니다. Claude가 저장소 외부의 임시 작업공간에서 설치 payload를 구성합니다.

## 사용 권리

이 저장소에는 오픈소스 라이선스가 없습니다. 저장소 열람 권한은 복제·수정·재배포·상업적 이용 권한을 자동으로 부여하지 않습니다. 수업 외 사용은 저장소 소유자에게 확인해 주세요.
