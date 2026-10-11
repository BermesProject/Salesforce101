# Claude 설치 실행 계약

이 폴더는 Salesforce 프로젝트가 아니라 metadata **설치 명세**입니다. 현재 디렉터리를 Salesforce DX 프로젝트로 간주하거나 저장소 안에 `sfdx-project.json`, `force-app`, `manifest/package.xml`을 추가하지 마세요.

## 목표

학생이 지정한 별도 Salesforce **Developer Edition**에 다음 구성요소만 설치합니다.

- Object 1개: `Consulting_Inquiry__c`
- Field 13개: `Field/`의 전체 XML
- Custom App 1개: `Ohana_Consulting_Core`
- Custom Tab 1개: `Consulting_Inquiry__c`
- Flow 1개: `Consulting_Inquiry_Escalation_Lab` — 반드시 `Draft`

설치 순서는 **Object → Field → Custom App → Flow**입니다. 앱보다 먼저 커스텀 탭을 준비하되, 둘은 `Custom App/` 범주의 한 단계로 취급합니다.

## 절대 규칙

1. 사용자가 지정한 org alias를 모든 `sf` 명령에 명시합니다. alias를 추측하지 마세요.
2. 시작할 때 Organization을 조회하여 `OrganizationType = Developer Edition`, `IsSandbox = false`인지 확인합니다.
3. Production, 고객 org, 공유 org, 예상하지 못한 org이면 중단합니다.
4. 토큰, 비밀번호, `sfdxAuthUrl`, org ID를 출력하거나 파일에 저장하지 않습니다.
5. 저장소 바깥의 임시 디렉터리에 일회용 Salesforce DX 작업공간을 만들고, 이 폴더의 XML 명세를 Salesforce source 형식으로 변환합니다. 임시 산출물을 이 저장소에 커밋하지 않습니다.
6. 대상 org의 동일 API Name 구성요소를 먼저 읽기 전용으로 조회합니다. 기존 정의와 충돌하거나 안전한 병합을 확신할 수 없으면 덮어쓰지 말고 차이를 보고합니다. `Consulting_Inquiry_Escalation_Lab`의 `FlowDefinition.ActiveVersionId`와 `LatestVersionId`를 조회하고, 활성 버전이 있으면 중단합니다. 기존 Flow를 비활성화하거나 삭제하지 않습니다.
7. 실제 배포 전에 정확한 payload와 영향 범위를 설명하고 사용자의 **명시적 승인**을 받습니다.
8. 동일 payload로 `dry-run`이 성공한 경우에만 실제 배포합니다. dry-run 실패를 우회하지 않습니다.
9. 승인 직후 배포하기 전에 alias와 Organization 정보를 다시 조회하여 dry-run 때 확인한 같은 Developer Edition인지 검증합니다. org ID는 출력하거나 저장하지 않습니다.
10. 배포 직후 Tooling API 또는 Metadata retrieve로 object, field 13개, app, tab, Flow를 **read-back**합니다.
11. `Consulting_Inquiry_Escalation_Lab`은 수업에서 구조만 관찰합니다. `Draft`를 유지하고 활성화하지 않습니다.
12. 이 설치에서 Salesforce User를 만들거나 레코드 `OwnerId`를 바꾸지 않습니다.
13. 데이터 레코드, Tableau, LWC, Apex, FlexiPage, Profile, Permission Set은 만들거나 변경하지 않습니다.
14. 실패나 부분 성공이 발생하면 완료라고 보고하지 말고, 적용된 구성요소와 미적용 구성요소를 구분해 보고합니다.

## 파일 해석

- 각 XML 루트 요소는 Salesforce Metadata API component type을 나타냅니다.
- 파일명의 `.object.xml`, `.field.xml`, `.app.xml`, `.tab.xml`, `.flow.xml`은 사람이 범주를 쉽게 구분하기 위한 이름입니다.
- 임시 DX 작업공간으로 옮길 때 Salesforce source-format 파일명으로 바꾸되 API Name과 XML 본문은 임의로 바꾸지 않습니다.
- `Object/Consulting_Inquiry__c.object.xml`에는 의도적으로 FlexiPage action override가 없습니다. 추가하지 마세요.
- `Custom App/Consulting_Inquiry__c.tab.xml`은 앱 내 `Consulting_Inquiry__c` navigation item의 선행 구성요소입니다.

## 실행 단계

### 1. 읽기 전용 사전 점검

- `catalog.json`의 수량과 실제 파일 수가 일치하는지 확인
- XML 파싱 확인
- 대상 org 종류와 현재 사용자 확인
- 같은 API Name의 object/app/tab/Flow 존재 여부와 기존 field 목록 조회

### 2. 임시 payload 구성

저장소 밖 임시 디렉터리에 최소 Salesforce DX 프로젝트를 생성하고 이 명세만 source-format 경로에 배치합니다. 그 임시 프로젝트는 전송 수단일 뿐이며 학생 배포 산출물이 아닙니다.

### 3. dry-run

- 대상 alias를 명시해 전체 payload를 dry-run
- component success/error 수와 Apex test 실행 수를 구분해서 보고
- Flow가 Draft인지 payload에서도 다시 확인

### 4. 승인 후 실제 배포

사용자가 승인한 경우에만 dry-run과 동일한 payload를 배포합니다. Flow 활성화, 데이터 생성, 권한 변경은 별도 승인 대상이며 이 설치 범위에는 없습니다.

### 5. read-back 완료 조건

- `Consulting_Inquiry__c`가 Deployed이며 Reports와 Activities가 활성화
- custom field 정확히 13개가 존재하고 XML의 type·formula·picklist·Lookup 계약과 일치
- `Assigned_Consultant__c` 값이 `석유진`, `조우찬`, `이채원`
- `Customer_Account__c → Account`, `Customer_Contact__c → Contact`
- 앱 label이 `Ohana Consulting`, navigation이 Account / Contact / Consulting Inquiry / Opportunity / Task
- FlowDefinition 조회에서 `ActiveVersionId = null`이고 `LatestVersionId`가 설치한 Draft 버전을 가리킴
- 최신 Flow version의 상태가 `Draft`이며 active version은 없음

## 첫 응답 형식

설치 요청을 받으면 곧바로 쓰기를 시작하지 말고 다음만 먼저 보고합니다.

1. 대상 org alias
2. Developer Edition 확인 결과
3. 기존 동일 API Name 충돌 여부
4. 생성할 임시 payload 구성요소 수
5. dry-run 실행 여부
6. 실제 배포 전에 다시 승인을 요청한다는 점
