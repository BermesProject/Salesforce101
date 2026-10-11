# Claude 설치 실행 계약

이 폴더는 Salesforce 프로젝트가 아니라 **설치 명세 키트**입니다. 현재 디렉터리를 Salesforce DX 프로젝트로 간주하거나 저장소 안에 `sfdx-project.json`, `force-app`, `manifest/package.xml`을 추가하지 마세요.

## 목표

학생이 지정한 별도 Salesforce **Developer Edition**을 정리하고 다음 구성을 설치합니다.

- Object 1개: `Consulting_Inquiry__c`
- Field 13개: `Field/`의 전체 XML
- Custom App 1개: `Ohana_Consulting_Core`
- Custom Tab 1개: `Consulting_Inquiry__c` — Permission Set에서 `Available`
- List View 5개: Consulting Inquiry 주요 필드 1개 + 표준 오브젝트 기존 All 리스트뷰 표시 열 4개
- System Admin Access Permission Set 1개 — 6개 오브젝트에 `View All Fields`
- Flow 1개: `Consulting_Inquiry_Escalation_Lab` — 반드시 `Draft`
- Account 8 / Contact 8 / Consulting Inquiry 30
- Product2 12 / Standard PricebookEntry 12
- Opportunity 24 / OpportunityLineItem 48

실행 순서는 **Cleanup → Object → Field → Custom App → List View → Access → Flow → Data**입니다. 각 쓰기 단계는 preview 또는 dry-run, 사용자 승인, 적용, read-back을 별도로 수행합니다.

## 절대 규칙

1. 사용자가 지정한 org alias를 모든 `sf` 명령에 명시합니다. alias를 추측하지 마세요.
2. 시작할 때 Organization을 조회하여 `OrganizationType = Developer Edition`, `IsSandbox = false`인지 확인합니다.
3. Production, 고객 org, 공유 org, 예상하지 못한 org이면 중단합니다.
4. 토큰, 비밀번호, `sfdxAuthUrl`, org ID는 출력하거나 커밋하지 않습니다. Record ID도 저장·커밋하지 않지만, cleanup 대상의 정확한 Account ID는 사용자가 삭제 대상을 식별하도록 현재 승인 화면에만 일시적으로 표시할 수 있습니다. org guard가 필요한 임시 파일은 저장소 밖에서 만들고 실행 직후 삭제합니다.
5. Cleanup, metadata 배포, Permission Set 할당, 데이터 seed는 서로 다른 승인 단계입니다. 하나의 승인을 다른 쓰기 작업의 승인으로 확대하지 않습니다.
6. `Cleanup/README.md`에 따라 삭제 후보 preview를 먼저 보여 주고, 사용자가 승인한 정확한 Account ID만 soft delete합니다. Product2, PricebookEntry, Lead, Campaign은 자동 삭제하지 않으며 hard delete도 하지 않습니다. Custom object가 이미 존재하면 후보 Account·Contact에 대한 `Consulting_Inquiry__c` 참조를 먼저 조회하고, 참조 중이면 중단합니다.
7. 저장소 바깥의 임시 디렉터리에 일회용 Salesforce DX 작업공간을 만들고 XML 명세를 Salesforce source 형식으로 변환합니다. 임시 산출물을 저장소에 커밋하지 않습니다.
8. 대상 org의 동일 API Name 구성요소를 먼저 읽기 전용으로 조회합니다. 기존 정의와 충돌하거나 안전한 병합을 확신할 수 없으면 덮어쓰지 말고 차이를 보고합니다.
9. `Consulting_Inquiry_Escalation_Lab`의 `FlowDefinition.ActiveVersionId`와 `LatestVersionId`를 조회하고, 활성 버전이 있으면 중단합니다. 기존 Flow를 비활성화하거나 삭제하지 않습니다.
10. metadata는 동일 payload의 `dry-run`이 성공한 경우에만 실제 배포합니다. dry-run 실패를 우회하지 않습니다.
11. 승인 직후 각 쓰기 전에 alias와 Organization 정보를 다시 조회하여 같은 Developer Edition인지 검증합니다.
12. `Access/README.md`에 따라 현재 설치 사용자가 정확히 `System Administrator`인지 확인하고, 명시적 승인 후 해당 사용자에게만 Permission Set을 할당합니다. Profile은 수정하지 않습니다.
13. `Data/README.md`에 따라 데이터 전체를 `EMPTY`, `COMPLETE`, `PARTIAL`로 분류합니다. `PARTIAL`, duplicate business key, 예상 밖 prefix가 있으면 DML 전에 중단합니다.
14. 데이터 생성 시 User를 만들거나 `OwnerId`를 지정·변경하지 않습니다. Account, Contact, Inquiry, Opportunity의 Owner는 설치·실행한 학생 사용자입니다.
15. Flow는 `Draft`로 유지하고 활성화하지 않습니다. 학생은 구조만 관찰하며 Debug는 강사 범위입니다.
16. Tableau, LWC, Apex Class, FlexiPage, Profile, 과거 비교 데이터는 만들거나 변경하지 않습니다.
17. 실패나 부분 성공이 발생하면 완료라고 보고하지 말고 적용·미적용 상태를 구분해 보고합니다.

