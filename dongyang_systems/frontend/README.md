# SIGenie Frontend Project

사전에 PC에 nodejs가 설치되어있어야 합니다.

nodejs 설치 - [nodejs.org/en/download](https://nodejs.org/en/download/prebuilt-installer)

## 프로젝트 실행

### 프로젝트 의존성 설치

```
npm install
```

#### \*\*\* 의존성을 추가할 경우

아래 두 가지 방법 중 하나 사용

1. 패키지 매니저로 추가

   ```
   npm install <의존성 이름>
   ```

2. 의존성 파일에 추가

   `package.json` 파일의 `"dependencies"` 속성 하위에 의존성을 추가한 뒤

   ```
   npm install
   ```

### 로컬 서버 구동 (개발 시)

```
npm start
```

-> 자동으로 `env/.env.development` 파일 로드

### 배포 서버 구동 (서비스를 위한 배포 시)

```
npm run build
```

-> 자동으로 `env/.env.production` 파일 로드
