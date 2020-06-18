-- MySQL dump 10.13  Distrib 5.7.22, for macos10.13 (x86_64)
--
-- Host: 192.168.105.139    Database: hm_topnews
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.13-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_basic`
--

DROP TABLE IF EXISTS `user_basic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_basic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobile` varchar(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `introduction` varchar(50) DEFAULT NULL,
  `article_count` int(11) DEFAULT NULL,
  `following_count` int(11) DEFAULT NULL,
  `fans_count` int(11) DEFAULT NULL,
  `profile_photo` varchar(130) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_basic`
--

LOCK TABLES `user_basic` WRITE;
/*!40000 ALTER TABLE `user_basic` DISABLE KEYS */;
INSERT INTO `user_basic` VALUES (1,'18516952650','黑马头条号','2018-11-29 11:46:10','',11,3,1,''),(2,'13552285417','蘑菇君','2018-11-29 13:47:21',NULL,3,1,2,NULL),(3,'18811179159','菜菜c','2018-11-29 13:48:04',NULL,2,2,2,NULL),(4,'13041092162','神棍刘','2019-02-15 17:47:30',NULL,5,3,2,NULL),(5,'18210568518','二牛','2019-02-15 17:59:18',NULL,8,4,1,NULL);
/*!40000 ALTER TABLE `user_basic` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 15:36:47
