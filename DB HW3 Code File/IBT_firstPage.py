from enum import auto
from logging import log
import tkinter.ttk as ttk
from tkinter import *
import re
from typing import final
import mysql.connector
import tkinter.font as tkFont
from tkinter import messagebox
import sql as sql


cnx = mysql.connector.connect(user='root', password='gritman1', \
                    host='localhost', database='intercity_bus_terminal_final')
cursor = cnx.cursor(buffered=True)

root = Tk()
root.title("Bus Reservation System")
root.geometry("600x600+50+0")

def show_cities():
  cursor.execute("SELECT DISTINCT DEPARTURE FROM PATH")
  return cursor.fetchall()

city_list = show_cities()
city_list = [_depart[0] for _depart in city_list]
city_list.sort()

#global variables
depart = ""
dest = ""
ymd = ""
adult = ""
child = ""
teenager = ""
path_id = ""
pathInfo = ""
pathList = []
reserved_seats1 = []
reserved_seats = []
selectedSeats = []
listboxPath = None

def btnSearchCmd():
  global depart, dest, ymd, pathInfo, pathList, adult, child, teenager
  depart = combobox_depart.get()
  dest = combobox_dest.get()
  adult = txtAdult.get("1.0",END)
  child = txtChild.get("1.0",END)
  teenager = txtTeen.get("1.0", END)
  year = combobox_year.get()
  year = year[0:4]
  month = combobox_month.get()
  month = re.sub(r'[^0-9]', '', month)
  day = combobox_day.get()
  day = re.sub(r'[^0-9]', '', day)
  ymd = year + '-' + month + '-' + day
  
  pathList = first_page(depart, dest, ymd)
  pathInfo = "<" + depart +" -> "+ dest +" "+ year + "년 " + month + "월 " + day + "일>"

  label7 = Label(root, text=">가능 경로 ")
  label7.grid(row = 7, column = 0)

  global listboxPath
  listboxPath = Listbox(root, selectmode="extended", height=0, width='60')
  for i, elem in enumerate(pathList):
    listboxPath.insert(i, getting_organized_info(elem))

  label8 = Label(root, text = pathInfo)
  label8.grid(row=7, column = 2)  
  label9 = Label(root, text = makeCommanInfo(pathList))
  label9.grid(row=8, column = 1, columnspan=3)
  listboxPath.grid(row=9, column=1, columnspan=3)

def makeCommanInfo(bus_routes):
  bus_route = bus_routes[0]
  commonInfo = ""
  duration_time = bus_route[4]
  commonInfo += " 소요 예상 시간 : {}분 / ".format(duration_time)
  adult_cost = int(duration_time * 2000 / 10) #소요 시간 10분당 2000원
  child_cost = int(adult_cost * 0.8) #어른의 20% 할인
  teen_cost = int(adult_cost * 0.9) #어른의 10% 할인
  commonInfo += "요금| 어른 : {}원 아동 : {}원 중고생 : {}원"\
    .format(adult_cost, child_cost, teen_cost)
  return commonInfo
  
def getting_organized_info(bus_route):
  path_id = bus_route[0]
  cursor.execute("SELECT SEATS_NUM FROM SEATS WHERE PATH_ID = %s", (path_id,))
  reserved_nums = cursor.fetchall()
  for elem in reserved_nums:
    reserved_seats.append(elem[0])
  unreserved_count = 28 - len(reserved_nums)
  str_time = bus_route[3].strftime("%H:%M") # datetime객체임
  duration_time = bus_route[4]
  s_ =  str(path_id)
  s_ += " 출발 시각 : "
  s_ += str_time
  s_ += " 잔여좌석/총좌석 : {}석 / 총 28석".format(unreserved_count)
  
  return s_

