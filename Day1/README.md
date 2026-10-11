# Salesforce 101 — Claude Install Kit

이 디렉터리는 **Salesforce DX 프로젝트가 아닙니다.** Claude가 읽어 학생의 Developer Edition을 안전하게 정리하고 metadata, 관리자 접근 권한, 최종 실습 데이터를 설치하는 명세 키트입니다.

## 구성

- `Cleanup/` — 기존 Developer Edition 샘플 데이터의 preview·승인·정리 계약
- `Object/` — `Consulting_Inquiry__c` 오브젝트 정의
- `Field/` — 커스텀 필드 13개
- `Custom App/` — `Ohana Consulting` Lightning 앱과 커스텀 탭
- `List View/` — Consulting Inquiry 주요 필드 리스트뷰와 표준 오브젝트 기존 All 리스트뷰 표시 열
- `Access/` — System Administrator 전체 접근, View All Fields, 탭 Available Permission Set
- `Flow/` — 구조 관찰용 Draft Flow 1개
- `Data/` — Account, Contact, Inquiry, Product, Price Book, Opportunity, Opportunity Product 데이터
- `catalog.json` — 실행 순서와 정확한 구성요소·레코드 수량
- `CLAUDE.md` — Claude가 따라야 하는 실행 계약

저장소에는 `sfdx-project.json`, `force-app`, 배포 manifest가 없습니다. Claude는 저장소 밖 임시 작업공간에서 Salesforce payload와 preview-first cleanup/seed loader를 만들고, 각 쓰기 단계마다 사용자 승인을 받아 실행합니다.

## 최종 실습 데이터

- Account 8 / Contact 8 / Consulting Inquiry 30
- Product2 12 / Standard PricebookEntry 12
- Opportunity 24 / OpportunityLineItem 48

Account, Contact, Inquiry, Opportunity의 Owner는 설치·실행한 학생 사용자이며 역할별 User를 만들거나 OwnerId를 강제로 설정하지 않습니다.

## 학생이 Claude에 입력할 문장

```text
이 폴더의 CLAUDE.md와 catalog.json을 먼저 읽고 내 Salesforce Developer Edition을 구성해 줘. 기존 샘플 데이터 정리 preview, metadata dry-run, System Admin 접근 확인, 실습 데이터 상태 preview까지만 먼저 진행해. Cleanup, metadata 배포, Permission Set 할당, 데이터 생성은 각각 실행 전에 내 승인을 받아.
```

## 포함하지 않는 것

Tableau, LWC, Apex Class, FlexiPage, Profile, 과거 비교 데이터, 인증정보와 고정 org/Record ID는 포함하지 않습니다.
