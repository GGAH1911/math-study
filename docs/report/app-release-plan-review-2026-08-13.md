---
sources: [docs/architecture/app-release-plan.md, docs/architecture/android-launch-checklist.md]
created: 2026-08-13
updated: 2026-08-13
---

# 🔍 앱 출시 계획 리뷰 리포트 (2026-08-13)

> 분류: Report / Review. **다중 에이전트 워크플로우 산출물**(13 에이전트 · 6개 렌즈 병렬 리뷰 →
> 렌즈별 적대적 검증 → 종합). 발견 **77건 → 검증 통과 41건 → 병합 22건**(기각률 47%).
>
> 렌즈: 사실검증 · 누락탐지 · 모순검사 · 가정스트레스 · 순서검증 · 비용재계산.
> 각 발견에 **파일:줄 / 재현 명령+출력 / 출처 URL** 중 하나를 증거로 강제했고,
> 검증 단계는 **기본값 기각**(판단이 서지 않으면 버림)으로 돌렸다.
>
> 실행 기록: 워크플로우 `wf_361c41f3-a34` · 소요 30분 · 서브에이전트 토큰 1.73M · 도구호출 474회.
> 비용은 Claude 구독(외부 API 미사용).

**이 리포트를 반영한 결과는 [[app-release-plan]] 에 있다. 여기는 원본 근거 보존용이다.**

---

# 앱 출시 문서 리뷰 — 검증된 지적 종합

두 문서(`docs/architecture/app-release-plan.md` 468줄 · `docs/architecture/android-launch-checklist.md` 114줄) 전문을 읽고, 6개 렌즈의 발견 41건을 중복 병합해 22건으로 정리했다. 문서는 수정하지 않았다.

**총평**: 결정 자체(Capacitor A안 · 배포방식 B · 드라이브 미채택 · 이벤트 동기화 원칙)는 대부분 살아남는다. 무너지는 것은 **결정을 떠받친 숫자들**과 **Phase 의존 관계**, 그리고 **계획에 통째로 빠진 항목 4개**(백업 · Play 테스트 게이트 · 유료 약관 · 심사용 계정)다.

---

## HIGH — 출시를 막거나 돈·데이터를 잃는다

### H1. 프로덕션 DB에 백업이 없다 (계획에도 없다)

- **무엇**: 유료 구독자의 진도·필기·대화가 도커 볼륨 하나에만 있다.
- **근거**: `grep -c 백업 docs/architecture/app-release-plan.md` → 0. DB는 `deploy/docker-compose.yml:12-30` 의 `postgres:16` + 이름있는 볼륨 `ms_pgdata` 단일. crontab의 백업 크론 2건은 `/home/insung/projects/scripts/ops/run_db_backup.sh:19` 에서 `-d legal_brain_db` 로 고정 — mathstudy 매치 0건. 필기 본문도 아직 DB 안이다(`db/migrations/0006_handwriting.sql:7` doc JSONB).
- **수정 문구**: Phase 5 행 내용에 추가 — `pg_dump -Fc 야간 크론 + 원격 1부(R2 또는 tme-laptop) + 30일 로테이션 + 월 1회 복구 리허설`. 통과 조건에 추가 — `빈 DB에 덤프를 복원해 로그인·필기 로드가 되는 것을 확인`. 그리고 한 줄 못박기: `사용자 데이터가 DB와 R2 로 쪼개지므로 백업은 두 곳을 같은 시점으로 묶는다 - 한쪽만 복구하면 참조 깨진 반쪽 데이터가 된다.`

### H2. Google Play 「12명 × 14일 비공개 테스트」 게이트가 두 문서 어디에도 없다

- **무엇**: 개인 개발자 계정(2023-11-13 이후 생성)은 최소 12명이 **연속 14일** 옵트인한 **비공개** 테스트를 마쳐야 프로덕션 액세스를 신청할 수 있다. 내부 테스트는 인정되지 않는다.
- **근거**: <https://support.google.com/googleplay/android-developer/answer/14151465> (조직 계정은 면제). 문서 측: `android-launch-checklist.md:86-88` 은 내부 테스트 트랙만 다루고, `app-release-plan.md:401` 은 "내부테스트 → 비공개테스트 → 프로덕션" 단계만 나열한다.
- **왜 심각한가**: 코드로 못 푸는 2주+ 리드타임이고, 실계정 12명 모집은 1인 개발자에게 가장 늦게 발견하면 가장 비싼 항목이다. 문서 스스로 `:415` 에서 "업로드 실패는 가장 늦게 드러나는 실패"라고 쓴 것과 정확히 같은 부류다.
- **수정 문구**: 체크리스트 「우리가 따로 해야 하는 것」에 항목 신설 — `⑥ 프로덕션 진입 게이트: 개인 계정이면 12명 × 연속 14일 비공개 테스트 필수(내부 테스트 불인정, 조직 계정은 면제). 계정 종류부터 Play Console 에서 확인한다.` Phase 2 내용란에 `빈 껍데기 업로드 시 비공개 테스트 트랙 개설 + 테스터 12명 모집 동시 착수`, Phase 8 통과 조건에 `비공개 테스트 14일 완주 + 프로덕션 액세스 승인`.

### H3. 임계 경로가 틀렸다 — Phase 5는 Phase 3에 종속이고, CSRF/CORS 공사가 계획에 0회 등장한다

세 렌즈에서 각각 나온 같은 뿌리다(ord-2 · ord-11 · miss-5).

