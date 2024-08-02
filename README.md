# 백엔드 개발 프로젝트
- Flask와 MySQL을 사용한 미니 SNS 서비스 개발
   - <깔끔한 파이썬 탄탄한 백엔드> 참고

## 1. 서비스 개요
- 회원가입, 로그인, 텍스트 전송, 좋아요, 팔로우, 타임라인, 프로필 사진 전송 기능을 갖춘 미니 sns 서비스

## 2. 서비스 구조
- Flask 프레임워크를 사용한 REST API 기반의 HTTP 요청, 응답 방식의 서비스 구현
- 레이어드 아키텍쳐 방식으로 view, service, model 레이어를 구분하고 각각 엔드포인트, 서비스의 로직, 데이터 베이스를 실행하도록 설계
- SNS 서비스의 특성상 테이블 간의 관계성이 중요하므로 RDBMS 방식의 MySQL을 사용
- AWS의 RDS와 S3에 각각 텍스트 데이터와 이미지 데이터를 저장하고 EC2 가상서버를 사용하여 서비스 배 

## 3. 디렉토리 구조
<img src="./images/dir_structure.png">

## 4. 소스코드 설명

### 1) 실행 로직
- setup 파일에서 AWS의 EC2 가상서버에서 api를 실행하기 위해 Twisted 모듈을 사용하여 app 객체를 연결
- config 파일에서 DB 접속 정보를 연결, app 파일에서 view, service, model 레이어를 연결
- view 파일에 각 엔드포인트 구현, service 파일에서 엔드포인트에서 요청에 대한 로직 실행, model 파일에서 DB 처리 요청에 응답

### 2) 엔드포인트
- ping, login, follow, unfllow, tweet, like tweet, timeline, profile image save, profile image download 엔드포인트를 생성하여 서비스의 기능을 구현

### 3) 로그인 인증
- bcrypt 패키지를 사용하여 로그인 비밀번호를 해쉬 암호화 하여 DB에 저장
- pyJWT 패키지를 사용하여 로그인 정보를 담은 json 데이터를 access token으로 변환 후 엔드포인트마다 access token을 인증하도록 데코레이터 함수 적용

### 4) 데이터 베이스
- SQLAlchemy를 사용하여 DB를 구축하고 MySQL을 사용하여 데이터 베이스 생성, 조회 
- users, tweets, like_tweet_list, user_follow_list 4개의 테이블을 생성하고 각 테이블을 user_id 컬럼을 외부키로 연결
- 이미지 데이터의 path를 DB에 저장할 때 werkzeug의 secure_filename 매서드를 사용하여 path에 로컬 시스템의 로직이 노출되지 않도록 보안이 강화된 path로 변환하여 사용

### 5) 데이터 관리
- message, like, follow, unfollow 데이터는 MySQL DB의 테이블에서 관리
- profile image 파일은 boto3 패키지를 사용하여 AWS의 S3 서버에서 관리

### 6) AWS 가상서버를 사용한 서비스 배포
- 클라우드에서 서비스를 배포하기 위하여 AWS의 EC2, ALB, RDS, S3, IAM 기능을 사용
- EC2 가상서버 2개를 생성하고 ALB 로드밸런서를 적용하여 라우팅 배분 및 HTTP 트래픽 자동 조정
- 텍스트 데이터의 저장을 위해 RDS DB를 생성하고 MySQL을 적용 후 EC2와 연결
- 이미지 데이터 관리를 위해 CDN(content delivery network) 서비스인 S3 서버를 생성하고 EC2와 연결
- 사용자 권한 관리 서비스인 IAM 적용하여 S3 서버에 공용접근 및 boto3 객체에서 접속 설정
- EC2 가상서버와 GitHub 레포지토리를 deploy key로 연결하여 소스코드 파일 다운로드
- 다운로드한 소스코드를 가상서버 환경에 맞도록 일부 수정 후 서비스 배포

#### AWS EC2
<img src="./images/aws_ec2.png">

#### AWS RDS
<img src="./images/aws_rds.png">

### 7) Unit Test
- pytest 모듈과 flask의 test_client() 함수를 사용하여 각 test 엔드포인트 별로 요청, 응답 일치 테스트
- test 시 DB에서 중복 데이터 오류가 발생하지 않도록 test 전후 자동으로 데이터를 생성하고 지울 수 있는 pytest의 setup_function(), teardown_function() 함수 사용
- S3 서버에 이미지 파일 전송 테스트시 저장공간, 비용 문제를 해결하기 위해 소스코드에서 mock 패키지를 사용하여 가짜 boto3 객체를 만들어 테스트 완료

## 5. 서비스 실행

### 1) ping 송수신 테스트
- ping curl을 보내면 "some some pong" 이라는 메시지를 응답한다.

<img src="./images/ping.png">

### 2) sign-up
- 회원가입을 하기 위해서 email, name, password, profile 을 입력해야한다. 
- 회원가입이 완료되면 입력한 정보를 json 형태로 반환한다.

<img src="./images/sign_up.png">

- DB에 저장 된 회원 정보 확인

<img src="./images/sign_up_db.png">

### 3) login
- 로그인을 하려면 email과 password를 입력하고 request 해야한다. 
- 입력한 회원 정보가 DB에 저장된 정보와 일치하는 지 확인후 일치하면 access_token을 생성하여 반환한다.

