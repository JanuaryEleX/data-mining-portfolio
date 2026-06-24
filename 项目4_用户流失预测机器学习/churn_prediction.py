from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
base = Path(__file__).resolve().parent

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid")

n = 1200
user_id = np.arange(100001, 100001 + n)
active_days = np.random.gamma(4, 8, n).clip(1, 120)
last_login_days = np.random.exponential(18, n).clip(0, 120)
order_count = np.random.poisson(3, n)
avg_order_amount = np.random.gamma(3, 90, n).clip(20, 1200)
coupon_used = np.random.binomial(1, 0.38, n)
complaint_count = np.random.poisson(0.3, n)
page_views_30d = np.random.gamma(5, 10, n).clip(1, 300)
cart_count_30d = np.random.poisson(3, n)
pay_count_30d = np.maximum(0, np.random.poisson(2, n) - complaint_count)
member_level = np.random.choice([0, 1, 2, 3], n, p=[0.45, 0.3, 0.18, 0.07])

logit = (
    -1.2
    + 0.035 * last_login_days
    + 0.45 * complaint_count
    - 0.018 * active_days
    - 0.22 * order_count
    - 0.003 * avg_order_amount
    - 0.18 * member_level
    - 0.08 * pay_count_30d
    + 0.25 * (coupon_used == 0)
)
prob = 1 / (1 + np.exp(-logit))
churn = np.random.binomial(1, prob)

df = pd.DataFrame(
    {
        "user_id": user_id,
        "active_days": active_days.round(1),
        "last_login_days": last_login_days.round(1),
        "order_count": order_count,
        "avg_order_amount": avg_order_amount.round(2),
        "coupon_used": coupon_used,
        "complaint_count": complaint_count,
        "page_views_30d": page_views_30d.round(0).astype(int),
        "cart_count_30d": cart_count_30d,
        "pay_count_30d": pay_count_30d,
        "member_level": member_level,
        "churn": churn,
    }
)
df.to_csv(base / "user_churn_data.csv", index=False, encoding="utf-8-sig")

features = [
    "active_days",
    "last_login_days",
    "order_count",
    "avg_order_amount",
    "coupon_used",
    "complaint_count",
    "page_views_30d",
    "cart_count_30d",
    "pay_count_30d",
    "member_level",
]
X = df[features]
y = df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42, class_weight="balanced"),
}

metrics = []
predictions = {}
for name, model in models.items():
    if name == "Logistic Regression":
        model.fit(X_train_scaled, y_train)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
    else:
        model.fit(X_train, y_train)
        y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)
    predictions[name] = (model, y_pred, y_proba)
    metrics.append(
        {
            "model": name,
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "auc": round(roc_auc_score(y_test, y_proba), 4),
        }
    )

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv(base / "model_metrics.csv", index=False, encoding="utf-8-sig")

best_name = metrics_df.sort_values("auc", ascending=False).iloc[0]["model"]
best_model, best_pred, best_proba = predictions[best_name]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.countplot(data=df, x="churn", ax=axes[0, 0], palette=["#22c55e", "#ef4444"])
axes[0, 0].set_title("Churn Label Distribution")
axes[0, 0].set_xticks([0, 1])
axes[0, 0].set_xticklabels(["Not Churn", "Churn"])
axes[0, 0].set_xlabel("")
axes[0, 0].set_ylabel("Users")

for name, (_, _, y_proba) in predictions.items():
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    axes[0, 1].plot(fpr, tpr, label=f"{name} AUC={auc:.3f}")
axes[0, 1].plot([0, 1], [0, 1], "--", color="gray")
axes[0, 1].set_title("ROC Curve")
axes[0, 1].set_xlabel("FPR")
axes[0, 1].set_ylabel("TPR")
axes[0, 1].legend()

cm = confusion_matrix(y_test, best_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[1, 0])
axes[1, 0].set_title(f"{best_name} Confusion Matrix")
axes[1, 0].set_xlabel("Predicted")
axes[1, 0].set_ylabel("Actual")

rf = predictions["Random Forest"][0]
importances = pd.DataFrame({"feature": features, "importance": rf.feature_importances_}).sort_values("importance", ascending=False)
sns.barplot(data=importances.head(8), x="importance", y="feature", ax=axes[1, 1], palette="viridis")
axes[1, 1].set_title("Random Forest Feature Importance TOP8")
axes[1, 1].set_xlabel("Importance")
axes[1, 1].set_ylabel("")

plt.tight_layout()
plt.savefig(base / "churn_model_dashboard.png", dpi=180, bbox_inches="tight")

risk_users = X_test.copy()
risk_users["user_id"] = df.loc[X_test.index, "user_id"].values
risk_users["churn_probability"] = best_proba
risk_users["actual_churn"] = y_test.values
risk_users = risk_users.sort_values("churn_probability", ascending=False).head(30)
risk_users.to_csv(base / "high_risk_users.csv", index=False, encoding="utf-8-sig")

report = f"""# 用户流失预测机器学习项目报告

## 项目背景

本项目模拟互联网平台用户行为数据，建立用户流失预测模型，提前识别高风险流失用户，并给出运营干预建议。该项目覆盖数据挖掘实习岗位常见技能：特征工程、分类建模、模型评估、特征重要性解释和高风险用户名单输出。

## 数据字段

| 字段 | 含义 |
|---|---|
| active_days | 用户累计活跃天数 |
| last_login_days | 最近一次登录距今天数 |
| order_count | 历史订单数 |
| avg_order_amount | 平均订单金额 |
| coupon_used | 是否使用过优惠券 |
| complaint_count | 投诉次数 |
| page_views_30d | 近30日浏览次数 |
| cart_count_30d | 近30日加购次数 |
| pay_count_30d | 近30日支付次数 |
| member_level | 会员等级 |
| churn | 是否流失 |

## 模型效果

{metrics_df.to_markdown(index=False)}

最佳模型：**{best_name}**

## 关键发现

1. 最近登录间隔越长，用户流失概率越高。
2. 投诉次数是强风险信号，应优先做客服回访。
3. 历史订单数、近30日支付次数、会员等级越高，流失概率通常越低。
4. 随机森林能捕捉非线性关系，整体 AUC 表现优于或接近逻辑回归。

## 运营建议

- 对 `high_risk_users.csv` 中 Top30 高风险用户发放召回券。
- 对投诉次数较高用户优先客服跟进，降低负面体验导致的流失。
- 对近30日浏览多但支付少用户推送限时优惠，促进转化。
- 建议每周重跑模型，形成用户流失预警机制。
"""
(base / "分析报告.md").write_text(report, encoding="utf-8")
print("用户流失预测项目完成")
print(metrics_df)