def first_page(depart, dest, depart_date):

  bus_route_sql = "SELECT * FROM PATH WHERE DEPART_TIME >= %s AND DEPART_TIME <= %s AND DEPARTURE = %s AND DESTINATION = %s"
  cursor.execute(bus_route_sql, (depart_date + " 00:00:00", depart_date + " 23:59:59", depart, dest))  
  bus_routes = cursor.fetchall()
  print(bus_routes)
  return bus_routes

#------------------------------------------------------------------------

def isBtnChecked(index, btnChecked):
  selectedSeats.append(index + 1)
  btnChecked[index] = 1
  print(btnChecked)
  print(selectedSeats)

def printSecondpage(newWindow, reservedSeats):
    newWindow.title("Select Seats")
    newWindow.geometry("500x900")
    str_  = ""

    seats = [str(i+1) for i in range(28)]
    isSeatReserved = ['normal' for _ in range(28)]
    btnChecked = [0 for _ in range(28)]

    for elem in reservedSeats:
      seats[elem -1] = 'x'
      isSeatReserved[elem-1] = 'disabled'
      str_ += str(elem) + " "
        
    labelStr = '이미 예약된 좌석: ' + str_
    label1 = Label(newWindow, text=labelStr)
    label1.grid(row = 0, column = 0, columnspan=6)

#row1
    btn10 = Button(newWindow, width=10, height=5, text = seats[0], state= isSeatReserved[0], command=lambda: isBtnChecked(0, btnChecked))
    btn10.grid(row=1, column=0)

    btn11 = Button(newWindow, width=10, height=5, text = seats[1], state= isSeatReserved[1], command=lambda: isBtnChecked(1, btnChecked))
    btn11.grid(row=1, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 1, column = 2)

    btn12 = Button(newWindow, width=10, height=5, text = seats[2], state= isSeatReserved[2], command=lambda: isBtnChecked(2, btnChecked))
    btn12.grid(row=1, column=3)

#row2
    btn13 = Button(newWindow, width=10, height=5, text = seats[3], state= isSeatReserved[3], command=lambda: isBtnChecked(3, btnChecked))
    btn13.grid(row=2, column=0)

    btn14 = Button(newWindow, width=10, height=5, text = seats[4], state= isSeatReserved[4], command=lambda: isBtnChecked(4, btnChecked))
    btn14.grid(row=2, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 2, column = 2)

    btn15 = Button(newWindow, width=10, height=5, text = seats[5], state= isSeatReserved[5], command=lambda: isBtnChecked(5, btnChecked))
    btn15.grid(row=2, column=3)

#row3
    btn16 = Button(newWindow, width=10, height=5, text = seats[6], state= isSeatReserved[6], command=lambda: isBtnChecked(6, btnChecked))
    btn16.grid(row=3, column=0)

    btn17 = Button(newWindow, width=10, height=5, text = seats[7], state= isSeatReserved[7], command=lambda: isBtnChecked(7, btnChecked))
    btn17.grid(row=3, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 3, column = 2)

    btn18 = Button(newWindow, width=10, height=5, text = seats[8], state= isSeatReserved[8], command=lambda: isBtnChecked(8, btnChecked))
    btn18.grid(row=3, column=3)

#row4
    btn19 = Button(newWindow, width=10, height=5, text = seats[9], state= isSeatReserved[9], command=lambda: isBtnChecked(9, btnChecked))
    btn19.grid(row=4, column=0)

    btn20 = Button(newWindow, width=10, height=5, text = seats[10], state= isSeatReserved[10], command=lambda: isBtnChecked(10, btnChecked))
    btn20.grid(row=4, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 4, column = 2)

    btn21 = Button(newWindow, width=10, height=5, text = seats[11], state= isSeatReserved[11], command=lambda: isBtnChecked(11, btnChecked))
    btn21.grid(row=4, column=3)

