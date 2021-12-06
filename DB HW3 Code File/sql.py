import mysql.connector
import random
import datetime

cnx = mysql.connector.connect(user='root', password='gritman1', host='localhost', database='intercity_bus_terminal_final')
cursor = cnx.cursor(buffered=True)

def show_cities():
  cursor.execute("SELECT DISTINCT DEPARTURE FROM PATH")
  return cursor.fetchall()

city_list = show_cities()
city_list = [_depart[0] for _depart in city_list]
city_list.sort()

def getting_organized_info(bus_route):
  path_id = bus_route[0]
  cursor.execute("SELECT SEATS_NUM FROM SEATS WHERE PATH_ID = %s", (path_id,))
  reserved_nums = cursor.fetchall()
  unreserved_count = 28 - len(reserved_nums)
  str_time = bus_route[3].strftime("%H:%M") # datetime객체임
  duration_time = bus_route[4]
  s_ = "출발 시각 : "
  s_ += str_time
  s_ += " 소요 예상 시간 : {}분".format(duration_time)
  adult_cost = int(duration_time * 2000 / 10) #소요 시간 10분당 2000원
  child_cost = int(adult_cost * 0.8) #어른의 20% 할인
  teen_cost = int(adult_cost * 0.9) #어른의 10% 할인
  s_ += " 어른요금 : {}원 아동요금 : {}원 중고생요금 : {}원".format(adult_cost, child_cost, teen_cost)
  s_ += " 잔여좌석/총좌석 : {}석 / 총 28석".format(unreserved_count)
  
  return s_

def inserting_card_info(card_number, card_type, bank_name):
  inserting_card_info_sql = "INSERT IGNORE INTO CARD(card_number, card_type, bank_name) VALUES(%s, %s, %s)"
  cursor.execute(inserting_card_info_sql, (card_number, card_type, bank_name))
  cnx.commit()

def inserting_passenger_info(person_name, birth, tel, password, card_number):
  cursor.execute("SELECT DISTINCT PASSENGER_ID FROM PASSENGER")
  passenger_id_list = cursor.fetchall()
  passenger_info_sql = "SELECT PASSENGER_ID FROM PASSENGER WHERE NAME = %s AND BIRTH = %s AND TEL = %s AND PASSWORD = %s"
  cursor.execute(passenger_info_sql, (person_name, birth, tel, password))
  searched_person = cursor.fetchall()
  if not searched_person: #리스트가 비어있다. 즉, 이전에 등록한 적이 없는 고객님임
    while True:
      rand_id = random.randrange(1, 1001)
      if rand_id not in passenger_id_list:
        break
    inserting_sql = "INSERT INTO PASSENGER(PASSENGER_ID, NAME, BIRTH, TEL, PASSWORD, CARD_NUMBER) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.execute(inserting_sql, (rand_id, person_name, birth, tel, password, card_number))
    cnx.commit()
    return rand_id
  else:
    return searched_person[0][0]

def final_page(card_number, card_type, bank_name, person_name, birth, tel, password, adult, teenager, children, path_id, seats_num_list):
  inserting_card_info(card_number, card_type, bank_name)
  passenger_id = inserting_passenger_info(person_name, birth, tel, password, card_number)
  cursor.execute("SELECT ORDER_ID FROM ORDERS")
  order_id_list = cursor.fetchall()
  while True:
    order_id = random.randrange(1, 1001)
    if order_id not in order_id_list:
      break
  order_time = datetime.datetime.now()
  inserting_sql = "INSERT INTO ORDERS(ORDER_ID, ADULT, TEENAGER, CHILDREN, PRICE, ORDER_TIME, PATH_ID, PASSENGER_ID) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
  cursor.execute("SELECT TIME_TAKEN FROM PATH WHERE PATH_ID = %s", (path_id,))
  time_taken = (cursor.fetchall())[0][0]
  adult_cost = int(time_taken * 2000 / 10) #소요 시간 10분당 2000원
  child_cost = int(adult_cost * 0.8) #어른의 20% 할인
  teen_cost = int(adult_cost * 0.9) #어른의 10% 할인
  price = int(adult_cost * int(adult) + teen_cost * int(teenager) + child_cost * int(children))
  cursor.execute(inserting_sql, (order_id, adult, teenager, children, price, order_time, path_id, passenger_id))
  cnx.commit()
  for seat_number in seats_num_list:
    inserting_sql = "INSERT INTO SEATS(PATH_ID, SEATS_NUM, ORDER_ID) VALUES(%s, %s, %s)"
    cursor.execute(inserting_sql, (path_id, seat_number, order_id))
  cnx.commit()
  return

