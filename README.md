## Introduction

Opensource music streaming site [SoundCloud](https://soundcloud.com/) clone. 
#### Topic
- 음원 스트리밍 사이트 클론 프로젝트

#### Team 
- 프론트앤드 2명, 백앤드 3명, 리엑트 네이티브 1명

#### Project Period 
- 2020.03.09 - 2020.03.20

#### Coworking 
- Trello를 스크럼방식 협업
- 주단위 백로그작성
- 일단위 스탠드업미팅
         
## 담당 개발 내역
[Django 프로젝트 초기 설계]
- my_settings.py : database 정보, secret key, jwt 알고리즘 정보 관리
- requirements.txt : 개발 환경 공유

[음원 메타데이터 크롤링]
- beautiful soup, requests
- pandas 를 통한 csv 파일 생성

[회원가입 기능]
- 이메일 유효성 검사
- bcrypt로 비밀번호 암호화

[로그인]
- bcrypt checkpw를 통해서 해쉬된 패스워드 비교
- 로그인 성공 시 jwt 토큰 밠행

[구글 소셜 회원가입]
- 클라이언트가 소셜로그인 후 받은 id token을 구글 에서 제공하는 url의 쿼리파라미터에 담아서 request를 보냄 
- 구글에 요청해서 받은 이메일과 이름을 데이터베이스에 저장하고 jwt 토큰을 리턴함

[구글 소셜 로그인]
- id token으로 구글에 요청해서 받은 유저의 이메일이 있으면 jwt 토큰을 리턴

[SNS 유저 팔로우 / 언팔로우 기능]
- 유저 테이블을 many to many(self 참조)로 하는 Follow 테이블 생성
- 토큰의 유저정보를 확인해서 팔로우를 하는 유저(from_user_id) 정보 등록
- 팔로우 한 유저를 다시 팔로우 한 경우 팔로우 취소

[업데이트 알림 기능 구현]
- 나를 팔로우 한 사람이 있거나 나에게 메세지를 보낸 사람이 있으면 표시
- 화면을 refresh할 때 마다 상태 api를 요청함

[상태창 기능 구현]
- 나를 팔로우 한 사람의 정보(음원 갯수, 프로필이미지, 팔로워 수) 표출
- 나와 상대방이 서로 팔로우 한 상태 여부 표출
- 상대방이 나를 팔로우 했는 상황을 내가 체크했는지 여부 표출

[메세지 보내기]
- 유저 테이블을 many to many(self 참조)로 하는 Message 테이블 생성
- 토큰 정보에 있는 유저를 송신자, 요청으로 받은 유저를 수신자로 하는 메세지 저장

[메세지 표출]
- 최근 보내거나 받은 메세지를 썸네일로 표출
- 대화창에 들어가서 전체 메세지 표출

[음악 댓글 기능 구현]
- 재생이 되고있는 위치에 댓글리 달림
- 저장할 때 재생 위치를 저장하고 표출할 때 재생 댓글과 재생위치를 표출

## Demo
Click below image to see our demo.

[![SoundCloud demo](https://images.velog.io/images/valentin123/post/3c2d9978-8f14-4773-8ee3-6d634c295120/%EC%95%B1.png)](https://www.youtube.com/watch?v=u6SGpbk2x5A&feature=youtu.be)

## Features
+ Self-made sign-up and sign-in features(Heechul Yoon).
+ Google sign-up and sign-in features(Heechul Yoon).
+ Send and reciption of message(Heechul Yoon).
+ Follow and unfollow feature(Heechul Yoon).
+ Notification for message and follow(Heechul Yoon).
+ Comment on song giving timely position(Heechul Yoon).
+ User recommendation to follow(Heechul Yoon).
+ MainPage page, Audio list API(Minkyu Kim).
+ Audio details (Minkyu Kim).
+ Auido Analizations and upload Audio file(Minkyu Kim).
+ Progressive download audio streaming (Minkyu Kim).

## Technologies
+ Python 3.8.0
+ Django 3.0.4
+ MySQL
+ Git : rebase 커밋관리
+ Django Unit Test
+ Bcrypt : 패스워드 암호화
+ JWT : 토큰 발행
+ AWS RDS
+ AWS S3

## API Documentation
+ [message, follow, notification](https://documenter.getpostman.com/view/10644576/SzS8rjpk?version=latest#db667abf-875b-4a91-8c64-466ad7f301f2)
+ [main page, stream list page, play audio view, streaming data](https://documenter.getpostman.com/view/10398707/SzfDvQ7Q?version=latest#ed51a1eb-edd3-4db4-8260-21b18355b0a1)
## Database Modeling
![SoundCloud ERD](https://media.vlpt.us/images/valentin123/post/ca1b2e01-6bcb-4e91-8720-63eafe514c6c/NotSoundCloud_20200412_23_27.png)