- **무엇**: 현재 CSRF 방어가 "동일 출처" 검사인데, Phase 5(SPA=Pages / API=Tunnel→tme)도 Phase 6(Capacitor WebView)도 태생적으로 크로스오리진이다. 지금 계획대로면 프런트를 쪼개는 순간 로그인부터 모든 쓰기 요청이 403 이 된다.
- **근거**: `web/src/lib/auth.ts:107` `sameSite:'lax'` · `auth.ts:124-141` `isSameOrigin()` 이 Origin 의 host 와 Host 를 문자열 비교하고 둘 다 없으면 거부 · `web/src/middleware.ts:83-88` 이 모든 POST/PUT/PATCH/DELETE 에 이 검사를 강제. `web/src/pages/api/account/delete.ts:7-8` 은 주석으로 "CSRF 는 미들웨어가 동일출처를 검증하므로 별도 토큰 불필요"라고 이 검사에 명시 의존한다. Capacitor 앱 오리진은 `capacitor://localhost` 라 영영 불일치. 문서 측: `for w in CSRF CORS 동일출처 Origin; do grep -c "$w" app-release-plan.md; done` → 전부 0.
- **수정 문구**:
  - `:136` 옆에 한 줄 추가 — `동일출처 CSRF 검사 폐기 → Authorization 베어러 토큰 + CORS 허용 오리진 화이트리스트(웹 도메인 · capacitor://localhost · https://localhost). middleware.ts:83-88 과 auth.ts:124 를 함께 손본다.`
  - `:405` 임계 경로를 `Phase 3(SSR 제거·최대 공사) → Phase 5(인프라) → 6(앱 셸) → 7(결제) → 8(심사)` 로, `:407` 을 `Phase 0·2·4 는 병렬 가능. Phase 5 는 Phase 3 의 토큰 전환이 선행되어야 한다(Pages 가 배포할 SPA 자체가 Phase 3 산출물이고, 호스트 분리가 동일출처 검사를 깨뜨린다).`
  - Phase 5 통과 조건에 `웹 SPA(Pages 도메인)가 tme API 를 크로스오리진으로 호출해 로그인·필기저장·탈퇴가 된다`, Phase 6 통과 조건에 `앱 origin(capacitor://localhost)에서 /api/chat · /api/handwriting POST 가 403 없이 통과`.

### H4. 토큰 전환이 기출 이미지 유료 게이팅을 조용히 뚫는다

- **무엇**: `/problem-images/` 는 지금 세션 쿠키로 게이팅되고 있는데, 소비처는 전부 평범한 `<img src>` 라 Authorization 헤더를 실을 수 없다. Phase 3 에서 쿠키를 걷으면 무인증 스크래핑이 열리고, 동시에 이미지 표시 자체가 깨진다.
- **근거**: `web/src/middleware.ts:53-56` 주석 "★기출 원본 이미지는 자산이지만 인증 뒤로 게이팅(무인증 스크래핑 차단·유료화 전제)" — 자산 판정보다 먼저 인증 경로로 보낸다. 소비처: `web/src/pages/problems/[...slug].astro:59` · `:201`(InkCanvas bgImage) · `web/src/lib/problem-card.ts:47` · `web/src/pages/exam/round/[...key].astro:41` · `web/src/pages/exam/random.astro:36`.
- **수정 문구**: Phase 3 내용란에 선행 조건 추가 — `토큰 전환 시 /problem-images/ 게이팅(middleware.ts:53-56)이 함께 무력화된다. 서명 URL(Phase 5 Workers) 또는 짧은 수명 쿠키 병행 중 하나가 같은 릴리스에 들어가야 한다.` 통과 조건 "기존 기능 회귀 0" 을 구체화 — `미로그인 상태에서 /problem-images 직접 요청이 여전히 차단됨`.

### H5. Phase 4 의 대전제가 코드와 어긋난다 — 재계산은 충돌 해소가 아니라 데이터 삭제가 된다

- **무엇**: `:226-228` 은 "mastery · problem_state 는 파생 상태이므로 서버가 problem_attempts 로 재계산하면 충돌 해소가 불필요"라고 못박았다. 그런데 두 테이블 모두 attempts 에 없는 독립 입력을 갖고 있다.
- **근거**: `web/src/pages/api/problem-state.ts:67-80` 의 `action='reset'`(행 DELETE) · `'mark-mastered'` · `'skip'` 이 problem_attempts 행을 만들지 않고 직접 UPSERT/DELETE 한다. mastery_evidence 는 `web/src/pages/api/mastery-promote.ts:43` 의 튜터 판단 텍스트(`chat-judgment @ ...`)와 `web/src/lib/user-claim.ts:17-42` 의 가입 시 frontmatter 시드에서만 온다. 즉 attempts 를 리플레이하면 reset 으로 지운 상태가 되살아나고 mark-mastered · skip · evidence 는 전부 사라진다 — Phase 4 통과 조건 "소실 0" 위반.
- **수정 문구**: `:226-228` 을 `problem_attempts 는 이벤트 정본이지만, mastery · problem_state 에는 attempts 로 환원되지 않는 사용자 명시 조작(reset · mark-mastered · skip)과 튜터 판단 evidence 가 있다. 이 조작들도 먼저 이벤트화한 뒤에야 재계산이 성립한다.` Phase 4 내용란에 선행 작업 — `problem-state.ts · mastery-promote.ts 의 직접 UPSERT/DELETE 3종을 이벤트 append 로 전환`. 통과 조건에 `기존 mastery_evidence · mark-mastered · skip 이 재계산 후에도 보존됨`.

### H6. 콘텐츠 규모 표가 통째로 틀렸다 — 이미지는 2.5배 과소, 텍스트는 최대 6배 과대

