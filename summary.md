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
- `기획자 product manager`
   - 개발하려는 서비스를 정의, 기획한다.
- `디자이너 desinger : UI, UX 구현 담당`
- 프론트엔드 개발자 frontend developer : 프론트엔드 시스템 구현
   - html, css, 자바스크립트 등 사용
   - html, css 부분만 담당하는 퍼블리셔 publisher 직군도 있음 (우리나라 특징)
- `백엔드 개발자 backend developer :  백엔드 시스템 구현`
   - API 개발자와 데이터 수집, 분석, 관리 등 데이터 관련 시스템 개발자와 나뉘는 편
   - API 개발 보다 데이터 분석 수집등의 개발이 더 난이도가 높다.
- `데브옵스 : development + operation`
   - 개발 경향 또는 개발 문화를 의미함
   - 개발자가 시스템 개발(development)과 운영(operation) 까지 담당하는 추세
   - AWS 발달 : 서버 구축, 운영 등의 인프라스트럭처(infrastructure) 구축 관리를 위해 실제 서버 하드웨어를 직접 다루지 않아도 됨 
   - 시스템 운영 담당자가 따로 없이 개발자들이 직접 시스템 인프라 스트럭쳐(클라우드 서비스 사용)를 구현하는 추세가 됨
- `풀스택 개발자 : full stack developer`
   - nodejs를 통해서 자바스크립트 만으로 프론트엔드와 백엔드 둘다 개발이 가능해짐 -> 풀스택 개발자들 많아짐
   - 풀스택 개발자도 프론트엔드, 백엔드 개발 둘다 잘 할수는 없음
   - 둘중하나 전문으로하고 나머지 하나는 부가적으로 키우는 것 추천
- `시스옵스 : sysops, system operations`
   - 시스템 인프라스트럭쳐의 구현과 관리 운영 담당
   - 실제 하드웨어를 다룰 수 있는 직군
   - 서버를 직접 설치하고 운영함, 물리적인 네트워크 구축 및 운영
- `데이터 사이언티스트 : data scientist`
   - 데이터 분석에 필요한 알고리즘과 모델링 구현
   - 빅데이터를 분석해서 새로운 정보와 가치를 만들어낼 수 있는 데이터 사이언티스트 직군
   - 고학력, 해당 분야의 경험이 널리 퍼져 있지 않음, 고연봉
- `데이터 엔지니어 : data engineer`
   - 데이터 사이언티스트와 함께 일하는 직군
   - 데이터 사이언티스트가 데이터 분석할 수 있도록 데이터를 정리하는 시스템 구현
- `테스터 : tester`
   - 시스템 테스트하여 검증
   - QA : quality assurance 테스터, 직접 손으로 하는 테스트, 매뉴얼 테스트 담당
   - 테스트 자동화 시스템 구현하는 테스터 : 테스트를 실행하는 시스템을 개발한다.
- `스크럼 마스터 : scrum master`
   - 스크럼 개발론에서 생겨난 직군
   - 개발자들의 생산성을 높이기 위해서 스크럼 개발론이 도입됨, 현실적으로 제대로 사용되지 않는 경우가 많아짐
   - 스크럼을 제대로 활용할 수 있도록 코치해주는 역할

## 2. API 개발 스타트

### 1) Flask : API 개발 프레임워크
- 파이썬으로 웹 어플리케이션을 구현할 때 사용되는 프레임 워크
   - "micro web framework" : 아주 가벼운 웹 프레임워크
   - 파이썬 기반 웹 프레임워크 : django 등 여러가지 있음
   - Flask는 학습이 쉽고 프로그램이 가벼운 장점 : API 개발에 많이 사용되지만 대규모 시스템 개발에도 사용됨
- `프레임워크란?`
   - 시스템 구현을 위해서 공통적으로 요구되는 기능과 구조를 재사용 가능하도록 구현해 놓은 것
   - 모든 웹 시스템은 "소켓socket"을 통해서 네트워크와 연결하여 외부 시스템으로 부터 통신을 주고받을 수 있어야 한다.
   - `소켓` : 웹 시스템이 외부 시스템과 네트워크할 수 있는 기능을 담당함
   - 프레임워크와 비슷한 개념 : 라이브러리 library
   - 라이브러리는 개발자가 자신의 코드 안에서 실행함
   - 프레임워크는 프레임워크가 개발자의 코드를 실행함 : 프레임워크가 제공하는 틀안에서 개발자가 코드를 구현한다.
- `API 개발 첫 단계`
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
- `HTTP : Hypertext transfer protocol` : 웹 상에서 서버와 서버, 클라이언트와 서버 사이의 네트워크를 통한 통신(커뮤니케이션)을 할 때 필요한 통신 규약, 통신 규칙, 통신 형식
   - 한국사람 - 영어 - 미국사람 : 영어가 공용어로써 통신 규칙인 것과 같다.
- API 시스템은 일반적으로 HTTP 프로토콜을 기반으로 통신한다.
- HTTP는 HTML을 주고 받을 수 있도록 만들어진 프로토콜이다.
   - 프로토콜 : 통신 규약
   - 여러가지 프로토콜 중 HTTP는 하나의 프로토콜이다.
- 현대의 웹 시스템에서는 HTTP를 통해서 HTML 뿐만 아니라 다양한 데이터를 전송하는데 사용된다.
#### `HTTP의 특징`
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
- `쿠키 cookie` : 웹 브라우저가 웹 사이트에서 보내온 정보를 저장할 수 있도록 하는 조그마한 파일
   - HTTP는 stateless 하므로 HTTP 요청을 보낼 떄 모든 정보를 포함해야한다. 클라이언트에서 이렇게 하려면 클라이언트의 정보를 저장해야하는데 웹 브라우저는 쿠키라는 파일을 사용해서 이것을 저장한다.
- `세션 session` : 쿠키와 같은 기능
   - HTTP 통신사에서 필요한 데이터를 저장할 수 있게 하는 매커니즘
   - 쿠키는 웹브라우저 = 클라이언트에서 저장한다.
   - 세션은 웹서버에서 데이터를 저장한다.
- `HTTP 요청, 응답 구조`
   - 요청 메시지 구조 : start line, headers, body 로 구성되어 있다.
   - Flask나 django 등의 웹 프레임워크가 HTTP의 요청, 응답 구조의 많은 부분을 자동으로 처리해 준다.
   - HTTP METHOD (GET, POST 등), status code, header 정보, body 부분을 구현하면 된다.
   - HTTP의 요청, 응답 구조는 알아야 한다.

#### `HTTP 요청의 구조`
- `<start line>`
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
- `<header>`
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
- `<body>`
   - HTTP 요청이 담고 있는 메시지 부분
   - 데이터가 없으면 비어 있음

#### HTTP 응답의 구조
- status line, headers, body 로 구성되어 있다.
- `<status line>`
   - "HTTP/1.1 404 Not Found"
   - HTTP version, status code, status text
   - status code : 응답의 상태를 나타내는 숫자 코드
   - status text : 응답 상태에 대한 설명
- `<header>`
   - 요청의 헤더와 같음
   - Server 헤더는 응답의 헤더에서만 사용됨
- `<body>`
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
- `자주 사용되는 HTTP "statud code, status text"`
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
- `API 엔드포인트 아키텍처 패턴`
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

#### 미니 SNS의 API 시스템 개발하기
- 미니터 개발하기 : 축소된 형태의 트위터
- 핵심 기능
   - 회원가입, 로그인, 트윗, 팔로우하기, 언팔로우하기, 타임라인

## 3. (5장) API 개발
- API 개발은 HTTP 통신을 기반으로 하므로, request와 response 구조로 프로그래밍을 한다.
   - request는 엔드포인트에 전송된 HTTP 요청 정보(헤더, body 등)를 저장하고 있다.
   - POST 엔드포인트의 경우 HTTP 요청에으로 전송된 입력값을 request에 json 데이터로 저장한다.
   - request.json은 requset에 저장 된 json 데이터를 dictionary로 변경해준다.
   - dictionary로 변경한 후 key,value 값을 사용하여 코드를 작성하고,
   - jsonity를 사용하여 dictionary를 json으로 변환하여 결과값으로 반환한다.
- flask의 route 기능을 사용하여 각 기능별 endpoint를 등록한다.
   - endpoint의 웹 주소인 URI에 등록한다.
- HTTP 통신을 위해서 각 엔드포인트마다 methods를 설정한다.
   - GET, POST, PUSH, DELETE, OPTIONS 등
- JSON 데이터 타입 형태로 request, response를 주고받으므로 각 엔드포인트의 코드마다 데이터 타입을 설정해준다.
   - flask의 jsonify 패키지는 dict을 json 타입으로 변환해준다.
- 중복 데이터를 일일이 검사하지 않기 위해서 set 데이터 타입을 사용할 경우 flask의 디폴트 json 엔코더의 값을 변경해준다.
   - CustomJSONEncoder 클래스를 만들고 이것을 flask의 디폴트 json encoder로 지정해준다.
   - flak.json의 JSONEncoder 패키지를 사용하여 set 데이터 타입을 list로 변환하도록 설정한다.
   - list는 json으로 변환할 수 있지만 set은 json으로 변환할 수 없기 때문에, set을 list로 변환한 후 json으로 다시 변환하기 위함이다.
- URL에 인자(parameter)를 전송할 때는 URL에 <type:value> 형식을 추가해 준다.
   - /timeline/<int:user_id> ===> timeline 엔드포인트에 int 타입의 user_id 값을 전송한다는 의미
      - 엔드포인트의 함수의 파라미터로 넣어주어야 사용할 수 있다. def login(user_id)

## 4. (6장) 데이터 베이스
- 현재 API 구조에서는 request-response 후 API가 다시 시작될 때마다 데이터가 사라지는 문제.
   - `데이터를 영구적으로 보관하기 위해서 데이터 베이스 시스템을 사용한다.`

### 1) 데이터 베이스 시스템
- `데이터를 저장하고 보존하는 시스템`
- 데이터를 읽고, 새로 쓰고, 업데이트
- 데이터 베이스 시스템의 대표적인 2가지 종류
   - 관계형 데이터베이스 시스템 : RDBMS(relational database management system)
   - 비관계형 데이터 베이스 : NoSQL(non-relational)
   - 더 많을 수 있음

#### 관계형 데이터 베이스 RDBMS
- 관계형 데이터 : 데이터들이 서로 상호관련성을 가진 형태
   - MySQL, PostgreSQL(Postgres) 가 대표적
- 모든 데이터가 2차원 테이블(table)로 표현된다.
   - row, column
   - column : 항목
   - row : 실제값
- 각각의 row는 고유키(primary key)가 있다. 프라이머리 키를 사용하여 해당 로우를 찾거나 인용할 수 있다.
   - 다른 값으로도 row를 검색할 수 있다.
- 외부키(foreign key)를 통해서 연결한다 : 한 테이블에서 다른 테이블의 특정 컬럼의 값으로 연결시는 과정
   - users의 id와 tweets의 user_id 값을 foreign key로 연결

#### 테이블간의 연결 형태
- one to one
   - 국가와 수도의 관계 : 한 국가는 하나의 수도를 갖는다.
- one to many
   - 사용자와 트윗의 관계 : 하나의 사용자가 여러가지 트윗을 갖는다.
- many to many
   - 사용자간의 팔로우 관계 : 한 사용자는 여러 사용자와 팔로우를 할 수 있다.

#### 관계형 데이터 베이스에서 중요한 기능 (1) : 정규화
- 하나의 테이블에 국가, 수도 혹은 id, name, email, profile, tweet 등을 다 관리하면 더 좋은 것 아닌가?
- 문제가 발생한다.
   - 하나의 테이블에 모든 데이터를 다 저장하면 동일한 데이터들이 중복되어 저장 될 수 있다. 외부키값만 저장하면 디스크 사용 공간이 절약된다.
   - 같은 데이터가 다른 테이블에서 다르게 저장될 수 있다. A 테이블에는 seoul로 저장되지만 B 테이블에서는 jeoul로 잘 못 저장 될 수 있다. 하지만 외부키를 사용하면 이러한 오류를 막을 수 있다.
   - 이러한 방법을 정규화 또는 normalization이라고 함

#### 관계형 데이터 베이스의 중요한 기능 (2) : 트랜젝션
- transaction : 일련의 작업들이 하나의 작업처럼 취급 된다. 하나의 unit으로 실행한다. 모두 다 실패하거나 모두 다 성공하는 것.
- 은행에서 현금을 인출하는 경우
   - 해당 고객의 계좌 확인, 잔금 확인
   - 충분한 잔금이 있다면 이체하려는 금액만큼 해당 계좌에서 차감
   - 이체 금액을 이체 대상인 계좌에 전송
   - 이체를 받는 계좌는 이체 금액을 잔고에 더함
