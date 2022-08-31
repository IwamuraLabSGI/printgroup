-- migrate:up
CREATE TABLE `qr_code_feature_hash_caches` (
    `hash` double unsigned UNIQUE NOT NULL COMMENT 'featureから計算されるhash',
    `qr_code_ids` JSON NOT NULL COMMENT 'hashを持つqr_code.idのリスト',
    KEY `index_hash` (`hash`)
) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_bin COMMENT='qrコードの特徴量から生成されるhashとその値を持つqr_code.idの集計テーブル';
ALTER TABLE `qr_codes`
    ADD COLUMN `feature_hash_cache_created` BOOLEAN DEFAULT FALSE NOT NULL COMMENT 'feature_hash_cacheが作成されたか',
    ADD KEY `index_feature_hash_cache_created` (`feature_hash_cache_created`);

-- migrate:down
DROP TABLE IF EXISTS `qr_code_feature_hash_caches`;
ALTER TABLE `qr_codes`
    DROP KEY `index_feature_hash_cache_created`,
    DROP COLUMN `feature_hash_cache_created`;