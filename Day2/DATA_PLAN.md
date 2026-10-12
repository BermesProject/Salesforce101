# 데이터 준비 목록과 연결 규칙

## 1. 공통 직원 6명

| 직원 코드 | 이름 | 주제 | 역할 | 상위 직원 |
|---|---|---|---|---|
| EMP-GAME-001 | 최산 | 게임 | 마케팅 담당 | 공란 |
| EMP-LUX-001 | 앤디 | 럭셔리 | 상담 직원 | EMP-LUX-002 |
| EMP-LUX-002 | 미란다 | 럭셔리 | 상위 매니저 | 공란 |
| EMP-AI-001 | 페퍼 | AI 제조업 | 영업 담당 | 공란 |
| EMP-AI-002 | 토니 | AI 제조업 | 기술 담당 | 공란 |
| EMP-AI-003 | 브루스 | AI 제조업 | 프로젝트 코디네이터 | 공란 |

직원 코드 `Employee_Number__c`는 Unique External ID입니다. 우영과 나이젤은 고객 역할이므로 직원 명부에는 넣지 않습니다. `Industry__c`의 아이웨어 저장값은 장표 계약과 맞춘 `럭셔리`입니다. User 생성, 이메일 주소, 로그인 비밀번호는 준비하지 않습니다.

## 2. 게임

| 파일 | 행 수 | 용도 |
|---|---:|---|
| `Game/Data/campaigns.csv` | 2 | 표준 Campaign의 공통 정보 |
| `Game/Data/performance.csv` | 120 | 2026-09-21~10-05의 15일 × 캠페인 2개 × 채널 4개 |
| `Game/Data/performance-first10.csv` | 10 | 전체 120건에 포함된 사전 검토용 부분집합 |
| `Game/Data/screen-entry.xlsx` | 2개 예제 | 화면 입력용이며 CSV 업로드 대상이 아닙니다 |

한 행은 **실적 기준일에 설치한 사용자 집단 × 캠페인 × 채널**입니다. 첫 경기·구매 지표는 설치 후 7일 이내 누적입니다. 관찰 마감은 2026-10-12이며 모든 값은 가상 수치입니다. 장표의 대량 데이터 설명과 별개로 이번 제공본은 120건으로 구성했습니다.

원본 Campaign 코드는 `Training_Campaign_Code__c`로 조회해 주세요. 실적의 고유키는 `Report_Date__c + "|" + 조회한 Campaign.Id + "|" + Channel__c 저장값`입니다. CSV에는 org별 Campaign ID나 완성된 Performance_Key를 저장하지 않습니다. CSV 로더와 화면 Flow에서 같은 키 규칙을 사용해 주세요.

| 기준일 / 캠페인 / 채널 | 초기값 | 예상 결과 |
|---|---|---|
| 10-05 / KA3-NEW / Community | 목표 1,000, 실제 620, 첫 경기 496 | 달성률 62%, 첫 경기 전환율 80% |
| 10-05 / KA3-NEW / Video | 목표 1,000, 실제 1,150, 첫 경기 575 | 달성률 115%, 첫 경기 전환율 50% |
| 10-05 / KA3-NEW / SNS | 목표 800, 실제·첫 경기 공란 | 두 비율 공란, 작성중 |
| 10-04 / KA3-RETURN / Offline | 실제 0, 첫 경기 0 | 달성률 0%, 첫 경기 전환율 공란 |
| 화면에서 10-05 / KA3-NEW / SNS 입력 | 실제 480, 첫 경기 240 | 기존 1건 수정, 60% / 50%, 전체 120건 |
| 화면에서 10-06 / KA3-NEW / Video 입력 | 목표 1,000, 실제 800, 첫 경기 480 | 신규 1건 생성, 80% / 60%, 전체 121건 |

CampaignMember, Lead, Contact, 사용자별 게임 로그는 이번 실습에 필요하지 않습니다. 우영의 스토리는 집계 지표의 의미를 이해하기 위한 사례입니다.

## 3. 아이웨어

`Eyewear/Data/consultation-templates.csv`의 10건을 준비합니다. 날짜를 고정하면 기한 실습이 달라지므로 **실제 준비 시각 t0**에 시간 오프셋을 더해 주세요. t0는 시간대가 있는 ISO 8601 값으로 한 번만 정하고, 3건·7건 등록에 같은 값을 사용해 주세요. 준비 후 4시간이 지나면 A/B도 기한 경과가 되므로 실습 직전에 준비해 주세요.