- 이 과정에서 하나라도 오류가 나면 문제가 생긴다. 따라서 이 과정이 모두 성공해야 이체가 완료, 즉 데이터 베이스에 영구적으로 반영이된다. 하나라도 오류가 발생하면 그 전 상태로 되돌아가는 기능을 트랜젝션이라고 한다.
- 이러한 트랜젝션 기능을 보장하기 위한 관계형 데이터 베이스의 성질 : ACID
   - Atomicity : 원자성
   - Consistency : 일관성
   - Isolation : 고립성
   - Durability : 지속성

### 2) 비관계형 데이터 베이스
- NoSQL 데이터 베이스라고 부른다.
- 비관계형 데이터를 저장할 때 주로 사용하는 데이터 베이스 시스템
- 관계형 데이터 베이스와 같이 테이블들의 스키마(schema)와 관계를 미리 구현할 필요가 없다.
- 데이터가 들어오는데로 단순 저장한다.
- 대표적인 비관계형 시스템
   - MongoDB, Redis, Cassandra 등
- 관계형 데이터 베이스와 비관계형 데이터 베이스의 비교
   - 어떤 시스템에서 어떤 데이터 베이스를 사용해야 할까?

### 3) 관계형, 비관계형 데이터 베이스의 장단점

#### 관계형 데이터 베이스
- 장점
   - 데이터를 효율적이고 체계적으로 저장하고 관리할 수 있다.
   - 저장하려는 데이터들의 구조(테이블 스키마)를 미리 정의하므로 데이터의 완전성이 보장된다.
   - 트랜젝션transaction 기능을 제공한다.
- 단점
   - 테이블을 미리 정의해야 한다. 따라서 테이블의 구조 변화 등에 유연하지 않다.
   - 확장이 어렵다. 테이블 구조(스키마)가 미리 정의되어야 하고, ACID가 보장되어야 한다. 따라서 확장할 경우 서버의 성능 자체도 높여야 한다.
   - 서버를 늘려서 분산저장하는 것이 어렵다. scale out(서버 수 늘리기)보다 scale up(서버 성능 높이기)으로 확장해야 한다.

#### 비관계형 데이터 베이스
- 장점
   - 데이터 구조를 미리 정하지 않으므로, 데이터 구조의 변화에 유연하다.
   - 데이터 베이스의 확장이 비교적 쉽다. scale out 방식으로 시스템 확장이 가능하다.
   - 구조 변화에 유연하고, 확장이 쉬워 빅데이터를 저장하고 관리하는데 유리하다.
- 단점
   - 데이터의 완전성이 덜 보장된다.
   - 트랜젝션 기능이 안되고, 되더라도 불안정하다.
- 따라서 관계형 데이터 베이스는 : 정형화된 데이터 또는 데이터의 완전성이 보장되어야 하는 데이터를 저장하는데 유용하다.
   - 전자상거래 정보, 은행 계좌 정보, 거래 정보 등
- 따라서 비관계형 데이터 베이스는 : 비정형화된 데이터 또는 완전성이 상대적으로 떨어지는 데이터를 저장하는데 유용하다.
   - 로그 데이터 저장
- 중요 데이터는 RDBMS, 로그 데이터는 NoSQL
   - 즉 유저 정보, 상품 구매 데이터는 등은 RDBMS인 MySQL, 단순 로그 데이터 등은 NoSQL인 mongodb 등을 사용

### 4) SQL 명령어 기본 
- `structured Query language` : 관계형 데이터 베이스(RDBMS)에서 데이터를 읽고, 생성하고 수정하기 위한 언어
   - CRUD : create(생성), read(읽기), update(수정), delete(삭제) 기능을 제공한다.
- SQL 구문
   - select col1, col2 from users where name="hong" : 관계형 데이터 베이스에서 데이터를 읽을 때 사용
   - insert into table_name(col1, col2) values(col1_value, col2_value) : 관계형 데이터 베이스에서 데이터를 생성할 때 사용
      - insert into users(col1, col2) values(col1_value, col2_value), (col1_value, col2_value) : 여러개의 데이터(row)를 생성할 때 사용
   - update table_name set col1=value1 where col2=value2 : where 조건을 만족하는 row의 col1을 value1으로 수정
   - delete from table_name where col=value : where 조건을 만족하는 데이터를 삭제
      - delete from users where age > 25
   - join : 여러 테이블을 연결할 때 사용
      - select table1.col1, table2.col2 from table1 join table1 on table1.id=table2.id
      - select users.name, user_addr.addr from users join user_addr on user_addr.id=user.id

### 5) 관계형 데이터 베이스 설치하기

#### MySQL 설치
- root 사용자 : master 사용자
- 우분투에서는 apt, apt-get으로 설치
   - sudo apt-get install mysql
   - pw 설정 또는 기존 master pw으로 자동 설정
- 서버 시작 : service mysql start
- 서버 상태 : service mysql status (서버 상태 등 정보 나옴)
- 서버 종료 : service mysql stop
- 서버 접속 : sudo /usr/bin/mysql -u root -p : 경로를 지정하여 실해하면 실행 된다.
   - root 사용자의 비번을 설정하면 아래 처럼 접속 할 수 있음
   - 또는 mysql -u root -p ===> -u는 아이디 명시 (root), -p는 pw 직접 입력 옵션
- mysql 접속 후 root 사용자 비번 설정 : mysql 서버를 관리하는 root 사용자의 비번을 설정할 수 있다.
   - SELECT user, plugin, host FROM mysql.user; ===> user 별 plugin 상태 확인
   - ALTER USER "root"@"localhost" IDENTIFIED WITH mysql_native_password BY "hshkuber1234" 
   - FLUSH PRIVILEGES ; ===> 바로 반영
   - root 관리자 비번이 hshkuber1234로 설정되고, mysql 접속시 pw 치라고 뜬다.
- mysql 접속 상태에서 커맨트 명령줄 삭제
   - system clear

#### API 데이터베이스 연결하기
- mysql 접속
   - mysql -u root -p
- 데이터 베이스 생성
   - CREATE DATABASE minitter ;
   - 데이터 베이스 안에 여러 테이블 생성을 해 나간다.
- 데이터 베이스 사용
   - USE minitter ; ===> minitter 데이터 베이스를 사용하겠다는 명령어
- 테이블 생성
   - CREATE TABLES users (id INT NOT NULL, user_id INT NOT NULL, PRIMARY KEY (id)) ;
   - 각 테이블마다 PRIMARY KEY를 설정하고 다른 테이블의 PRIMARY KEY와 연결할 수 있다.
   - 데이터가 저장, 수정 될 때의 시간을 자동 저장 할 수 있다.
      - created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ===> NOT NULL 이면 디폴트 값으로 CURRENT_TIMESTAMP 를 사용 (현재 시각이 입력됨)
      - updated_at TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP ===> 값이 NULL이어도 되지만, 수정(업데이트)되면 수정 된 시간의 값을 자동으로 생성한다.
   - UNIQUE KEY email (email) ===> email 컬럼의 값은 유니크하게 설정하여, 중복 된 값이 올 수 없도록 한다.

#### SQL Alchemy
- `파이썬에서 DB와 연결하여 SQL을 실행할 수 있게 해주는 라이브러리`
- SQLAlchemy : ORM(Object Relational Mapper)
   - ORM : 관계형 데이터 베이스의 테이블들을 프로그래밍 언어어의 클래스 class 로 표현할 수 있게 해주는 것을 의미함
   - CRUD가 가능하다 (Create, Remove, Update, Delete)
   - ORM은 SQL 처럼 따로 배워야 함
- SQLAlchemy 설치
   - 파이썬 가상 환경 활성화 한 후 pip로 설치
   - pip install sqlalchemy
- SQLAlchemy에서 MysQL 사용하려면 MySQL용 DBAPI 설치 해야함
   - DB를 사용하기 위한 API
   - MySQL의 공식 파이썬 DBAPI 인 MySQL-Connector 사용
   - 종류 여러가지 있음
   - pip install mysql-connector-python

#### sql 서버 구축 설치 과정 정리
- sudo apt-get install mysql ===> pip install sqlalchemy ===> pip install mysql-connector-python

### 6) SQLAlchemy 를 사용한 minitter 개발
- 데이터 베이스를 연결한 플라스크 객체 app을 함수 밖에서도 사용하려면
   - from flask import current_app
   - return app 을 받는다.
- sqlalchemy 모듈의 create_engine 패키지를 사용하여 config 파일에 저장 된 데이터 베이스 서버 정보를 가져와 엔진을 만든다.
   - database = create_engine(app.config["DB_URL"])
   - app.database = database ===> 플라스크의 api 객체의 database에 이 데이터 베이스 엔진을 저장한다.
- 데이터 베이스 엔진 객체를 사용하여 SQL 쿼리를 사용하는 방법
   - 책의 tutorial은 예전 버전이라 실행이 안된다.
   - execute 속성을 사용하는 방식이 바뀌었음
   - with current_app.database.connect() as connection :
   -      user = connection.execute(text("""SELECT * FROM users"""))
   - current_app 매서드는 Flask 객체를 정의한 함수 바깥에서 Flask 객체를 사용할수 있게 해준다.
   - current_app을 사용하지 않고 create_app 함수 안에서 여러 함수들을 사용할 때는 app=Flask(__name__) 에서 app을 사용하면 된다.
- `sqlalchemy의 engine은 SQL문을 호출 할 수 있는 connection 객체를 갖는다.`
   - connection 객체는 DBAPI에 연결하기 위한 프록시 객체이다.
   - connection.execute() 가 처음 호출 되면 자동시작 동작으로 실행된다.
   - connection.commit() 이나 connection.rollback() 매서드가 호출 될때까지 트랜젝션이 그대로 유지된다.
   - engine.connect() : connection 객체를 호출하는 매서드
   - Connection 객체를 호출하는 매서드로 connect()와 begin()이 있고 begin()은 트랜젝션이 한번 열렸다 닫힌다.(?)
      - connect()는 commit()으로 트랜젝션 종료시점을 입력해줘야 하고, begin()은 commit() 없이 한번만 트랜젝션을 허용해준다.
- with app.database.connect() as con : 에서 SQL INSERT 문이 작동하지 않은 이유
   - SQL 문을 실행 한 후 con.commit() 으로 트랜젝션을 닫아(?) 줘야 한다. : connect()는 트랜젝션이 계속 열려 있다.
   - 또는 connect() 대신 begin()을 사용하면 connection.commit() 매서드로 닫지 않아도 SQL 문을 실행 할 수 있다.

## 5. (7장) 인증 authentication
- `API에서 공통적으로 구현되는 엔드포인트 중 하나`
   - private, public API 등 에서 모두 인증 엔드포인트가 요구 된다
   - private API 는 사용할 수 있는 사용자를 제한 해야 하므로 인증 엔드포인트 필요
   - public API 는 사용 횟수 제한, 남용 방지, 사용자 통계 등을 위해 인증 엔드포인트 구현
- `사용자의 비밀번호 암호화 구현 및 인증 엔드포인트 구현하여 미니터 API에 적용`
   - 인증 authentication
   - 사용자 비밀번호 암호화
   - Bcrypt
   - JWT(json web tokens)

### 1) 인증
- 사용자 user의 신원 identification을 확인 하는 절차
- 웹 사이트 로그인시 사용자의 아이디와 비밀번호를 확인하는 과정
- 로그인 기능을 구현하는 것이 인증 엔트포인트이다.
- 인증을 구현하는 시스템적 과정
   - 회원가입 : /"sign-up" : 아이디와 비밀번호 생성 
   - 아이디와 비밀번호를 데이터 베이스에 저장 : 비밀번호를 암호화해서 저장한다.
   - 사용자가 로그인할 때 아이디와 비밀번호를 입력한다.
   - 입력한 비밀번호를 암호화 한 후 데이터베이스에 저장한 암호화된 비밀번호화 비교한다.
   - 비밀번호가 일치하면 로그인 성공
   - 로그인 성공시 백엔드 API 서버는 access token을 프론트엔드 혹은 클라이언트에게 전송한다. : 캐쉬
   - 프론트엔드는 로그인 성공후 부터 사용자의 access token을 첨부하여 request를 서버에 전송하여 매번 로그인 하지 않아도 요청-응답이 이루어질 수 있도록 한다. (HTTP 통신의 특징 : stateless)

### 2) 사용자 비밀번호 암호화
- 왜? 필요한가?
- 사용자 비밀번호는 그대로 데이터 베이스에 저장하지 않는다. 
   - 외부 해킹의 위험성 : 대부분의 사용자들이 여러 사이트에서 동일한 비밀번호를 사용하는 경우가 많음
   - 내부 상황에 의해 데이터 베이스가 노출 될 가능성
      - 보안 인프라스트럭쳐, 보안 절차를 마련했다면 사실상 내부적인 위험에 더 노출 된 경우가 많다.
      - 개발자, 관련자들이 데이터 베이스에 접근 할 수 있기때문.

