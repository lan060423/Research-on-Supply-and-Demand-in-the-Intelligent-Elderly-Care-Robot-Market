# 求是学术项目——桑榆非晚，科技为光：智能养老服务机器人市场供需错配识别与需求转化机制研究——技术实现

## 一、项目简介

本仓库用于存放“桑榆非晚，科技为光：智能养老服务机器人市场供需错配识别与需求转化机制研究”项目的技术实现内容，包括数据采集、数据清洗、功能分类、供需量化、供需错配识别、需求转化机制分析以及可视化输出等。

本项目围绕智能养老服务机器人市场，构建“供给侧数据—需求侧数据—供需匹配模型—需求转化机制”的技术路径，识别不同功能类型养老机器人在市场供给与老年群体实际需求之间的错配情况，为产品优化、市场配置和政策支持提供数据依据。

## 二、研究对象

本项目关注智能养老服务机器人，并按照功能划分为六大类型：

1. 失能照护
2. 失智照护
3. 情感陪护
4. 健康管理
5. 智慧环境
6. 日常生活辅助

六大功能类型将贯穿数据采集、供给侧分类、需求侧测度、供需匹配建模和结果可视化全过程。

## 三、数据来源

### 1. 供给侧数据

供给侧数据主要来自公开可访问的政府招投标网站、政府采购平台和电商平台，时间范围暂定为：

```text
2025.05.19—2026.05.19
```

计划采集的数据来源包括：

- 中国政府采购网
- 中国招标投标公共服务平台
- 各省市公共资源交易平台
- 其他公开招投标与采购信息平台
- 抖音电商
- 京东
- 淘宝

供给侧数据字段包括但不限于：

- 来源平台
- 发布日期或上架时间
- 产品或项目名称
- 品牌或供应商
- 价格或中标金额
- 销量、评价数、成交量或采购数量
- 产品描述
- 功能参数
- 地区
- 适用场景
- 原始链接
- 功能分类标签
- 主功能标签

供给侧养老机器人将根据文本描述和功能关键词划分为六大功能类型，并支持多标签分类。

### 2. 需求侧数据

需求侧数据用于刻画老年人、家庭照护者、养老机构以及区域养老服务体系对智能养老服务机器人的真实需求。

计划整理的数据包括：

- 问卷调查数据
- 访谈文本数据
- 老年人口统计数据
- 区域养老服务资源数据
- 养老政策文本
- 老龄化程度、失能失智规模、慢病管理需求等辅助指标

需求侧数据将用于构建不同区域、不同功能类型下的需求强度指标。

### 3. 辅助数据

辅助数据主要用于标准化处理和模型计算，包括：

- 行政区划代码表
- 区域名称映射表
- 养老机器人功能词典
- 六大功能分类关键词表
- 招投标平台字段映射表
- 电商平台字段映射表

## 四、仓库结构说明

```text
Sangyu-Intelligent-Elderly-Care-Robot-Supply-Demand-Mismatch/
│
├── README.md
├── .gitignore
│
├── 00_project_docs/
│   ├── application_form/
│   ├── presentation_ppt/
│   ├── research_notes/
│   └── meeting_records/
│
├── 01_raw_data/
│   ├── supply_side_data/
│   │   ├── government_procurement/
│   │   ├── bidding_platforms/
│   │   ├── douyin_ecommerce/
│   │   ├── jd_ecommerce/
│   │   └── taobao_ecommerce/
│   │
│   ├── demand_side_data/
│   │   ├── questionnaire_data/
│   │   ├── interview_texts/
│   │   ├── elderly_care_statistics/
│   │   ├── regional_population_data/
│   │   └── policy_texts/
│   │
│   └── auxiliary_data/
│       ├── region_code_table/
│       ├── robot_function_dictionary/
│       └── keyword_dictionary/
│
├── 02_processed_data/
│   ├── cleaned_supply_data/
│   ├── cleaned_demand_data/
│   ├── function_classification_data/
│   ├── regional_mapping_data/
│   └── supply_demand_score_data/
│
├── 03_crawler/
│   ├── government_bidding_crawler/
│   ├── procurement_platform_crawler/
│   ├── douyin_crawler/
│   ├── jd_crawler/
│   ├── taobao_crawler/
│   └── crawler_config/
│
├── 04_data_cleaning/
│   ├── data_deduplication/
│   ├── text_preprocessing/
│   ├── missing_value_processing/
│   ├── price_sales_standardization/
│   └── region_standardization/
│
├── 05_function_classification/
│   ├── disability_care/
│   ├── dementia_care/
│   ├── emotional_companionship/
│   ├── health_management/
│   ├── smart_environment/
│   ├── daily_life_assistance/
│   └── multi_label_classification/
│
├── 06_supply_demand_matching/
│   ├── supply_score_calculation/
│   ├── demand_score_calculation/
│   ├── regional_weight_mapping/
│   ├── mahalanobis_distance_model/
│   ├── mccm_coordination_model/
│   └── mismatch_identification/
│
├── 07_demand_transformation_mechanism/
│   ├── demand_feature_extraction/
│   ├── demand_pain_point_analysis/
│   ├── supply_gap_analysis/
│   └── transformation_path_model/
│
├── 08_visualization/
│   ├── supply_function_ratio_charts/
│   ├── demand_distribution_charts/
│   ├── supply_demand_mismatch_charts/
│   ├── regional_heatmaps/
│   └── ppt_figures/
│
├── 09_results/
│   ├── statistical_tables/
│   ├── model_outputs/
│   ├── figures/
│   └── final_reports/
│
├── 10_scripts/
│   ├── run_crawler/
│   ├── run_cleaning/
│   ├── run_classification/
│   ├── run_matching_model/
│   └── run_visualization/
│
├── 11_notebooks/
│   ├── exploratory_analysis/
│   ├── supply_side_analysis/
│   ├── demand_side_analysis/
│   └── model_validation/
│
└── 12_archive/
    ├── old_versions/
    └── backup_files/
```

