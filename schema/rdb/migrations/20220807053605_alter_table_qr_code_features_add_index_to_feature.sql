-- migrate:up
CREATE INDEX `index_feature` ON `qr_code_features` (`feature`)

-- migrate:down
DROP INDEX `index_feature` ON `qr_code_features`