<img src="./images/login.png">

### 4) send message
- 로그인 후 tweet 메시지를 보내려면 tweet과 access_token 값을 함께 request에 보내야한다.

<img src="./images/tweet.png">

- access_token이 DB에 저장된 정보와 일치하면 tweet이 DB의 tweets 테이블에 저장 된다.

<img src="./images/tweet_db.png">

### 5) follow
- 다른 아이디를 가진 사용자를 flow 하는 기능으로, 로그인 된 상태에서 follow할 대상의 아이디 값을 reqeust에 보낸다. 이때도 acesse_token 값을 함께 입력한다.

<img src="./images/follow.png">

- acesse_token 값이 DB의 정보와 일치하면 follow가 성공하고, users_follow_list 테이블에 저장된다.

<img src="./images/follow_db.png">

### 6) timeline
- 사용자의 tweet과 follow한 사용자의 tweet을 볼 수 있는 타임라인 기능으로, request시 사용자의 모든 tweet을 반환한다.

<img src="./images/timeline.png">

### 7) profile img upload
- 사용자의 프로필 이미지를 업로드하기 위해 request를 보내면 AWS 클라우드의 저장소에 이미지 파일이 업로드 되고, 동시에 로컬 DB의 users 테이블에 이미지의 AWS url 값이 저장된다.

<img src="./images/profile_img_upload.png">

- DB

<img src="./images/profile_img_upload_db.png">

- AWS S3

<img src="./images/profile_img_upload_aws.png">

### 8) profile img download
- 프로필 이미지의 AWS 저장소 url을 다운로드 하면 원하는 디렉토리에 저장 할 수 있다. 

<img src="./images/profile_img_download.png">


# 전과정 정리 요약
- 미니 sns 서비스를 만드는 과정의 챕터별 핵심과 이슈들을 정리 요약

## 1. 백엔드 개발을 위한 지식 및 명령어들

### 1) 개발 가상환경 : 아나콘다 기준
- 아나콘다
- **파이썬 패키지 매니저 + 개발환경 매니저 기능이 들어 있음**
   - pip + venv의 기능
- venv는 python3에 포함되어 있는 가상환경 기능
- 콘다는 아나콘다의 툴
   - 아나콘다는 데이터 사이언스 용 패키지들이 들어있어서 용량이 큰 편
   - 간단하게 사용할 때는 miniconda를 사용해서 패키지 매니저 + 개발환경 매니저를 사용해도 됨
- 대부분의 개발은 가상환경에서 이루어진다.
   - 프로젝트 마다 사용하는 패키지의 버전이 다른 경우가 많기때문
- 우분투나 윈도우에서 아나콘다(또는 미니콘다)를 설치해서 사용
   - anaconda 또는 미니콘다 설치 스크립트 url 주소 복사 ===> wget <url 주소> ===> 다운로드 (.sh 파일) ===> 콘다가 설치될 디렉토리로 파일 이동 ===> 설치 (bash ./Miniconda~.sh) ===> 설치 완료 되면 conda list 로 설치 결과 확인
   - conda list : 아나콘다 패키지 리스트
   - conda --version : 아나콘다 설치 후 버전 확인
- git 설치
   - sudo apt update ===> sudo apt install giㅅ ===> git --version 확인
   - git은 코드의 버전관리 시스템
   - tig 설치 : git 커밋 히스토리를 터미널에서 보여주는 툴
      - sudo apt install tig
- 가상환경에서 패키지 목록 설치 관련
   - 가상환경에서 pip install -r req.text
      - pip freeze > req.text : 현재 pip 설치 내용을 텍스트로 저장
      - req.text를 한번에 설치 할 수 있다.
   - 한번에 지울 때
      - pip uninstall -r req.text -y
      - pip list 를 한번에 지우면 환경 구성 관련 패키지들도 지워져 conda가 실행이 안되므로 지우지 말것

### 2) 현재 연결 된 포트 확인
- lsof -i :<포트번호>
   - list open file 의 약자 : 리눅스는 VFS(virtual file system)을 사용하므로 일반 파일, 디렉토리, 네트워크 소켓, 라이브러리 등 모든 것을 파일로 처리하고 lsof에서 상세정보를 확인 할 수 있다.
   - 5000 번 포트를 사용중인 경우 PID 확인
   - -i 옵션 뒤에 포트번호 입력 하면 해당 포트를 실행 중인 파일의 정보들이 나옴
- kill -9 <PID 번호>
   - PID를 죽이면 해당 포트의 사용이 종료 된다. (PID는 process id의 약자)
   - kill -9는 실행중인 포트를 직접 종료하는 것이므로 여기에 실행 중인 자원이나 객체들이 제대로 정리되지 않은 채 종료 되지 않을 수 있음
   - kill -INT 또는 kill -TERM 을 사용해서 포트를 죽이는 방법 추천
- netstat 패키지를 사용하여 확인 할 수도 있다.
   - sudo apt install net-tools
   - apt를 사용하여 설치 한다.

### 3) 시스템, 환경 

#### 우분투 linux 메모리 정리
- sudo su : root 계정으로 전환 (pw 입력)
- echo 3 > /proc/sys/vm/drop_caches
   - caches 정리
- free -h : 메모리 사용 현황 GB로 요약
   - free -m : 메모리 사용 현황 MB로 요약