네 렌즈가 독립적으로 같은 결론에 도달했다(fact-1 · cons-1 · assume-8 · cost-4).

- **무엇**: `160MB (5,728장)` 은 `du` 가 심링크를 0바이트로 센 값이다. 5,728장 중 4,164장이 `../../../db/raw/<회차>/images/*.png` 심링크다. 반대로 텍스트 행들은 `du -sh` 의 블록 오버헤드(소파일 다수)로 부풀려져 있다.
- **근거(재현)**:
  ```
  $ cd web/public/problem-images && du -sh . && du -shL .
  160M / 404M
  $ find . -type l | wc -l → 4164   (실파일 1731)
  $ ls -d db/raw/*/ | wc -l → 116
  $ du -sh / du -sb / gzip -9:
    docs/problems  19M → 12.9MB → gzip 2.4MB
    db/solutions   17M →  2.5MB → gzip 1.0MB
    docs/concepts  6.8M →  3.9MB → gzip 0.9MB
  ```
  WebP 무손실 33.9% 는 독립 재측정에서 확인됨(무작위 40장 33.8-35.8%). 404MB × 0.339 ≈ **137MB**.
- **내부 모순도 같이 있다**: `:337` 총 54MB ÷ 116회차 = 0.47MB 인데 `:344` 는 "회차당 약 0.9MB" 라고 적혀 있다.
- **수정 문구**:
  - `:51` → `문제 이미지 | 약 404MB (5,728장) ※du -shL 기준. du -sh 가 160MB 로 보이는 것은 4,164장이 db/raw 심링크이기 때문`
  - `:48` 제목 → `콘텐츠 규모 - 약 425MB`, 텍스트 행은 실제 바이트로(문제 md 12.9MB · 풀이 2.5MB · 개념 3.9MB)
  - `:333` 제목 → `전체 콘텐츠: 약 425MB → 약 145MB`, `:336` → `404MB → 약 137MB`
  - `:344` → `116개 회차 · WebP 후 회차당 평균 약 1.2MB`
  - 측정 명령을 각주로 박을 것 — 이 레포 구조에서 `du -sh` 로 잰 수치는 재현 즉시 틀린다.
  - **결론 영향**: `:57` "전량 번들은 비현실적" 은 오히려 강화된다. 다만 R2 무료 저장 10GB 대비 여유 판단(`:367`)과 초기 다운로드 산정은 다시 해야 한다.

### H7. 「첫 실행부터 오프라인 완전 동작」이 「이미지는 회차 단위 다운로드」와 모순이다 — 4.2 방어 논거가 조건부가 된다

- **무엇**: `:343` 은 텍스트 번들만으로 첫 실행부터 오프라인 완전 동작이라 하고, `:169` 표는 문제 열람을 무조건 "가능"으로 적었다. 그런데 문제 화면의 본체가 이미지이고, 그 이미지는 `:344` 에서 회차 단위 다운로드 + `:355` 구독 확인 후 서명 URL 이다.
- **근거**: `web/src/pages/problems/[...slug].astro:32,59` 가 `/problem-images/<stem>` 원본 이미지를 본문으로 렌더하고 `:201` InkCanvas `bgImage` 도 같은 이미지다. `web/src/pages/exam/round/[...key].astro:41` 회차 목록 카드도 이미지. 즉 회차를 안 받은 상태에서는 열람도 필기 배경도 성립하지 않는다.
- **왜 심각한가**: `:175` 가 "지하철에서 데이터 없이 기출 풀고 손풀이" 를 4.2 방어 논거로 삼는데, 심사자가 설치 직후 비행기모드로 켜면 빈 화면을 본다.
- **수정 문구**: `:169` 를 `개념·위젯 열람 = 가능 / 문제·풀이 열람 = 다운로드한 회차만 가능` 으로 분리. `:343` 뒤에 한 줄 추가 — `최근 1-2회차(WebP 약 2.4MB)는 앱에 프리번들한다. 설치 직후 · 로그인 전 · 비행기모드에서 기출 열람과 필기가 실제로 되는 상태가 4.2 심사 시연 경로다.` Phase 5 통과 조건에 `미다운로드 회차의 오프라인 빈 상태 UX` 추가.

### H8. 이용약관에 유료·결제·환불·청약철회 조항이 통째로 없다

- **무엇**: 월 15,000원 구독을 파는데 약관에 요금 조항이 0개다.
- **근거**: `grep -n '<h2>' web/src/pages/terms.astro` → 제1조 목적부터 제11조 준거법까지, 유료·결제·환불 조 없음. `grep -n '환불\|청약철회\|결제' terms.astro` → 각 0건. 반대로 `web/src/pages/privacy.astro:63-64` 는 이미 "대금결제 및 재화 등의 공급에 관한 기록: 5년" 을 전제한다.
- **수정 문구**: 「심사·법무 체크리스트」(`:155-162`)에 항목 추가 — `유료서비스 약관 신설 - 이용요금 · 결제수단(스토어 IAP) · 자동갱신 시점 · 청약철회(전자상거래법 제17조, 디지털콘텐츠 예외) · 환불 주체가 구글·애플이라는 점과 우리 창구 · 서비스 중단 시 잔여기간 처리 · 쿼터(월 3,000턴 · 일 200턴) 명시.` `:26` 이 연간 보류 사유로 든 "중단 시 환불 의무" 가 바로 이 조항으로 처리된다.

### H9. 심사자에게 줄 테스트 계정과 수동 구독 부여 수단이 없다

