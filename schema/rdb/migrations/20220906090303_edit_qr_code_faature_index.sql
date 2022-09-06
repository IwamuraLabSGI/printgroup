-- migrate:up
drop index index_feature on qr_code_features;

create index index_feature_and_color
    on qr_code_features (feature, color);



-- migrate:down
drop index index_feature_and_color on qr_code_features;

create index index_feature
    on qr_code_features (feature);