- top : 윈도우의 작업관리자 같은 summary : 실시간 메모리 사용 현황

#### 우분투 버전 확인
- cat /etc/issue

#### apt 업데이트
- sudo apt-get update
- sudo apt update

#### 파이썬 위치
- which python
- ls -lath 위치


### 4) 디렉토리, 파일 조회

#### 디렉토리 생성
- mkdir -p ~/project/api : -p는 중간 경로 디렉토리가 없으면 자동으로 생성하라는 뜻
- mkdir {view, service, model} : 현재 위치에서 {} 안의 디렉토리를 한번에 생성

#### grep 명령어
- OR :
   - pip list | grep -E "Tw|pl"
   - pip list | grep -e Tw -e pl
- AND :
   - cat filename | grep pattern1 | grep pattern2
   - cat filename | grep -E 'pattern1.*pattern2'

#### history 명령어
- history | grep ssh
- !40 : 40번째 명령어 실행

#### tree 명령어 (디렉토리의 구조를 격자로 보여줌)
- tree api -L 2 -I __pycache__
   - tree <디렉토리 이름>
   - -L : 조회할 하위 디렉토리의 계층 수
   - -I : 제외할 문자

#### pip show 패키지이름1 패키지이름2 패키지이름3 
- 패키지의 정보를 보여준다.
- 설치 날짜는 나오지 않는다.

#### vim 에서 특정 문자열 다음의 문자열을 모두 지우기
- :%s/<원하는 문자열 입력, 빈공간 가능>.* /<대체할 문자열, 빈공간 가능>/
   - 모든 행에서 email 다음의 모든 문자열을 한번에 지워준다.
   - <> 과 <> 다음에 오는 모든 문자열 선택 <>.*
   - <>... : .하나가 다음 문자열 1개를 선택해준다.
   - <>.* 을 // 이것을 replace 한다. 즉 비어있는 값으로 바꿔준다.
   - %s/file/apple/ ---> file을 apple로 replace 한다.
   - %s/file../apple/ ---> file 다음 .. 2개 문자열까지 선택한 후 apple로 replace 한다.
      - file@@@ 인경우 2번째 @까지 선택됨

## 2. 백엔드 개발의 히스토리

### 1) 코딩 에디터
- IDE : Integrated Development Environment
- 파이참, 비주얼 스튜디오 코드, vim, 서브라임 텍스트
   - vim 은 사용하기 어렵지만 개발 생산성에 많은 도움을 준다. IDE는 아니고 단순 에디터이지만 많은 플러그인이 개발되어 있어서 IDE 수준으로 사용할 수 있다.
  - openvim.com : vim 교육 사이트
   - vscode 사용 + vim 사용

### 2) CLI
- command-line interface : 명령줄 인터페이스
   - 백엔드 관련 개발은 CLI와 터미널 환경에 익숙해져야 함