#row5
    btn22 = Button(newWindow, width=10, height=5, text = seats[12], state= isSeatReserved[12], command=lambda: isBtnChecked(12, btnChecked))
    btn22.grid(row=5, column=0)

    btn23 = Button(newWindow, width=10, height=5, text = seats[13], state= isSeatReserved[13], command=lambda: isBtnChecked(13, btnChecked))
    btn23.grid(row=5, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 5, column = 2)

    btn24 = Button(newWindow, width=10, height=5, text = seats[14], state= isSeatReserved[14], command=lambda: isBtnChecked(14, btnChecked))
    btn24.grid(row=5, column=3)

#row6
    btn25 = Button(newWindow, width=10, height=5, text = seats[15], state= isSeatReserved[15], command=lambda: isBtnChecked(15, btnChecked))
    btn25.grid(row=6, column=0)

    btn26 = Button(newWindow, width=10, height=5, text = seats[16], state= isSeatReserved[16], command=lambda: isBtnChecked(16, btnChecked))
    btn26.grid(row=6, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 6, column = 2)

    btn27 = Button(newWindow, width=10, height=5, text = seats[17], state= isSeatReserved[17], command=lambda: isBtnChecked(17, btnChecked))
    btn27.grid(row=6, column=3)

#row7
    btn28 = Button(newWindow, width=10, height=5, text = seats[18], state= isSeatReserved[18], command=lambda: isBtnChecked(18, btnChecked))
    btn28.grid(row=7, column=0)

    btn29 = Button(newWindow, width=10, height=5, text = seats[19], state= isSeatReserved[19], command=lambda: isBtnChecked(19, btnChecked))
    btn29.grid(row=7, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 7, column = 2)

    btn30 = Button(newWindow, width=10, height=5, text = seats[20], state= isSeatReserved[20], command=lambda: isBtnChecked(20, btnChecked))
    btn30.grid(row=7, column=3)

#row8
    btn31 = Button(newWindow, width=10, height=5, text = seats[21], state= isSeatReserved[21], command=lambda: isBtnChecked(21, btnChecked))
    btn31.grid(row=8, column=0)

    btn32 = Button(newWindow, width=10, height=5, text = seats[22], state= isSeatReserved[22], command=lambda: isBtnChecked(22, btnChecked))
    btn32.grid(row=8, column=1)

    btn_ = Button(newWindow, width=10, height=5, text="", state= 'disabled')
    btn_.grid(row = 8, column = 2)

    btn33 = Button(newWindow, width=10, height=5, text = seats[23], state= isSeatReserved[23], command=lambda: isBtnChecked(23, btnChecked))
    btn33.grid(row=8, column=3)

#row9
    btn34 = Button(newWindow, width=10, height=5, text = seats[24], state= isSeatReserved[24], command=lambda: isBtnChecked(24, btnChecked))
    btn34.grid(row=9, column=0)

    btn35 = Button(newWindow, width=10, height=5, text = seats[25], state= isSeatReserved[25], command=lambda: isBtnChecked(25, btnChecked))
    btn35.grid(row=9, column=1)

    btn36 = Button(newWindow, width=10, height=5, text = seats[26], state= isSeatReserved[26], command=lambda: isBtnChecked(26, btnChecked))
    btn36.grid(row = 9, column = 2)

    btn37 = Button(newWindow, width=10, height=5, text = seats[27], state= isSeatReserved[27], command=lambda: isBtnChecked(27, btnChecked))
    btn37.grid(row=9, column=3)

    def quit():
      newWindow.destroy()

    btnEnd = Button(newWindow, command=quit, text="창 닫고 예약한 좌석 확인하기")
    btnEnd.grid(row=10, column=1, columnspan=2)
#-----------------------------------------------------------------------------------

label_depart = Label(root, text=">출발지  ")
label_depart.grid(row = 0, column=0, pady = 5)

combobox_depart = ttk.Combobox(root, height=5, width=60, values=city_list)
combobox_depart.grid(row=0, column=1, columnspan=3)
combobox_depart.set("서울")

label_depart = Label(root, text=">도착지  ")
label_depart.grid(row = 1, column=0, pady = 5)