| 키 | 접수 / 기한 | 시작 상태 | 저장 시 확인하실 결과 |
|---|---|---|---|
| GM-ESC-A | t0 / t0+4시간 | 일반 진행 | 앤디 / 미요청 |
| GM-ESC-B | t0 / t0+4시간 | 도움 필요, 타 매장 재고 조정 | 미란다 / 요청 |
| GM-ESC-C | t0-5시간 / t0-1시간 | 첫 응답 공란 | 미란다 / 요청, 첫 응답 기한 초과 |
| GM-BASE-01 | t0-2시간 / t0+46시간 | 일반 등급, 접수 | 앤디 / 미요청 |
| GM-BASE-02 | t0-2시간 / t0+22시간 | 프리미엄, 진행 | 앤디 / 미요청 |
| GM-BASE-03 | t0-6시간 / t0-2시간 | 기한 내 첫 응답 완료 | 앤디 / 미요청 |
| GM-BASE-04 | t0-50시간 / t0-2시간 | 상담 완료, 이관 이력 없음 | 앤디 / 미요청 |
| GM-BASE-05 | t0-1시간 / t0+23시간 | 매니저 도움 필요 | 미란다 / 요청 |
| GM-BASE-06 | t0-25시간 / t0-1시간 | 기한 후 첫 응답 완료 | 앤디 / 미요청: 이 실습은 현재 미응답 건만 이관합니다 |
| GM-BASE-07 | t0-3시간 / t0+45시간 | 첫 응답 완료 | 앤디 / 미요청 |

모두 초기 에스컬레이션 상태는 미요청이며 현재 처리 직원·이관 사유·이관 시각은 공란입니다. **Flow 활성화만으로 기존 레코드가 처리되지는 않습니다.** 각 레코드를 다시 저장한 후 예상 결과를 확인해 주세요. 완료 건을 포함한 분기와 재저장 시 최초 이관 시각 보존도 확인합니다.

`GM-ESC-D`, `GM-ESC-E`는 장표에서 직접 만드는 추가 시험용 키로 비워 두었습니다. 기본 CSV에 중복 생성하지 않습니다. SLA는 일반 48시간, 프리미엄 24시간, 플래티넘 4시간이며 영업시간 계산이 아닌 경과 시간입니다.

## 4. AI 영업

`AI-Sales/Data/projects.csv`의 네 행은 **같은 도입 평가를 조건별로 나눈 비교 사례**입니다. 서로 다른 수주 4건의 합계로 해석하지 않습니다.

| 키 | 차이 | AI가 확인해야 할 내용 |
|---|---|---|
| AI-POC-A | 정상 | 고객 요구·평가 조건·세 담당자·다음 행동을 요약합니다 |
| AI-POC-B | 보안 검토 중 | 통과/승인 완료로 바꾸어 쓰지 않습니다 |
| AI-POC-C | 성공 기준 공란 | 숫자 기준을 만들어 내지 않고 확인 질문을 제안합니다 |
| AI-POC-D | 코디네이터 공란 | 브루스를 추정하여 넣지 않고 담당자 확인을 제안합니다 |

고객 요청 원문과 구조화 필드를 함께 준비합니다. 누락 사례는 원문에서도 같은 정보를 제거했습니다. AI 요약·이메일 초안·발송 시각은 공란, AI 검토 상태는 미검토, 이메일 상태는 미발송입니다. 모델명·성공 기준은 가상 고객의 평가 요청이며 퓨리오사AI의 공식 지원·측정 결과를 의미하지 않습니다. 이메일 주소·실제 메일 발송·Flow는 기본 데이터에 포함하지 않습니다.

## 변환 컬럼 매핑

아래 컬럼을 제외한 CSV 열은 해당 schema.json의 동일한 API 필드에 연결해 주세요. `Name`은 Employee와 Campaign에서만 직접 입력합니다.

| CSV 컬럼 | Salesforce 필드 / 처리 |
|---|---|
| Common `Manager_Employee_Code` | Employee.Manager_Employee__c, 전체 직원 생성 후 연결 |
| Game `Campaign_Code` | Campaign__c, Campaign.Training_Campaign_Code__c로 조회 |
| Game `Assigned_Employee_Code` | Assigned_Employee__c, 직원 코드로 조회 |
| Eyewear `Advisor_Code` | Advisor__c, 직원 코드로 조회 |
| Eyewear `Manager_Employee_Code` | Manager_Employee__c, 직원 코드로 조회 |
| Eyewear `Current_Handler_Code` | Current_Handler__c, 초기 공란 |
| Eyewear `Received_Offset_Hours` | Received_At__c = t0 + 시간 오프셋 |
| Eyewear `Due_Offset_Hours` | Response_Due_At__c = t0 + 시간 오프셋 |
| Eyewear `First_Response_Offset_Hours` | First_Response_At__c, 공란이면 null |
| AI `Sales_Employee_Code` | Sales_Employee__c, 직원 코드로 조회 |
| AI `Technical_Employee_Code` | Technical_Employee__c, 직원 코드로 조회 |
| AI `Project_Coordinator_Code` | Project_Coordinator__c, 직원 코드로 조회; D는 null |

시간 변환에는 [준비 스크립트](scripts/prepare_eyewear.py)를 사용하실 수 있습니다. 이 스크립트는 org에 접속하지 않으며 직원 코드를 실제 ID로 바꾸지 않습니다. 코드→ID 연결은 Claude가 현재 org를 조회한 후 수행합니다.
