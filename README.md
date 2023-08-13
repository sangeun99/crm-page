<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project

  <center><img src="https://github.com/sangeun99/crm-page/assets/63828057/24e9e15c-113e-4ea4-aca3-6106f2a34245" width="80%" height="80%"></center>
 
  프랜차이즈 카페의 고객을 관리할 수 있는 CRM 시스템입니다.
  고객과 카페, 아이템, 주문 정보를 관리할 수 있습니다.
  [데이터생성기](https://github.com/sangeun99/data-generator.git) 를 통해 생성된 더미데이터로 데이터베이스를 구성했습니다.

### Built With

1. 웹 개발 및 프레임워크
* Python
* Flask
2. 프론트엔드
* Jinja Template
* HTML
* CSS
* Bootstrap
3. 데이터베이스
* sqlite3
* Flask SQLAlchemy

<!-- GETTING STARTED -->
## Getting Started

다음의 간단한 작업 후에 프로그램을 실행시킬 수 있습니다.

### Installation

1. [데이터생성기](https://github.com/sangeun99/data-generator.git)를 통해 데이터를 생성합니다.
- 해당 데이터생성기는 csv 파일로 데이터를 생성하기 때문에 터미널을 통한 sqlite3 접속 후 csv 파일을 DB 테이블로 옮겨주는 작업이 필요합니다
- 예시) users.csv 파일을 user 테이블로 작업하기
```
sqlite3 crm.db
.mode csv
.import users.csv user
```
2. 이 레파지토리를 Clone합니다.
```
git clone https://github.com/sangeun99/crm-page.git
```

3. python 패키지를 설치합니다.
```
pip install -r requirements.txt
```

4. 메인 파일을 실행합니다.
```
python app.py
```
혹은
```
flask run
```
<!-- USAGE EXAMPLES -->
## Usage
user는 kiosk를 통해 주문 또한 가능합니다.
(version 1에서 가능, version 2 수정 중)

다양한 쿼리문을 통해 정의된 통계 결과를 확인할 수 있습니다.
<center><img src="https://github.com/sangeun99/crm-page/assets/63828057/4d31e030-3b90-4a9e-9a2b-0b34fcf1da0f" width="80%" height="80%"></center>

user 주문 정보를 이용한 통계 결과
<center><img src="https://github.com/sangeun99/crm-page/assets/63828057/ef46aebd-c0ec-4c3b-8759-49cf55d255cd" width="80%" height="80%"></center>

user와 store, item은 수기로 추가가 가능합니다.
<center><img src="https://github.com/sangeun99/crm-page/assets/63828057/fcd367e2-2ca3-453d-9a75-9d4cada0d743" width="80%" height="80%"></center>


<!-- LICENSE -->
## License

MIT 라이센스에 따라 배포. 자세한 내용은 `LICENSE`를 참조하세요.

<!-- CONTACT -->
## Contact

* 엄상은
* sangeun99@khu.ac.kr
* sangeun.e.9@gmail.com