#### 암호화 방법
   - `단방향 해시 함수 : one-way hash function`
      - 복호화를 할 수 없는 암호화 알고리즘
      - 즉 실제 비밀번호에서 암호화 값을 구할 수는 있으나, 암호화 된 값에서 원래 비밀번호를 구할 수 없다.
      - 실제 비밀번호는 문자하나가 다르더라도 암호화된 해시 함수 값은 완전히 다른 값이 나올 수 있다.
      - 애벌런시 효과 : avalanche effect : 원본 값과 해시 값 사이에 직접적인 연관성이 없게 되는 것
      - python 의 단방향 해시 함수 모듈 : import hashlib
      - 단방향 해시 함수 암호화도 해킹에 취약한 면이 있다. 즉 해쉬값으로 원본값을 구할 수 있는 가능성이 있다.
         - 무수히 많은 해쉬값 샘플을 생성하여 대조
      - hash 함수는 원래 데이터 검색을 위해 설계된 것 (딕셔너리나 set 값 사용)으로 rainbow attack과 같은 해킹 방법에 사용되어 매우 많은 조합을 빠른시간안에 적용하는데 사용되기도 한다.
      - 대부분 user의 비밀번호가 복잡하지 않으므로, 이러한 방법으로 단시간에 해쉬값을 복호화 할 수 있다.
   - `bcrypt 암호 알고리즘`
      - 단방향 해쉬 함수의 취약점을 보완하기 위한 방법
         - salting 과 key stretching 특징
      - salting : 간을 맞추기 위해 소금을 추가하듯이. 비밀번호에 랜덤데이터를 추가함. 해킹을 당하여 비밀번호를 알아내도 어떤 부분이 유저가 입력한 비밀번호인지 랜덤값인지 알 수 없다.
      - key stretching : 해시값을 여러번 반복하는 방식. 비번 -> 해시 비번 -> 해시 비번 -> ... -> 해시 비번
      - salting과 key stretching 방식을 구현한 해시 함수 중 하나 : bcrypt
      - pip install bcrypt : bcrypt 알고리즘을 구현하기 위하여 제공되는 외부 라이브러리

### 3) access token
- 백엔드 서버에서 access token을 프로트엔드로 전송 : 로그인 성공에 대한 access token 값
   - 프론트엔드에서 access token을  받아서 보관하고 있다가 HTTP request에 첨부하여 다시 서버에 전송하여 현재 유저가 로그인이 이미 되었다는 것을 전달한다.
   - HTTP 통신은 stateless 특징에 의해서 모든 요청-응답이 독립적이다.
   - 따라서 현재 HTTP 통신에서 이전에 인증이 진행됐는지 알 수 없다. 따라서 로그인 정보를 access token에 담아서 서버에 전송하여 해당 사용자가 로그인에 성공했다는 것을 확인한다.
   - 프론트엔드와 백엔드 서버가 서로 HTTP 요청 응답을 주고 받을 때 access token이 담긴 메시지를 주고 받는다.

#### JWT : json web tokens : access token을 생성하는 방법 중 하나
- json 데이터를 token으로 변화하는 방식
   - 프론트엔드는 쿠키 등에 access token을 저장하고 있다가 HTTP 요청을 백엔드 서버 API에 보낼때 이것을 첨부하여 보낸다.
   - 백엔드 API 서버는 이 access token을 복호화하여 json 데이터를 얻어 해당 사용자가 이미 로그인 했다는 것을 확인 한다.
   - jwt는 access token이 백엔드 API 서버에서 생성한 것인지, 임의로 다른 사용자가 생성한 token 인지 확인 할 수 있는 기능이 있다.
      - json 을 token화 하는 것은 API 서버가 아니어도 할 수 있다.

#### JWT 구조
- jwt의 일반적인 형태 : xxxxx.yyyyy.zzzzz
   - xxxxx : header, yyyyy : payload, zzzzz : signature
- header
   - token type과 해시 알고리즘 지정
   - { "alg": "HS256", "typ": "JWT" }
- payload
   - 서버간에 전송하고자 하는 데이터 부분
   - HTTP 메시지에서 body에 해당
   - { "user_id": 2, "exp": 15348720 }
   - payload는 base64url로 코드화 되어 저장되는데 암호화 된것이 아니어서 복원이 가능하므로 민감정보는 담지 않는다.
- signature
   - JWT가 해당 token이 원본이라는 것을 확인할 때 사용하는 부분
   - Base64URL 코드화 된 header, payload, jwt secret를 header에 지정된 암호화 방식으로 암호화하여 전송한다.
   - 프론트엔드에서 백엔드 API 서버로 HTTP 요청을 보낼때 JWT을 담아서 보내는데, 백엔드 API 서버는 JWT의 signature 부분을 통해서 원본인지 아닌지를 확인한다.
- 파이썬 라이브러리
   - pip install pyJWT : 파이썬에서 JWT를 생성하고 복호화 할 수 있게 해주는 라이브러리.   
      
### 4) 인증 절차 구현
- '로그인'을 한 사용자에 대해서 follow, unfollow, tweet 엔드포인트에 접근할 수 있도록 한다.
   - 1. 회원가입시 비밀번호를 입력하면 bcrypt.hashpw()로 단변수 해쉬값 hashed_password 으로 변환하여 저장한다.
      - bcrypt : salting (랜덤값 추가), key stretching(키 스트래칭, 해쉬값을 여러번 적용)
   - 2. 로그인 시 입력한 비밀번호와 저장된 해쉬값 비번을 bcrypt.checkpw()로 같은지 비교한다.
      - True, False
   - 3. True 이면 id와 signature 값을 저장한 payload (jwt의 구조중 body에 해당) json 데이터를 만들고 해당 jwt 해쉬값에서 id를 추출한다.
   - 4. 이것을 jwt.encode()를 사용하여 access token 값을 만든다.
   - 5. 인증 기능을 하는 함수 login_reuqired() 함수를 데코레이터 함수로 만들고 로그인을 한 사용자의 acess token을 사용하여 id를 확인 하고 전역변수에 넘긴다.
   - 6. tweet, follow, unfollow 엔드포인에 login_requierd 데코레이터 함수를 적용하여, HTTP request 메시지에 Authorization 값을 입력하지 않으면 에러가 발생하도록 한다.
- 즉 로그인을 통과한 유저의 acess token을 로그인 후 기능을 사용하기 위한 인증값으로 사용한다.
   - 모든 HTTP 통신에 인증 여부 정보를 첨부
- git hub에서 clone 받은 프론트엔드 페이지를 실행하면 minitter api 일부 기능만 작동함


## 6. (8장) Unit Test
- `test : 개발 시스템이 정상적으로 작동하는지 확인 하는 과정`

### 1) 테스트 자동화의 중요성
- 시스템 테스트에서 가장 중요한 부분은 테스트를 자동화 하는 것
- 매뉴얼 테스트 manual test : 사람이 직접 실행하여 테스트 하는 방식, 대부분의 시스템 테스트 방식
   - 장점 : 누구든지 직관적으로, 큰 계획없이 테스트 실행 가능
   - 단점 : 테스트 실행 속도가 느리고, 테스트를 자주 할 수 없음, 부정확 확률이 높은편
   - 대체로 시스템 개발하는 스타트업에선 테스트 과정을 빨리 넘어감
   - 인력 문제, 시간 문제 등
   - 최우선 순위는 시스템 개발을 완료하고 서비스 출시하는 것에 초점이 맞춰짐
   - 서비스를 첫 출시할 때 팀원 전부가 매뉴얼 테스트를 진행하기도..
   - 큰 규모의 출시가 아니면 자세한 시스템 테스트는 안하기도...
   - 서비스를 테스트 하지 않은 경우 시스템 버그가 생길 확률이 높음
- 자동화 테스트 auto test
   - 자주 실행, 정확도 높고, 반복적으로, 시스템의 모든 부분을 테스트함 
- `테스트의 방법`
   - 기능을 중점으로 하는 경우
      - UI test / End-To-End test
      - integration test
      - unit test

### 2) UI test = End To End test
- 시스템의 UI (user interface)를 사용한 테스트
   - 웹 브라우저를 통해서 웹 사이트에 접속
   - UI에 직접 입력, 클릭 등을 함
- 장점
   - 사용자가 실제 시스템을 사용하는 방식과 가장 동일하게 테스트 함
   - 정확하고 확실하게 테스트 할 수 있음
- UI test (end-to-end) 단점
   - 시간이 많이 소요됨
   - 프론트앤드, 백엔드 모든 시스템을 실행하고 연결해야 가능 한 테스트
   - 자동화하기 까다롭다.
   - selenium 같은 UI test 프레임워크 사용

### 3) integration test
- 서버를 실행하고, 테스트 HTTP request 요청을 실행하여 테스트 하는 방식
   - HTTP 또는 서버를 작동시킬 수 있는 요청이나 명령어 등을 사용하기도
   - 터미널에서 테스트용 HTTP 요청을 로컬의 API 서버에 전송하여 올바른 HTTP response가 리턴되는 지 확인하는 방식
   - 실제 시스템을 실행하고 테스트 하는 것은 UI test와 비슷함, UI test는 프론트엔드, 백엔드, 기타 서비스의 모든 시스템을 전부 실행하고 테스트하는 방식
   - integration test는 모든 시스템에 대한 테스트가 아니라 테스트하려는 해당 시스템 예컨데 백엔드 API 시스템만 테스트하는 방식
   - 백엔드 API 시스템 같이 UI 요소가 없는 시스템을 테스트하므로 시간이 단축되고, 자동화도 상대적으로 쉽다.
   - 그래도 여전히 자동화를 하려면 까다로운 부분이 많다.
   - 전체 테스트 과정 중 20% 정도를 할당하면 좋다.

### 4) unit test
- UI test, integration test와 조금 다름
   - unit : 단위 ===> 코드의 함수나 매소드 별로 테스트
- 시스템을 실행하고 테스트한다기 보다 코드를 테스트하는 개념
   - 코드를 테스트하는 코드를 작성해서 테스트
   - 코드를 코드로 테스트 하는 방식
- plus() 함수 테스트
   - assert plus(2) == 4
   - assert False 이면 AssertionError Exception 반환됨
   - 이러한 방식이 unit test
- `장점`
   - 코드를 코드로 테스트하므로 자동화가 100% 가능
   - 언제든지 반복적으로 실행 가능
   - 실행 속도도 빠름
   - 디버깅이 비교적 쉽다. 함수 단위로 테스트를 하므로 문제를 파악하기 쉽다.
- `단점`
   - 전체 시스템을 테스트하는데 제한적이다.
   - unit 함수별 테스트가 끝났다고 하더라도 전체적으로 연결되었을때 잘 작동하는지 확신하기 어렵다.
   - 따라서 integration test 나 UI test와 함께 사용한다.
- 이러한 방식으로 모든 함수와 모든 매소드를 테스트 한다.
- 전체 시스템에 대한 테스트 비중, 테스트 피라미드
   - 10% UI test
   - 20% integration test
   - 70% unit test

### 5) pytest 실행
- python3에 unittest 모듈 있음
- `외부 모듈인 pytest를 사용하여 unit test 실행`
   - unittest 모듈보다 pytest가 더 직관적이고 간결하게 만들 수 있다. 
   - pip install pytest
- `pytest의 특징`
   - 파일 앞 부분에 test_ 라는 부분이 있어야만 테스트 파일로 인식한다. (test_app_sql.py 등)
   - 함수 앞에도 test_ 라고 되어 있는 함수만 unit test 함수로 인식한다. (test_plus() 등)
      - def test_multiply_by_two() :
      -      assert multiply_by_two(4) == 7
   - test_ex_file.py 를 만들고 해당 디렉토리에서 pytest 커맨드를 입력하면 자동으로 테스트 후 어떤 부분이 문제인지 결과를 반환해준다.