- **무엇**: 전량 유료 + 로그인 필수인데, 심사자가 페이월에서 멈추면 4.2 방어 논거(오프라인·펜)를 볼 기회조차 없이 반려된다. Play 는 로그인 게이팅 앱에 심사용 접근 정보 제공을 의무화한다.
- **근거**: `grep -c '테스트 계정\|심사용\|데모'` → 두 문서 모두 0. 로그인 필수 `:173`, 전량 유료 `:28`. 게다가 DB에 구독·등급 개념이 아예 없어 수동 부여도 불가 — `grep -rniE 'subscription|entitlement|billing|iap|tier' db/migrations/` 에서 매치는 문제 난이도 `killer_tier` 뿐이고, `db/migrations/0003_membership.sql:11-23` users 테이블에 tier 컬럼이 없다.
- **수정 문구**: Phase 7 통과 조건에 `관리자가 임의 계정에 구독 권한을 부여·회수할 수 있다(스토어 결제 없이)`. Phase 8 스토어 자산 목록에 `심사용 테스트 계정 ID/PW + 앱 접근 방법 메모`. 설계 힌트 한 줄 — `구독 미러 테이블에 source 컬럼(store / manual)을 두면 심사 계정과 실제 결제를 섞지 않는다.`

### H10. LLM 단가 ₩0.37/턴은 실측의 1/3 이하다 — 쿼터 절의 결론 문장이 무너진다

네 렌즈가 각기 다른 경로로 같은 결론에 도달했다(assume-1 · cost-1 · fact-8 · assume-11). **주의: 렌즈들이 제시한 대체 수치도 서로 달라, 아래는 내가 실측으로 재수렴시킨 값이다.**

- **문서 내부 모순부터**: `:87` `LLM(평균 600턴) −₩222`(= ₩0.37/턴) vs `:101` `luna ₩330`(= ₩0.55/턴). 같은 대상인데 49% 어긋난다.
- **실측 근거**:
  - luna 단가 역산(`.llm-monitor/ab_results*.json` 전 행에 오차 0.03%로 적합): input $0.125/Mtok · cache_read $0.01/Mtok · output $0.60/Mtok.
  - 제품 경로 실계측 — `docker exec deploy-db-1 psql -U mathstudy -d mathstudy -c "select model,count(*),round(avg(input_tokens)),round(avg(cache_read_tokens)),round(avg(output_tokens)) from tutor_usage group by 1"` → `tutor | 9 | 13496 | 9767 | 99`. 이 값으로 계산하면 **₩0.86/턴**(₩1,380/USD).
  - 출력이 짧은 초기 턴이라 낙관적이다. 출력 300토큰 · 히스토리가 찬 성숙 대화 기준 **₩1.0-1.6/턴**, 캐시 0%·긴 출력 최악 **약 ₩3/턴**.
- **정정값**: 600턴 = **₩520-1,000**(최악 약 ₩2,000) · 3,000턴 = **₩2,600-5,000**.
- **무너지는 문장**: `:187` "한도를 꽉 채워도 원가는 수취액의 9.6%" → 실제 **22-43%**. `:101` "LLM 은 어느 규모에서도 2% 미만 · 원가 절감은 이미 끝났다" 도 근거를 다시 대야 한다. `:101` 의 "13배" 는 하네스에서 재현되지 않는다(캐시 적용 시 8배, 미적용 시 36배).
- **결론은 살아남는다**: 캡 소진 · 최악 단가에서도 학생 1명당 `11,591 − 5,000 − 150 = 약 ₩6,400` 흑자다. 마진이 규모와 무관하다는 판단도 유지된다.
- **수정 문구**: `:87` → `LLM (평균 600턴) | −₩520 ~ −₩1,000`, `:88` 남는 돈 → `약 ₩10,400 ~ ₩10,900 (70-73%)`, `:90` → `한도를 꽉 채우면(3,000턴 = ₩2,600 ~ ₩5,000) 남는 돈 ₩6,400 ~ ₩8,800 · 55-76%`, `:187` → `한도를 꽉 채워도 원가는 수취액의 22-43% - 쿼터가 없으면 이 구간이 열린다`. 표 아래 각주 필수 — `※ 턴 단가 산출식 = (1−캐시적중)×시스템프롬프트토큰×$0.125/Mtok + 캐시적중×동토큰×$0.01/Mtok + 히스토리토큰×$0.125/Mtok + 출력토큰×$0.60/Mtok. 단가 출처 .llm-monitor/ab_results*.json 역산, 프롬프트 구성은 tutor_usage 실측, 환율 ₩1,380/USD. 캐시적중률을 명시하지 않으면 이 숫자는 다시 검증 불가능해진다.`

### H11. 스토어 수수료 행이 두 군데 틀렸다 — 안 해도 되는 일을 하게 하고, 실재하는 레버를 닫아버린다

