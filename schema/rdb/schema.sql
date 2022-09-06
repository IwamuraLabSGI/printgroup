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
-- Table structure for table `qr_code_feature_hash_caches`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qr_code_feature_hash_caches` (
  `hash` double unsigned NOT NULL COMMENT 'featureから計算されるhash',
  `qr_code_ids` json NOT NULL COMMENT 'hashを持つqr_code.idのリスト',
  UNIQUE KEY `hash` (`hash`),
  KEY `index_hash` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='qrコードの特徴量から生成されるhashとその値を持つqr_code.idの集計テーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qr_code_features`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qr_code_features` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `qr_code_id` bigint(20) unsigned NOT NULL COMMENT 'ID',
  `feature` double NOT NULL COMMENT '特徴量',
  `color` enum('cyan','magenta','yellow') COLLATE utf8mb4_bin NOT NULL COMMENT '特徴量抽出に使用した色',
  PRIMARY KEY (`id`),
  KEY `fk_to_qr_code` (`qr_code_id`),
  KEY `index_feature_and_color` (`feature`,`color`),
  CONSTRAINT `fk_to_qr_code` FOREIGN KEY (`qr_code_id`) REFERENCES `qr_codes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='qrコードの特徴量を管理するテーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qr_codes`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qr_codes` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `s3_uri` varchar(255) COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'QRコード画像があるs3のuri',
  `feature_hash_cache_created` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'feature_hash_cacheが作成されたか',
  `file_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'QRコード画像の名前',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_s3_uri` (`s3_uri`),
  KEY `index_feature_hash_cache_created` (`feature_hash_cache_created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='qrコードを管理するテーブル';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schema_migrations`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schema_migrations` (
  `version` varchar(255) COLLATE latin1_bin NOT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'qr_auth'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed

--
-- Dbmate schema migrations
--

LOCK TABLES `schema_migrations` WRITE;
INSERT INTO `schema_migrations` (version) VALUES
  ('20220624083846'),
  ('20220713075203'),
  ('20220807053605'),
  ('20220807073623'),
  ('20220811101855'),
  ('20220904082712'),
  ('20220906090303');
UNLOCK TABLES;
