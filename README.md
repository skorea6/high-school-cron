# 프로젝트 제목
고등학교 홈페이지 급식표/공지사항 크롤링 파이썬

# 주요 특징
* 매우 간단한 코드입니다.
* 급식표 URL: http://unjung.hs.kr/?act=lunch.main&month=날짜
* 공지사항 URL: http://unjung.hs.kr/?act=board.list&code=1131&page=페이지
* 급식표는 날짜를 +1 달씩 올리면서 크롤링하는 형식이며, 공지사항은 페이지수를 하나씩 올리면서 크롤링합니다.
* 크롤링을 할때마다 DB와 중복 검사를 실행합니다. 중복이 아닐때만 Insert 쿼리.