combobox_dest = ttk.Combobox(root, height=5, width=60, values=city_list)
combobox_dest.grid(row=1, column=1, columnspan=3)
combobox_dest.set("부산")

#년월일 배열 생성
years = [str(i) + '년' for i in range(2021, 2030)]
months = [str(i) + '월' for i in range(1, 13)]
days = [str(i) + '일' for i in range(1, 32)]

label3 = Label(root, text=">출발날짜 ")
label3.grid(row = 2, column = 0, pady = 5)

combobox_year = ttk.Combobox(root, height=5, width=14, values=years)
combobox_year.grid(row=2, column=1)
combobox_year.set("_ _ _ _년")
combobox_year.set("2021년")

combobox_month = ttk.Combobox(root, height=12, width=14, values=months)
combobox_month.grid(row=2, column=2)
combobox_month.set("_ _월")
combobox_month.set("10월")

combobox_day = ttk.Combobox(root, height=15, width=14, values=days)
combobox_day.grid(row=2, column=3)
combobox_day.set("_ _일")
combobox_day.set("14일")

label4 = Label(root, text=">어른  ")
label4.grid(row = 3, column = 0, pady = 5)

txtAdult = Text(root, height=1, width=63)
txtAdult.grid(row = 3,  column=1, columnspan=3)

label5 = Label(root, text=">아동  ")
label5.grid(row = 4, column = 0, pady = 5)

txtChild = Text(root, height=1, width=63)
txtChild.grid(row = 4,  column=1, columnspan=3)

label6 = Label(root, text=">중고생 ")
label6.grid(row = 5, column = 0, pady = 5)

txtTeen = Text(root, height=1, width=63)
txtTeen.grid(row = 5,  column=1, columnspan=3)

btnSearch = Button(root, height=1, width=16, text='Q 조회', command=btnSearchCmd)
btnSearch.grid(row = 6, column=3)

#버스 좌석 선택창 버튼 구성
selectedSeats =[] #선택된 좌석의 배열을 저장
def new_window():
  global reserved_seats1, path_id
  newWindow = Toplevel(root)
  selectedRouteNum = listboxPath.curselection()[0]
  path_id = pathList[selectedRouteNum][0]
  print(path_id)
  cursor.execute("SELECT SEATS_NUM FROM SEATS WHERE PATH_ID = %s", (path_id,))
  reserved_nums = cursor.fetchall()
  reserved_seats1 = []
  print(reserved_nums)
  for elem in reserved_nums:
    reserved_seats1.append(elem[0])  
  print(reserved_seats1)
  printSecondpage(newWindow, reserved_seats1)

btn1 = Button(root, text='버스 좌석 선택하기', command=new_window)
btn1.grid(row=10, column=0)

def checkSelectedSeats(selectedSeats):
  selectedSeats.sort()
  ss = ""
  for elem in selectedSeats:
    ss += str(elem) + " "
  labelSelecedSeats = Label(root, text = '선택한 좌석: '+ ss)
  labelSelecedSeats.grid(row=11, column=1, columnspan=2)

btn2 = Button(root, text="선택 좌석 확인하기", command=lambda: checkSelectedSeats(selectedSeats))
btn2.grid(row=11, column=0)

fontStyle = tkFont.Font(family="Lucida Grande", size=7)

