-- auto-generated definition
create table company_registration
(
    id                             bigint unsigned auto_increment
        primary key,
    company_id                     bigint unsigned                    null comment '公司id',
    legal_representative           varchar(32)                        null comment '法人',
    operating_status               varchar(32)                        null comment '经营状态',
    registered_capital             varchar(32)                        null comment '注册资本(万元)',
    paidIn_capital                 varchar(32)                        null comment '实缴资本(万元)',
    industry                       varchar(32)                        null comment '行业',
    social_credit_code             varchar(32)                        not null comment '统一社会信用代码	',
    taxpayer_identification_number varchar(32)                        null comment '纳税人识别号',
    company_registration_number    varchar(32)                        not null comment '工商注册号',
    organization_code              varchar(32)                        null comment '组织机构代码',
    registration_authority         varchar(32)                        null comment '登记机关',
    establishment_date             date                               not null comment '成立日期',
    enterprise_type                varchar(32)                        null comment '企业类型',
    operating_period_begin         date                               null comment '营业期限开始',
    operating_period_end           varchar(32)                        null comment '营业期限结束',
    administrative_divisions       varchar(32)                        null comment '行政区划',
    annualInspection_date          date                               null comment '审核/年检日期',
    registered_address             varchar(256)                       null comment '注册地址',
    business_scope                 text                               null comment '经营范围',
    create_at                      datetime default CURRENT_TIMESTAMP null comment '创建时间',
    update_at                      datetime                           null comment '更新时间'
)
    comment '公司注册信息';

create index idx_company_id
    on company_registration (company_id);

