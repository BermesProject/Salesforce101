# AI 영업 실습

퓨리오사AI의 사업을 참고한 가상 공급사 **매드맥스**가 **타노스전자**의 도입 평가를 지원합니다. 교육생께서는 Prompt Builder와 Agentforce를 직접 사용하여 고객 요청 요약과 이메일 초안을 만드십니다.

## 준비 데이터와 환경

1. 페퍼·토니·브루스의 공통 직원 코드를 확인해 주세요.
2. `schema.json`으로 `B2B_AI_Project__c`와 22개 필드를 준비해 주세요. Name은 AutoNumber `BAP-{0000}`입니다.
3. 앱 `B2B_AI_Sales_Operations`, 프로젝트 탭, Permission Set `B2B_AI_Project_User`를 구성해 주세요. 직원과 프로젝트를 탐색할 수 있게 해 주세요.
4. 화면에 고객 요청, 평가 조건, 담당자, AI 결과·검토 상태를 묶어 배치해 주세요.
5. `Data/projects.csv` 4건을 준비하고 원문과 구조화 필드가 일치하는지 확인해 주세요. AI-POC-C의 기준과 AI-POC-D의 코디네이터는 필수 필드로 만들거나 자동 보완하지 않습니다.

Agentforce와 Prompt Builder가 활성화되어 있다는 수업 조건을 전제로 하되, 실제 실행 User의 템플릿 작성/실행 권한과 Agent 실행 권한은 org에서 확인해 주세요. 권한 이름이나 사용 가능한 모델은 UI에서 확인한 값을 사용해 주세요. Custom Object 권한만으로 AI 기능 권한이 모두 생기지는 않습니다.

## 수업 실습 순서

1. Flex Prompt Template `B2B_POC_Email_Draft`를 만들고 입력 `Project`를 `B2B_AI_Project__c` 레코드에 연결해 주세요.
2. [프롬프트 명세](PROMPTS.md)의 필요한 필드들을 리소스 선택기로 삽입해 주세요. 문서의 설명용 대괄호를 실제 merge syntax로 그대로 입력하지 않습니다.
3. A와 B를 비교하여 보안 검토 상태가 반영되는지 확인해 주세요. 결과를 검토한 뒤 이메일 초안 필드에 저장합니다. 템플릿의 Preview만으로 레코드 필드가 저장되지는 않습니다.
4. Flex Template `B2B_POC_Request_Summary`를 만들고 Prompt Template 기반 Agent Action으로 연결해 주세요. Agent가 프로젝트 키로 레코드를 조회한 다음 실제 조회 레코드를 입력으로 전달하도록 구성해 주세요.
5. A/B/C/D와 존재하지 않는 `AI-POC-Z`를 시험해 주세요. 조회 0건이면 키를 확인하고, 여러 건이면 선택을 요청해야 합니다. 다른 프로젝트 내용을 가져오지 않도록 해 주세요.

이 실습에는 이메일 발송용 Flow를 만들지 않습니다. 이메일을 시험하려면 교육생 본인 주소를 직접 확인한 뒤 메일 앱에서 보내 주세요. 본인에게 실제 테스트 발송한 후에만 `Email_Status=테스트 발송 완료`, `Sent_At`을 기록합니다. 고객 역할의 실명 주소는 데이터에 제공하지 않습니다.

## 예상 결과

| 사례 | 확인할 기준 |
|---|---|
| A | 고객 목적, 모델·요청 조건, 성공 기준, 일정, 페퍼/토니/브루스, 다음 행동이 근거와 일치합니다 |
| B | 보안 검토가 진행 중이며 평가 착수 전 확인이 필요하다고 표현합니다 |
| C | 정량 성공 기준이 미정이라고 밝히고 확인 질문을 제안합니다. 원문에 없는 임계값은 만들지 않습니다 |
| D | 코디네이터 미정을 밝힙니다. 브루스에게 임의 배정하지 않습니다 |
| Z | 조회되지 않았다고 안내하고 올바른 프로젝트 키를 확인합니다 |

출력 문장은 매번 달라질 수 있으므로 문장 일치가 아닌 위 사실 기준으로 검토해 주세요. 기본 CSV에는 정답 요약이나 완성된 초안을 넣지 않았습니다. 성공 기준의 숫자는 교육용 고객 요구이며 공식 하드웨어 성능을 주장하는 자료가 아닙니다.

## 공식 참고 자료

- [Flex 템플릿 구성](https://developer.salesforce.com/workshops/agentforce-workshop/prompt-builder/4-flex-template)
- [Prompt Template 기반 Agent Action](https://developer.salesforce.com/workshops/agentforce-workshop/employee-agents/7-prompt-template-actions)
- [Prompt Builder 시작하기](https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-prompt-builder.html)