def printThirdPage(new_window):
  label0 = Label(new_window, text=">카드정보 입력")
  label0.grid(row=0, column=0)

  label01 = Label(new_window, text="* 신용카드 결제를 위해 필요한 정보이므로 정확하게 입력하여 주십시오."\
    ,font = fontStyle)
  label01.grid(row=0, column=1, columnspan=4)

  label1 = Label(new_window, text="* 카드구분")
  label1.grid(row = 1, column = 0)

  radio_var = StringVar()
  rdb_credit = Radiobutton(new_window, text="신용", value = "신용", variable=radio_var)
  rdb_check = Radiobutton(new_window, text="체크", value="체크", variable=radio_var)
  rdb_credit.grid(row = 1, column=1)
  rdb_check.grid(row = 1, column=2)

  bankArr = ['국민', '기업', '신한', '우리', '카카오', '새마을', '우체국', '농협', '수협']
  bankArr.sort()

  label2 = Label(new_window, text="* 카드선택")
  label2.grid(row = 2, column = 0)
  comboBank = ttk.Combobox(new_window, height=5, values = bankArr, width=20)
  comboBank.grid(row = 2, column = 1, columnspan=2)
  comboBank.set("카드선택")

  label3 = Label(new_window, text="* 카드번호")
  label3.grid(row = 3, column = 0)
  txtCN1 = Text(new_window, width=9, height = 1)
  txtCN1.grid(row=3, column = 1)
  txtCN2 = Text(new_window, width=9, height = 1)
  txtCN2.grid(row=3, column = 2)
  txtCN3 = Text(new_window, width=9, height = 1)
  txtCN3.grid(row=3, column = 3)
  txtCN4 = Text(new_window, width=9, height = 1)
  txtCN4.grid(row=3, column = 4)

  label4 = Label(new_window, text="* 유효기간")
  label4.grid(row = 4, column = 0)

  years = [str(i) + '년' for i in range(2021, 2030)]
  months = [str(i) + '월' for i in range(1, 13)]  

  comboCVM = ttk.Combobox(new_window, height=12, width=6, values=months)
  comboCVM.grid(row=4, column=1)
  comboCVM.set("_ _월")

  comboCVY = ttk.Combobox(new_window, height=10, width=6, values=years)
  comboCVY.grid(row=4, column=2)
  comboCVY.set("_ _ _ _년")


  label5 = Label(new_window, text="* 카드비밀번호")
  label5.grid(row = 5, column = 0)

  txtPW = Text(new_window, width=9, height = 1)
  txtPW.grid(row=5, column = 1)
  label51 = Label(new_window, text = " **  (비밀번호 앞 2자리를 입력해주세요.", font = fontStyle)
  label51.grid(row = 5, column = 2, columnspan= 2)


  label6 = Label(new_window, text="* 주민번호 앞 6자리")
  label6.grid(row = 6, column = 0)
  txtBC = Text(new_window, width=18, height = 1)
  txtBC.grid(row=6, column = 1, columnspan=2)

  labelBlank = Label(new_window, text="")
  labelBlank.grid(row = 7, column=0)

  label8 = Label(new_window, text = ">예매조회정보 입력")
  label8.grid(row = 8, column=0)

  label81 = Label(new_window, text = "* 아래는 예매 사항을 조회하기 위한 정보입니다.", font = fontStyle)
  label81.grid(row = 8, column=1, columnspan=3)

  labelName = Label(new_window, text = "* 예매자 이름")
  labelName.grid(row = 9, column=0)

  txtName = Text(new_window, height=1, width = 9)
  txtName.grid(row = 9, column=1)

  label9 = Label(new_window, text = "* 생년월일")
  label9.grid(row = 10, column=0)

  years = [str(i) + '년' for i in range(1940, 2022)]
  months = [str(i) + '월' for i in range(1, 13)]
  days = [str(i) + '일' for i in range(1, 32)]

  combobox_year = ttk.Combobox(new_window, height=15, width=6, values=years)
  combobox_year.grid(row=10, column=1)
  combobox_year.set("_ _ _ _년")

  combobox_month = ttk.Combobox(new_window, height=12, width=6, values=months)
  combobox_month.grid(row=10, column=2)
  combobox_month.set("_ _월")

  combobox_day = ttk.Combobox(new_window, height=15, width=6, values=days)
  combobox_day.grid(row=10, column=3)
  combobox_day.set("_ _일")

  label10 = Label(new_window, text = "* 휴대폰 번호")
  label10.grid(row = 11, column=0)

  txtPN1 = Text(new_window, height=1, width = 9)
  txtPN1.grid(row = 11, column=1)

  txtPN2 = Text(new_window, height=1, width = 9)
  txtPN2.grid(row = 11, column=2)

  txtPN3 = Text(new_window, height=1, width = 9)
  txtPN3.grid(row = 11, column=3)

  label11 = Label(new_window, text = "* 로그인 비밀번호")
  label11.grid(row = 13, column=0)

  txtLogPW = Text(new_window, height=1, width = 9)
  txtLogPW.grid(row = 13, column = 1)

  label12 = Label(new_window, text = "(휴대폰번호 뒤4자리)")
  label12.grid(row = 14, column=0)
  
  paymentInfo = {}
  def btnPayment(paymentInfo):
    year = combobox_year.get()
    year = year[0:4]
    month = combobox_month.get()
    month = re.sub(r'[^0-9]', '', month)
    day = combobox_day.get()
    day = re.sub(r'[^0-9]', '', day)
    ymd = year + '-' + month + '-' + day

    paymentInfo["card_type"] = radio_var.get()
    paymentInfo["card_bank"] = comboBank.get()
    paymentInfo["card_num"] = txtCN1.get("1.0",END) + txtCN2.get("1.0",END) + txtCN3.get("1.0",END)+ txtCN4.get("1.0",END)
    paymentInfo["card_VD"] = comboCVM.get() + '/' + comboCVY.get()
    paymentInfo["card_PW"] = txtPW.get("1.0",END)
    paymentInfo["birth_six"] = ymd + " 00:00:00"

    paymentInfo["pass_name"] = txtName.get("1.0",END)
    paymentInfo["phone_num"] = txtPN1.get("1.0",END) + txtPN2.get("1.0",END) + txtPN3.get("1.0",END)
    paymentInfo["login_pw"] = txtLogPW.get("1.0",END)

    def btnQuit():
      MsgBox = messagebox.askquestion('Exit App','결제 정보를 모두 확인하셨습니까?')
      if MsgBox == 'yes':
        try:
          #def final_page(card_number, card_type, bank_name, person_name, birth, tel, password, adult, teenager, children, path_id, seats_num_list):
          sql.final_page(paymentInfo["card_num"],paymentInfo["card_type"], paymentInfo["card_bank"],\
                paymentInfo["pass_name"], paymentInfo["birth_six"], paymentInfo["phone_num"], \
                paymentInfo["login_pw"], adult, teenager, child, path_id, selectedSeats)
          new_window.destroy()
        except:
          messagebox.showinfo("Input Error", '정보가 잘못 입력되었습니다. 정보를 수정한 후 "예매하기" 버튼을 눌러주세요.')
      else:
        messagebox.showinfo("Exit App", '창을 유지합니다. 변경한 정보가 있다면 "예매하기" 버튼을 다시 눌러주세요.')
      
      
    btnQuit = Button(new_window, width=20, text="창 닫기(예매 확정)", command=btnQuit)
    btnQuit.grid(row = 15, column = 1, columnspan=2)

  #---------------------------------------------------------------------------------------------------          
  btn1 = Button(new_window, width=20, text="예매하기", command=lambda: btnPayment(paymentInfo))
  btn1.grid(row = 14, column = 1, columnspan=2)

  return paymentInfo


