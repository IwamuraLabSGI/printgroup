-- migrate:up
CREATE TABLE `qr_code_features`
(
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `qr_code_id` bigint(20) unsigned NOT NULL COMMENT 'ID',
    `feature` double NOT NULL COMMENT '特徴量',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_to_qr_code` FOREIGN KEY (`qr_code_id`) REFERENCES qr_auth.qr_codes (`id`)
) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_bin COMMENT='qrコードの特徴量を管理するテーブル';
ALTER TABLE qr_auth.qr_codes COMMENT 'qrコードを管理するテーブル';

-- migrate:down
DROP TABLE IF EXISTS `qr_code_features`;
ALTER TABLE qr_auth.qr_codes COMMENT 'qrコードとその特徴量を管理するテーブル';