- **무엇**: (a) "소규모 사업자 프로그램" 은 애플 용어다. Google Play 구독은 2022-01부터 **등록 여부·매출 규모와 무관하게 15%** 다. Android 우선 출시 계획에서 "등록" 은 15%의 조건이 아니다. (b) 반대로 **Apple 은 SBP 신청·승인이 필요**하고, 미등록이면 구독 첫 12개월 30%다. (c) `:102` "15%가 이미 최선" 은 사실이 아니다 — 한국은 **2026-12-31부터** 서비스 수수료 10% + Play 결제 사용 시에만 결제수수료 5% 구조로 바뀐다.
- **근거**: <https://support.google.com/googleplay/android-developer/answer/112622> · <https://developer.apple.com/app-store/small-business-program/> · <https://android-developers.googleblog.com/2026/06/play-expanded-billing.html> · 전자신문 <https://www.etnews.com/20260306000070>
- **왜 지금 중요한가**: 이 문서는 `:387-389` 에서 "날짜 없이 관문으로만" 이라고 못박았다. 실제 출시가 2026-12-31 을 넘길 가능성이 높고, 그 시점에 결제 경로 선택이 5%p 레버가 된다(학생 1명당 월 약 ₩680, 1,000명이면 월 약 ₩68만).
- **수정 문구**: `:27` → `| 스토어 수수료 | **15%** — Google Play 구독은 규모·등록 무관 15%(별도 등록 절차 없음) / Apple 은 Small Business Program 신청 필수(승인 회계월 종료 +15일 발효, 미등록 시 1년차 30%) |`. `:102` → `수수료는 닫힌 문제가 아니다 - 한국은 2026-12-31부터 서비스 10% + Play 결제 시 5% 구조로 전환. 대체결제·외부 웹링크를 쓰면 5%p 를 더 아낀다. Phase 7 착수 시 재확인.` 그리고 체크리스트에 `iOS 상품 등록 전 SBP 신청` 을 추가할 것.

---

## MEDIUM — 나중에 크게 비싸진다

### M1. 튜터 첨부 이미지 진단 ①의 수치가 약 10배 틀렸고, 처방 ②의 근거가 무효다

- **근거**: 클라이언트는 이미 표시용 512px 다운스케일본만 저장한다 — `web/src/lib/image-utils.ts:12` `const DISPLAY_LONG_EDGE = 512;`, 비전 타일은 저장 전 제거 `web/src/lib/chat/persistence.ts:51`. DB 실측: 저장 이미지 1장당 53-66KB, 최대 blob 은 468×512 RGBA PNG 63,262 B. 상한은 `web/src/pages/api/chat-history.ts:39` 의 2MB → 도달에 약 30장 필요. 문제 ②("이미지가 다음 턴에 사라진다")는 코드로 확인됨 — `web/src/pages/api/chat.ts:87-97` 이 `m.content` 만 넘기고 `:318` 이 `lastUser.images` 만 읽는다.
- **수정 문구**: `:290` "data URL 통째로" → `표시용 512px 다운스케일 PNG(1장 약 53-66KB)가 base64 로`. `:292` "사진 3-4장이면 413" → `약 30장이면 2MB 상한(chat-history.ts:39)에 걸린다 - 급한 불은 아니고, 스토리지 분리의 진짜 이유는 대화 1건이 568KB 라는 jsonb 비대화다`. `:304` 결정 2 는 "2-8MB → 150-300KB" 근거가 무효(원본은 애초에 DB에 안 들어간다)이므로, **1,600px 로 올릴지 512px 를 유지할지를 판독 충실도 vs 저장량으로 다시 결정**하고 근거를 적을 것.

### M2. 필기 gzip 2.3KB 가 재현되지 않는다 (약 19배 낙관) + 568KB 비교 문장이 약 700배 어긋난다

- **근거**: DB의 실제 InkCanvas 문서(10획 · 363점)를 문서가 명시한 최적화(`[x,y]` · 소수 2자리)로 변환해 gzip 하면 **6.12 B/점** — 120획 × 60점 = 7,200점이면 약 **43-45KB** 다. 코드도 필기를 큰 데이터로 취급한다: `web/src/pages/api/handwriting.ts:10` `const MAX_BYTES = 4_000_000;   // 4MB cap (필기는 스트로크 점 배열이라 큼)`. 별건으로 `:291` "학생 1,000명 필기 전체(0.4GB)보다 대화 하나(568KB)가 무겁다" 는 자기 표(`:274`)와 700배 어긋난다.
- **수정 문구**: `:271` → `문서당 약 45KB`, 표는 `학생 1,000명 × 문제 200개 = 9GB · 학생 10,000명 × 문제 500개 = 225GB(약 월 ₩4,600)`. **드라이브 미채택 결론은 그대로 유효**(여전히 월 몇 천 원). 다만 `:367` "우리는 한참 안쪽" → `콘텐츠는 여유. 필기는 학생 1,000명부터 R2 무료 저장 10GB 를 넘어선다(그래도 월 ₩수천)`. `:291` → `대화 하나(568KB)가 필기 문서 하나(gzip 약 45KB)의 약 12배`.

### M3. "SSR 제거 = 45개 페이지" 는 실제 이전 대상을 약 80% 부풀린 숫자다

- **근거**: `find web/src/pages -name '*.astro' | wc -l` → 45, 그중 `find web/src/pages/dev -name '*.astro' | wc -l` → 20 (concept-figures · corrector-gallery · shape-gallery 등). 이들은 `web/src/middleware.ts:43-48` ADMIN_PATHS 의 `/^\/dev(\/|$)/` 로 관리자 전용이라 앱에 안 실린다. 사용자 대면은 25개, 그중 login/signup/terms/privacy 4개는 사실상 정적. (API 23개는 정확)
- **수정 문구**: `:133` 과 `:447` 의 "45개" → `사용자 대면 25개(전체 45개 중 /dev 관리자 도구 20개는 SSR 유지 · 앱 미포함)`. `:60` 은 "재작성하면 버리는 자산" 맥락이라 45가 맞으니 그대로. 단 /dev 를 SSR 로 남기면 `:370` "tme 는 API 만" 과 충돌하므로 존치 여부를 Phase 3 내용란에서 결정할 것.

### M4. 마크다운 렌더 파이프라인 이전이 공사 목록에 없다 — 링크 재작성은 원리적으로 브라우저에서 못 돈다

