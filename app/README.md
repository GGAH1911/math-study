# math-study 앱 셸 (Capacitor / Android)

Phase 2 — **"기능 0 인 앱이 업로드·구동되는가"** 를 앱을 만들기 **전에** 확인하는 껍데기다.

> 로드맵이 이걸 일찍 하라고 못 박은 이유: *업로드 실패는 가장 늦게 드러나는 실패다.*
> 포렌식은 targetSdk 34 로 전부 만들어놓고 업로드에서 막혔다.

## 구조

```
app/
├── package.json            Capacitor 8 (web/ 과 분리 — CI 의 web npm ci 에 안 섞인다)
├── capacitor.config.json   appId kr.co.mathstudy · webDir www
├── www/index.html          기능 0 껍데기. Phase 3 에서 webDir 을 ../web/dist 로 돌린다
└── android/                npx cap add android 산출물
```

사양은 로드맵과 일치한다 — **AGP 8.13.0 · Gradle 8.14.3 · minSdk 24 · compile/target 36 · Java 21**.
(Capacitor 8 기본값이 이미 그렇다.)

## 빌드

```bash
cd app/android
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export ANDROID_HOME=/home/insung/android-sdk
echo "sdk.dir=$ANDROID_HOME" > local.properties   # gitignore

./gradlew assembleDebug     # 실기기 구동 확인 — 서명 불필요
./gradlew bundleRelease     # AAB — 서명 필요(아래)
```

## ★서명 키 — 사장님이 직접 만드셔야 합니다

**이 키는 앱의 정체성입니다.** 잃어버리면 같은 패키지명으로 업데이트를 **영구히** 낼 수 없고,
기존 설치자는 새 앱을 따로 깔아야 합니다. 그래서 비밀번호를 아는 사람이 사장님이어야 하고,
에이전트가 대신 만들지 않습니다.

```bash
cd app/android/app
keytool -genkeypair -v \
  -keystore release.keystore \
  -alias mathstudy \
  -keyalg RSA -keysize 4096 -validity 10000
```

물으면 비밀번호(store/key)와 이름·조직을 입력한다. 그다음 비밀번호를 파일에 적는다:

```bash
cat > app/android/keystore.properties <<'EOF'
storePassword=<입력한 store 비밀번호>
keyPassword=<입력한 key 비밀번호>
keyAlias=mathstudy
EOF
```

`keystore.properties` 와 `release.keystore` 는 **`.gitignore` 에 이미 등재**돼 있다.
백업은 레포 밖 안전한 곳에(비밀번호와 함께). 키를 잃는 것과 유출되는 것 **둘 다** 치명적이다.

### 서명이 없으면 어떻게 되나

`bundleRelease`·`assembleRelease` 같은 **릴리스 태스크를 요청했을 때만** 빌드가 멈춘다.

```
안드로이드 릴리스 서명 정보가 없습니다.
  app/android/keystore.properties 에 … 넣고 app/android/app/release.keystore 를 두거나,
  MS_ANDROID_* 환경변수를 지정하세요.
```

★`signingConfigs` 블록 안에서 던지면 **어떤 태스크를 돌리든 configuration 단계에서 평가**되어
디버그 빌드까지 막힌다(실측: `assembleDebug` 실패). 그래서 값이 있을 때만 서명을 구성하고
`gradle.taskGraph.whenReady` 에서 판정한다 — *조용히 서명 없는 산출물을 내지 않는다* 는
원칙은 지키면서 실기기 구동 확인은 키 없이 가능하다.

## 남은 것 — 물리적 개입

| 단계 | 누가 |
|---|---|
| 서명 키 생성 | **사장님** (비밀번호 소유) |
| AAB 빌드 | 에이전트 가능 (키가 있으면) |
| **Play Console 내부 테스트 업로드** | **사장님** (계정 로그인) |
| 실기기 설치·구동 | **사장님** (물리 단말) |

내부 테스트 트랙은 **공개 스토어 페이지를 만들지 않으므로**(포렌식 실측) 지금 올려도 부담이 없다.

## Phase 3 이 오면

`capacitor.config.json` 의 `webDir` 을 `../web/dist` 로 바꾸고 `www/` 를 지운다.
그 전까지 이 껍데기는 **업로드 경로가 살아 있는지**만 증명한다.