### 3) 현대 웹 시스템 구조 및 아키텍처
- 왜 API(application programming interface, 어떤 서비스에 대한 프로그래밍 소스 코드 또는 서비스 그자체) 개발이 필요한지
- 백엔드 개발자들은 어떤 역할을 하는지, 그 기술이나 요구 능력
- 웹 시스템의 발전의 역사
   - 초기 : 웹 브라우저(web browser)가 웹 서버(web server)에서 받은 HTML을 랜더링하여 보여줌
      - 브라우저가 요청하면 서버에서 html 페이지를 보내줌
      - 정적 static 구조
      - 사용자 인터렉션의 중요성이 높아짐 user interaction : 웹 페이지에서 사용자와의 동적인 상호작용 중요, 단순히 정적인 형태의 데이터나 문서를 보여주는 것이 아님
      - 자바스크립트 : 웹 브라우저에서 실행이 가능한 프로그래밍 언어, 동적인 기능들을 제공하기 위함
      - 동일한 서버에서 HTML, 자바스크립트, 데이터 등을 웹 브라우저 등의 클라이언트로 xml 구조로 전송해줌
      - xml : 데이터를 전송하기 위한 markup 언어, html과 구조가 비슷함
   - 프로트엔드와 백엔드의 구분 시기
      - 동적 서비스의 중요성과 자바스크립트의 역할이 커짐
      - 자바스크립트가 html 파일에 속한 한 부분이었는데 자바스크립트가 html 생성부터 사이트의 모든 부분을 구현하는 언어가 됨, 부분적으로 동적인 기능들이 전체 페이지가 동적인 형태가 됨
      - SPA : Single Page Application 방식의 프론트엔드 개발 인기, 단일 페이지로 모든 웹사이트/웹서비스의 기능을 구현하는 것
      - 프론트엔드 서버와 백엔드 서버가 나뉘게 됨 : 프론트엔드 서버는 페이지 랜더링에 필요한 HTML, 자바스크립트 파일 전송 역할 담당, 백엔드 서버는 페이지에서 필요한 데이터 생성 과 전송을 담당하는 역할
      - 프론트엔드 개발자 : UI user interface, UX user Experience 구현
      - 백엔드 API 개발자 : 프론트엔드 시스템 또는 다른 클라이언트 시스템과 데이터를 실시간으로 주고 받을 수 있는 기능 구현 -> 많은 양의 동시요청을 장애 없이 실시간으로 최대한 빠른 속도로 처리할 수 있는 시스템 구현
      - 백엔드 개발 언어 : java, scala, rust, python, ruby, php, nodejs 등 안정적, 확장성, 실행속도
      - nodejs : 자바스크립트로 구현된 백엔드 시스템
   - `현대의 웹 시스템`
      - 웹 시스템 규모 커짐, 동시에 처리해야하는 요청수와 데이터 규모가 기하학적으로 급증
      - API : application programming interface 시스템이 방대해지고 복잡해짐
         - 응용프로그램과 응용체제간의 통신을 연결해준다.
         - 개발과 통합 작업에 필요한 프로토콜 세트
         - 컴퓨터나 컴퓨터 프로그램 사이의 연결
         - 프로그램과 프로그램 사이의 연결
         - 손님이 요리를 주문하면 요리사가 요리를 만들어 줄때, 손님과 요리사 사이에 점원의 역할과 같다.
         - 점원은 손님에게 메뉴를 알려주고, 손님은 요리를 요청하고, 점원이 이 요청을 다시 요리사에게 요청을 하고, 요리사는 요리를 점원에게 주고, 점원은 요리를 손님에게 전달해 준다.
         - API는 명령 목록을 정리하여 프로그램에 주고, 명령을 받으면 응용프로그램과 상호작용하여 요청 명령에 대한 값을 전달해준다.
         - 프로그램들이 서로 상호작용하는 것을 도와주는 매개체
      - `API의 역할`
         - 서버와 데이터베이스에 대한 출입구 역할 : 데이터 베이스에 접근할 수 있도록 서버의 접근성을 허가받은 사람에게만 부여한다.
         - 애플리케이션과 기기가 원활하게 통신할 수 있도록 함 : 스마트폰 어플이나 프로그램이 기기와 데이터를 원활하게 주고 받을 수 있도록 한다.
         - 모든 접속을 표준화 한다. : 모든 접속을 표준화하여 기계, 운영체제 등과 상관없이 동일한 액세스를 얻을 수 있다. 범용 플러그 처럼 작동.
      - 데이터의 양이 늘어남, ETL과 Data Pipeline 시스템이 발전
      - ETL : Extract, Transfer, Load
      - Hadoop 등 대용량 분석 프레임워크의 발달 => big data 분석 시스템을 위한 백엔드 시스템에 도입됨
      - 현대의 백엔드 개발자 : API 시스템 개발, Data Pipeline 시스템, Machine Learing 시스템, big data 분석 시스템의 비실시간 또는 대규모 데이터 수집 과 분석 시스템 + ML 시스템까지 넓어지고 있음
   - 백엔드 개발자 초기 : API 시스템 구현하다가 대용량 데이터 수집 및 분석 시스템 구현, 데이터 수집 분석 시스템 구현이 더 어렵다.

### 4) API application programming interface 추가 검색
- 프로그램과 프로그램간의 연결을 돕는 소프트웨어 도구
   - 응용프로그램과 응용체제간의 연결
   - 어플리케이션과 기기간의 연결 (어플리케이션 : 카톡, 기기 : 여러사람의 스마트폰)
- 어떤 서버의 특정한 부분에 접속해서 그 안에 있는 데이터와 서비스를 이용할 수 있게 해주는 소프트웨어 도구(위시켓 사이트)
- `REST API`
   - representational state transfer : 네트워크를 통해서 컴퓨터들끼리 통신할 수 있게 해주는 아키텍처 스타일
   - 인터넷 식별자 URI와 HTTP 프로토콜을 기반으로 한다.
   - REST API의 데이터 포멧은 JSON을 사용한다.
   - 클라이언트와 서버 사이에 통신할 수 있게 한다. 아키텍처를 만들 수 있게 한다.
   - REST API이면 클라이언트-서버 모델로 구축되었다는 것을 의미한다. 
   - 단일한 인터페이스 사용, 웹에 최적화, 주로 JSON 포멧이라 브라우저 간의 호환성 좋음, 확장성 좋음
   - 텍스트, HTML, XML, JSON 등 데이터 포멧 허용
   - 기능이 정지되거나 앱을 먹통으로 만들 수 도 있다. 이러한 문제 해결을 위해 GraphQL 같은 언어가 생김.
   - 캐시 사용 가능
- `SOAP API`
   - simple object access protocol
   - 그 자체로 프로토콜이다. 즉 규약, 규칙이다.
   - 보안이나 메시지 전송에서 REST API보다 더 많은 표준들이 정해져 있어서 복잡한 편이다.
   - 보안, 트랜젝션, ACID(원자성, 일관성, 고립성, 지속성)를 준수해야하는 종합적인 방식에 적합하다.
   - 은행 어플 같은 보안 수준이 높은 기능, 신뢰할 수 있는 메시징 앱 등에 사용된다.
   - XML 데이터 포멧만 사용함
   - 캐시사용할 수 없음 

### 5) 현대 개발팀의 구조
- 웹 시스템의 발전과 함께 개발팀의 구조도 변화해 왔다.
   - 시스템 개발할 때 여러 개발자와 구성원들이 함께 개발한다.
   - 따라서 어떤 구성원이 어떤 역할을 하는지 이해해야한다. 
- 기획자 product manager 
   - 개발하려는 서비스를 정의, 기획한다.
