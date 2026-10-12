# Developer Edition 샘플 데이터 정리

이 단계는 metadata 설치 전에 수행하는 선택적 정리 절차입니다. 새 Developer Edition에 기본으로 포함된 레코드 중 DAY 1 실습과 겹치는 **Account 계열만** 사용자가 직접 확인하고 승인한 범위에서 정리합니다.

## 범위

정리 후보:

- Account
- 승인된 Account에 연결된 Contact
- 승인된 Account에 연결된 Opportunity와 OpportunityLineItem
- 승인된 Account·Contact·Opportunity에 연결된 Task와 Event
- 승인된 Account·Contact에 연결된 Case

자동 정리 금지:

- `Product2`
- `PricebookEntry`
- `Lead`
- `Campaign`
- 승인되지 않은 Account와 그 하위 레코드
- 교육생이 만든 레코드 또는 출처가 불분명한 레코드
- 이미 존재하는 교육용 `Consulting_Inquiry__c` 레코드

## 안전 계약

1. 먼저 `OrganizationType = Developer Edition`, `IsSandbox = false`인지 확인합니다.
2. Account와 연관 레코드를 읽기 전용으로 조회하고 Account 이름, 정확한 Account ID, 하위 객체별 건수를 보여 줍니다. 정확한 Account ID는 현재 승인 화면에만 일시적으로 표시하고 파일·로그·저장소에는 남기지 않습니다.
3. 이름이나 개수만으로 샘플을 추정하지 않습니다. 사용자가 삭제할 **정확한 Account ID**를 선택해야 합니다.
4. 승인 전 임시 스크립트는 반드시 `RUN_DELETE = false`인 preview 상태여야 합니다.
5. preview에는 Account별 Contact, Opportunity, OpportunityLineItem, Task, Event, Case 수와 전체 삭제 예정 수를 표시합니다.
6. preview 결과를 보여 준 뒤 사용자의 **명시적 승인**을 받습니다. 승인되지 않은 ID를 추가하지 않습니다.
7. 삭제 실행 직전 대상 alias가 같은 Developer Edition인지 다시 확인합니다.
8. `Consulting_Inquiry__c` object가 이미 존재하면 승인 후보 Account와 그 Contact를 참조하는 `Customer_Account__c`, `Customer_Contact__c`를 읽기 전용으로 조회합니다. Lookup의 `deleteConstraint=SetNull`에 기대어 관계를 조용히 지우지 않습니다. 기존 Inquiry가 하나라도 참조 중이면 중단하고 해당 Account를 cleanup 후보에서 제외합니다. 관계 변경은 이 cleanup 범위에서 승인받거나 실행하지 않습니다.
9. 실행은 저장소 밖 임시 디렉터리의 anonymous Apex에서 수행합니다. 대상 org ID와 승인 ID는 그 임시 파일에서만 사용하고 출력·커밋하지 않으며 실행 직후 파일을 즉시 삭제합니다.
10. Apex는 `Savepoint`를 만든 뒤 오류가 하나라도 발생하면 전체 `rollback`하고 실패를 보고해야 합니다.
11. 삭제 순서는 **OpportunityLineItem → Task/Event → Case → Opportunity → Contact → Account**입니다.
12. 삭제 후 같은 트랜잭션 안에서 승인된 Account와 수집한 하위 Record ID가 남지 않았는지 재조회합니다.
13. Recycle Bin을 비우는 hard delete는 금지합니다. 일반 **soft delete**만 사용합니다.
14. 적용 후 다시 preview하여 승인된 범위의 삭제 후보가 0건인지 확인합니다.

## Claude가 생성할 임시 Apex의 필수 구조

저장소에는 삭제 스크립트를 넣지 않습니다. Claude가 저장소 밖에서 아래 계약을 만족하는 일회용 anonymous Apex를 생성합니다.

- `Boolean RUN_DELETE = false;`가 기본값
- 실행 시점의 예상 org ID와 실제 `Organization.Id` 일치 검증
- Developer Edition 및 non-sandbox 검증
- `APPROVED_ACCOUNT_IDS`에 사용자가 승인한 정확한 ID만 포함
- Account ID 중복, 존재하지 않는 ID, 승인 목록 밖 조회 결과 발견 시 DML 전 중단
- 모든 대상 Record ID를 DML 전에 고정하고 객체별 예상 건수 출력
- `RUN_DELETE = false`에서는 DML 0
- `RUN_DELETE = true`에서는 하나의 `Savepoint`와 `try/catch` 안에서 삭제·read-back 수행
- 오류 또는 read-back 불일치 시 `Database.rollback(savepoint)` 실행
- 성공·실패와 객체별 건수만 보고하고 org ID나 Record ID를 로그에 출력하지 않음

## 중단 조건

다음 중 하나라도 발생하면 삭제하지 않습니다.

- Developer Edition이 아니거나 sandbox인 경우
- 교육생이 보고 있는 org와 CLI 대상이 다른 경우
- 정확한 Account ID 승인이 없는 경우
- 삭제 후보에 교육생이 만든 레코드나 교육용 데이터가 섞였을 가능성이 있는 경우
- Product·Price Book 레코드가 존재하지만 기본 샘플인지 판별할 수 없는 경우
- preview와 실행 직전의 대상 건수가 달라진 경우
- 일부 삭제 또는 read-back 검증 실패
