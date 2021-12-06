-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: intercity_bus_terminal_final
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bus`
--

DROP TABLE IF EXISTS `bus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus` (
  `bus_id` int NOT NULL,
  `bus_license_num` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `bus_years` int NOT NULL,
  PRIMARY KEY (`bus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus`
--

LOCK TABLES `bus` WRITE;
/*!40000 ALTER TABLE `bus` DISABLE KEYS */;
INSERT INTO `bus` VALUES (1101,'399 수 4782',2012),(1102,'556 케 9023',2019),(1103,'623 사 8421',2015),(1104,'486 비 0429',2017),(1105,'151 대 1793',2015);
/*!40000 ALTER TABLE `bus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `card` (
  `card_number` varchar(30) NOT NULL,
  `card_type` varchar(20) NOT NULL,
  `bank_name` varchar(20) NOT NULL,
  PRIMARY KEY (`card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `card`
--

LOCK TABLES `card` WRITE;
/*!40000 ALTER TABLE `card` DISABLE KEYS */;
INSERT INTO `card` VALUES ('\n\n\n\n','','카드선택'),('1\n1\n1\n\n','','국민'),('1\n1\n1\n1\n','신용','기업'),('1\n2\n3\n3\n','체크','농협'),('1111\n1111\n1111\n1111\n','체크','기업'),('1111\n2222\n1111\n1111\n','신용','기업'),('1111\n2222\n1111\n2222\n','','농협'),('1111\n2222\n3333\n4444\n','신용','기업'),('1111-2222-3333-4444','credit','하나'),('1111-4444-0000-2222','check','카카오'),('1122-3344-5566-7788','check','기업'),('1334\n4524\n4568\n1531\n','신용','기업'),('1672-5194-0000-2222','check','하나'),('2222\n1111\n3333\n4444\n','체크','기업'),('5555-6666-7777-8888','credit','국민'),('9454\n5567\n1156\n7861\n','신용','기업'),('9999-8888-7777-6666','check','농협');
/*!40000 ALTER TABLE `card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `adult` int DEFAULT NULL,
  `teenager` int DEFAULT NULL,
  `children` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `order_time` datetime DEFAULT NULL,
  `path_id` int NOT NULL,
  `passenger_id` int NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `path_id` (`path_id`),
  KEY `passenger_id` (`passenger_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`path_id`) REFERENCES `path` (`path_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`passenger_id`) REFERENCES `passenger` (`passenger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (25,1,1,1,75600,'2021-11-25 04:15:36',2150,890),(61,1,1,1,64800,'2021-11-25 19:04:02',2230,568),(68,1,0,1,43200,'2021-11-22 22:48:45',3621,200),(231,1,1,1,75600,'2021-11-25 20:42:36',2140,589),(248,1,1,1,75600,'2021-11-24 19:17:42',2150,139),(373,1,1,1,64800,'2021-11-26 14:32:42',2230,547),(392,2,1,1,103600,'2021-11-22 22:21:35',2130,804),(457,1,1,1,64800,'2021-11-26 14:03:07',2230,228),(589,1,1,1,64800,'2021-11-25 21:53:09',3631,167),(779,1,1,1,75600,'2021-11-25 21:40:56',2130,460),(929,1,1,1,64800,'2021-11-25 19:08:42',2240,449);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `passenger_id` int NOT NULL,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `birth` date NOT NULL,
  `tel` varchar(20) NOT NULL,
  `password` varchar(30) NOT NULL,
  `card_number` varchar(30) NOT NULL,
  PRIMARY KEY (`passenger_id`),
  KEY `card_number` (`card_number`),
  CONSTRAINT `passenger_ibfk_1` FOREIGN KEY (`card_number`) REFERENCES `card` (`card_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES (5,'ddd\n','2023-03-07','666\n666\n666\n','666\n','1111\n1111\n1111\n1111\n'),(67,'1\n','2022-01-02','1\n1\n1\n','1\n','1\n1\n1\n1\n'),(139,'ddd\n','2022-04-05','222\n2222\n2222\n','2222\n','1111\n1111\n1111\n1111\n'),(167,'ddd\n','1991-01-01','010\n1234\n4567\n','4567\n','1111\n2222\n3333\n4444\n'),(196,'엄태현\n','2021-09-06','222\n3245\n4563\n','1111\n','2222\n1111\n3333\n4444\n'),(200,'영칠이','1987-03-25','010-5354-1987','2114','1672-5194-0000-2222'),(223,'1111\n','2022-04-06','1111\n2222\n3333\n','1234\n','1111\n2222\n3333\n4444\n'),(228,'엄태현\n','1999-02-26','010\n9949\n3752\n','\n','9454\n5567\n1156\n7861\n'),(314,'1\n','2022-02-04','1\n1\n1\n','1111\n','1\n1\n1\n\n'),(431,'11\n','2022-01-02','111\n1111\n1111\n','1111\n','1111\n1111\n1111\n1111\n'),(449,'1111\n','2022-03-05','1111\n2222\n1111\n','2222\n','1111\n2222\n1111\n2222\n'),(460,'ddd\n','1941-02-04','111\n2222\n3333\n','1111\n','1111\n1111\n1111\n1111\n'),(514,'ddd\n','2022-02-04','111\n111\n111\n','1111\n','1\n2\n3\n3\n'),(547,'엄태현\n','1999-02-26','010\n9949\n3752\n','3752\n','1111\n2222\n3333\n4444\n'),(568,'1111\n','2022-05-10','1111\n2222\n1111\n','2222\n','1111\n2222\n1111\n2222\n'),(589,'ddd\n','2021-01-01','111\n2222\n3333\n','1111\n','1111\n2222\n1111\n1111\n'),(701,'11\n','2022-03-03','1\n1\n1\n','1\n','1\n1\n1\n1\n'),(801,'홍길동','1999-01-01','010-1111-2222','1234','1111-2222-3333-4444'),(802,'임꺽정','2011-05-05','010-3333-4444','5678','9999-8888-7777-6666'),(803,'선덕구','1998-06-25','010-5555-6666','0038','5555-6666-7777-8888'),(804,'서라비','1970-09-16','010-8888-1111','1954','1111-4444-0000-2222'),(805,'토니 수다그','1986-12-30','010-3000-0536','1123','1122-3344-5566-7788'),(885,'엄태현\n','2023-03-07','010\n9949\n3752\n','1111\n','1334\n4524\n4568\n1531\n'),(890,'황승훈\n','2023-02-13','010\n5564\n7786\n','3355\n','1111\n2222\n3333\n4444\n'),(993,'dja\n','2022-01-02','111\n1111\n1111\n','1111\n','1111\n1111\n1111\n1111\n');
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `path`
--

DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `path` (
  `path_id` int NOT NULL,
  `departure` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `destination` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `depart_time` datetime NOT NULL,
  `time_taken` int NOT NULL,
  `bus_id` int NOT NULL,
  PRIMARY KEY (`path_id`),
  KEY `bus_id` (`bus_id`),
  CONSTRAINT `path_ibfk_1` FOREIGN KEY (`bus_id`) REFERENCES `bus` (`bus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `path`
--

LOCK TABLES `path` WRITE;
/*!40000 ALTER TABLE `path` DISABLE KEYS */;
INSERT INTO `path` VALUES (2130,'서울','부산','2021-10-14 08:00:00',140,1103),(2140,'서울','부산','2021-10-14 13:00:00',140,1101),(2150,'서울','부산','2021-10-14 18:00:00',140,1105),(2230,'서울','강릉','2021-10-22 06:00:00',120,1104),(2240,'서울','강릉','2021-10-22 14:00:00',120,1102),(2250,'서울','강릉','2021-10-22 19:00:00',120,1105),(3621,'강릉','서울','2021-10-26 18:00:00',120,1102),(3631,'강릉','서울','2021-10-26 08:00:00',120,1105),(3641,'강릉','서울','2021-10-26 12:00:00',120,1101),(3721,'강릉','부산','2021-12-10 09:00:00',180,1104),(3731,'강릉','부산','2021-12-10 13:00:00',180,1105),(3741,'강릉','부산','2021-12-10 21:00:00',180,1102),(4361,'부산','강릉','2021-12-26 22:00:00',180,1104),(4371,'부산','강릉','2021-12-26 16:00:00',180,1103),(4381,'부산','강릉','2021-12-26 10:00:00',180,1102),(4461,'부산','서울','2021-12-03 06:00:00',140,1101),(4471,'부산','서울','2021-12-03 09:00:00',140,1102),(4481,'부산','서울','2021-12-03 17:00:00',140,1104);
/*!40000 ALTER TABLE `path` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seats`
--

DROP TABLE IF EXISTS `seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seats` (
  `path_id` int NOT NULL,
  `seats_num` int NOT NULL,
  `order_id` int DEFAULT NULL,
  KEY `path_id` (`path_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`path_id`) REFERENCES `path` (`path_id`),
  CONSTRAINT `seats_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seats`
--

LOCK TABLES `seats` WRITE;
/*!40000 ALTER TABLE `seats` DISABLE KEYS */;
INSERT INTO `seats` VALUES (2130,2,392),(2130,3,392),(2130,6,392),(2130,7,392),(3621,12,68),(3621,13,68),(2150,10,248),(2150,11,248),(2150,12,248),(2150,13,25),(2150,14,25),(2150,15,25),(2230,1,61),(2230,2,61),(2230,3,61),(2240,4,929),(2240,5,929),(2240,6,929),(2140,4,231),(2140,5,231),(2140,6,231),(2130,4,779),(2130,5,779),(3631,4,589),(3631,5,589),(3631,6,589),(2230,4,373),(2230,5,373),(2230,6,373);
/*!40000 ALTER TABLE `seats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-26 14:57:44
