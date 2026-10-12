# 공통 Employee 준비

`Employee__c`는 가상 직원의 업무 담당을 연결하는 명부입니다. 로그인, 표준 Owner, 레코드 공유, 승인 권한을 대신하지 않습니다. 교육생께서는 본인의 기존 User 한 개로 실습하시면 됩니다.

## 구성요소

- `Object/Employee__c.object.xml`: 직원 오브젝트 1개, Name은 Text입니다.
- `Field/`: 직원 코드·주제·부서·업무 역할·활성 여부·상위 직원, 총 6개입니다.
- `Custom App/Employee__c.tab.xml`: 세 주제 앱에서 공통으로 사용할 탭입니다.
- `Access/Salesforce101_Day2_Employee_User.permissionset.xml`: 현재 실습 User의 Read/Create/Edit 및 필드 접근입니다.
- `Data/employees.csv`: 직원 6명입니다.
- `schema.json`: 같은 구성을 기계가 읽을 수 있도록 정리한 정본입니다.

직원 코드는 필드 수준 Unique External ID로 구성하고, `Active__c` 기본값은 true로 설정해 주세요. 기존 Employee가 있으면 추가 생성하지 마시고 필드와 선택값을 비교해 주세요. 기존 직원이나 항공 관련 값이 있어도 지우지 말아 주세요.

## 등록 순서

1. 직원 코드로 여섯 명의 존재 여부를 확인해 주세요.
2. 신규 직원은 상위 직원 Lookup을 비운 상태로 먼저 생성해 주세요.
3. 같은 단계 안에서 미란다의 현재 org ID를 조회한 뒤 앤디의 `Manager_Employee__c`를 연결해 주세요. 같은 트랜잭션의 Savepoint를 사용하여 연결 실패 시 신규 생성도 되돌려 주세요.
4. 앤디→미란다 관계, 여섯 코드의 유일성, 모든 직원의 활성 상태를 read-back해 주세요. OwnerId를 지정하거나 변경하지 말아 주세요.

이미 완성된 명부이면 DML 없이 확인만 해 주세요. 이름이 같아도 코드가 다르면 임의로 같은 직원으로 합치지 말아 주세요.