### 6) minitter API unit test 순서
- Flask 로 구현한 엔드포인트도 함수이므로 unit test가 가능하다.
   - 1. `test_endpoints.py 생성`
   - 2. `테스트용 데이터 베이스 생성` : test 데이터를 읽고 저장할 데이터 베이스 만들기 : minitter 데이터 베이스와 동일
      - CREATE DATABASE test_db;
      - CREATE TABLE users ()
   - 3. `test database 접속 설정` : config.py 에 추가 ===> 여기까지 데이터베이스 생성하고 접속 설정하 동일
      - config.py 파일에서 URL의 패턴을 정확하게 입력 해주어야한다. f"{test_db['PORT']}"
   - 4. `test_endpoints.py 에 config.py의 설정을 읽는 코드 입력`
      - @pytest.fixture : decorator 함수 실행 시 import pytest 필요함
         - @pytest.fixfure 데코레이터 함수가 적용 된 함수가 다른 함수의 파라미터로 사용된 경우 자동으로 넘겨준다. 여기에서는 def api() 함수가 함수에서 사용되면 자동으로 넘겨준다.
      - from app import create_app : 여기서 app은 minitter API 소스코드 파일 app.py를 의미한다.
         - app.py에서 플라스크 객체인 app 모듈을  불러오고 app 모듈에서 create_app() 매서드를 임포트
   - 5. `Flask의 test_client 함수 사용` : 엔드포인트를 테스트하려면 request에 methods를 보내야 함. 그러려면 API 서버를 실행해야하는데 그렇지 않기 때문에 GET HTTP 요청을 보낼 수 없음 ===> test_client 함수를 사용하여 unit test 상에서 엔드포인트를 테스트 할 수 있다. 실제로 HTTP 전송을 하는 것과 같은 기능. 네트워크상에서 이뤄지는 것이 아니라 메모리상에서만 실행 됨.
      - api = app.test_client()
      - api.get('/ping')
   - 6. `pytset 실행전과 실행후에 자동으로 실행되는 함수를 만들고 테스트 데이터의 입력과 삭제를 자동으로 처리한다.`
      - pytest에서 인식한다.
      - 이렇게 자동으로 처리하지 않으면 test_db에 중복값을 허용하지 않기때문에 테스트를 할때마다 새로운 user 데이터를 생성해주어야 한다.
      - def setup_function() : 테스트 실행전에 자동으로 실행되는 함수이다. : 여기에 test user data를 test_db의 users 테이블에 생성하는 코드를 넣는다.
      - def teardown_function() : 테스트 실행후에 자동으로 실행되는 함수이다. : 여기에 sqlalchemy 명령어를 사용하여 test_db에 생성된 test user data를 삭제하는 코드를 넣는다.
      - FOREIGN_KEY 가 설정되어 있기때문에 TRUNCATE (삭제하기) 명령어를 사용할 수 없다. 따라서 FOREIGN_KEY를 임시적으로 비활성화한 후 다시 활성화 하는 명령어를 입력하여 데이터가 삭제되도록 한다.
      - 현업에서는 사용하면 안된다고 함...
   - 7. `테스트 하고자 하는 기능의 이름 앞에 test_를 붙여서 함수를 만든다.`
      - def test_tweet(api) : test_client() 객체를 @pytest.fixture 데코레이터 함수로부터 넘겨 받는다.
      - 각 기능은 minitter의 소스코드인 app.py에 test_client 객체인 api를 통해서 로컬 메모리상에 HTTP 요청과 응답을 주고 받음으로써 minitter의 기능을 테스트한다. (api.get(), api.post())
      - 따라서 app.py에 구현된 인증 프로세스에 맞춰서 순서데로 코드를 입력한다.
   - 8. `def test_tweet()`
      - api 객체를 받는다.
      - access_token을 받기 위해서 /login URI에 POST 요청을 보낸다.
      - request 메시지의 요소별로 입력 
         - data : json.dumps() 매서드에 email과 password를 dict에 담는다.
         - content_type : 'application/json'
      - request 에 대한 response로 app.py의 login() 함수로부터 access_token을 반환받는다. (user_id, exp 값이 들어있는 json 데이터를 jwt 모듈을 사용하여 암호화 한 값)
      - api 객체를 사용하여 /tweet URI에 POST 요청을 보낸다.
         - data : json.dumps() 매서드에 tweet 내용을 담는다.
         - content_type : 'application/json'
         - header : access_token 값을 담는다.
      - header 값으로 access_token 값을 입력해야, app.py의 /tweet 엔드포인트가 실행될 때 login_required() 데코레이터 함수를 통해 인증절차를 거치게 된다.
      - /tweet 엔드포인트가 인증을 거쳐 제대로 실행되면  response 값을 반환받는다.
      - api 객체를 사용하여 /timeline 엔드포인트에 POST 요청을 보낸다.
      - app.py의 /timeline 엔드포인트도 login_required 데코레이터를 거쳐 인증을 해야하므로 요청 메시지에 header 값으로 access_token 값을 입력해준다.

### 7) unit test 핵심 정리
- pytest 사용
- 현재 디렉토리의 파일 중 test_로 시작하는 파일을 테스트함
   - config.py : mysql server의 데이터베이스에 접속하기 위한 코드
   - app.py : api의 소스코드 (flask의 app을 반환받는다.)
   - test_file.py : pytest용 파일, config.py와 app.py를 import 하여 사용할 수 있다. 
- 테스트 명령어 : pytest -r no:warnings -vv -s
   - python -m pytest ./test_service.py -vv -s -r no:warning : 특정 테스트 파일만 pytest 할 수 있다.
- @pytest.fixture : 이 데코레이터가 적용된 함수의 이름을 다른 함수에서 호출하면 자동으로 보낸다. 따라서 flask의 test_client 객체를 반환하도록 하고 다른 함수에서 이 객체를 호출하여 테스트한다.
   - app.test_client() : 서비스 api의 소스코드 app.py를 호출하여 app을 return 받고, 이 app의 test_client() 매서드를 사용하여 test를 진행한다. test_client 매서드는 api에 연결하지 않고 로컬 메모리를 사용하여 엔드포인트의 기능에 HTTP 요청, 응답을 보낸다.
- pytest의 특별한 기능
   - def setup_function() : 테스트 시작 전 실행하는 함수 : test user 데이터를 server에 저장하는 명령어 등
   - def teardown_function() : 테스트가 끝난 후 실행하는 함수 : test user 관련 데이터를 server에서 삭제하는 명령어 등
- 엔드포인트 작동 테스트 : api 소스코드에 만들어 놓은 각 엔드포인트를 test_client 매서드를 사용하여 기능을 테스트 한다.
   - 테스트하려는 함수를 만들고 이름앞에 test_를 붙여야 pytest가 인식한다.
   - HTTP request methods : api.get(), api.post()
      - api.post('/tweet', data=json.dumps({'tweet': 'hello'}), Content-Type='application/json')
   - 테스트 방법은 api 소스코드에 만든 엔드포인트의 코드를 호출하는 json 데이터를 만들고 이것을 methods에 입력한다.
      - response 값을 변수에 저장한 후 검증하고 싶은 내용을 코드로 작성한다.
      - assert resp.status_code == 200
      - assert b'access_token' in resp.data
   - 하나의 엔드포인트를 테스트하기 위해서, 소스코드의 시스템 프로세스 대로 하나하나 입력하여 그 흐름을 검토한다.
   - <ex> /tweets 엔드포인트를 테스트 하려면
      - 1. /sign-up 엔드포인트 요청 (또는 setup_function()에 명령어 입력)
      - 2. /login 엔드포인트 요청 : access_token을 response 받는다.
      - 3. /tweets 엔드포인트 요청 : tweet 메시지를 보내기 위한 request 메시지 작성, access_token을 header 값으로 사용하여, login_required() 데코레이터 함수의 인증절차를 통과한다.
      - 4. 성공하면 HTTP 응답 메지싲 중 status line에 저장된 status code 값 200을 반환 받으므로 이것을 테스트 기준으로 삼는다.
      - 5. /timeline 엔드포인트 요청 : tweet을 성공했다면 타임라인을 확인 하고 이것을 테스트 기준으로 삼는다.
   - 반드시 엔드포인만의 기능을 테스트 해야된다는 것은 아니다. 위의 방법으로 엔드포인트들의 기능을 확인 할 수 있는 어떤 논리적 접근법을 가진 테스트 함수들을 만들고 테스트 기준을 적용하면 된다.
   - 확실히 pytest를 통해 unit test 코드를 만들어 놓는다면, api 서비스가 점차 고도화 될때 어떤 부분에서 에러가 발생하는지 쉽게 파악 할 수 있을 것 같다.
   - "unit test는 개발자들의 방패이다. unit test가 잘 구현되어 있으면 더 쉽게 기존 코드를 업데이트하고 확장시킬 수 있다. 새로 업데이트 된 코드를 배포하거나 푸시 할 때 발생하는 버그를 고칠 수 있다. 버그가 unit test 이후의 과정에서 발견되면 integration test 나 UI test 등, 버그를 고치는 비용이 더 늘어나게 된다. 버그를 분석해야하는 범위도 더 넓어진다. 대부분의 버그는 unit test 만 잘 구현해도 고칠 수 있는 것들이 많다. 즉 버그는 반드시 생기기 마련인데, 발견 시기가 늦어지면 늦어질 수록 고치는 비용이 높아지고, 코드를 개발한 개발자만 골치 아파진다. 코드 개발과 함께 unit test를 잘 만들자."

## 7. AWS에 배포하기

### 1) API를 AWS에 배포하기
- EC2, RDS, load balance 서비스 사용
   - EC2 : Elastic Compute Cloud (가상 서버)
   - RDS : Relational Database Service (클라우드의 DB)
   - ALB : Application Load Balancer (로드밸런서, 라우팅을 EC2에 배분한다.)
   - 이 외에도 여러가지 서비스들이 있음
- API 코드를 깃헙에 올리고 (로컬에서 git hub로 push)
- RDS 서비스의 MySQL을 데이터 베이스로 설정
- EC2 서버를 만들고 각 퍼블릭 IP를 통해서 접속 (로컬에서 EC2 또는 AWS의 자체 콘솔에서 접속가능)
- git hup에서 API 소스코드를 받는다. (git colne)
- API 관련 소스코드를 다운 받고, 관련 패키지+라이브러리를 설치하면 API 배포 완료
- load balance를 설정하여 외부에서도 API를 사용할 수 있도록 한다.
- load balance의 대상그룹으로 EC2를 설정하고
- EC2를 RDS와 연결한다. (RDS의 mysql db에 데이터를 생성, 조회 할 수 있게 된다.)
- AWS, AWS EC2, AWS RDS, AWS ALB, 배포(deploy)

### 2) AWS
- `AWS : Amazon Web Service`
- 클라우드 서비스 cloud service
   - 시스템 배포 및 운영을 위해서 필요한 서버, 데이터베이스, 네트워크 등의 물리적 장치를 로컬에 설치하지 않고 AWS 사이트 혹은 인터페이스를 통해서 쉽게 설정할 수 있는 서비스.
   - AWS, Google Cloud 등의 클라우드 서비스가 많이 사용됨 (현재는 다른 클라우드 서비스들이 많아짐)

#### AWS 가입
- 일정 기간 무료 이용
- 서버, 데이터 베이스 등 생성한 것들을 삭제하지 않으면 비용이 청구될 수 있다.

#### RDS
- `RDS : Relational Database Service`
   - 원하는 데이터베이스 시스템, 버전, 설정 등을 하고 바로 사용가능
   - 개발자가 직접 데이터베이스를 운영하는 것보다 더 저렴한 편이다.
- seoul 지역 설정
- MySQL 설정파일 : default 되어 있지만 utf-8로 바꿔주어야 함. minitter는 한국말을 사용하므로.
- parameter group 설정
   - 여러가지 parameter 값들을 필요한 값으로 변경해준다.
- 이 설정을 토대로 mysql 데이터베이스를 생성한다.

### 3) AWS 생성 과정
- 회원 가입 : rock / Lt_6 / hshkuber
- root 사용자

