-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: projectdb
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `controller`
--

DROP TABLE IF EXISTS `controller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `controller` (
  `controller_id` int(11) NOT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `hotspot_ssid` varchar(45) DEFAULT NULL,
  `hotspot_psk` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`controller_id`),
  KEY `controler_idx` (`controller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controller`
--

LOCK TABLES `controller` WRITE;
/*!40000 ALTER TABLE `controller` DISABLE KEYS */;
INSERT INTO `controller` VALUES (0,'169.254.10.1',NULL,NULL);
/*!40000 ALTER TABLE `controller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `takel`
--

DROP TABLE IF EXISTS `takel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `takel` (
  `takel_id` int(11) NOT NULL,
  `controller_id` int(11) DEFAULT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `START_POS` int(11) DEFAULT NULL,
  `END_POS` int(11) DEFAULT NULL,
  `CURR_POS` int(11) DEFAULT NULL,
  `Connectie_status` int(11) DEFAULT NULL,
  `subnet` int(11) DEFAULT NULL,
  `universe` int(11) DEFAULT NULL,
  `channel` int(11) DEFAULT NULL,
  PRIMARY KEY (`takel_id`),
  UNIQUE KEY `takel_id_UNIQUE` (`takel_id`),
  KEY `controller_id_idx` (`controller_id`),
  CONSTRAINT `controller_id` FOREIGN KEY (`controller_id`) REFERENCES `controller` (`controller_id`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takel`
--

LOCK TABLES `takel` WRITE;
/*!40000 ALTER TABLE `takel` DISABLE KEYS */;
/*!40000 ALTER TABLE `takel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-15 21:16:59