def view_page(person_name, birth, tel, password):
  view_sql = "SELECT PASSENGER_ID FROM PASSENGER WHERE NAME = %s AND BIRTH = %s AND TEL = %s AND PASSWORD = %s"
  cursor.execute(view_sql, (person_name, birth, tel, password))
  passenger_id = cursor.fetchall()
  if not passenger_id: # 이러한 고객님이 없으면
    print("이러한 정보의 승객이 없습니다.")
  else:
    passenger_id = passenger_id[0][0]
    order_sql = "SELECT * FROM ORDERS WHERE PASSENGER_ID = %s"
    cursor.execute(order_sql, (passenger_id,))
    orders_list = cursor.fetchall()
    if not orders_list: # 주문내역이 없으면
      print("주문 내역이 없습니다")
    else:
      total_payment_info = [] #order51234, placeList00/01, seatlist->seat[0]~end
      print("------주문 내역------")
      place_sql = "SELECT DEPARTURE, DESTINATION FROM PATH WHERE PATH_ID = %s"
      seats_sql = "SELECT SEATS_NUM FROM SEATS WHERE PATH_ID = %s AND ORDER_ID = %s"
      for order in orders_list: # (order_id, adult, teenager, children, price, order_time, path_id, passenger_id)
        print("예약한 시각 : {}".format(order[5]))
        print("어른 : {}명".format(order[1]))
        print("청소년 : {}명".format(order[2]))
        print("아이 : {}명".format(order[3]))
        print("가격 : {}원".format(order[4]))
        path_id = order[6]
        order_id = order[0]
        cursor.execute(place_sql, (path_id,))
        place_list = cursor.fetchall() # [(출발지, 도착지)]
        print("출발지 : {}".format(place_list[0][0]))
        print("도착지 : {}".format(place_list[0][1]))
        cursor.execute(seats_sql, (path_id, order_id))
        seats_list = cursor.fetchall()
        print("예약된 좌석번호 : ", end="")
        for seat in seats_list:
          print("{}번 ".format(seat[0]), end="")
        print("\n\n")
        total_payment_info.append(order)
        total_payment_info.append(place_list)
        total_payment_info.append(seats_list)
        return total_payment_info
        

def first_page(depart, dest, year, month, day, adult, child, teenager):
  print("출발 날짜\n")
  depart_date = year + '-' + month + '-' + day
  print(depart_date)
  
  print("도시들 목록\n")
  for departments in city_list:
    print(departments)
    
  print("\n\n가능한 버스 노선들\n\n")
  bus_route_sql = "SELECT * FROM PATH WHERE DEPART_TIME >= %s AND DEPART_TIME <= %s AND DEPARTURE = %s AND DESTINATION = %s"
  cursor.execute(bus_route_sql, (depart_date + " 00:00:00", depart_date + " 23:59:59", depart, dest))
  
  bus_routes = cursor.fetchall()
  
  for bus_route in bus_routes:
    print(bus_route, end="\n\n")
    path_info = getting_organized_info(bus_route)
    print(path_info, end="\n\n\n")


#main함수
#first_page('서울', '부산', '2021', '10', '14', 1, 1, 1)
#first_page('서울', '강릉', '2021', '10', '22', 1, 1, 1)

#final_page('1672-5194-0000-2222', 'check', '하나', '영칠이', '870325', '010-5354-1987', '2114', 1, 0, 1, 3621, [12, 13])
#final_page(카드번호, 카드종류, 은행종류, 예약하는 사람이름, 생년월일, 전화번호, 비밀번호4자리, 어른, 청소년, 아이, path_id, 예약한 좌석번호 리스트)
view_page('영칠이', '870325', '010-5354-1987', '2114')
#view_page(예약한 사람이름, 생년월일, 전화번호, 비밀번호4자리)