## 파일 해석

- `Cleanup/` — 기존 Developer Edition 샘플 데이터의 승인 기반 정리 계약
- `Object/`, `Field/`, `Custom App/`, `List View/`, `Access/`, `Flow/` — metadata 입력 명세
- `Data/` — Record ID가 없는 최종 실습 데이터와 관계 계약
- XML 파일명의 `.object.xml`, `.field.xml`, `.app.xml`, `.tab.xml`, `.permissionset.xml`, `.flow.xml`은 사람이 구분하기 위한 이름입니다.
- 임시 DX 작업공간으로 옮길 때 Salesforce source-format 파일명으로 바꾸되 API Name과 XML 본문은 임의로 바꾸지 않습니다.
- `Object/Consulting_Inquiry__c.object.xml`에는 FlexiPage action override가 없습니다. 추가하지 마세요.
- `Custom App/Consulting_Inquiry__c.tab.xml`은 앱 navigation의 선행 구성요소이며 Access Permission Set의 `tabSettings`에서 `Available`이어야 합니다.
- `List View/`의 표준 오브젝트 파일은 기존 All 리스트뷰의 표시 열만 변경합니다. 배포 전 `filterScope`, `label`, `filters`가 예상 상태인지 retrieve하고 다르면 중단합니다.
- `Access/Salesforce101_Day1_System_Admin_Access.permissionset.xml`은 System Admin의 앱·오브젝트·필드·레코드 접근과 6개 오브젝트의 `View All Fields`를 명시적으로 보강합니다.

## 실행 단계

### 1. 읽기 전용 사전 점검

- `catalog.json`의 metadata와 data 수량이 실제 파일과 일치하는지 확인
- XML 파싱과 CSV 관계 계약 확인
- 대상 org 종류, 현재 사용자, Profile 확인
- 관련 표준 오브젝트의 현재 레코드 수 확인
- 같은 API Name의 object/app/tab/permission set/Flow와 field 목록 확인
- Flow 활성 버전 존재 여부 확인

### 2. 샘플 데이터 정리

`Cleanup/README.md`를 읽고 Account, Contact, Opportunity 및 연결된 line item, Task, Event, Case의 삭제 후보 preview를 만듭니다. 정확한 Account ID는 현재 승인 화면에만 일시적으로 표시하고 Account 이름, 하위 객체별 건수와 함께 별도의 명시적 승인을 받습니다. `Consulting_Inquiry__c`가 이미 존재하면 후보 Account·Contact에 대한 `Customer_Account__c`, `Customer_Contact__c` 참조를 먼저 조회하며, 하나라도 참조 중이면 중단합니다. 승인된 범위만 Savepoint 안에서 soft delete하고 read-back합니다.

### 3. 임시 payload 구성

저장소 밖 임시 디렉터리에 최소 Salesforce DX 프로젝트를 생성하고 Object, Field, Custom App, List View, Access, Flow XML만 source-format 경로에 배치합니다. 이 임시 프로젝트는 전송 수단일 뿐 학생 배포 산출물이 아닙니다.