- 디자이너 desinger : UI, UX 구현 담당
- 프론트엔드 개발자 frontend developer : 프론트엔드 시스템 구현
   - html, css, 자바스크립트 등 사용
   - html, css 부분만 담당하는 퍼블리셔 publisher 직군도 있음 (우리나라 특징)
- 백엔드 개발자 backend developer :  백엔드 시스템 구현
   - API 개발자와 데이터 수집, 분석, 관리 등 데이터 관련 시스템 개발자와 나뉘는 편
   - API 개발 보다 데이터 분석 수집등의 개발이 더 난이도가 높다.
- 데브옵스 : development + operation
   - 개발 경향 또는 개발 문화를 의미함
   - 개발자가 시스템 개발(development)과 운영(operation) 까지 담당하는 추세
   - AWS 발달 : 서버 구축, 운영 등의 인프라스트럭처(infrastructure) 구축 관리를 위해 실제 서버 하드웨어를 직접 다루지 않아도 됨 
   - 시스템 운영 담당자가 따로 없이 개발자들이 직접 시스템 인프라 스트럭쳐(클라우드 서비스 사용)를 구현하는 추세가 됨
- 풀스택 개발자 : full stack developer
   - nodejs를 통해서 자바스크립트 만으로 프론트엔드와 백엔드 둘다 개발이 가능해짐 -> 풀스택 개발자들 많아짐
   - 풀스택 개발자도 프론트엔드, 백엔드 개발 둘다 잘 할수는 없음
   - 둘중하나 전문으로하고 나머지 하나는 부가적으로 키우는 것 추천
- 시스옵스 : sysops, system operations
   - 시스템 인프라스트럭쳐의 구현과 관리 운영 담당
   - 실제 하드웨어를 다룰 수 있는 직군
   - 서버를 직접 설치하고 운영함, 물리적인 네트워크 구축 및 운영
- 데이터 사이언티스트 : data scientist
   - 데이터 분석에 필요한 알고리즘과 모델링 구현
   - 빅데이터를 분석해서 새로운 정보와 가치를 만들어낼 수 있는 데이터 사이언티스트 직군
   - 고학력, 해당 분야의 경험이 널리 퍼져 있지 않음, 고연봉
- 데이터 엔지니어 : data engineer
   - 데이터 사이언티스트와 함께 일하는 직군
   - 데이터 사이언티스트가 데이터 분석할 수 있도록 데이터를 정리하는 시스템 구현
- 테스터 : tester
   - 시스템 테스트하여 검증
   - QA : quality assurance 테스터, 직접 손으로 하는 테스트, 매뉴얼 테스트 담당
   - 테스트 자동화 시스템 구현하는 테스터 : 테스트를 실행하는 시스템을 개발한다.
- 스크럼 마스터 : scrum master
   - 스크럼 개발론에서 생겨난 직군
   - 개발자들의 생산성을 높이기 위해서 스크럼 개발론이 도입됨, 현실적으로 제대로 사용되지 않는 경우가 많아짐
   - 스크럼을 제대로 활용할 수 있도록 코치해주는 역할

## 2. API 개발 스타트

### 1) `Flask` : API 개발 프레임워크
- 파이썬으로 웹 어플리케이션을 구현할 때 사용되는 프레임 워크
   - "micro web framework" : 아주 가벼운 웹 프레임워크
   - 파이썬 기반 웹 프레임워크 : django 등 여러가지 있음
   - Flask는 학습이 쉽고 프로그램이 가벼운 장점 : API 개발에 많이 사용되지만 대규모 시스템 개발에도 사용됨
- 프레임워크란?
   - 시스템 구현을 위해서 공통적으로 요구되는 기능과 구조를 재사용 가능하도록 구현해 놓은 것
   - 모든 웹 시스템은 "소켓socket"을 통해서 네트워크와 연결하여 외부 시스템으로 부터 통신을 주고받을 수 있어야 한다.
   - `소켓` : 웹 시스템이 외부 시스템과 네트워크할 수 있는 기능을 담당함
   - 프레임워크와 비슷한 개념 : 라이브러리 library
   - 라이브러리는 개발자가 자신의 코드 안에서 실행함
   - 프레임워크는 프레임워크가 개발자의 코드를 실행함 : 프레임워크가 제공하는 틀안에서 개발자가 코드를 구현한다.
- API 개발 첫 단계
   - 파이썬 가상환경 생성하기
   - conda create --name hong python=3.7 : hong 이라는 이름의 가상환경, python 3.7 버전을 사용
      - hong 가상환경에 기본 패키지, 파이썬 등이 설치됨
   - conda activate hong : hong 이라는 가상환경을 활성화
   - conda deactivate : 가상환경 비활성화
   - conda env list : 가상환경 리스트
   - 여러가지 버전으로 가상환경을 만들고 사용하게 됨
   - 모든 패키지는 해당 가상환경을 활성화하고 설치해야함. pip 패키지 매니지먼트를 사용
   - 가상환경을 활성화하지 않고 패키지를 설치하면 시스템에 설치되어 있는 파이썬에 종속된다.
   - 가상환경에서 pip 패키지 매니저로 설치한 파일을 삭제할 때는 pip uninstall 패키지이름 으로 삭제해야한다.
   - pip freeze : 모든 패키지 리스트와 버전
