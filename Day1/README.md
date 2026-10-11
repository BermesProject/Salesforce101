# Salesforce 101 — Claude Install Kit

이 디렉터리는 **Salesforce DX 프로젝트가 아닙니다.** 학생에게 완성 프로젝트 구조를 배포하지 않고, Claude가 읽어 대상 Developer Edition에 설치할 최소 metadata 명세만 제공합니다.

## 구성

- `Object/` — `Consulting_Inquiry__c` 오브젝트 정의
- `Field/` — 해당 오브젝트의 커스텀 필드 13개
- `Custom App/` — `Ohana Consulting` Lightning 앱과 커스텀 탭
- `Flow/` — 구조 관찰용 Draft Flow 1개
- `catalog.json` — 설치 순서, 수량, 제외 범위
- `CLAUDE.md` — Claude가 따라야 하는 안전한 설치 계약

XML 파일은 원본 설계를 정확히 전달하기 위한 **입력 명세**입니다. 저장소 자체에는 `sfdx-project.json`, `force-app`, 배포 manifest가 없습니다. Claude는 대상 org를 확인한 뒤 임시 작업공간에서 필요한 Salesforce metadata 형태를 구성하고, dry-run과 사용자의 승인을 거쳐 설치해야 합니다.

## 학생이 Claude에 입력할 문장

```text
이 폴더의 CLAUDE.md와 catalog.json을 먼저 읽고, Flow / Custom App / Object / Field 명세를 내 Salesforce Developer Edition에 설치해 줘. 먼저 대상 org와 기존 구성요소를 읽기 전용으로 확인하고 dry-run까지만 진행해. 실제 배포 전에는 내 승인을 받아.
```

## 포함하지 않는 것

데이터 seed, Tableau, LWC, Apex, FlexiPage, Profile, Permission Set, 인증정보, org ID는 포함하지 않습니다. 데이터 생성은 별도 수업 단계로 다룹니다.