- **근거**: `web/astro.config.mjs:210-213` `remarkPlugins: [remarkMath, remarkKatexCompat, remarkRewritePaths, remarkStripSolutionPlaceholder], rehypePlugins: [[rehypeKatex, katexOptions]]`. 이 중 `remarkRewritePaths` 는 `astro.config.mjs:22-49` 의 CONCEPT_LEAF_MAP 에 의존하고, 그 맵은 `readdirSync` 로 `../docs/concepts` 전체를 훑어 만든다(`:36`). 클라이언트에 있는 것은 튜터 답변용 경량 렌더러(`web/src/lib/chat/markdown.ts`)뿐이다. getCollection/getEntry 로 서버 렌더 중인 콘텐츠 소비 페이지가 12개다.
- **수정 문구**: `:133-136` 공사 목록에 다섯 번째 항목 추가 — `마크다운 렌더 파이프라인 이전 - remark 4종 + rehype-katex 를 클라이언트로 포팅하거나 빌드 시 HTML 로 선렌더해 번들한다(CONCEPT_LEAF_MAP 은 JSON 으로 함께 출하).` 아울러 `:343` "텍스트 약 10MB 번들" 이 md 인지 선렌더 HTML 인지 명시할 것 — gzip 실측은 md 기준 4.3MB(문제 2.4 + 풀이 1.0 + 개념 0.9)이고, 선렌더 HTML 이면 KaTeX 인라인 마크업 때문에 더 커진다.

### M5. Phase 5 통과 조건 "비구독자 다운로드 차단" 은 Phase 7 전에 검증 불가능하다

- **근거**: `db/migrations/` 6개 전체(0001-0006)에 subscription/entitlement/billing/iap 매치 0건. 구독 상태 테이블이 아예 없으니 Worker 가 구독을 확인할 대상 자체가 없다. 게다가 `:213` 이 권한 상태를 우리 DB에 미러링한다고 정한 이상 `:369` "tme 를 거치지 않으니 서버 부하 0" 도 무조건 성립하지는 않는다.
- **수정 문구**: Phase 5 통과 조건 → `미인증 사용자 다운로드 차단(서명 URL 발급에 유효 세션/토큰 필요)`, "비구독자 차단" 은 Phase 7 통과 조건으로 이동. `:369` → `구독 확인 → R2 서명 URL 발급. tme 가 발급한 단수명 JWT 를 Worker 가 서명만 검증하면(DB 조회 없음) 서버 부하 0`. 그 JWT 발급 엔드포인트를 Phase 3 토큰 작업에 포함시킬 것.

### M6. 필기 병합 모델이 실제 저장 포맷과 맞지 않는다 — Phase 4 "소실 0" 을 못 맞춘다

- **근거**: `web/src/components/InkCanvas.tsx:10` `type Stroke = { tool; color; width; dashed; pressure; pts }` — **id 필드 없음**. `:145` 저장 포맷은 `{ v: 2, layers, strokes, activeId }` 이고 strokes 는 `Record<layerId, Stroke[]>`(`:143-144`) — 문서 모델(`:247`)에 **레이어가 통째로 빠져 있다**. 편집 연산은 전부 배열 인덱스 기반(undo `:13-16` · 선택 드래그 `:81`/`:314` · 선택 계산 `:346`). 결정적으로 `:207` `if (localStorage.getItem(KEY)) return;` — 로컬에 뭐라도 있으면 서버 pull 을 통째로 건너뛰고, 저장은 `:143-153` 문서 통째 POST(last-writer-wins)라 **두 기기 시나리오에서 지금도 덮어쓰기가 난다**.
- **수정 문구**: `:247` 모델을 레이어까지 확장 — `문서 = { v:3, layers:[{id, name, visible, deleted?}], strokes: {layerId:[{id, ...}]}, deletedStrokes:[id] }`, 레이어 tombstone 포함, 레이어 간 stroke 이동(`InkCanvas.tsx:16` move)을 삭제+추가로 표현할지 명시. Phase 4 내용란에 선행 작업 두 줄 — `InkCanvas 의 인덱스 기반 undo/선택/mutate 를 id 기반으로 전환(v2→v3 마이그레이션 포함)` · `InkCanvas.tsx:207 의 로컬 우선 pull 스킵 제거 → seq 비교 후 병합`.

### M7. Phase 0 의 "WebP 전환" 한 줄이 감추는 작업량 + 이중 개명

- **근거**: `grep -rl '\.png' docs/problems | wc -l` → **4164 파일**, `grep -rho '\.png' docs/problems | wc -l` → **13819곳**. 코드 하드코딩: `web/src/lib/problem-card.ts:47` · `web/src/pages/exam/round/[...key].astro:41` · `web/src/pages/exam/random.astro:36`. 데이터: `web/src/data/figure-triage.json` 키가 전부 `/problem-images/*.png`. 게다가 `:348-351` Phase 5 에서 같은 파일을 내용주소 해시 이름으로 또 바꾼다.
- **수정 문구**: Phase 0 의 WebP 항목을 좁힐 것 — `본문·코드의 경로 문자열은 건드리지 않고, 서빙 계층에서 확장자를 해석하는 매핑(또는 Accept 기반 협상)으로 먼저 붙인다. 실제 파일명 확정은 Phase 5 의 매니페스트·내용주소 작업과 한 번에 한다.` 지금 개명하겠다면 작업 목록을 명시 — `docs/problems 4,164파일 13,819곳 일괄 치환 + problem-card.ts:47 · exam/round:41 · exam/random:36 · data/figure-triage.json 동시 수정 + 인제스트 파이프라인 산출 확장자 변경`.

