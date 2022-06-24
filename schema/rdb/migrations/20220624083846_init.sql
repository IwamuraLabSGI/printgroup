-- migrate:up
CREATE TABLE `qr_codes`
(
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `s3_uri` varchar(255) COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT 'QRコード画像があるs3のuri',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='qrコードとその特徴量を管理するテーブル';

-- migrate:down
DROP TABLE IF EXISTS `qr_codes`;