#### RDS (Relational Database Service)
- seoul 선택
- 서비스에서 RDS 검색 ===> RDS 선택
- 파라미터 그룹 ===> 파라미터 그룹 생성 ===> 그룹 패밀리 (mysql8.0) ===> 이름 (hshbackend)
- minitter api의 한글사용을 위해서 몇가지 파라미터값을 변경
   - 생성한 파라미터 그룹 누르고 ===> 편집 ===> 파라미터 검색하여 원하는 값으로 변경 (직접 입력) ===> 변경사항 저장 ===> 변경한 사항 확인
   - 대쉬보드 ===> 데이버베이스 생성 ===> 엔진 옵션 (mysql) ===> 엔진버전 (파라미터에서 설정한 버전이 선택됨 mysql8.0) ===> 템플릿에서 free tier 선택 ===> 설정 (DB 인스턴스 식별자 : backend-test-1, 마스터 이름 : root, 마스터 암호 : hshkuber1234) ===> 인스턴스 구성 (엔진에서 지원하는 옵션들 설정, 기본설정) ===> 연결 (컴퓨팅 리소스 : EC2 연결안함, 네트워크 유형 : IPv4, 퍼블릭 엑세스 (yes), 데이터베이스 포트 (3306), 나머지 기타 항목 기본설정 ===> 추가구성 (초기데이터베이스 이름 변경 : mydb, db파라미터 그룹 : hshbackend, 옵션그룹 : default:mysql_8_0) ===> 나머지 기타 항목 기본설정 ====> 데이터베이스 생성
- 데이터베이스 생성 후 인스턴스에 방금 만든 데이터베이스가 생성 된다.
- 데이터베이스 누르면 정보 페이지 ===> 엔드포인트 주소 확인 (이 주소로 데이터베이스에 접속함)
   - backend-test-1.c1mer0obgfjg.ap-northeast-2.rds.amazonaws.com
- 보안그룹 (네트워크 방화벽 설정) ===> 인바운드 규칙 ===> 인바운드규칙편집 ===> (유형 : mysql/aurora, protocol : TCP, Port Range : 3306, Source : 내IP, 내IP 선택시 에러가 나면 새규칙 추가하여 입력하면 됨)
   - 어디서든 접근할 수 있도록 설정함
   - 실무에서는 이렇게 하면 안된다. 해킹 등 보안 문제.
- RDS를 사용하여 데이터베이스를 생성하고 설정했다. AWS 클라우드에서 mydb 데이터베이스가 운영되고 있다. 
- 터미널에서 AWS 데이터베이스 접속
   - mysql -h <endpoint addr> -u <master username> -p
   - mysql -h backend-test-1.c1mer0obgfjg.ap-northeast-2.rds.amazonaws.com -u root -p
   - minitter 데이터베이스와 똑같이 테이블 설정
   
#### EC2 (Elastic compute cloud)
- `EC2는 AWS에서 사용하는 가상서버`
   - "클라우드용 가상서버"
- `"EC2 Instance에 API를 배포한다."`
   - 각각의 서버에 모두 API 소스코드를 저장하고 관련 패키지를 설치한다.
   - 즉 이제 API 서비스를 가상 서버에서도 실행 할 수 있게 된 것.
- 여러가지 옵션 제공
   - 사양 좋을 수록 비쌈
   - 운영체제도 우분투, centos, 윈도우서버 등 다양하다.
- 서비스 검색창에서 EC2 ===> EC2 이동  ===> 인스턴스 시작 ===> os 이미지 선택 (ubuntu 22.04) ===> 인스턴스 유형 (t2.micro 프리티어 사용가능함) ===> 네트워크 설정 편집 (퍼블릭 IP 자동할당 : 활성화, 기존보안그룹, default sg-080d8~~으로 설정함) ===> 요약에서 인스턴스 갯수 2개 설정 ===> EBS 볼륨 (탄력적 블록 스토어로 인스턴스에 설치되는 저장 장치 같은 것(??), 크기 : 20gb 프리티어 30gb까지 설정 가능) ===> 인스턴스 시작===> pem key 생성 (키페어 생성) : pem key를 사용하여 EC2 서버에 SSH 접속을 할 수 있다. ===> 키페어 이름(backend_test) ===> 키페어 유형 (RSA) ===> 파일형식 (.pem) ===> 다운로드 됨 ===> 인스턴스 시작 ===> 시작 완료 페이지
- 옆에 메뉴에서 인스턴스 클릭 ===> 인스턴스 2개 정보나옴 ===> 아무거나 하나 누르고 ===> 보안그룹의 번호 누르고 ===> 인바운드 규칙 편집 ===> 보안그룹 새규칙 추가 ===> SSH (프로토콜 : TCP, 포트 범위 : 22, 소스 : 내IP), HTTP (프로토콜 : TCP, 포트범위 : 80 (책에선 5000인데 변경이 안됨), 소스 : 내IP)
- 보안그룹의 인바운드 규칙이 3개가 생김 : RDS의 보안그룹에서 생성한 규칙 1개, EC2의 보안그룹에서 생성한 규칙 2개
- 터미널에서 EC2 instance의 public ip 주소를 통해서 접속 한다. : "미니터 API를 배포하기 위해서"
   - ssh -i <pem key 경로> ubuntu@<EC2 public ip 주소>
   - pem key 파일이 공개가 되어 있어서 에러가 발생, 권한설정 변경해주기
      - "unprotect", "too open" 
   - chmod 600 backend_test.pem : backend_test.pem 키의 권한설정을 변경
   - 다시 접속하면 잘 된다.
   - 두 가지 인스턴스의 각각 퍼블릭 ip 주소로 접속 가능하다.
- 사용안할 때는 RDS와 EC2 중지 (비용 안나옴)
   - RDS 중지 : 일시중지 기능, 내용 그대로 유지, 다시 킬 수 있음 (시작)
   - EC2 인스턴스 중지 : 파워 off, 내용 그대로 유지, 다시 킬 수 있음 (시작)
      - EC2 인스턴스의 종료 : 내용 삭제 및 종료
- EC2 인스턴스는 AWS에서도 연결이 가능하다.      
   - 해당 인스턴스 선택 ===> 연결 ===> 연결 하면 콘솔창이 뜬다.
   - 로컬에서 접속하여 만든 디렉토리가 있는 것을 볼 수 있다. 
   
### 4) ERROR : git hub의 push 권한인증이 변경 됨
- DSS12 에서는 SSH key를 생성하고  github 에 이 키를 등록 하여 인증없이 사용했었음
   - SSH 키 설정을 root 단위에서 추가로 설정했었던 것 같기도 함... 
- ubuntu linux 에서는 push 할때 username, password를 입력해야 한다.
   - username : saint-hong
   - password : access token
   - access token 생성 관련 페이지, 여기에서 "Creating a fine-grained personal access token" 부분을 따라하면 된다. 
   - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token
   - 액세스 토큰을 만들때 특정 repository에만 사용할 수 있게 할 수 있다. 
   - 다양한 권한 설정을 할 수 있다.
   - study-backend 용 토큰 : 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
- push 할때마다 이름과 토큰을 입력해야하는지 다른 방법이 있는지 확인 필요

### 5) ERROR : EC2 instance의 pem key 분실 혹은 삭제
- EC2 instance의 접속시 필요한 pem key의 분실 혹은 삭제시 복잡함
- 인스턴스에 새로운 pem key를 적용해야하는데 방법이 매우 복잡하다.
   - 새 키페어 만들고 EBS 볼륨을 분리시켰다가 새 키페어 적용하고 다시 볼륨 연결하고 등등..
- 인스턴스 (가상서버)에 아직 패키지나 라이브러리등을 설치 하지 않았으므로 새로 만드는게 낫다. 
- 간단하게 새로 만들 수 있다.
- 새로운 인스턴스와 키페어 파일을 받고 .pem 연결하면 연결된다.   
   
### 6) ERROR : !!!! 새로운 장소에서 RDS와 EC2 접속시 !!!!
- 보안그룹의 인바운드 규칙 3가지의 소스 설정이 "내IP"로 되어 있음
   - 따라서 장소가 바뀌었으므로 다시 내IP로 설정을 하여 현재 IP 주소로 적용해주어야 한다.
- 소스의 설정을 anywhere로 변경이 됐다.
   - 처음에 설정할 때는 안됐다..
   - 내Ip 재 설정 필요없이 어디에서든지 접속이 가능하도록 되었다.

## 8. 미니터 API 배포 serving, deploy

### 1) 소스코드 수정 : 배포를 하려면 기존 minitter 소스코드에서 코드를 일부 수정해주어야 한다.
- 웹 서버 설정 : 현재까지는 개발용 서버를 사용했다. 이것을 프로덕션 서버로 바꿔준다.
   - 프로덕션 서버에서 Flask가 실행되도록 설정을 한다.

#### flask-twisted 설치 (라이브러리)
- flask가 twisted 안에서 실행되도록 한다.
   - pip install flask-twisted

#### flask_script 설치 (플러그인)
- twisted를 이용해서 flask를 실행할 때 필요한 플러그인
   - pip install flask_script

#### minitter api가 있는 디렉토리에 setup.py 파일 + requirements.text 생성
- requirements.text 파일은 EC2 instance에 미니터 api를 배포할 때 설치할 패키지, 라이브러리 목록이다.
   - pip freeze > requirements.text : 가상환경에서 실행해야 minitter api 실행에 관련된 패키지, 라이브러리 목록을 가져올 수 있다. 다른 가상환경이거나, 가상환경이 아닌 경우 상관없는 패키지들이 목록으로 만들어지게 된다.
      - 따라서 프로젝트 단위로 가상환경을 만들고 개발하고 pip 설치 하는 것을 추천한다는 것과 같다.

#### config.py 파일 변경
- 데이터베이스 설정 변경 : 로컬 호스트 데이터베이스 -> AWS RDS 데이터베이스로 변경
   - host, user, password, database 모두 RDS backend-test-1 데이터베이스로 바꿔줘야 한다.
   - user : root, password : hshkuber1234, host : RDS 엔드포인트, database : minitter
   - AWS RDS DB 인스턴스에 연결시
      - host : 엔드포인트

### 2) git hub를 통해서 minitter api 배포
- config.py는 실무에서는 git hub에 push 하지 않는다.
   - repo 만들고 ===> .gitignore (Python) ===> Public (중요한 코드는 private)
   - 디렉토리에서 git repository 생성 및 커밋
      - git init ===> git add . (현재 디렉토리의 파일을 add) ===> git commit -m "minitter api" ===> 깃헙 연결 (새로 만든 레포지토리와 연결, git remote add origin <repo url>) ===> git push -u origin master (minitter 관련 파일 push)
      - github에 repo 만들고 ===> 로컬에서 git repo 만들 디렉토리에서 ===> git clone <repo 주소> ===> git add ===> git commit ===> git push ===> username, password(토큰) (이 방법이 좀 더 간편함)
      - study-backend : 로컬의 git repo 디렉토리

#### github repo에 push 완료 후 EC2에 배포
- 로컬 터미널에서 EC2 인스턴스에 접속
   - 접속시 퍼블릭 IPv4 주소가 달라진다. aws 콘솔에서 확인한 후 입력해야 함.

### 3) EC2 인스턴스 접속 후 deploy key 생성
- deploy key는 EC2 server에서 github 키를 받아오기 위해서 사용된다.
   - github 용 read-only SSH key
   - 배포를 위해 github에서 먼저 받아와야 하므로 deploy key라고 함
   - ssh-keygen -t rsa -b 4096 -C "rock.me.baby@me.com"
   - ~/.ssh 폴더에 id_rsa, id_rsa.pub 파일로 저장됨 (password : deploy123)

#### deploy key 복사 후 github 레포지토리에 deploy key로 등록 해야함
- EC2 인스턴스 접속 상태에서 ===> cat ~/.ssh/id_rsa.pub ===> 복사
   - git hub의 레포지토리 ===> settings ===> Deploy key ===> 붙여넣기
      - Tittle : minitter_deploy_key

#### ubuntu EC2 서버에서 git clone 하여 minitter api 파일들을 가져온다.
- study-backend 디렉토리 생성
   - git hub 과 연결된 디렉토리

### 4) ubuntu EC2 서버에 miniconda 설치
- 아나콘다는 데이터 사이언스용 패키지들이나 라이브러리가 있어서 용량이 큼
- 미니콘다 설치할 디렉토리로 이동
   - miniconda 다운로드 페이지 : https://docs.conda.io/projects/miniconda/en/latest/
   - Linux 용 64bit 항목에서 링크주소 복사
   - 터미널에서 wget <링크주소> ===> 설치 스크립트 파일이 다운로드 됨
   - bash ./Miniconda-latest-Linux-x86_64.sh
   - 여러가지 설명글 엔터로 이동 ===> 마지막에 동의여부에 yse
   - /home/ubuntu/miniconda3 경로에 설치 여부 ===> 엔터
   - 인스턴스 접속 끊었다가 다시 접속 후 conda list 하면 설치된 패키지 리스트 나옴 설치 완료
- ubuntu EC2 서버에 conda 가상환경 생성
   - conda create --name backendenv python=3.8.18
   - 로컬의 minitter 개발 가상환경과 동일하게 생성
   - 가상환경 활성화 : conda activate backendenv
- ubuntu EC2 backendenv 가상환경에서 github repo로 이동 후 requirement 설치
   - pip install -r requirements.txt
   - reqirements.text 파일에 패키지이름과 버전이 있고, path가 포함되어 있는 것들이 있음. 이런경우는 파일을 생성한 위치에서의 path가 입력되므로, 가상서버에서 설치하려고 하면 path가 존재하지 않아 에러가 발생한다. 설치가 안된다.
    - 이런경우 requirements.text 파일에서 path에 해당하는 부분을 삭제한 후 다시 설치를 하면 된다.
       - vim에서 :%s/file.* //
    - minitter api를 실행하기 위해서 로컬의 backendenv 에서 설치했던 패키지와 라이브러리들이 동일하게 설치 된다.
    - ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: '/home/conda/feedstock_root/build_artifacts/asttokens_1694046349000/work'

### 5) api 실행
- setup.py 파일을 실행하면, api를 실행한다.
- nohup python setup.py runserver --host=0.0.0.0 &
   - nohup 으로 해도 되고, FLASK_APP으로 연결해도 된다. 로컬에서 실행한 것과 똑같이 사용 가능(가상환경에서)

#### !!! error !!! : api 연결이 안된다.
- nohup으로 파일을 실행한 후 nohup.out 파일이 생성됨, cat nohup.out 을 확인하면 현재 어떤 상황인지 메시지가 나온다.
   - nohup.out 파일을 삭제해도 다시 nohup을 실행하면 새로 생긴다. 여기에 nohup 상황 메시지가 저장되는 것 같다.
   - setup.py 파일의 from flask_script import Manger를 실행하는 과정에서 error가 난것으로 보인다.
   - 이와 관련한 모듈을 실행하는 과정에서 from flask._compat import text_type 에서 문제가 생긴 것으로 보인다.
   - No Module named 'flask._compat' : 해당 모듈이 없거나, 못 찾는 것
   - 해당 오류가 발생한 위치의 __init__.py 15 line : from flask._compat import text_type 를 ===> from flask_script._compat import text_type로 바꿔주면 에러가 사라진다. Flask의 버전을 바꾸라는 해결방법도 있지만 이 해결방법이 쉬운 것 같음

#### !!! error !!! : from flask_twisted import Twisted 에서 no module named 'flask_twisted'
- Twisted를 임포트할 flask_twisted 모듈이 없거나 못찾는 것
   - pip install flask_twisted 다시 실행 : Twisted 라는 웹 서버 프레임워크, python 네트워크 환경을 만들 수 있게 해준다. Twisted 안에서 플라스크를 실행시키도록 해주는 라이브러리 이다.
   - pip install flask_script : Twisted를 사용해서 flask를 실행하려면 flask_script 플러그인도 설치 해주어야 한다.
   - nohup 으로 runserver api를 실행한 후 ===> 커서 깜빡이는 상태에서 curl localhost:5000/ping 요청 ===> pong response가 돌아 온다.
- 성공~~~~~~

#### EC2 서버에서 pip install falsk_twisted 설치
- githup에는 Flask-Twisted==0.1.2를 추가한 requirements.text를 다시 push
   - 다른 인스턴스 서버에서도 설치를 해주어야 한다.
- EC2 서버의 flask._compat 실행 위치에서 __init__.py 에서 해당 모듈이름 변경
   - from flask._compat import text_type ===> from flask_script.compat import text_type
   - 로컬에서 해결한 것과 같은 방식으로 ubuntu의 EC2 서버에서도 해결이 됨
   - nohup으로 runserver 한 상태에서

### 6) 나머지 EC2 인스턴스 서버에도 똑같이 적용한다.!!!!
- ubuntu EC2 서버 접속
- deploy key 생성 후 github에 추가 키 등록
   - ssh-keygen -t rsa -b 4096 -C "rock.me.baby@me.com"
- github repo 를 clone
- 다른 디렉토리에서 miniconda 설치 파일 다운
   - wget <주소>
- miniconda 설치 파일 실행
   - bash ./Mini~~~.sh
   - 엔터 여러번 눌러서 설명글 스크롤한 후 yes
- conda를 PATH에 추가
   - . ~/.bashrc
- 재접속 후 conda list로 설치 확인
- conda 가상환경 생성
   - conda create --name backendenv python=3.8.18
- 가상환경 활성화
   - conda activate backendenv
- nohup으로 api 실행
   - `flask._comapt` 에러 발생시 해당 위치로 가서 __init__.py 의 from~import 수정
- /ping 엔드포인트에 HTTP 요청, pong response 확인

### 7) Load Balancer 생성
- `로드 밸런서는 백엔드 서버들에 전송되는 HTTP나 다른 종류의 네트워크 트래픽을 여러 서버들에 동일하게 분배한다.`
   - EC2 인스턴스 2개에 직접 HTTP 요청이 가는게 아니라 로드 밸런서를 거쳐서 전달된다.
   - 다른 서버가 멈추면 다른 서버에 배분하여 트래픽을 감당할 수 있도록 한다.

#### EC2 인스턴스에 로드밸러서 생성
- EC2 페이지 ===> 로드 밸런싱 (로드 밸런서 메뉴 선택) ===> 로드 밸런서 생성 ===> 3가지 타입 중 선택 (application load balancer) ===> 설정 페이지 (이름 : lb-minitter, 체계 : 인터넷 경계(internet-facing??, 외부에서 HTTP 전송이 가능하도록 함), id 주소 유형 : ipv4, vpc : 하나만 뜸 (EC2가 속해있는 vpc 선택), 매핑 subnet 선택(vpc가 돌아가는 위치?) : 모든 subnet 선택, 보안그룹 : default 선택) ===> 리스너와 라우팅 (로드 밸런서가 대상그룹에 라우팅하고 상태 확인을 하는 설정) HTTP, 포트 : 5000 ===> 대상그룹 선택 ===> 세부사항 선택 (대상유형 : 인스턴스, 그룹이름 : minitter-server-2, 디폴트값 선택, 상태검사 (로드밸런서가 상태 확인 을 위해 이 대상에 HTTP 요청을 보내도록 함) : HTTP, /ping ===> 로드밸러서 생성
- 로드밸런서의 DNS 주소가 API 주소가 된다. 여기에 HTTP 요청을 보내면, 각 EC2 서버에 배분되면 응답을 받게 된다. ---> 어떻게 하지???? ---> Route53 이라는 기능을 연결 해줘야함...
- 대상그룹의 대상유형에서 인스턴스를 선택해주어야 EC2 인스턴스 2개를 선택할 수 있는 창이 나온다.
   - 로드밸런서를 대상그룹(EC2 인스턴스 2개가 포함된)과 연결한 후 시간이 지나면 활성화가 된다.
   - 로드밸런서에서 대상그룹 (minitter-instance-2)로 테스트 요청을 보내서 상태를 체크한다.
   - 상태가 unhealty 나온다.. 여러가지 시도 중...
   - EC2, 로드밸런서, 대상그룹이 모두 공유하는 보안그룹의 인바운드 규칙에서 불필요한 규칙을 제거한다.
   - 로드밸런서에서 리스너가 대상그룹에 보내는 테스트 요청은 HTTP, 5000포트 인데 HTTP, 88포트에 해당하는 보안그룹의 인바운드 규칙이 있었다. 이것을 제거 하고, HTTP, 5000포트에 해당하는 인바운드 규칙을 만들어 준다.
   - 각 인스턴스를 로컬에서 접속한다.
   - 상태가 healthy로 바뀌었다. (시간이 지나서 healthy 가 된건지, 로컬에서 인스턴스에 접속하여 활성화가 되어서 healthy가 된건지 정확하진 않다. >>> 시간이 지나서 상태가 바뀐거 같다.. 접속 종료를 해도 상태가 정상이다.)

#### RDS와 인스턴스의 연결
- HTTP 요청을 보내면 데이터가 RDS DB에 저장되어야 한다. (또는 조회, 삭제 등)
- 데이터 베이스 RDS 창에서 데이터 베이스 선택 ===> 작업 ===> EC2 연결설정 ===> 인스턴스 2개 각각 연결
- 인스턴스와 DB에 각각 새로운 보안그룹과 VPC 그룹이 생성된다. ===> 연결 완료
- 로컬에서 인스턴스에 접속 후 HTTP 요청을 보내면 데이터가 DB에 저장 된다. !!!!
   - API가 작동 한다. SQLAlchemy를 통한 DB 조회, 저장, 삭제 등의 쿼리 작업이 가능하다는 의미
      - request에 Auth를 입력하는 방법 : curl -X POST
      - -H 'Auth: exeksld123' -H 'Content-Type: application/json'
      - Header = {"Auth": "exeksld123", "Content-Type": "application/json"}
      - curl 명령어를 사용해도 되고, httpie 패키지를 다운 받아서 http -v POST 형태로 사용해도 된다.
   - 인스턴스에 접속하지 않고 로드밸런서를 통해서 HTTP 요청 - 응답을 받는 것이 목적이다.
- 로드밸런서를 만들었다. 그 다음 어떻게 HTTP 요청을 로드밸런서를 통해서 각 인스턴스로 분배하지??????
   - AWS Route 53과 로드밸런서를 연결하여 라우팅을 할 수 있다.
   - Route 53 (루트 53)은 DNS(domain name system) 웹 서비스, 도메인 등록, DNS 라우팅, 상태확인 기능이 있다.
   - 즉 트래픽을 로드밸런서로 라우팅하도록 Route 53을 구성(셋팅)한다.

## 9. (10장) API 아키텍쳐
- `API의 소스 코드 전체 구조를 체계적이고 효율적으로 구조화한다.`
   - 코드의 아키텍쳐 architecture
   - 아키텍쳐의 패턴 : 레이어드 패턴 layered pattern

### 1) 코드 구조의 중요성
- 현재 미니터의 소스코드는 app.py 파일 하나에 저장되어 있음
- 하나의 파일에 소스코드를 저장하면 간단하다.
   - 복잡성을 줄일 수 있다.
   - 개발이 덜 복잡해진다.
   - 그러나 이러한 방식은 전문성이나 고도화에 적합하지 않다.
- 코드의 양이 많아지고 고도화되면 하나의 파일에서 관리하는 방식은 적절하지 않다.
   - 기능단위, 논리적 단위 별로 코드를 관리해야한다.
   - 코드를 효율적으로 구현하는 것을 아키텍쳐라고 한다. architecture
   - 아키텍쳐라는 용어는 여러가지로 사용 된다. 서버, 네트워크의 구조 등에도 사용됨
- 아키텍쳐의 요소들
   - 확장성 extensiblity : 서비스가 간단한 형태에서 점차 복잡해지고 규모도 커지게 되므로 확장성이 높아야 한다.
   - 재사용성 reusablity : 재사용성이 높을 수록 코드의 양이 적어지고, 개발 속도도 높아진다. 안전하고 견고해진다. 함수나 클래스의 재사용이 아니라 구조적으로 재사용성이 좋아야 한다.
   - 보수 유지 가능성 maintability : 보수 유지가 잘 되려면 구조적으로 로직이 잘 정리되어 있어야 한다. 여러 로직이 뒤엉켜 있으면 보수 유지가 힘들다. 코드를 함수와 클래스를 사용하여 추상화 abstraction하고 독립적인 로직을 분리한다. 추상화화 독립적으로 분리가 필요하다.
   - 가독성 readability : 어려운 로직일 수록 가독성이 높게 구현되어야 한다. 코드의 구조도 이해하기 쉽게 구현되어야 한다. 복잡하면 가독성이 떨어지고(로직의 구조를 이해하기 어렵고) 그만큼 보수 유지도 힘들어진다.
   - 테스트 가능성 testability : 테스트는 개발 과정에서 중요한 부분이다. 따라서 unit test를 잘 구현할 수 있는 코드 아키텍쳐가 좋다. 코드가 추상화 되어 있고 로직단위로 독립적으로 관리 되면 unit test하기 쉬워진다. 

### 2) 레이어드 패턴 layered pattern
- 코드 아키텍쳐에 관한 여러가지 패턴들과 사례들이 있다.
- 백엔드 API 코드에서 가장 널리 적용되는 패턴은 레이어드 패턴
   - Multi-tier 아키텍쳐 패턴이라고도 한다.
   - 코드를 논리적인 부분들, 역할에 따라서 독립된 모듈들로 나누어서 구성하는 방식
   - 각 모듈이 서로 의존에 따라서 층층이 쌓여있듯이 연결된다.
- 레이어드 패턴의 구조
   - 프레젠테이션 레이어 presentation layer : 서비스를 사용하는 사용자, 클라이언트 시스템과 직접 연결되는 부분. 웹사이트에서는 UI 부분에 해당, 백엔드 API에서는 엔드포인트 부분에 해당한다. business layer에서 엔드포인트를 정의하고 HTTP 요청을 읽어들이는 로직을 구현한다. 그 이상의 역할은 하지 않고, 실제 시스템이 구현하는 것은 비즈니스 레이어로 넘긴다.
   - 비즈니스 레이어 business layer : 실제 시스템이 구현해야 하는 로직들을 담고 있다. 트윗 엔드포인트에서 글자수를 판단하는 코드, 로그인 엔드포인트에서 jwt 암호를 생성하는 부분, 타임라인 엔드포인트에서 user id에 대한 트윗 데이터를 조회하는 부분 등. 엔드포인트의 실제 코드 부분.
   - 퍼시스턴스 레이어 persistance layer : 데이터 베이스와 관련 된 로직을 담고 있다. 비즈니스 레이어에서 필요한 데이터 베이스 관련 데이터 생성, 수정, 조회 등을 처리하는 부분이다. 
- 레이어드 아키텍쳐의 핵심
   - 각각의 레이어 (presentation, business, persistance)는 하위의 레이어에 의존한다.
   - 따라서 business는 presentation에 독립적이고, persistance는 business, presentation에 독립적이다.
   - 각각의 레이어의 역할이 명확해야 한다.
   - presentation 레이어에는 로직이 아예 구현되어 있지 않다. business 레이어에서 이 로직에 해당하는 코드를 호출한다.
- 코드 아키텍쳐의 5가지 요소들에 적합한 방식이다.
   - 확장성, 재사용성, 가독성, 보수유지 가능성, 테스트 가능성 
   - business layer는 다른 서비스의 presentation layer에 호출하여 사용할 수 있다. (재사용성이 높다.) 

### 3) 레이어드 아키텍쳐 적용하기
- 디렉토리 생성
   - mkdir {view, service, model}
- `api`
   - view (presentation) : 엔드포인트
      - __init__ : 엔드포인트 코드 : app.py에서 view.py의 create_endpoints 함수를 호출한다. app객체와 service객체를 넘겨준다.
   - service (business) : 비즈니스 로직
      - __init__ : app.py에서 service모듈을 통해 UserService와 TweetService 클래스를 한번에 임포트 할 수 있도록 한다. 각각의 .py 파일로부터 클래스를 임포트하여 __all__ 에 저장한다.
      - UserService 클래스 : user의 개인 데이터, 로그인, 팔로우, 언팔로우 명령을 처리한다.
      - TweetService 클래스 : user의 tweet 쓰기, timeline 가져오기 명령를 처리한다.
   - model (persistence) : 데이터 베이스에서 명령을 처리한다.
      - __init__ : app.py에서 model 모듈을 통해서 UserDao와 TweetDao 클래스를 한번에 호출할 수 있도록 한다. 각각의 .py 파일로부터 클래스를 임포트하여 __all__에 저장한다.
      - UserDao 클래스 : UserService에서 호출을 받아 데이터베이스에서 데이터를 생성, 조회, 팔로우, 언팔로우하는 명령을 처리한다.
      - TweetDao 클래스 : TweetService에서 호출을 받아 데이터베이스에서  tweet 데이터 생성, 타임라인 조회 명령을 처리한다.
   - app.py : 데이터베이스와 연결하고 플라스크 객체를 만들어 각각의 레이어들을 연결한다.
      - 데이터 베이스 연결 : config.py
      - 플라스크 객체 생성 : app = Flask(__name__)
      - 레이어 연결 : user_dao, tweet_dao, services.user_service, services.tweet_service, create_endpoints()
   - config.py : 데이터베이스에 연결하기 위한 접속 정보 저장
      - app.py에서 데이터베이스에 접속한 객체를 만들때 사용됨
      - app.py에서 데이터베이스 객체를 user_dao와 tweet_dao에 인자로 입력하여 sqlalchemy를 통해 쿼리 명령을 처리한다.

### 4) 레이어별 unit test 2
- unit test 1에서는 엔드포인트만 test 할 수 있었다.
- 레이어드 패턴으로 만든 코드에서는 각 레이어별로 테스트 할 수 있다.
- api 디렉토리에 test 디렉토리 생성
   - test_service.py, test_model.py, test_view.py
   - pytest -vv -s -p no:warnings ===> 실행하면 test가 붙은 파일들이 실행됨
   - test_view.py는 엔드 포인트를 unit_test 해야하므로 flask의 test_client() 메서드를 호출해야함
      - api = app.test_client()
- unit test에서 중요한 부분은 테스트할 기능의 반환되는 값의 데이터 타입을 잘 파악해야 한다는 것. 결국 각 기능별 반환 되는 데이터 타입의 연결성이 전체 소스코드의 구조의 뼈대가 되는 것 같다.
- /sign-up 엔드포인트의 반환값 ===> /sign-up에서 호출하는 user_service의 create_new_user, get_user 함수의 반환값 ===> 이 함수에서 호출하는 user_dao의 insert_user, get_user_data 함수의 반환

### 5) unit test 2를 마친 후 api 디렉토리의 구조
- setup.py : 플라스크를 클라우드 서비스의 가상 서버에서 실행하기 위한 파일
- requrirements.text : 현재 서비스를 실행하기 위한 가상환경의 라이브러리 구성 파일
- `api 구조`
   - app.py
   - config.py
   - model
      - __init__.py
      - tweet_dao.py
      - user_dao.py
   - requirements.text
   - service
      - __init__.py
      - tweet_service.py
      - user_service.py
   - setup.py
   - test
      - test_model.py
      - test_service.py
      - test_view.py
   - view
      - __init__.py

## 10. 파일 업로드/다운로드 엔드포인트
- Flask에서 파일 업로드 엔드포인트 생성
   - AWS S3에 저장
   - 파일 전송 속도 높음
   - 효율적인 저장 공간 관리 가능
- 순서
   - 파일 업로드 엔드포인트
   - 파일 GET 엔드포인트
   - S3
   - boto(AWS python client)
   - mock & patch

### 1) 파일 업로드 HTTP request의 방식
- HTTP request를 사용하여 파일을 업로드 한다.
   - GET, POST를 사용함
- content_type 방식이 다르다.
   - content_type은 HTTP request 메시지의 body(실제 내용)의 type을 지정한다.
   - content_type : 'application/json'===> json 형태의 데이터를 요청할 때
   - content_type : 'multipart/form-data' ===> 파일 형태의 데이터를 요청할 때
- body를 boundary 값으로 구분한다.
   - content_type 에 boundary 값을 추가하여 request의 body를 여러 boundary로 구분한다.
   - body를 boundary로 구분하고 여기에 파일 데이터에 대한 정보를 담는다.
   - 이렇게 구분된 body의 boundary에 파일 데이터와 다른 데이터를 함께 request 할 수 있다.
   - content_type : multipart/form-data ; boundary = "----WebKitFormBoundaryePkpFF7tjBAqx29L"
   - 이 바운더리 값을 사용하여 boundary의 시작과 끝을 명시해주고, 그 사이에 정보를 추가한다.

### 2) 파일 업로드 엔드포인트의 구현
- 업로드 POST 방식과 불러오기 GET 방식으로 구현
   - 이미지 파일을 업로드(db 저장)만 해서는 별 의미가 없다. GET 요청으로 업로드한 이미지를 불러와야 의미가 있다.
* 업로드 엔드포인트 *
   - 하드코어 코드로 한번에 만들 수 있지만 layered 방식으로 구성한다. 3개 레이어 별로 기능을 구분.
   - view ===> service ===> model 레이어 순으로 이미지 파일을 db에 저장 하도록 한다.
   - request.files 객체에 이미지 파일 정보가 있는지 확인
   - werkzeug.utils 모듈의 secure_filename 매서드를 사용하여 filename의 보안 처리
      - 시스템 파일 이름 등의 경로가 이름에 포함 될 경우 바꿔준다.
      - from werkzeug.utils import secure_filename
      - werkzeug 는 Flask에서 사용하는 엔진 중의 하나, WSGI(web service gateway interface) 규약을 처리하도록 도와준다.
   - db에 컬럼 추가
      - ALTER TABLE users ADD COLUMN profile_picture VARCHAR(255) ;
   - view 레이어에서 request.files에 저장 된 이미지 파일 객체와 파일이름을 가져오고, config.py에서 파일 저장 경로를 가져온다. 이것들을 user_id와 함께 service 레이어로 전달한다.
   - service 레이어에서 경로와 파일이름을 사용해 path를 만든 후 picture 객체를 해당 경로에 저장한다. 저장 후 에 path를 user_id와 함께 model 레이어로 전달한다.
      - os.path.join(path, filename)
      - picture.save(path)
   - model 레이어에서 sqlalchemy 명령을 통해 파일의 경로를 user_id의 db 컬럼에 업데이트 한다.
      - UPDATE user SET profile_picture = :profil_path WHERE id = :user_id
      - GET 엔드포인트에서 이 경로를 사용하여 이미지를 불러온다.
- 실행
   - FLASK_APP=setup.pyp FALSK_DEBUG=1 flask run
   - sign-up ===> login ===> auth token ===> http -v --form localhost:5000/profile-picture profile-pic@/home/hshkuber/Pictures/profile.png "Authorization:<auth token>"

### 3) 불러오기 엔드포인트 GET
- /profile-picture 엔드포인트를 그대로 사용하고 GET methods를 사용한다.
   - view 레이어에서 user_id 를 service 레이어의 get_profile_picture 함수에 전달한다. 반환받은 이미지 경로를 Flask의 send_file() 모듈을 사용하여 이미지를 불러온다.
      - 이미지는 binary 데이터이므로 화면에 출력 되지 않는다.
      - wget localhost:5000/profile-picture/1 -O test.png 로 파일을 실제 다운받을 수 있다.
   - service 레이어에서는 user_id를 다시 user_dao의 get_profile_picture에 전달한다.
   - model 레이어에서는 user_id를 사용하여 db에서 저장된 파일의 경로를 가져와 service 레이어에 반환환다.
- db에 저장 된 파일의 경로를 반환받아 send_file() 모듈을 사용하여 이미지를 불러온다.
- `실행`
   - 이미지 저장 후
   - http -v GET localhost:5000/profile-picture/1
      - 이미지가 binary로 되어 있어서 보이진 않는다.
   - wget을 사용하여 해당 데이터를 다운 받을 수 있다. (현재 로컬의 db 서버이지만, 현재 위치에 다운이 된다.)
      - wget localhost:5000/profile-picture/1 -O profile.png
      - -O를 사용하면 저장할 파일 명을 설정할 있다.
- `성공`

## 11. AWS S3에 이미지 파일 저장하기

### 1) 로컬 DB를 사용한 파일 송수신의 문제
- 이미지 파일을 /profile-picture 엔드포인트를 통해 업로드하고 다운로드 받을 수 있다.
- 그러나 문제가 있다.
   - 저장 공간 문제와 파일 전송 속도, 확장성 문제
- 저장공간 문제
   - 사이즈 큰 이미지 파일은 MB 단위
   - 업로드 이미지 갯수가 늘어나면 디스크 공간에 부담이 가게 됨
   - AWS EC2 사용시 비용 발생의 큰 부분도 디스크 사용량
- 파일전송 속도 문제
   - 파일의 크기가 커지므로 전송 속도도 줄어들게 된다.
   - api 시스템을 사용하는 사용자가 늘어날 수록, 예컨테 프로필 사진 이용자가 늘어날 수록 서버에 부담이 된다.
   - Flask는 특히 파일 전송에 특화된 프레임워크가 아님
- 확장성의 문제
   - scale out : 서버의 수를 늘리는 것
   - 백엔드 API 서버의 수를 늘려야 하는 문제
   - 서버의 수가 늘어날 수록 파일을 업로드 하는 서버는 한대에 집중 됨
   - 서버의 수가 늘어날 수록 파일을 다운로드 할 때 복잡성이 증가하게 됨 (?)
      - 여러 서버에서 파일 업로드 서버에 요청이 보내지고, 또 응답해야하기 때문?
   - 따라서 static 파일 저장 과 전송을 전담하는 "중앙 파일 서버"가 필요하게 됨

### 2) CDN content Delivery network 
- `콘텐츠를 네트워크에서 전송하는 "서버"`
   - 컨텐츠 파일의 저장, 전송에 최적화 되어 있는 시스템
   - 웹 서버보다 더 잘 기능한다.
- content : static files : 이미지, 영상 파일 등
- 웹 사이트에서 보이는 이미지나 영상은 웹 서버에서 직접 전송하는 것이 아닌 CDN을 통해서 전송한다.
   - 저장 공간 문제, 전송 속도 문제, 확장성 문제를 해결 해준다.
- 미니터 api의 profile 이미지도 CDN 서버를 사용해서 전송하도록 구현한다.
- `CDN 사용 방법`
   - 1. 직접 구현한다. : 방법이 전문적이고 규모가 크다.
   - 2. 유료 CDN을 사용한다. : AWS의 S3 (simple storage service) 사용 가능

### 3) AWS S3 서비스를 사용한 파일 송수신
- `S3 : simple storage service`
   - AWS의 CDN 서비스
   - 간단한 저장 서비스 : AWS 상에서 파일을 저장, 전송할 수 있고, python을 통해서 시스템에서도 S3로 업로드, 다운로드 할 수 있다.

#### 장점
- 유료 서비스이다.
   - 비용이 저렴한 편이다.
   - EC2에 저장하는 것보다 저렴하고 안전하다.
   - TB까지 저장할 수 있다.
- 총량이 무제한이다.
   - AWS의 인프라스트럭쳐는 규모가 매우 크므로 개인 사용자들의 입장에서는 거의 무제한에 가깝다.
   - 웬만한 기업입장에서도 무제한에 가깝게 사용가능
   - 비용이 발생한다.
- AWS S3에 저장 된 데이터는 훼손 될 가능성이 거의 없다.
   - 가용성, 신뢰도 99.99% 보장
- S3를 통해서 직접 파일 전송 가능
   - 파일마다 고유의 URL을 부여하여 저장, 전송이 가능하다.

#### 단점
- S3는 엄밀히 말하면 CDN 서버는 아니다.
   - 주로 파일 저장 서비스로 사용. 여러 기능 중 CDN 기능도 있다.
   - 파일 사이즈가 크면 전송 속도가 줄어들 수 있다.
- 이러한 경우 CloudFront 서비스와 S3를 함께 사용하면 좋다. (전송 속도가 중요한 경우)
   - CloudFront는 파일 전송이 빠른 CDN 서비스
   - 전 세계의 edge server 에 파일들을 캐시해 놓음...(?)
   - 파일 저장은 S3, 전송은 CloudFront 이렇게 구분해서 사용
- 실제 서비스를 구축하고 국내, 해외에서 파일을 전송해야 한다면 ClounFront CDN 사용 권장

### 4) AWS S3 설정
- `S3의 bucket의 전송, 권한 등의 설정`
- AWS ===> S3 ===> bucket 만들기 (bucket : S3의 단위) ===> 일반구성 설정(이름 : minitterbucket, AWS 리전 : 아시아 태평양 서울, 기존버킷설정복사 : 없음) ===> 객체소유권 (ACL 비활성화 : 현재 계저이 버킷 소유) ===> 버킷의 퍼블릭 액세스 차단 설정(추천은 4가지 퍼블릭 액세스 차단활성화, 여기에서는 S3를 CDN으로 사용하기 위해서 어느정도 퍼블릭 액세스가 필요하므로, "정책 policies" 관련된 차단 2개만만 체크 해체한다. 책에서 설명하는 예시와 달라짐) ===> versioning 버킷버전관리는 비활성화 ====> 태크 없음 ===> 기본암호화설정(책에는 없는 메뉴, Amazon S3 관리형 키 암호화 선택 SSE-S3) ===> 버킷 생성 ===> minitterbucket 누르면 여러가지 설정 정보를 확인 할 수 있다. 수정도 가능 ===> 권한(permission) ===> 버킷 정책(bucket policy) ===> json 을 입력하여 버킷에 저장된 파일을 누구나 읽을 수  있도록 설정한다.(json 문 작성하면 오류 있는 부분을 알아서 지적해준다.) ===> 저장 ===> CORS(cross-origin 리소스 공유) 설정 (S3에서 각 파일에 부여된 URL을 사용해야하는데 CORS 설정을 하여 모든 도메인에서 GET 요청을 허용하라는 명령어, 책에 나온 예제는 XML 형식인데, 입력하는 창에서는 json 형식만 가능, CORS 설정에 관한 AWS 가이드에 json 구성 방식 참고하여 설정함 + CORSRules 에대한 설명 참조)

#### AWS IAM 설정
- python을 사용해 S3에 파일을 업로드하려면 IAM 사용자 설정이 필요하다.
- AWS의 사용자 권한 관리 서비스 : 특정 권한만 가진 사용자를 생성하고 할당할 수 있다. (?)
   - AWS의 리소스에 대한 액세스를 안전하게 제어한다.
   - AWS의 리소스에 사용자가 접근할 수 있는 권한을 중앙에서 관리할 수 있다.
   - 사용자별로 인증 및 권한 부여 대상을 제어할 수 있다.
   - 무료이다.
   - 생성한 S3 bucket에 관한 권한만 가진 IAM 사용자를 생성하고, 파이썬 코드로 파일을 bucket에 업로드할 수 있도록 한다.
- AWS ===> IAM ===> 사용자 Users ===> 사용자 생성 Add user ===> 사용자 세부 정보 설정 (이름 : minitter-iam, AWS mangement console 사용자 액세스 권한 제공 체크 안함, console에 접속하지 않고 python code로 실행할 것이므로) ===> 다음 ===> 권한 설정(권한옵션 : 직접정책 연결 ---> 권한정책에서 S3 검색 ---> amazonS3fullaccess 체크, s3의 모든 권한을 준다는 의미, 더 보안을 강화하려면 모든 권한주기 보다 특정 버킷에 대한 권한을 줄 수 있다, 권한경계설정도 같은 policy 선택) ===> 태그 없음 ===> 사용자 생성 ===> minitter-iam 누르고 ===> 액세스 키 생성 ===> 로컬 코드 선택 (EC2에서 어플리케이션 실행 키도 있는데 우선 로컬 메뉴 선택) ===> 태그 생성 (minitter-api-local-access-key) ===> (키 : AKIA2ARTLA6KYVL7L3GF, pw : uOY9ruu/NA2P4H/T3cgssEKl1R51WNLX80Nemgk8) ===> csv 다운  ===> 완료, iam 사용자 페이지에서 다른 액세스 키를 만들 수 있음
- Access key ID, Secret access key 다운로드 보관 ===> 소스코드에서 S3에 접속할 때 사용한다.
   - 다운로드 안 하거나 분실하면 다시 받아야 함.
   - 이 key들을 사용하여 로컬에서 python 코드로 S3에 파일을 업로드 할 수 있게 된다.
- AWS를 어떤 방식으로 사용할 지에 따라서 액세스 키가 여러 종류가 있다.
   - 하나 만들고 또 만들 수 있다.

## 12. 소스코드에서 Boto3를 사용하여 S3 연결 설정
- `AWS SDK : software development kit`
   - python에서 S3 같은 AWS 서비스에 접근하여 기능들을 쓸 수 있게 해준다.
- Boto3 설치 후 IAM key로 S3 접속 설정
   - pip install boto3
   - confit.py 에 IAM 액세스 키 지정
   - 이 액세스 키를 사용하여 boto3가 AWS의 S3에 접속할 수 있다.
- S3 URL 
   - url 형식이 바뀜, 버킷에 액세스하기 위한 매서드 페이지에서 확인 가능
   - https://bucket-name.s3.region-code.amazonaws.com/key-name
   - https://minitterbucket.s3.ap-northeast-2.amazonaws.com/
   - key-name 은 S3에 업로드 된 파일의 이름   
- view, model 레이어는 그대로 사용, service 레이어에서 파일 저장 위치, 전송 위치를 S3로 수정
   - boto3를 사용하여 S3에 접속한 후 이미지를 업로드하고, 이 파일을 다시 S3에서 전송받는 구조
   - db에 저장되는 것은 img의 url
- /login ===> token ===> /profile-picture + path + token ===> s3에 업로드 됨
   - boto3.client()의 upload_fileobj() 매서드를 사용 하여 S3 에 업로드 한다.
      - self.s3.upload_fileobj(picture, self.config['S3_BUCKET'], filename)
   - minitterbucket의 페이지에 가면 apple.png 객체가 업로드 되어 있다.
   - 파일명을 누르면 파일에 대한 여러 정보 페이지가 나온다. 여기에서 URL을 확인 할 수 있다. 
- GET /profile-picture 하면 db에 저장 된 S3 파일의 URL을 가져온다.
- wget <img url> -O <파일명> : 현재 디렉토리에 S3에 업로드한 파일을 다운 받는다.

## 13. mock 을 사용한 unit test
- model 레이어의 unit test는 쉽다.
   - 로컬 서버에 url을 저장하고 반환하는 코드이므로 간단하게 테스트 할 수 있다.
- service 레이어는 test에 문제가 있다.
   - 1) service 레이어의 save_profile_picture()를 테스트 하면 파일을 업로드 시키고 확인 해야한다.
   - 2) unit test는 여러번 대량으로 실행 할 수 있는데, 이러한 경우 S3에 많은 데이터를 업로드 할 수 있다.
   - 3) test용 버킷을 만들고 실행할 수도 있지만 결과적으로 S3에 의존하게 된다.
   - 4) S3가 문제가 생긴 경우 test 자체가 정확하지 않을 수 있다.
   - 5) 그러므로 mock 라이브러리를 사용하여 가짜 boto3 객체를 만들어서 사용한다.

