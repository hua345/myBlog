-- auto-generated definition
create table company
(
    id                 bigint unsigned auto_increment comment '公司统一社会信用代码'
        primary key,
    social_credit_code varchar(32)                        not null comment '统一社会信用码',
    company_name       varchar(64)                        not null comment '公司名称',
    company_phone      varchar(32)                        null comment '公司电话',
    company_email      varchar(32)                        null comment '公司邮箱',
    official_website   varchar(32)                        null comment '官网',
    company_address    varchar(128)                       null comment '公司地址',
    company_profile    text                               null comment '公司简介',
    create_at          datetime default CURRENT_TIMESTAMP null comment '创建时间',
    update_at          datetime                           null comment '更新时间',
    constraint idx_social_credit_code
        unique (social_credit_code)
)
    comment '公司';

