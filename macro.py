#-*- encoding:utf8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from PIL import Image
from PIL import ImageOps
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import time

# 이미지를 선명하게 바꿔주는 함수
def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 180 else 220)
    borderImage = ImageOps.expand(image, border=0, fill='white')
    borderImage.save(imagePath)

# 활동로그를 기록하는 함수
def log(logText):
    # 현재 시간을 구한다.
    now = time.localtime()
    nowTime = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    # 활동로그를 기록한다.
    log = open("log.txt", "a", encoding="utf-8")
    log.write("[" + nowTime + "] " + str(logText) + "\n")
    log.close()

# main
if __name__=="__main__":
# 프로그램 시작
    # 활동로그
    log("프로그램 시작")

    try:
    # 사용자 입력 받기
        # 사용자 정보
        print("_____사용자 정보를 입력해주세요_____")

        # ID, PW
        userID = input("ID : ")
        userPW = input("PW : ")

        # 주민등록번호
        userNum = input("주민등록번호 앞자리 : ")

        # 상품 정보
        print("______상품 정보를 입력해주세요______")

        # 상품명
        userSearch = input("상품명 : ")

        # 날짜 정보
        userDate = input("날짜(YYYYMMDD) : ")

        # 입력값의 유효성검사를 한다.
        now = time.localtime()
        if (int(userDate[4:6]) <= 12) & (1 <= int(userDate[4:6])) != True :
            # 1월 ~ 12월이 아닐 경우
            userDate = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
        if int(userDate[:4]) < now.tm_year :
            # 연도가 현재 날짜 정보보다 이전일 경우
            userDate = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
        elif (int(userDate[:4]) == now.tm_year) & (int(userDate[4:6]) == now.tm_mon) & (int(userDate[6:]) < now.tm_mday) :
            # 연도와 월이 현재 날짜 정보와 일치하는데 날짜가 현재보다 이전일 경우
            userDate = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

        # 회차
        userTime = input("회차 (n회차) : ")

        # 할인 정보
        userTicket = input("할인 : ")

        # 은행 정보
        userBank = input("은행 : ")
        if userBank.find("농협") != -1 : userBank = 38052
        elif userBank.find("중앙") != -1 : userBank = 38052
        elif userBank.find("국민") != -1 : userBank = 38051
        elif userBank.find("우리") != -1 : userBank = 38054
        elif userBank.find("기업") != -1 : userBank = 38057
        elif userBank.find("씨티") != -1 : userBank = 38055
        elif userBank.find("신한") != -1 : userBank = 38056
        elif userBank.find("우체국") != -1 : userBank = 38058
        elif userBank.find("하나") != -1 : userBank = 38053
        else : userBank = 38051

        # 활동로그
        log("사용자 입력 받기")

    # 인터파크 화면 띄우기
        # 드라이브 객체 생성
        url = 'C:/Users/USER/Downloads/chromedriver'  # 드라이브가 있는 경로
        driver = webdriver.Chrome(url)

        # 인터파크 화면 띄우기
        driver.get("https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login")

    # 로그인
        # ID, PW 입력하기
        driver.find_element_by_name('UID').send_keys(userID)  # ID 입력
        driver.find_element_by_name('PWD').send_keys(userPW)  # PW 입력

        # 로그인 버튼 누르기
        driver.execute_script("javascript:login();")

        # 활동로그
        log("로그인 성공")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 검색
        # 검색어 입력 (뮤지컬 레베카, 현대카드 체인스모커스 부산, 쏜애플 콘서트 ‘불구경’)
        driver.find_element_by_xpath("//div[@class='box']//input[@id='Nav_SearchWord']").send_keys(userSearch)

        # 검색 버튼 누르기
        driver.execute_script('Nav_Search(); return false;')

        # 활동로그
        log(userSearch + " 검색")

    # 예매하기_1
        # 예매하기 _2 로 이동하기
        driver.find_element_by_xpath("//div[@class='Poster']//img").click()

    # 예매하기_2
        # 예매창 열기
        driver.execute_script('javascript:fnNormalBooking();')

        # 활동로그
        log("예매창 띄우기")

    # 예매창 객체 받아오기
        driver.switch_to.window(driver.window_handles[1])

        # 닫기 버튼 누르기 (만 n세 미만)
        try:
            elem = driver.find_element_by_xpath("//span[@class='btn02']")
            elem.click()
        except:
            elem = ''

    # 관람일/회차선택 (1단계)
        # 날짜
        # 1단계 프레임 받아오기
        frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to.frame(frame)

        # 달(月) 바꾸기
        # 현재 날짜 정보 가져오기
        #print(driver.page_source)
        YY = driver.find_element_by_xpath("//div[@class='month']//span[2]//em[1]").text
        MM = driver.find_element_by_xpath("//div[@class='month']//span[2]//em[2]").text
        if len(MM) < 2 : MM = "0"+MM
        YYMM = YY+MM

        # 사용자 입력값에서 연도와 월만 따로 추출한다.
        userYYMM = userDate[:6]

        # 결과에 따라 달을 바꿔 준다
        while YYMM < userYYMM :
            # 12월인지 아닌지 확인한다.
            if MM == "12":
                MM = "01"
                YY = int(YY) + 1
                YYMM = str(YY) + str(MM)
            else:
                MM = int(MM)+1
                if len(str(MM)) < 2: MM = "0" + str(MM)
                YYMM = str(YY) + str(MM)

            # 달을 바꾼다.
            driver.execute_script("javascript: fnChangeMonth('"+YYMM+"');")

        # 날짜 선택하기
        # 달력 정보 가져오기
        #print(driver.page_source)
        bs4 = BeautifulSoup(driver.page_source, "html.parser")
        calender = bs4.findAll('a', id='CellPlayDate')
        elem = calender[0]["onclick"]

        # 사용자의 입력값과 일치하는 함수를 찾는다.
        for i in range(0, len(calender)):
            if "fnSelectPlayDate("+str(i)+", '"+userDate+"')" == calender[i]["onclick"]:
                elem = "fnSelectPlayDate("+str(i)+", '"+userDate+"')"
                break

        # 날짜 선택하기
        driver.execute_script("javascript:"+elem)

        # 페이지 로딩 대기
        time.sleep(0.5)

        # 회차 선택하기
        # 회차 정보 가져오기
        #print(driver.page_source)
        bs4 = BeautifulSoup(driver.page_source, "html.parser")
        timeList = bs4.find('div', class_='scrollY').find('span', id='TagPlaySeq').findAll('a', id='CellPlaySeq')

        # 회차 유효성 검사
        try:
            if int(userTime[0]) <= len(timeList) :
                elem = timeList[int(userTime[0])-1]["onclick"]
            else :
                elem = timeList[0]["onclick"]
        except:
            elem = timeList[0]["onclick"]

        # 회차 선택하기
        driver.execute_script("javascript:" + elem)

        # 다음단계
        # 메인 프레임 받아오기
        driver.switch_to.default_content()

        # 2단계 넘어가기
        driver.execute_script("javascript:fnNextStep('P');")

        # 당일 예매 경고창 감지
        try:
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            elem = ''

        # 활동로그
        log("관람일/회차선택")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 좌석 선택 (2단계)
        # 안심 예매
        # 2단계 프레임 받아오기
        driver.switch_to.default_content()
        frame = driver.find_element_by_id('ifrmSeat')
        driver.switch_to.frame(frame)

        # Captcha 뚫기
        try:
            # Captcha가 있을 경우
            while(True):
                # Captcha 사진 가져오기
                bs4 = BeautifulSoup(driver.page_source, "html.parser")
                Captcha = bs4.find('div', class_='capchaInner').find('img', id='imgCaptcha')['src']
                #print(Captcha['src'])

                # Captcha.jpg 만들기
                #captchaUrl = Captcha
                urlretrieve(Captcha, "captcha.jpg")
                cleanImage("captcha.jpg")

                # Captcha 해석하기
                print("_________Captcha 해석하기_________")
                text = input("Captcha : ")
                #image = Image.open('captcha.jpg')
                #text = image_to_string(image)

                # Captcha 값 입력하기
                driver.find_element_by_xpath("//div[@class='capchaInner']//span").click()
                driver.find_element_by_xpath("//input[@id='txtCaptcha']").send_keys(text)

                # Captcha 입력완료
                driver.execute_script("javascript:fnCheck();")

                # 성공 여부 검사
                bs4 = BeautifulSoup(driver.page_source, "html.parser")
                Captcha_ch = bs4.find('div', class_='validationTxt alert')

                if Captcha_ch == None:
                    # 성공했을 경우
                    break
                else:
                    # 실패했을 경우
                    # Captcha 새로고침
                    driver.execute_script("javascript:fnCapchaRefresh();")
                    continue

        except:
            # Captcha가 없을 경우
            elem = ''

    # 다양한 경우에 대한 빈 좌석 칮가
        # 2단계 프레임 받아오기
        driver.switch_to.default_content()
        frame = driver.find_element_by_id('ifrmSeat')
        driver.switch_to.frame(frame)

        # 미니맵 존재여부 검사
        try:
            frame = driver.find_element_by_id('ifrmSeatView')
            driver.switch_to.frame(frame)
            bs4 = BeautifulSoup(driver.page_source, "html.parser")
            elem = bs4.find('map')
        except:
            elem = None

        # 미니맵, 구역의 상태에 따라 동작을 다르게 한다.
        # 미니맵 = O, 구역 = O
        if elem != None :
            # 미니맵이 존재할 경우
            # 구역 리스트 받아오기
            stepList = bs4.findAll('area')

            # 빈 좌석 찾기
            seatch = False
            while seatch != True :
                for i in range(0, len(bs4.findAll('area')) + 1) :
                    # 좌석 프레임 받아오기
                    driver.switch_to.default_content()
                    frame = driver.find_element_by_id('ifrmSeat')
                    driver.switch_to.frame(frame)
                    frame = driver.find_element_by_id('ifrmSeatDetail')
                    driver.switch_to.frame(frame)

                    # 좌석 정보를 읽어온다.
                    bs4 = BeautifulSoup(driver.page_source, "html.parser")
                    seat = bs4.find('img', class_='stySeat')

                    # 좌석 유무를 확인한다.
                    try:
                        # 좌석이 있을 경우
                        # 좌석 선택하기
                        driver.execute_script(seat['onclick'] + ";")

                        # 2단계 프레임 받아오기
                        driver.switch_to.default_content()
                        frame = driver.find_element_by_id('ifrmSeat')
                        driver.switch_to.frame(frame)

                        # 3단계 넘어가기
                        #driver.execute_script("javascript:fnSelect();")

                        # 활동로그
                        log("빈좌석 찾기 성공")

                        # 페이지 로딩 대기
                        time.sleep(0.5)

                        # 반복문 종료
                        seatch = True
                        break

                    except:
                        # 좌석이 없을 경우
                        # 미니맵 프레임 받아오기
                        driver.switch_to.default_content()
                        frame = driver.find_element_by_id('ifrmSeat')
                        driver.switch_to.frame(frame)
                        frame = driver.find_element_by_id('ifrmSeatView')
                        driver.switch_to.frame(frame)

                        # 구역 리스트 받아오기
                        bs4 = BeautifulSoup(driver.page_source, "html.parser")
                        stepList = bs4.findAll('area')

                        # 구역 바꾸기
                        if i == len(stepList) :
                            # 마지막 반복 단계
                            driver.execute_script(stepList[0]["href"])
                        else :
                            # 그 외
                            driver.execute_script(stepList[i]["href"])

                        # 페이지 로딩 대기
                        time.sleep(0.5)

                        # 좌석을 불러오기 경고창 감지
                        try:
                            alert = driver.switch_to_alert()
                            alert.accept()
                        except:
                            elem = ''

        else :
            # 미니맵이 존재하지 않을 경우
            # 좌석 프레임 받아오기
            driver.switch_to.default_content()
            frame = driver.find_element_by_id('ifrmSeat')
            driver.switch_to.frame(frame)
            frame = driver.find_element_by_id('ifrmSeatDetail')
            driver.switch_to.frame(frame)

            # 구역 존재여부 검사
            bs4 = BeautifulSoup(driver.page_source, "html.parser")

            # 미니맵 = X, 구역 = O
            if bs4.find('map') != None :
                # 구역이 존재할 경우
                # 구역 리스트 받아오기
                areaList = bs4.findAll('area')

                # 빈 좌석 찾기
                seatch = False
                while seatch != True :
                    for i in range(5, len(areaList)) :
                        # 좌석 프레임 받아오기
                        driver.switch_to.default_content()
                        frame = driver.find_element_by_id('ifrmSeat')
                        driver.switch_to.frame(frame)
                        frame = driver.find_element_by_id('ifrmSeatDetail')
                        driver.switch_to.frame(frame)

                        # 구역 바꾸기
                        driver.execute_script(areaList[i]["href"])

                        # 좌석 유무를 확인한다.
                        try:
                            # 좌석이 있을 경우
                            # 좌석 선택하기
                            driver.find_element_by_xpath("//span[@value='N']").click()

                            # 2단계 프레임 받아오기
                            driver.switch_to.default_content()
                            frame = driver.find_element_by_id('ifrmSeat')
                            driver.switch_to.frame(frame)

                            # 3단계 넘어가기
                            #driver.execute_script("javascript:fnSelect();")

                            # 활동로그
                            log("빈좌석 찾기 성공")

                            # 페이지 로딩 대기
                            time.sleep(0.5)

                            # 반복문 종료
                            seatch = True
                            break

                        except:
                            # 좌석이 없을 경우
                            # 2단계 프레임 받아오기
                            driver.switch_to.default_content()
                            frame = driver.find_element_by_id('ifrmSeat')
                            driver.switch_to.frame(frame)

                            # 좌석도 전체보기
                            driver.execute_script("javascript:fnSeatUpdate();")

                            # 페이지 로딩 대기
                            time.sleep(0.5)

            # 미니맵 = X, 구역 = X
            else :
                # 구역이 존재하지 않을 경우
                # 빈 좌석 찾기
                while (True):
                    # 좌석 프레임 받아오기
                    driver.switch_to.default_content()
                    frame = driver.find_element_by_id('ifrmSeat')
                    driver.switch_to.frame(frame)
                    frame = driver.find_element_by_id('ifrmSeatDetail')
                    driver.switch_to.frame(frame)

                    # 좌석 정보를 읽어온다.
                    bs4 = BeautifulSoup(driver.page_source, "html.parser")
                    seat = bs4.find('img', class_='stySeat')

                    # 좌석 유무를 확인한다.
                    try:
                        # 좌석이 있을 경우
                        # 좌석 선택하기
                        driver.execute_script(seat['onclick'] + ";")

                        # 2단계 프레임 받아오기
                        driver.switch_to.default_content()
                        frame = driver.find_element_by_id('ifrmSeat')
                        driver.switch_to.frame(frame)

                        # 3단계 넘어가기
                        #driver.execute_script("javascript:fnSelect();")

                        # 활동로그
                        log("빈좌석 찾기 성공")

                        # 페이지 로딩 대기
                        time.sleep(0.5)
                        break

                    except:
                        # 2단계 프레임 받아오기
                        driver.switch_to.default_content()
                        frame = driver.find_element_by_id('ifrmSeat')
                        driver.switch_to.frame(frame)

                        # 좌석 다시 선택 (새로고침)
                        driver.execute_script("javascript:fnRefresh();")

                        # 페이지 로딩 대기
                        time.sleep(0.5)
                        continue

    # 가격/할인선택 (3단계)
        # 3단계 프레임 받아오기
        driver.switch_to.default_content()
        frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to.frame(frame)

        # 표 선택하기
        # 표 정보를 가져온다.
        #print(driver.page_source)
        bs4 = BeautifulSoup(driver.page_source, "html.parser")
        ticketList = bs4.findAll('select')

        # 사용자의 입력값과 일치하는 함수를 찾는다.
        elem = "001" # 만약 일치하는 값이 없을 경우 일반표를 잡는다.
        for i in range(0, len(ticketList)):
            ticketStr = ticketList[i]["pricegradename"]
            if ticketStr.find(userTicket) != -1:
                elem = ticketList[i]["index"]
                break

        # 표 선택하기
        elem = driver.find_element_by_xpath("//td[@class='taL']//select[@index='"+elem+"']//option[@value='1']")
        elem.click()

        '''
        # 특수표 경고창 감지
        try:
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            elem = ''
        # '''

        # 다음단계
        # 메인 프레임 받아오기
        driver.switch_to.default_content()

        # 4단계 넘어가기
        driver.execute_script("javascript:fnNextStep('P');")

        # 활동로그
        log("가격/할인선택")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 배송선택/주문자확인 (4단계)
        # 4단계 프레임 받아오기
        frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to.frame(frame)

        # 주문자 정보 입력 (주민번호 앞 6자리 : YYDDMM)
        #print(driver.page_source)
        driver.find_element_by_xpath("//td[@class='form']//input[@id='YYMMDD']").send_keys(userNum)  # 주민번호 입력

        # 이메일 정보를 받아온다.
        bs4 = BeautifulSoup(driver.page_source, "html.parser")
        userEmail = bs4.find('input', id='Email')["value"]

        # 다음단계
        # 메인 프레임 받아오기
        driver.switch_to.default_content()

        # 5단계 넘어가기
        driver.execute_script("javascript:fnNextStep('P');")

        # 활동로그
        log("배송선택/주문자확인")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 결제하기_1 (5-1단계)
        # 5-1단계 프레임 받아오기
        frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to.frame(frame)

        # 결제 수단 선택 (무통장입금)
        #print(driver.page_source)
        elem = driver.find_element_by_xpath("//tr[@id='Payment_22004']//input[@name='Payment']")
        elem.click()

        # 은행 선택 (무통장입금)
        elem = driver.find_element_by_xpath("//select[@id='BankCode']//option[@value='" + str(userBank) + "']")
        elem.click()

        # 다음단계
        # 메인 프레임 받아오기
        driver.switch_to.default_content()

        # 5-2단계 넘어가기
        driver.execute_script("javascript:fnNextStep('P');")

        # 활동로그
        log("결제하기")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 결제하기 _2 (5-2단계)
        # 5-1단계 프레임 받아오기
        frame = driver.find_element_by_id('ifrmBookStep')
        driver.switch_to.frame(frame)

        # 약관 동의
        # 취소수수료/취소기한을 확인하였으며, 동의합니다.
        elem = driver.find_element_by_xpath("//input[@id='CancelAgree']")
        elem.click()

        # 제3자 정보제공 내용에 동의합니다.
        elem = driver.find_element_by_xpath("//input[@id='CancelAgree2']")
        elem.click()

        # 다음단계
        # 메인 프레임 받아오기
        driver.switch_to.default_content()

        # 5-2단계 넘어가기
        driver.execute_script("javascript:fnNextStep('P');")

        # 활동로그
        log("예매 완료")

        # 페이지 로딩 대기
        time.sleep(0.5)

    # 예매 정보 출력
        # 예매 완료 페이지 받아오기
        driver.switch_to.default_content()
        frame = driver.find_element_by_id('ifrmBookEnd')
        driver.switch_to.frame(frame)

        # 예매 정보를 기록할 파일을 만든다
        result = open("result.txt", "w", encoding="utf-8")

        # 상품정보
        print("___________ 상품정보 ___________")
        result.write("___________ 상품정보 ___________\n")

        # 예약 번호
        text_1 = driver.find_element_by_xpath("//p[@class='tit']//span[1]").text
        text_2 = driver.find_element_by_xpath("//p[@class='tit']//span[2]").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 상품
        text_1 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[1]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[1]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 장소
        text_1 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[2]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[2]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 일시
        text_1 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[3]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[3]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 좌석
        text_1 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[4]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contT']//table//tbody//tr[4]//td//div[@class='box_scroll']").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 예매자 정보
        print("__________ 예매자 정보 __________")
        result.write("__________ 예매자 정보 __________\n")

        # 예매자
        text_1 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[1]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[1]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 예매자 연락처
        text_1 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[2]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[2]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 티켓수령방법
        text_1 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[3]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='contB']//table//tbody//tr[3]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 결제정보
        print("___________ 결제정보 ___________")
        result.write("___________ 결제정보 ___________\n")

        # 총 결제금액
        text_1 = driver.find_element_by_xpath("//table[@class='new_t']//thead//tr[1]//th").text
        text_2 = driver.find_element_by_xpath("//table[@class='new_t']//thead//tr[1]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 티켓금액
        text_1 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[1]//th").text
        text_2 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[1]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 수수료
        text_1 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[2]//th").text
        text_2 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[2]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 배송료
        text_1 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[3]//th").text
        text_2 = driver.find_element_by_xpath("//table[@class='new_t']//tbody//tr[3]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 취소기한
        text_1 = driver.find_element_by_xpath("//div[@class='completeL']//ul//li[1]").text
        print(text_1)
        result.write(text_1 + "\n")

        # 결제상세정보
        print("_________ 결제상세정보 _________")
        result.write("_________ 결제상세정보 _________\n")

        # 결제방법
        text_1 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[1]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[1]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 입금마감일시
        text_1 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[2]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[2]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 입금계좌
        text_1 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[3]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[3]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 예금주명
        text_1 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[4]//th").text
        text_2 = driver.find_element_by_xpath("//div[@class='completeR']//table//tbody//tr[4]//td").text
        print(text_1, end=' : ')
        print(text_2)
        result.write(text_1 + " : ")
        result.write(text_2 + "\n")

        # 예매 정보를 기록한 파일을 닫아준다.
        result.close()

        # 활동로그
        log("예매 정보 출력")

    # 예매창 닫기
        driver.close()

        # 활동로그
        log("예매창 닫기")

    # 이메일 보내기
        # 보내는 주소 & 포트
        host = 'smtp.gmail.com'
        port = '587'

        # 보내는 사람 & 받는 사람
        sender = 'interparkmacro@gmail.com'
        recipient = userEmail

        # 메세지 객체 생성
        msg = MIMEBase('multipart', 'mixed')
        msg['Subject'] = '인터파크 예매내역'
        msg['From'] = sender
        msg['To'] = recipient

        # 전달할 내용 입력
        result = open('result.txt', 'r', encoding="utf-8").readlines()
        resultText = ''
        for i in range(0, len(result)) :
            resultText = resultText + result[i]
        resultPart = MIMEText(resultText, _charset='utf-8')
        msg.attach(resultPart)

        # 이메일 보내기
        send = smtplib.SMTP(host, port)
        send.ehlo()
        send.starttls()
        send.ehlo()
        send.login(sender, 'password:123')
        send.sendmail(sender, [recipient], msg.as_string())
        send.close()

        # 활동로그
        log("이메일 전송")

    # 마이페이지 접속
        # 기존 창으로 제어를 이동한다.
        driver.switch_to.window(driver.window_handles[0])

        # 마이페이지로 이동
        elem = driver.find_element_by_xpath("//div[@class='login']//a[@class='btn']")
        elem.click()

        # 활동로그
        log("마이페이지 접속")

    # 예매결과 확인
        # 예매내역 중 가장 최신 내역을 확인한다.
        driver.execute_script("javascript: fnPlayBookDetail(0);")

        # 활동로그
        log("예매결과 확인")

    except:
        # 에러 발생할 경우
        print("error")

        # 활동로그
        log("에러 발생")

# 프로그램 종료
    # 활동로그
    log("프로그램 종료")