### 1) mock 패키지를 사용하여 unit test
- `mock : 동일한 구조이지만 흉내만 내는 객체`
- app.py, user_service.py 코드 수정
   - user_service.py 에서 boto3.client() 객체를 app.py에서 전달 받도록 코드를 수정 한다.
   - app.py에서 boto3.client() 객체를 생성하고 user_service()에 인자로 전달하도록 수정한다.
   - user_service에서 함수 __init__(s3_client)에서 s3에 접속한 boto3.client() 객체를 받는다.
- pytest 파일인 test_service.py도 mock 라이브러리를 사용하여 코드를 수정
   - mock.Mock() 객체를 UserService() 클래스의 s3_client 인자의 위치에 입력하여 전달하면, Mock() 객체가 s3_client() 객체의 가짜 객체가 된다.
   - !!! mock의 정확한 사용 방법 알아보기 !!!
   
### 2) config.py test_config 수정
- S3 접속정보를 key, value 값으로 추가한다.
   - unit test에서 사용하기 위함

## 14. 서비스 배포 deploy
- EC2 각각 파일 업데이트 하고 실행
- load balancer와 연결 되어 있으므로 다른 EC2가 설정으로 지연될 경우 나머지 EC2에서 응답을 하게끔한다.
   - 이미 load balancer가 실행됨

