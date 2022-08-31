-- migrate:up
ALTER TABLE `qr_codes`
    ADD COLUMN `file_name` varchar(255) COLLATE utf8mb4_bin COMMENT 'QRコード画像の名前',
    ADD CONSTRAINT `unique_s3_uri` UNIQUE(`s3_uri`);

-- migrate:down
ALTER TABLE `qr_codes`
    DROP COLUMN `file_name`,
    DROP KEY `unique_s3_uri`;