- `ping 엔드포인트 구현하기`
   - 엔드포인트 : endpoint : API 서버가 제공하는 통신 채널 혹은 접점
   - 프론트엔드 서버와 백엔드 API 서버와 통신할 때 엔드포인트에 접속하는 형태로 통신한다.
   - 각각의 엔드포인트는 고유의 URL 주소를 갖는다.
   - 고유의 URL 주소를 통해서 해당 엔드포인트로 접속할 수 있게 된다.
   - 각각의 엔드포인트는 고유의 기능을 담당한다. 엔드포인트들이 모여서 하나의 API를 구성한다.
      - sns 서비스 API : 사용자 sign up 엔드포인트, 사용자 로그인 엔드포인트, 새로운 포스팅 생성 엔드포인트, 친구맺기 엔드포인트 등 여러 엔드포인트들로 구성된다.
   - 단 하나의 엔드포인트로 모든 기능을 제공하는 형태의 기술도 있다. : GraphQL
   - ping 엔드포인트 : pong 이라는 텍스트를 리턴하는 엔드포인트. 간단한 엔드포인트. API 서버가 현재 운행되는지 정지되었는지를 간단하게 확인할 때 주로 사용함. 헬스체크 엔드포인트라고도 함.
   - 해당 API 접속하지 않고서 API의 정상 운행 여부를 간단하게 체크할 수 있다.
   - mkdir -p ~/project/api : -p는 중간 경로 디렉토리가 없으면 자동으로 생성하라는 뜻
   - app.route("/ping", methods=["GET"]) : route 데코레이터를 사용하여 ping 이라는 엔드포인트를 등록하고 그 아래 ping 함수를 구현한다.
   - 즉 API 코드에서 엔드포인트들을 함수 형태로 구현하면 된다. 이것이 API에서 가장 큰 부분을 차지한다.
- `API 실행하기`
   - 간단한 ping 엔드포인트가 있는 app.py를 실행한다.
   - api 실행할때는 가상환경을 활성화하고 터미널에 명령어 입력
   - FLASK_APP=app.py FLASK_DEBUG=1 flask run
   - 지정한 파일이 명령을 실행시키는 디렉토리에 존재해야한다.
   - FLASK_DEBUG=1 : 디버그 모드 활성화, 코드 수정되엇을때 자동으로 flask app이 재시작되어 새로 수정한 코드가 반영되도록 하는 모드이다. 매우 유용함.
   - sudo apt install httpie : 터미널 환경에서 http 요청을 보낼 수 있게 해주는 툴
      - http -v POST localhost:5000/ping
- API는 HTTP 통신에 기반을 두고 있으므로 HTTP에 대해서 잘 알아야 함
- HTTP 는 프로토콜의 한 종류, API는 다른 프로토콜을 사용하는 경우도 많음

### 2) HTTP 프로토콜
- HTTP : Hypertext transfer protocol : 웹 상에서 서버와 서버, 클라이언트와 서버 사이의 네트워크를 통한 통신(커뮤니케이션)을 할 때 필요한 통신 규약, 통신 규칙, 통신 형식
   - 한국사람 - 영어 - 미국사람 : 영어가 공용어로써 통신 규칙인 것과 같다.
- API 시스템은 일반적으로 HTTP 프로토콜을 기반으로 통신한다.
- HTTP는 HTML을 주고 받을 수 있도록 만들어진 프로토콜이다.
   - 프로토콜 : 통신 규약
   - 여러가지 프로토콜 중 HTTP는 하나의 프로토콜이다.
- 현대의 웹 시스템에서는 HTTP를 통해서 HTML 뿐만 아니라 다양한 데이터를 전송하는데 사용된다.
- HTTP의 특징
   - 요청 request 과 응답 reponse
      - HTTP를 기반으로 통신할 때 클라이언트가 HTTP 요청을 보냄 -> 서버는 이 요청을 처리한 후 결과를 HTTP 응답으로 클라이언트에게 보낸다. 이 사이클이 HTTP 통신.
      - /ping 주소에 GET 요청을 보냄
      - 200 ok 상태 코드와 함께 pong 이라는 텍스트를 응답함
      - ping 함수에서 HTTP 요소가 없지만 HTTP 통신이 가능했던 것은 Flask가 HTTP 부분을 자동으로 요청, 응답으로 처리해 준 것.
   - stateless
      - "상태 없음"
      - HTTP 통신에서는 상태state 라는 개념이 없다.
      - 클라이언트와 서버가 주고받는 여러 요청-응답에서 HTTP 통신들은 서로 독립적이다. 그 전에 처리된 HTTP에 대해서도 전혀 알지 못함
      - stateless 하기때문에 서버 디자인이 간단하고 효과적인 장점. HTTP 통신 상태를 저장할 필요가 없으므로 HTTP 통신 간의 진행상태, 연결 상태, 처리 상태 등의 저장을 구현하지 않아도 됨
      - 각각의 HTTP 요청에 대해 독립적인 HTTP 응답을 보내주면 된다.
      - 단점은 HTTP 통신이 독립적이므로 각각의 HTTP에 모든 데이터를 담아서 요청해야한다. 즉 로그인을 이전에 했으면 이후의 HTTP 통신에서는 로그인한 상태를 함께 보내줘야 한다. 이것을 쿠키 cookie나 세션 session 등을 사용해서 HTTP 요청을 처리할때 저장한다.
