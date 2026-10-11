# List View 표시 열 계약

이 폴더는 Custom App이 생성된 뒤 배포할 ListView 명세입니다.

## Consulting Inquiry

`Consulting_Inquiry__c.All_Consulting_Inquiries`를 새로 만들고 다음 주요 필드를 표시합니다.

- Inquiry Number
- Inquiry Title
- Customer Account / Customer Contact
- Inquiry Status / Priority
- Assigned Consultant
- Next Contact Date
- Manager Attention

## 표준 오브젝트

표준 오브젝트에는 새 교육용 리스트뷰를 추가하지 않습니다. 기존 `All` 리스트뷰의 **표시 열만** 다음 파일대로 조정합니다.

- Account: `AllAccounts`
- Contact: `AllContacts`
- Opportunity: `AllOpportunities`
- Product2: `AllProducts`

표준 `All` 리스트뷰의 `fullName`, `label`, `filterScope=Everything`은 유지하고 `filters`를 추가하지 않습니다. 배포 전 대상 org에서 동일 리스트뷰를 retrieve하여 이 계약과 비교하고, label·filterScope·filters가 예상과 다르면 덮어쓰지 말고 중단합니다.

배포 후 다섯 ListView를 read-back하여 표시 열 순서, label, filterScope와 filters 부재를 확인합니다.
