# 何易 · 数据挖掘/数据分析作品集

> 成都工业学院 · 金融科技（数据挖掘方向）· 本科 2027届  
> 求职目标：数据挖掘实习生 / 数据分析实习生 / 商业数据分析实习生

---

## 👋 关于我

我是成都工业学院金融科技专业数据挖掘方向本科生，熟悉 Python、SQL、pandas、scikit-learn、Excel 等数据分析工具，具备从业务问题拆解、数据清洗、特征工程、建模分析到可视化汇报的完整项目经验。

---

## 📂 项目总览

| 项目 | 方向 | 技术栈 | 亮点 |
|---|---|---|---|
| 项目1：电商用户行为分析与RFM分层 | 用户运营 / 数据挖掘 | Python、pandas、RFM、Apriori | 用户价值分层、关联规则、转化漏斗 |
| 项目2：上市公司财务分析与杜邦模型 | 金融数据分析 | Python、财务建模、线性回归 | ROE拆解、现金流预测、行业对标 |
| 项目3：SQL用户运营分析 | SQL / 业务分析 | SQLite、SQL、pandas | GMV、留存、复购、渠道转化、漏斗 |
| 项目4：用户流失预测机器学习 | 机器学习 / 风控运营 | scikit-learn、逻辑回归、随机森林 | AUC评估、特征重要性、高风险用户名单 |

---

## 🛒 项目一：电商用户行为分析与RFM分层

**技术栈：** Python · pandas · matplotlib · seaborn · RFM · Apriori

**项目内容：**
- 对电商平台用户行为数据进行清洗、EDA探索和可视化分析
- 构建 RFM 用户价值模型，将用户划分为高价值、发展、保持、挽留四类
- 使用 Apriori 关联规则挖掘品类交叉销售机会
- 分析浏览 → 加购 → 支付转化漏斗，定位关键流失环节

**对应文件：** `项目1_电商用户行为分析/ecommerce_analysis.ipynb`

---

## 📈 项目二：上市公司财务分析与杜邦模型

**技术栈：** Python · pandas · matplotlib · scikit-learn · 杜邦分析 · 线性回归

**项目内容：**
- 选取美的、格力、海尔三家家电龙头公司近3年财务数据
- 使用杜邦分析模型拆解 ROE：净利率 × 资产周转率 × 权益乘数
- 分析营收、净利润、毛利率、ROE、资产负债率趋势
- 使用线性回归预测经营现金流，并通过雷达图做行业对标

**对应文件：** `项目2_上市公司财务分析/financial_analysis.ipynb`

---

## 🧮 项目三：SQL用户运营分析

**技术栈：** SQLite · SQL · pandas · matplotlib · seaborn

**项目内容：**
- 设计 `users / products / orders / events` 四张业务表，模拟互联网电商数据仓库结构
- 使用 SQL 完成月度 GMV、订单数、客单价、渠道付费转化率分析
- 计算用户复购率、7日留存率、浏览-加购-支付转化漏斗
- 输出 TOP 品类 GMV 贡献，为渠道投放和品类运营提供决策依据

**核心能力：** 多表 JOIN、条件聚合、CTE、日期函数、业务指标口径设计

**对应文件：** `项目3_SQL用户运营分析/analysis.sql`

---

## 🤖 项目四：用户流失预测机器学习

**技术栈：** Python · pandas · scikit-learn · Logistic Regression · Random Forest

**项目内容：**
- 构建用户行为特征：活跃天数、最近登录间隔、历史订单数、近30日支付次数、投诉次数等
- 训练逻辑回归和随机森林模型预测用户流失概率
- 使用 Accuracy、Precision、Recall、AUC、混淆矩阵评估模型效果
- 通过特征重要性解释流失原因，并输出 Top30 高风险用户名单用于运营召回

**核心能力：** 特征工程、二分类建模、模型评估、特征解释、业务落地

**对应文件：** `项目4_用户流失预测机器学习/churn_prediction.py`

---

## 🏆 竞赛奖项

| 竞赛 | 奖项 | 时间 |
|---|---|---|
| 全国高校商业精英挑战赛 · 会计与商业管理案例竞赛 | 国家级三等奖 | 2025 |
| 全国大学生电子商务“创新、创意及创业”挑战赛 | 校级一等奖 | 2025.05 |

---

## 🛠 技术能力

| 技能类别 | 具体内容 |
|---|---|
| 编程语言 | Python、SQL |
| 数据处理 | pandas、numpy、数据清洗、缺失值处理、异常值识别、EDA |
| 数据挖掘 | RFM、Apriori、聚类、分类、用户分层、流失预测 |
| 机器学习 | 逻辑回归、随机森林、模型评估、ROC/AUC、特征重要性 |
| 可视化 | matplotlib、seaborn、Excel数据透视表、业务看板 |
| 数据库 | SQLite/MySQL基础、多表JOIN、窗口/聚合查询、CTE |
| 金融分析 | 杜邦分析、财务指标分析、现金流预测、行业对标 |

---

## 🚀 运行方式

```bash
bash setup.sh

# 项目3：SQL业务分析
cd 项目3_SQL用户运营分析
python3 generate_data.py
python3 run_analysis.py

# 项目4：用户流失预测
cd ../项目4_用户流失预测机器学习
python3 churn_prediction.py
```

---

## 📬 联系方式

- GitHub: https://github.com/JanuaryEleX/data-mining-portfolio
- Email: [your-email@example.com]
- Phone: [your-phone-number]
