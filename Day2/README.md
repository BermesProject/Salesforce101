# Day 2 실습 준비

2026년 10월 13일 수업용 **게임·아이웨어·AI 영업** 설치 명세와 가상 데이터입니다. Day 1에서 사용하신 Developer Edition을 그대로 사용하시면 됩니다. 항공 주제는 이번 설치에서 제외했습니다.

## 준비 데이터

| 구분 | 준비할 데이터 | 제공 수량 | 확인하실 내용 |
|---|---|---:|---|
| 공통 | `Employee__c` 직원 명부 | 6명 | 최산, 앤디, 미란다, 페퍼, 토니, 브루스의 담당자 관계 |
| 게임 | 표준 Campaign | 2건 | 신규 감독 모집, 복귀 감독 초대 |
| 게임 | `Game_Marketing_Performance__c` | 120건 | 날짜·캠페인·채널별 실적과 목표 달성률 |
| 게임 | 화면 입력 예제 | 2건 | 기존 1건 수정, 신규 1건 생성 |
| 아이웨어 | `Luxury_Client_Consultation__c` | 10건 | 정상 응대, 매니저 도움 요청, 첫 응답 지연 |
| AI 영업 | `B2B_AI_Project__c` | 4건 | 정상, 보안 검토 중, 성공 기준 누락, 담당자 누락 |

자세한 필드·관계·예상 결과는 [데이터 준비 목록](DATA_PLAN.md)을 확인해 주세요. 모든 레코드는 교육용으로 만든 가상 데이터이며 실제 기업의 고객 정보나 성능 측정값이 아닙니다. 기업 레퍼런스는 넥슨 FC 시리즈, 아이아이컴바인드의 젠틀몬스터, 퓨리오사AI입니다.

## 시작하기

저장소 루트에서 다음 명령으로 Claude Code를 실행해 주세요.

```sh
cd Day2
claude
```

먼저 공통 직원 명부를 준비하실 때 아래 문장을 전달해 주세요.

```text
CLAUDE.md, catalog.json, DATA_PLAN.md와 Common/README.md를 읽어 주세요.
Day 1에서 사용한 제 Developer Edition을 확인한 뒤 공통 Employee 오브젝트,
탭, 권한과 직원 6명을 준비해 주세요. 기존 Day 1 데이터와 다른 주제는 보존해 주세요.
대상 org와 변경 목록, dry-run 결과를 먼저 보여 주세요.
확인한 범위에 대해 제가 설치를 승인하면 배포·권한 할당·데이터 등록과 검증을 진행해 주세요.
```

공통 준비를 마치신 뒤 필요한 주제만 요청하시면 됩니다.

```text
Game/README.md와 schema.json을 읽고 게임 실습 환경을 준비해 주세요.
제가 직접 만드는 오브젝트·필드는 먼저 존재 여부를 확인해 주세요.
Campaign과 실적 10건을 먼저 확인하고, 검토 후 나머지 110건을 추가해 주세요.
기존 10건은 다시 만들거나 덮어쓰지 말아 주세요. Flow는 아직 활성화하지 말아 주세요.
```

아이웨어는 `Eyewear/README.md`, AI 영업은 `AI-Sales/README.md`를 지정해 주세요. AI 영업은 교육생께서 Prompt Builder와 Agentforce를 직접 실습하시는 구성입니다.

## Day 1과 달라진 점

- **Cleanup을 실행하지 않습니다.** Day 1의 Account·Contact·Opportunity·Inquiry 및 다른 주제의 구성과 레코드를 유지합니다.
- 실제 로그인은 본인의 Salesforce User로 하시고, 업무 담당자는 공통 직원 Lookup으로 연결합니다.
- 이 저장소는 Salesforce DX 프로젝트가 아닙니다. Claude가 명세를 읽고 저장소 밖 임시 작업공간에 배포 파일을 구성합니다.
- 공통 Employee는 XML을 제공하며, 주제별 오브젝트·필드는 `schema.json`이 정본입니다. 앱·권한·화면 구성은 각 README를 함께 확인해 주세요.
- 데이터부터 등록하고 Flow·Prompt Template·Agent Action은 수업에서 만듭니다. 완성된 자동화나 AI 결과를 미리 넣지 않습니다.
- 재실행 시 기존 실습 결과를 보존합니다. 데이터 초기화나 기존 값 덮어쓰기는 별도 요청이 있을 때만 진행합니다.

## 로컬 검증

다음 명령은 Salesforce에 접속하거나 데이터를 변경하지 않습니다.

```sh
python3 -m unittest discover -s Day2/tests -v
```

위 명령은 저장소 루트에서 실행해 주세요. 실제 배포 가능 여부는 대상 org의 metadata dry-run과 배포 후 조회로 확인합니다.