### M8. 플러그인 최소집합이 구현된 Google 로그인을 빼고 미구현 카카오를 전제한다

- **근거**: `web/src/pages/api/auth/google/start.ts` · `callback.ts` 구현됨, `web/src/pages/login.astro:57-58` 이 `GOOGLE_OAUTH_CLIENT_ID` 설정 시 버튼 노출. 카카오 관련 코드는 레포에 0건. 반면 `:150` 최소집합 = "인앱결제 · 카카오 SDK · Apple 로그인 …", `:160` 은 14세 미만 분기를 카카오 `age_range` 에 매달아 놓았다.
- **수정 문구**: `:150` → `인앱결제 · **Google 로그인(구현됨)** · Apple 로그인 · 보안저장소 · 파일시스템 (카카오는 미구현 - 도입 시 신규 작업)`. `:160` → `Google OAuth 는 연령대를 주지 않으므로 가입 시 생년월일 입력으로 분기`. Phase 6 내용란에 추가 — `WebView 안 OAuth 리다이렉트 처리(커스텀 스킴 / Browser 플러그인) - api/auth/google/start.ts 의 쿠키+리다이렉트 흐름은 앱에서 그대로 안 돈다`. 참고로 Google OAuth 도 제3자 로그인이라 4.8 Sign in with Apple 요구를 동일하게 촉발한다.

### M9. 장애 알림 채널과 크래시 리포팅이 둘 다 없다

- **근거**: `web/scripts/run_tutor_healthcheck.sh:7` 이 스스로 "알림 채널은 추후 - 우선 기록부터" 라고 적었고 `:9` `LOG=/tmp/tutor_health.log` 가 유일 싱크(재부팅 시 소실). 실사고 기록은 `deploy/docker-compose.yml:52-54` — "2026-08-12 claudeAiOauth 블록이 사라져 튜터가 15시간 죽었고, /api/health 는 내내 200이라 아무도 몰랐다". 클라이언트 쪽 `grep -rn 'Sentry\|Crashlytics\|bugsnag' web/src web/package.json` → 0건. 계획 쪽 `grep -c '크래시\|모니터링'` → 0.
- **수정 문구**: Phase 5 통과 조건에 `헬스체크 3연속 실패 시 사장님 폰으로 알림이 실제로 도착한다`(텔레그램 봇 또는 이메일이면 충분). Phase 6 `:150` 플러그인 절에 크래시 리포터 채택 여부를 명시하고, 넣지 않는다면 `앱의 전역 에러 핸들러가 스택트레이스를 우리 API 로 POST` 경로 하나는 남길 것. 지금 계획대로면 "앱이 켜지자마자 죽는다" 를 스토어 별점으로 알게 된다.

### M10. 고객지원 창구가 코드에도 계획에도 없다

- **근거**: `grep -rln 'mailto:' web/src` → 0건. `grep -rln '고객센터\|문의하기' web/src` → `terms.astro` 하나뿐이고 그 내용이 `:129` "고객센터를 통하여 이용계약의 해지" — 존재하지 않는 창구로 안내한다. `web/src/pages/privacy.astro:148-149` 는 `개인정보 보호책임자: [성명] / [직책]` · `연락처: [이메일] / [전화번호]` 플레이스홀더 그대로다.
- **수정 문구**: Phase 8 스토어 자산 목록에 추가 — `지원 이메일 1개(개인 gmail 아닌 도메인 메일) + 앱 내 「문의하기」 진입점 + 개인정보 보호책임자 실명·연락처 기입`. Play 스토어 등록정보는 개발자 연락처 이메일을 공개 노출하므로 어차피 필요하다. `terms.astro:129` 의 "고객센터" 표현도 그 창구와 일치시킬 것.

---

## LOW — 개선 제안

### L1. Phase 표에 Phase 1 이 없다

`:392-401` 의 Phase 행 = 0, 2, 3, 4, 5, 6-전 관문, 6, 7, 8. `grep -n 'Phase 1' app-release-plan.md` → 매치 0. 임계 경로(`:405`)와 병렬 목록(`:407`)도 1을 언급하지 않아 삭제인지 오타인지 판별 불가.
→ **수정**: 0-7 로 재번호하거나, 표 아래 각주 한 줄 — `Phase 1(구 콘텐츠 최적화)은 Phase 0·5 로 흡수됨.` 번호는 이후 커밋·이슈에서 계속 인용되므로 지금 정리하는 편이 싸다.

### L2. `minSdk 24 — Android 5.x 가 빠진다` (checklist:40)

API 24 = Android 7.0 이라 6.0/6.0.1(API 23)도 함께 빠진다(<https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels>).
→ **수정**: 제목을 `minSdk 24 - Android 6.x 이하(API 23 이하)가 빠진다` 로. 결론(점유율 극소, 실질 영향 없음)은 그대로. 참고로 Capacitor 8 기본값(minSdk 24 · compileSdk 36 · AGP 8.13.0 · Gradle 8.14.3 · Java 21)은 <https://capacitorjs.com/docs/updating/8-0> 로 전부 확인됨.

### L3. 「targetSdk 36 확정」이 이 문서의 대원칙과 충돌한다