### 배포 순서
- 1. 로컬에서 api 최종 파일과 디렉토리를 git hup study-backend 레포지토리로 push 한다.
   - setup.py : falsk_twist 를 사용하여 서버에서 api를 실행할 수 있다.
   - app.py : flask 객체를 만들고, view, service, model 레이어별 클래스 모듈을 연결한다.
   - config.py : DB 접속 정보, S3 접속 정보가 들어 있다.
   - view, service, model 디렉토리 : 각각 레이어에 해당하는 소스 코드가 들어 있다.
   - requirements.text : api를 실행하는 가상환경의 pip 설치 리스트가 들어 있다.
- 2. EC2 ubuntu 서버에 접속 한다.
   - ssh -i <pem key> ubuntu@<ec2의 접속 ip>
- 3. git hub과 연결된 디렉토리에서 git pull 을 한다.
   - 1 에서 업로드 한 파일을 다운 받는다.
- 4. 콘다 가상환경을 실행한 후 pip 설치를 한다. 
   - 로컬의 api 개발 가상환경의 pip list 와 동일한 패키지, 라이브러리를 설치 하기 위함
   - pip install -r requirement.text
- 5. flask_script error 를 해결한다.
   - 에러가 발생한 __init__.py 파일에서 모듈 임포트하는 부분을 수정한다.
   - flask_script 패키지를 설치한다. pip install flask_script
