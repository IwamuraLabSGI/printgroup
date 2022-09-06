-- migrate:up
alter table qr_code_features
    add column color enum ('cyan', 'magenta', 'yellow') not null comment '特徴量抽出に使用した色';

-- migrate:down
alter table qr_code_features
    drop column color;