`checklist:22-24` 는 "2026-08-31~ API 36" 다음 행 없이 "우리는 그 이후에 낸다 → 36 확정" 으로 끝난다. 그런데 `app-release-plan.md:387-389` 는 "날짜를 박으면 관문을 건너뛴다" 며 날짜를 안 박겠다고 못박았다. 구글은 매년 8월 31일에 한 단계 올린다 — 2027-08-31 이후 제출이면 API 37 이다. 하필 문서 스스로 "가장 늦게 드러나는 실패" 라고 적은 자리다.
→ **수정**: 표에 `2027-08-31~ | API 37 (매년 +1)` 행 추가. "36 확정" → `착수 시점 기준 36 - 제출이 2027-08-31 을 넘기면 37 로 재확인(연 1회 갱신 규칙)`. 문서 frontmatter 에 `review_by:` 필드를 두고 만료성 서술을 한 절에 모을 것. 같은 부류: `app-release-plan.md:313-315` 의 90일 예외 건은 `2026-09-27 까지 스토리지 미구축 시 자동 삭제 대상 - 그 전에 백업` 으로 날짜를 명시.

### L4. 손익분기 고정비에 개발자 계정 연회비가 빠져 있다

`:104-110` 인프라 표 합계는 ₩32k-92k 인데 `:100` 은 중간값 ₩50k 만 쓴다. iOS 출시를 전제하면서 Apple Developer Program $99/년(약 ₩11.4k/월, 쓴 고정비의 23%)이 어디에도 없다. Google Play 등록비 $25(1회)도 마찬가지.
→ **수정**: 인프라 표에 `개발자 계정 · 사업자 고정비 | ₩12-15k | Apple $99/년 · Play $25 1회 · 통신판매업 등록면허세` 행 추가. `:100` → `손익분기 = 학생 6명(고정비 월 약 ₩62k, LLM 실측 단가 기준)`. 아울러 `:86` 구독관리 1% 는 초과분이 아니라 MTR **전액**에 붙으므로 비고를 `월매출 약 ₩3.4M 미만 무료. 넘으면 MTR 전액의 1% - 구독자 약 227명 구간에서 월 약 ₩34k 계단` 으로 보완(규모표의 "마진율이 규모와 무관" 에 대한 유일한 예외다).

### L5. R2 무료 한도를 잘못 인용했고 Workers 비용 행이 없다

`:367` 은 "Class A 100만/월 — 우리는 한참 안쪽" 이라 적었는데, 콘텐츠 다운로드는 전부 **Class B(읽기)** 이고 그 무료 한도는 1,000만/월이다(<https://developers.cloudflare.com/r2/pricing/>). 실제로 바인딩되는 숫자를 인용하지 않았다. 그리고 `:369` Workers 는 인프라 표에 비용 행이 없다 — 이미지 1장당 서명 URL 을 발급하는 설계면 학생 1,000명 = 573만 호출/월로 무료 10만req/일을 넘는다.
→ **수정**: `:367` 괄호를 `(무료 한도: 저장 10GB · Class B 읽기 1,000만/월 · Class A 쓰기 100만/월)` 로. 인프라 표에 `Cloudflare Workers | ₩0-7k | 서명 URL 을 이미지 단위가 아니라 회차 단위로 발급하면 호출 수가 1/50` 과 `백업·모니터링 | ₩5-10k` 두 행 추가. **회차 단위 서명은 비용보다 설계 관점에서 더 중요하다** — Phase 5 통과 조건에 넣을 만하다.

---

## 지금 당장 고쳐야 할 것 3개

**1. DB 백업 크론을 오늘 만든다 (H1)**
문서 수정이 아니라 실행이다. 지금 mathstudy 프로덕션 DB의 유일 사본은 `ms_pgdata` 볼륨 하나이고, 돌고 있는 백업 크론 2건은 포렌식 DB 전용이다(`run_db_backup.sh:19`). 필기 본문까지 아직 DB 안에 있다. 유료 구독자를 받기 전이 아니라 **오늘** 이 상태를 끝내야 한다. 30분짜리 작업이고, 안 하면 되돌릴 수 없는 유일한 항목이다.

**2. Play Console 계정 종류를 확인하고, 12명 × 14일 게이트를 Phase 2로 끌어올린다 (H2)**
개인 계정이면 프로덕션 진입에 **실계정 12명 + 연속 14일** 이 하드 게이트다. 코드로 못 푸는 리드타임이라, Phase 8 에서 발견하면 그때부터 2주가 더 붙는다. 계정 확인은 5분이고, 조직 계정이면 이 리스크는 통째로 소멸한다. 개인 계정이면 Phase 2("빈 껍데기 조기 업로드")에 테스터 모집을 붙이는 것만으로 리드타임이 임계 경로 밖으로 나간다.

**3. 임계 경로를 정정한다 — Phase 5는 Phase 3 뒤, CSRF/CORS 공사를 Phase 3 에 명시 (H3)**
`:407` "Phase 0·2·4·5 는 병렬 가능" 이 지금 계획에서 가장 비싼 오류다. Phase 5 가 배포할 SPA 자체가 Phase 3 산출물이고, 호스트를 쪼개는 순간 `middleware.ts:83-88` 의 동일출처 검사가 모든 쓰기 요청을 403 으로 막는다. 문서에 CORS 는 0회 등장한다. 이 한 줄을 지금 고치면 문서 수정이고, 안 고치면 Phase 5 를 병렬로 착수했다가 되돌리는 일이 된다. H4(이미지 게이팅)와 M8(WebView OAuth 리다이렉트)도 같은 공사에 딸려 있으니 Phase 3 내용란에 한꺼번에 적어두는 편이 싸다.

---
## 🔗 지식망 연결
- **상위 분류**: [[00_REPORT]]
- 대상: [[app-release-plan]] · [[android-launch-checklist]]