paymentInfo = {}
def new_window2():
  global paymentInfo
  newWindow = (Toplevel(root))
  newWindow.geometry('450x350+900+300')
  newWindow.title("Payment Information")
  paymentInfo = printThirdPage(newWindow)

btn3 = Button(root, text="결제 정보 입력하기", command=new_window2)
btn3.grid(row=12, column=0)

label00 = Label(root, text = "*----------------------------예매정보 확인하기----------------------------*")
label00.grid(row=13, column=0, columnspan=4)

labelNameL = Label(root, text = "* 예매자 이름")
labelNameL.grid(row = 14, column=0)

txtNameL = Text(root, height=1, width = 9)
txtNameL.grid(row = 14, column=1)

label9 = Label(root, text = "* 생년월일")
label9.grid(row = 15, column=0)

yearsL = [str(i) + '년' for i in range(1940, 2022)]
monthsL = [str(i) + '월' for i in range(1, 13)]
daysL = [str(i) + '일' for i in range(1, 32)]

combobox_yearL = ttk.Combobox(root, height=15, width=6, values=yearsL)
combobox_yearL.grid(row=15, column=1)
combobox_yearL.set("_ _ _ _년")

combobox_monthL = ttk.Combobox(root, height=12, width=6, values=monthsL)
combobox_monthL.grid(row=15, column=2)
combobox_monthL.set("_ _월")