## 五、文件夹功能说明

### 00_project_docs

存放项目申报书、汇报 PPT、研究笔记和会议记录等项目文档。

### 01_raw_data

存放原始数据，包括供给侧爬虫数据、需求侧调查数据、访谈文本、统计数据和政策文本等。

### 02_processed_data

存放清洗后的中间数据，包括去重后的供给数据、清洗后的需求数据、功能分类结果、区域映射结果和供需得分数据。

### 03_crawler

存放爬虫代码。爬取对象包括政府采购网站、招投标平台、抖音电商、京东和淘宝等。

### 04_data_cleaning

存放数据清洗代码，包括去重、文本预处理、缺失值处理、价格与销量标准化、地区字段标准化等。

### 05_function_classification

存放养老机器人六大功能分类代码，包括规则分类、关键词匹配、多标签分类和主功能识别等。

### 06_supply_demand_matching

存放供需匹配模型相关代码，包括供给得分计算、需求得分计算、区域权重映射、马氏距离错配识别模型和多功能交叉协调度模型。

### 07_demand_transformation_mechanism

存放需求转化机制分析代码，包括需求特征提取、需求痛点分析、供给缺口分析和转化路径建模。

### 08_visualization

存放统计图和可视化代码，包括六大功能供给比例图、需求分布图、供需错配图、区域热力图和 PPT 汇报图。

### 09_results

存放最终输出结果，包括统计表、模型结果、图片、报告和汇报材料。

### 10_scripts

存放一键运行脚本，用于统一执行爬取、清洗、分类、建模和可视化流程。

### 11_notebooks

存放 Jupyter Notebook，用于探索性分析、模型验证和阶段性结果展示。

### 12_archive

存放旧版本文件和备份文件。

## 六、技术流程

本项目的技术实现流程如下：

```text
数据采集
→ 原始数据存储
→ 数据清洗与去重
→ 六大功能分类
→ 供给侧指标构建
→ 需求侧指标构建
→ 区域招投标权重映射
→ 供需错配识别
→ 多功能协调度分析
→ 需求转化机制分析
→ 统计图与汇报材料输出
```

## 七、核心模型

### 1. 供给侧功能分类

通过产品标题、详情页文本、招投标公告文本和功能参数，对养老机器人进行功能识别。

六大功能分类包括：

- 失能照护：移位、翻身、助浴、排泄、喂饭、康复辅助、行动辅助等
- 失智照护：防走失、定位、认知障碍、异常行为识别、记忆提醒等
- 情感陪护：聊天、陪伴、语音交互、娱乐、情绪安抚等
- 健康管理：血压、血糖、心率、体征监测、慢病管理、用药提醒等
- 智慧环境：跌倒监测、紧急呼叫、烟雾监测、燃气监测、门磁、床垫监测、智能家居联动等
- 日常生活辅助：送餐、取物、清洁、导航、购物、生活提醒等

对于具备多个功能的产品，保留多标签分类结果，并设置“主功能”字段。

### 2. 供需量化得分

项目将分别构建供给侧得分和需求侧得分。

供给侧得分主要考虑：

- 产品数量
- 项目数量
- 价格或中标金额
- 销量、评价数或成交量
- 供应商数量
- 区域分布
- 功能覆盖情况

需求侧得分主要考虑：

- 老年人口规模
- 失能失智需求
- 慢病与健康管理需求
- 情感陪伴需求
- 养老机构与社区养老服务需求
- 区域养老服务资源缺口
- 问卷和访谈反映的需求强度

### 3. 单功能错配识别

项目采用马氏距离衡量单一功能类型的供需错配程度。该方法可以在考虑功能间相关性的基础上，识别某一功能在特定区域或场景下是供给过剩还是供给不足。

错配方向判断逻辑为：

```text
供给得分 > 有效需求得分：供给过剩
供给得分 < 有效需求得分：供给不足
```

### 4. 多功能交叉协调度

项目进一步构建多功能交叉协调度模型，用于衡量多个功能组合下的综合供需协调情况。

该模型关注的不只是单一功能是否匹配，还关注多个功能之间是否存在结构性不均衡。例如，某一区域可能健康管理类机器人供给充足，但失能照护和情感陪护类机器人供给不足，这种情况需要通过多功能协调度进行综合识别。


## 八、数据与隐私说明

本项目仅采集和使用公开可访问的数据，不采集、不存储、不分析任何个人隐私信息。

电商平台和招投标平台数据采集将遵守平台公开访问规则，控制访问频率，仅用于学术研究和项目分析。

涉及问卷和访谈的数据将在匿名化处理后使用，所有可识别个人身份的信息均不进入公开仓库。

## 九、项目关键词

智能养老服务机器人、养老机器人、供需错配、供给侧数据、需求侧数据、政府采购、招投标、电商平台、功能分类、马氏距离、多功能协调度、需求转化机制、智慧养老。