- 쿠키 cookie : 웹 브라우저가 웹 사이트에서 보내온 정보를 저장할 수 있도록 하는 조그마한 파일
   - HTTP는 stateless 하므로 HTTP 요청을 보낼 떄 모든 정보를 포함해야한다. 클라이언트에서 이렇게 하려면 클라이언트의 정보를 저장해야하는데 웹 브라우저는 쿠키라는 파일을 사용해서 이것을 저장한다.
- 세션 session : 쿠키와 같은 기능
   - HTTP 통신사에서 필요한 데이터를 저장할 수 있게 하는 매커니즘
   - 쿠키는 웹브라우저 = 클라이언트에서 저장한다.
   - 세션은 웹서버에서 데이터를 저장한다.
- HTTP 요청, 응답 구조
   - 요청 메시지 구조 : start line, headers, body 로 구성되어 있다.
   - Flask나 django 등의 웹 프레임워크가 HTTP의 요청, 응답 구조의 많은 부분을 자동으로 처리해 준다.
   - HTTP METHOD (GET, POST 등), status code, header 정보, body 부분을 구현하면 된다.
   - HTTP의 요청, 응답 구조는 알아야 한다.
- HTTP 요청의 구조
- <start line>
   - HTTP method : 해당 HTTP 요청이 의도하는 액션을 정의하는 부분
      - GET : 서버로부터 데이터를 받고자 할때
      - POST : 서버에 새로운 데이터를 저장하고자 할때
      - GET, POST, PUT, DELETE, OPTIONS 등
   - request target
      - 해당 HTTP 요청이 전송되는 목표 주소를 의미한다.
      - app.route("/ping", method=["GET"]) 에서 request target은 /ping 이다.
   - HTTP version
      - 해당 요청의 HTTP 버전을 의미한다.
      - 1.0, 1.1, 2.0
      - HTTP의 버전에 따라서 요청 메시지 구조가 조금씩 다르므로 서버가 이 버전에 맞춰서 응답을 보내게 된다.
