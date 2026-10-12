# DAY 1 실습 데이터

이 폴더는 Salesforce Record ID 없이 이식 가능한 최종 실습 데이터 명세입니다. Claude는 CSV의 business key를 읽어 대상 Developer Edition에서 Lookup ID를 동적으로 해석합니다.

## 데이터 범위

- `accounts.csv`: Account 8건
- `contacts.csv`: Contact 8건 — AccountName으로 연결
- `inquiries.csv`: Consulting Inquiry 30건 — AccountName과 ContactEmail로 연결
- `products.csv`: Product2 12건과 Standard Price Book 가격 12건
- `opportunities.csv`: Opportunity 24건 — AccountName으로 연결
- `opportunity-products.csv`: OpportunityLineItem 48건 — OpportunityName과 ProductCode로 연결

총 데이터 계약:

- Account 8 / Contact 8 / Consulting Inquiry 30
- Product2 12 / Standard PricebookEntry 12
- Opportunity 24 / OpportunityLineItem 48
- Opportunity별 상품 2개, Quantity 1
- Opportunity Amount는 두 line item의 TotalPrice 합계와 일치
- `OH-0002` 1건만 원본 `배송 지연 대응 연결` 데이터 품질 시나리오를 보존하기 위해 Contact Lookup이 의도적으로 null
- Assigned Consultant는 석유진 10 / 조우찬 10 / 이채원 10

## Owner 계약

CSV에는 `OwnerId`가 없습니다. Account, Contact, Consulting Inquiry, Opportunity는 설치·실행한 교육생 사용자가 Owner가 됩니다. 역할별 Salesforce User를 만들거나 Owner를 재배정하지 않습니다. Permission Set은 접근 권한만 부여하며 소유권을 바꾸지 않습니다.

## 설치 순서

1. Account
2. Contact
3. Consulting Inquiry
4. Product2
5. Standard Price Book 활성 상태 확인 및 PricebookEntry
6. Opportunity
7. OpportunityLineItem

Opportunity의 `Amount` 열은 검증 기대값입니다. Opportunity insert에서 Amount를 직접 설정하지 말고 OpportunityLineItem 생성 후 Salesforce가 계산한 Amount를 read-back하여 비교합니다.

## Preview-first 상태 판정

Claude는 저장소 밖의 임시 anonymous Apex 또는 동등한 안전한 loader를 생성합니다. 저장소에는 org ID나 Record ID가 들어간 실행 파일을 남기지 않습니다.

각 business key 그래프를 다음 중 하나로만 분류합니다.

- `EMPTY`: 대상 key가 하나도 없음
- `COMPLETE`: 모든 key, 필드, 관계, 가격과 line composition이 정확히 일치
- `PARTIAL`: 일부만 존재하거나 값·관계·수량이 다름

`PARTIAL`, duplicate key, 예상하지 못한 동일 prefix, 비활성 Opportunity Stage, 다른 Price Book 연결이 발견되면 DML 전에 중단합니다. 기존 레코드를 삭제하고 다시 만드는 방식으로 수렴시키지 않습니다.

Preview는 항상 DML 0이어야 합니다. `EMPTY`일 때만 정확한 생성 건수와 영향을 보여 주고 사용자의 명시적 승인을 받은 후 적용합니다. `COMPLETE`일 때는 read-back 검증만 하고 DML 0으로 종료합니다.

## 적용 안전성

- 대상 Organization ID, Developer Edition, non-sandbox를 실행 직전에 다시 검증
- Account Name, Contact Email, Inquiry Title, ProductCode, OpportunityName의 유일성 검증
- 모든 Lookup business key를 DML 전에 해석
- Standard Price Book이 비활성이면 승인된 seed transaction 안에서만 활성화
- 하나의 `Savepoint` 이후 전체 생성과 read-back 수행
- 오류나 검증 불일치 시 전체 `rollback`
- 생성 순서와 반대로 부분 삭제하거나 재시도하지 않음
- 적용 직후 전체 그래프를 read-back
- 같은 loader를 다시 실행하여 `COMPLETE`, DML 0 확인
- 임시 loader와 org-specific 파일은 실행 직후 삭제

## read-back 완료 조건

- Account 8건과 Contact 8건의 정확한 business key 및 관계
- Inquiry 30건의 모든 필드, Account 30건 연결, Contact 29건 연결 + 의도된 null 1건
- Product2 12건 active
- Standard PricebookEntry 12건 active, `UseStandardPrice=false`, CSV 가격 일치
- Opportunity 24건의 Account, StageName, CloseDate, Description, NextStep 일치
- OpportunityLineItem 48건의 ProductCode, Quantity, UnitPrice, TotalPrice, Description 일치
- Opportunity별 product pair 2개와 Amount 합계 일치
- 교육생이 소유해야 하는 생성 레코드의 Owner가 설치·실행한 교육생 사용자

실제 쓰기는 metadata 배포와 System Administrator Permission Set 할당이 성공한 뒤 별도 승인을 받아 진행합니다.