- 6. api를 실행한다.
   - nohub 명령어를 실행하게 되면 실행 기록 관련 파일이 생성되어 귀찮다.
   - FLASK_APP=setup.py FLASK_DEBUG=1 flask run 실행
- 7. 새로운 터미널에서 동일한 EC2 인스턴스에 접속 후 콘다 가상환경 실행
- 8. api 에 HTTP request 를 전송한다.
   - curl 명령어를 사용 : curl -X GET localhost:5000/ping
   - httpie를 설치하여 HTTP 명령을 간편하게 쓸 수 있도록 한다.
      - pip install httpie
   - curl 명령을 사용하면 헤더, 데이터 등을 구분하는 명령어 등을 써야 한다. 양식이 달라서 request 메시지를 만들기 까다롭다.
   - httpie 명령을 사용하면 비교적 간편하게 request 메시지를 만들 수 있다. 
   - curl과 httpie에 대해서 확인 해볼 것
- 9. RDS에 접속하여 user 데이터가 잘 저장 됐는지 확인한다.
   - 로컬에서 : mysql -h <rds 엔드포인트> -u <rds의 db 이름 : root> -p
- 10. /login 엔드포인트 요청을 보내 token 을 받는다.
- 11. /profile-picture/s3 엔드포인트 요청을 보내 파일을 전송한다.
   - http -v POST localhost:5000/profile-picture/s3 profile-pic@<이미지 파일의 path> "Authorization:<토큰>"
- 12. AWS의 S3에서 업로드 된 파일을 확인 한다.
- 13. 업로드한 파일을 다운로드 한다.
   - http -v GET localhost:5000/profile-picture/s3/<user_id>
   - wget <aws s3의 이미지 객체 주소>

## 15. 더 나은 개발자를 위한 배워야 할 주제들
- 1) 자료구조
- 2) 데이터베이스에 대해 더 공부
   - 여러 데이터베이스를 사용할 줄 알아야
   - RDBMS mysql 말고 비관계형 DB인 NoSQL(mongodb)도 다룰 줄 알아야
- 3) database maigration
   - 데이터 베이스의 스키마의 형상 관리 필요
   - sqlalchemy의 ORM 등이 있다.
   - Liquibase 추천 : 스키마를 yaml 파일로 만들면 다른 db에서도 사용할 수 있도록 sql로 변경해준다. 범용성 높음
- 4) api의 인프라스트럭쳐 구조
   - minitter는 모놀로식(monolithic) 구조
      - 하나의 서버에 모든 기능이 구현되어 있는 구조
   - micro service architecture
      - 하나의 서버에 하나의 서비스만 구현하는 방식
      - EC2 하나당 user_service, tweet_service를 각각 구현하는 방식
      - 전체 시스템을 다 추상화 한다.
      - 큰 규모의 서비스로 가면 이런식으로 관리하게 됨
- 5) 리눅스와 데브옵스
   - 리눅스에 대한 이해 필요 : 서버에 오류가 났을때 리눅스 서버에 접속해서 문제를 해결할 수 있느냐 없느냐
   - 시스템을 관리할 수 있는 능력의 필요
   - 데브옵스 : CICD 개발환경 구축, IAC(infrastructure as code) 기술 사용
   - 서버 설정과 관리에 필요한 기술들
   - docker, terraform 등
   - terraform은 IAC로 AWS 클라우드 서비스를 사용하는 경우 유용하다.
      - AWS에서 전체 인프라스트럭쳐를 코드로 구현하고 관리할 수 있게 해준다.       