combobox_dayL = ttk.Combobox(root, height=15, width=6, values=daysL)
combobox_dayL.grid(row=15, column=3)
combobox_dayL.set("_ _일")

label10 = Label(root, text = "* 휴대폰 번호")
label10.grid(row = 16, column=0)

txtPN1L = Text(root, height=1, width = 9)
txtPN1L.grid(row = 16, column=1)

txtPN2L = Text(root, height=1, width = 9)
txtPN2L.grid(row = 16, column=2)

txtPN3L = Text(root, height=1, width = 9)
txtPN3L.grid(row = 16, column=3)

label11 = Label(root, text = "* 로그인 비밀번호")
label11.grid(row = 17, column=0)

txtLogPWL = Text(root, height=1, width = 9)
txtLogPWL.grid(row = 17, column = 1)

def checkReservation():
  finalWindow = Toplevel(root)
  finalWindow.geometry("300x300")

  year = combobox_yearL.get()
  year = year[0:4]
  month = combobox_monthL.get()
  month = re.sub(r'[^0-9]', '', month)
  day = combobox_dayL.get()
  day = re.sub(r'[^0-9]', '', day)
  ymd = year + '-' + month + '-' + day

  birth = ymd + " 00:00:00"
  cus_name = txtNameL.get("1.0",END)
  phone_num = txtPN1L.get("1.0",END) + txtPN2L.get("1.0",END) + txtPN3L.get("1.0",END)
  log_pw = txtLogPWL.get("1.0",END)

#total_payment_info = [] #order51234, placeList00/01, seatlist->seat[0]~end
#def view_page(person_name, birth, tel, password)
  total_payment_info = sql.view_page(cus_name, birth, phone_num, log_pw)
  txtTotalInfo = Text(finalWindow, width=50, height=50)
  txtTotalInfo.insert("1.0", "예약한 시각: " + str(total_payment_info[0][5]) + "\n\n")
  txtTotalInfo.insert("2.0", "어른  : " + str(total_payment_info[0][1]) + "명"+ "\n\n")
  txtTotalInfo.insert("3.0", "아이  : " + str(total_payment_info[0][2]) + "명"+ "\n\n")
  txtTotalInfo.insert("4.0", "청소년: " + str(total_payment_info[0][3]) + "명"+ "\n\n")
  txtTotalInfo.insert("5.0", "가격  : " + str(total_payment_info[0][4]) + "원"+ "\n\n")
  txtTotalInfo.insert("6.0", "출발지: " + str(total_payment_info[1][0][0])+ "\n\n")
  txtTotalInfo.insert("7.0", "도착지: " + str(total_payment_info[1][0][1])+ "\n\n")
  seatList = ""
  for elem in total_payment_info[2]:
    seatList += str(elem[0]) + "번 "
  txtTotalInfo.insert("8.0", "예약된 좌석번호: " + seatList)


  label99 = Label(finalWindow, text="예약 정보")
  label99.pack()
  txtTotalInfo.pack()


btn4 = Button(root, text="예매 정보 확인하기", command=checkReservation)
btn4.grid(row=18, column=0)


root.mainloop()