- <header>
   - start line 다음 부분에 온다.
   - 헤더 정보는 HTTP 요청 그 자체에 대한 정보를 담고 있다.
   - python 딕셔너리 타입 처럼 key, value로 되어 있다. {key : value}
      - request.header.get['Auth']
   - "HOST : google.com"
      - 요청이 전송되는 HOST의 URL 주소가 google.com 이라는 헤더이다. 
   - "User-Agent : Mozila/5.0"
      - 요청을 보내는 클라이언트에 대한 정보를 나타내는 헤더이다.
      - 웹 정보 같은 것들
   - "Accept : application/json"
      - 응답 response의 body의 데이터 타입을 알려주는 헤더이다.
      - MIME(multipurpose internet mail extensions) type으로 데이터 타입을 지정한다.
      - application/json, application/octet-stream, text/csv, text/html, image/jpeg, image/png, text/plain, application/xml 등이 주로 사용됨
      - */* 은 모든 데이터 타입을 다 허용한다는 의미
      - Mozila의 MIME type 페이지에 자세히 나와 있음
   - "Connection : keep-alive"
      - 요청이 끝난 후 클라이언트와 서버가 계속 네트워크 연결을 유지할지 말지에 대한 헤더
      - HTTP 요청 때마다 네트워크 연결을 새로 하는 것이 아니라, 처음 만든 네트워크 연결을 재사용하는 방식이 선호됨. 이러한 정보를 담는 헤더이다.
      - keep-alive 는 HTTP 요청이 종료되어도 클라이언트와 서버간의 네트워크 연결을 유지하라는 의미
      - clos는 네트워크 연결을 종료하라는 의미
   - "Content-Type : application/json"
      - HTTP 요청 메시지의 body type을 의미하는 헤더
      - Accept 헤더 처럼 MIME type이 사용된다.
   - "Content-Length : 257"
      - HTTP 요청 메시지의 body의 총 사이즈를 알려주는 헤더
- <body>
   - HTTP 요청이 담고 있는 메시지 부분
   - 데이터가 없으면 비어 있음
- HTTP 응답의 구조
- status line, headers, body 로 구성되어 있다.
- <status line>
   - "HTTP/1.1 404 Not Found"
   - HTTP version, status code, status text
   - status code : 응답의 상태를 나타내는 숫자 코드
   - status text : 응답 상태에 대한 설명
- <header>
   - 요청의 헤더와 같음
   - Server 헤더는 응답의 헤더에서만 사용됨
- <body>
   - HTTP 요청의 body와 같음
   - 전송하는 응답 데이터가 없으면 비어 있음
- 자주 사용되는 "HTTP 메소드"
   - HTTP 요청의 start line의 구성요소인 method
   - 요청이 의도하는 액션을 의미함
   - <GET> : 자주 사용되는 메서드
      - 어떤 데이터를 서버로부터 요청할 때 사용함
      - 단순히 데이터를 받아오는 요청
      - GET 메서드가 사용되면 해당 HTTP 요청의 body는 비어있는 경우가 많다. 서버에 전송할 데이터가 없음.
   - <POST> : 자주 사용되는 메서드
      - 데이터를 생성, 수정, 삭제 등의 요청을 할 때 사용
   - <OPTIONS> : 특정한 엔드포인트에서 허용하는 메소드들을 요청할 때 사용
      - 엔드포인트는 허용하는 메서드가 지정되어 있음, 허용하지 않은 HTTP 메서드 요청이 오면 405 응답 메시지를 보낸다.
      - OPTIONS 메서드 요청을 보내면, header에 "ALLOW : GET, HEAD, OPTIONS" 처럼 허용하는 메서드에 대한 응답이 온다.
      - Flask를 사용하여 엔드포인트를 만들고 허용 메서드로 GET 만 넣어도, OPTIONS 메서드 요청을 보내면 HEAD와 OPTIONS 메서드가 함께 응답 header로 되돌아온다. Falsk에서 자동을 HEAD와 OPTIONS 메서드를 구현해 줌.
   - <PUT> : POST 메소드와 비슷한 메소드
      - 데이터를 새로 생성할 때 사용한다.
      - 데이터 생성, 수정 관련한 요청은 보통 POST를 사용한다. PUT은 생성만 가능
   - <DELETE>
      - 삭제 요청을 위한 HTTP 메소드
      - POST를 주로 사용한다. DELETE는 삭제만 가능
- 자주 사용되는 HTTP "statud code, status text"
   - HTTP 응답 메시지의 앞부분인 status line에 포함되는 메시지
   - <200 OK> : HTTP 요청이 성공적으로 처리 됐다는 것을 의미한다.
   - <301 Moved Permanently> : HTTP 요청을 보낸 엔드포인트의 URL 주소가 변경됐다는 것을 의미한다.
      - HTTP 응답 header 값에 "Location: "으로 바뀐 URL 주소가 나타난다.
      - 이 바뀐 엔드포인트 URL 주소로 다시 HTTP 요청을 보낸다. ==> "redirection"
   - <400 Bad Request> : HTTP 요청이 잘 못 됐다는 것을 의미한다.
      - 주로 요청에 포함된 input 값들이 잘 못된 경우에 사용된다.
      - 전화번호를 저장하는 HTTP 요청인데, input 값으로 숫자가 아닌 글자가 있는 경우 서버는 이 status code를 보낸다.
   - <401 Unauthorized> : HTTP 요청을 처리하기 위해서, 요청을 보낸 주체의 신분(credential) 확인을 할 수 없을 때 사용된다.
      - 주로 HTTP 요청을 보내는 사용자가 로그인이 필요한 경우 401 응답을 보낸다.
   - <403 Forbidden> : HTTP 요청을 보낸 사용자, 클라이언트, 주체가 해당 요청에 대한 권한이 없을 때 사용
      - 비용 결제를 해야지만이 볼 수 있는데 비용 결제를 하지 않고 요청하는 경우 응답으로 사용된다.
   - <404 Not Found> : 요청을 보내고자 하는 URI가 존재하지 않을 떄 사용된다.
      - 잘 못된 주소의 웹페이지를 찾으려고 하면 "해당 페이지를 찾을 수 없습니다"라는 메시지가 뜨는데, 이러한 페이지를 404 페이지라고 부른다.
   - <500 Internal Server Error> : 내부 서버 오류에 사용된다.
      - HTTP 요청을 받은 서버에서 해당 요청을 처리하는 과정에서 서버 오류가 나서 요청을 처리할 수 없을 때 사용된다.
      - API 개발자들이 가장 싫어하는 응답 코드
- API 엔드포인트 아키텍처 패턴
   - RESTful HTTP API : API 시스템을 구현하기 우한 아키텍처의 한 방식, 리소스를 특정 URI로 표현하고, 이 리소스에 요청하고자 하는 의도를 HTTP 메소드로 정의하는 방식
      - 서버가 정의한 틀로 클라이언트는 이 틀에 맞춰서 요청을 해야한다.
      - "HTTP/1.1 GET /users" ==> /users 라는 리소스에서 GET 메서드를 요청한다. 즉 회원정보를 요청한다는 것.
      - "HTTP/1.1 POST /user" ==> /user 라는 리소스에서 POST 메서드를 요청한다. 즉 회원정보를 생성하겠다는 것.
      - API 개발하면 엔드포인트가 많아지게 된다. RESTful HTTP API 방식은 구조가 직관적이고 알아보기 쉽게 간단해지는 장점이 있다.
   - GraphQL : REST API 방식으로 만든 시스템의 구조적 문제를 해결하기 위해서 만들어진 방식
      - API 구조가 특정한 클라이언트에게 맞춰저서 다른 클라이언트는 사용하기 적합하지 않게 된다는 문제
      - 페이스북에서 앱 개발을 하는 과정에서 REST API의 문제가 발견됨
      - GraphQL 은 엔드포인트가 오직 하나이다. 이 하나의 엔드포인트에 클라이언트가 필요한 것을 요청하는 방식.
      - REST API는 여러번의 엔드포인트에 대한 요청을 한번에 하려면 HTTP 요청이 복잡해지지만, GraphQL은 간단하게 하나의 엔드포인트에서 처리할 수 있다. REST API 보다 장점이 많지만 REST AIP 방식이 많이 사용되어 왔다.

* 실제 API 시스템 개발하기
- 미니터 개발하기 : 축소된 형태의 트위터
- 핵심 기능
   - 회원가입, 로그인, 트윗, 팔로우하기, 언팔로우하기, 타임라인

















