### 4. metadata dry-run

- 대상 alias를 명시해 전체 payload를 dry-run
- component success/error 수와 Apex test 실행 수를 구분해서 보고
- Flow가 Draft인지 payload에서도 재확인
- Access Permission Set에 6개 오브젝트의 CRED, View All Records, Modify All Records, View All Fields, 앱 visibility, `Consulting_Inquiry__c` 탭 `Available`, 11개 명시 field permission이 있는지 확인
- List View 5개의 표시 열과 표준 All 리스트뷰의 label, filterScope, filters 보존을 확인

### 5. 승인 후 metadata 배포

사용자가 승인한 경우에만 dry-run과 동일한 payload를 배포합니다. 배포 직후 object, field 13개, app, tab, List View 5개, Permission Set, Flow를 Metadata 또는 Tooling API로 read-back합니다.

### 6. System Admin 접근 할당

`Access/README.md`를 따라 현재 설치 사용자의 Profile.Name이 `System Administrator`인지 확인합니다. PermissionSetAssignment가 없다면 대상 사용자와 권한을 보여 주고 별도 승인을 받은 뒤 `Salesforce101_Day1_System_Admin_Access`를 할당합니다. 할당과 권한을 read-back합니다.

### 7. 실습 데이터 preview와 생성

`Data/README.md`와 6개 CSV를 읽습니다. 전체 그래프가 `EMPTY`일 때만 정확한 생성 수량을 보여 주고 별도 승인을 요청합니다. 승인 후 하나의 Savepoint 안에서 Account → Contact → Inquiry → Product2 → Standard PricebookEntry → Opportunity → OpportunityLineItem 순서로 생성하고 전체 관계를 read-back합니다.

`COMPLETE`이면 DML 0으로 검증만 합니다. `PARTIAL`이면 생성·삭제·수정하지 않고 차이를 보고합니다.

### 8. 최종 완료 조건

Metadata:

- `Consulting_Inquiry__c`가 Deployed이며 Reports와 Activities 활성화
- custom field 13개의 type, formula, picklist, Lookup 계약 일치
- 앱 label `Ohana Consulting`, navigation Account / Contact / Consulting Inquiry / Opportunity / Task
- `Consulting_Inquiry__c` 탭 `Available`
- Consulting Inquiry 주요 필드 리스트뷰 1개와 표준 All 리스트뷰 4개의 표시 열 일치
- Permission Set의 앱, 탭, 6개 objectPermissions(CRED / View All Records / Modify All Records / View All Fields), 11개 명시 fieldPermissions 일치
- 현재 System Administrator의 PermissionSetAssignment 1건
- FlowDefinition `ActiveVersionId = null`, `LatestVersionId`는 최신 Draft 버전

Data:

- Account 8 / Contact 8 / Inquiry 30
- Inquiry Account Lookup 30, Contact Lookup 29 + 의도된 null 1
- Assigned Consultant 석유진 10 / 조우찬 10 / 이채원 10
- Product2 12 / Standard PricebookEntry 12
- Opportunity 24 / OpportunityLineItem 48
- Opportunity별 상품 2개, Quantity 1, line sum과 Amount 일치
- 학생 소유 대상 레코드의 Owner가 설치·실행한 학생 사용자
- 완료 상태 재실행은 `COMPLETE`, DML 0

## 첫 응답 형식

설치 요청을 받으면 곧바로 쓰기를 시작하지 말고 다음을 먼저 보고합니다.

1. 대상 org alias와 Developer Edition 확인 결과
2. 현재 사용자와 Profile
3. 삭제 후보 Account와 연결 레코드의 preview 수량
4. 기존 동일 metadata API Name 충돌 여부
5. metadata payload 구성요소 수와 dry-run 계획
6. 기존 실습 데이터의 EMPTY / COMPLETE / PARTIAL 상태
7. Cleanup, metadata, 권한 할당, 데이터 생성마다 별도 승인을 요청한다는 점
