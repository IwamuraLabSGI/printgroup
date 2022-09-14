-- migrate:up
alter table qr_code_features
    modify feature BIGINT not null comment '特徴量';





-- migrate:down
alter table qr_code_features
    modify feature DOUBLE not null comment '特徴量';





