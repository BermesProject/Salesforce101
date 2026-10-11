# System Administrator 접근 보장

`Salesforce101_Day1_System_Admin_Access.permissionset.xml`은 DAY 1 metadata와 실습 레코드를 설치한 관리자에게 명시적으로 전체 접근을 부여하기 위한 Permission Set 명세입니다. Profile을 직접 수정하지 않습니다.

## 포함 권한

- `Ohana_Consulting_Core`의 `applicationVisibilities = true`
- `Consulting_Inquiry__c` 탭 Available
- Account, Contact, Opportunity, Product2, Pricebook2, Consulting_Inquiry__c의 Create / Read / Edit / Delete
- 위 6개 오브젝트의 View All Records / Modify All Records / View All Fields
- Consulting Inquiry 필드 11개의 명시적 `fieldPermissions`
- Formula 필드 `Attention_Reason__c`, `Manager_Attention__c`는 readable=true, editable=false
- 필수 필드 `Inquiry_Title__c`, `Received_Date__c`는 Salesforce가 암시적으로 접근을 부여하므로 Permission Set XML에 넣지 않습니다. required custom field의 fieldPermissions를 추가하면 배포가 거부될 수 있습니다.

## 할당 절차

1. metadata dry-run과 실제 배포가 성공한 뒤 현재 로그인 사용자의 Profile을 조회합니다.
2. 사용자의 Profile.Name이 정확히 `System Administrator`인지 확인합니다. 다른 Profile이면 중단하고 사용자가 지정할 때까지 추측하지 않습니다.
3. `Salesforce101_Day1_System_Admin_Access` Permission Set과 현재 사용자의 기존 `PermissionSetAssignment`를 조회합니다.
4. 이미 할당되어 있으면 COMPLETE / DML 0으로 처리합니다.
5. 미할당 상태라면 대상 사용자와 추가될 권한을 보여 주고 사용자의 **명시적 승인**을 받습니다.
6. 승인 후 현재 설치 사용자에게만 할당합니다. 다른 활성 System Administrator에게 일괄 할당하지 않습니다.
7. 할당 직후 `PermissionSetAssignment`를 read-back하고, Permission Set metadata의 `objectPermissions`, `fieldPermissions`, `applicationVisibilities`, tabSettings를 다시 확인합니다.

## 완료 조건

- 정확히 한 개의 대상 Permission Set이 존재
- 현재 설치 사용자가 `System Administrator`
- 현재 설치 사용자에 대한 PermissionSetAssignment 정확히 1건
- 앱과 Consulting Inquiry 탭 접근 가능
- 6개 오브젝트의 CRED, View All Records, Modify All Records, View All Fields가 모두 true
- 11개 명시 필드 접근과 2개 required-field 암시 접근 확인
- Formula 필드는 읽기 전용

Permission Set은 레코드 `Owner`를 바꾸지 않습니다. Data seed에서 생성되는 Account, Contact, Inquiry, Opportunity는 설치·실행한 학생 사용자가 Owner가 됩니다.
