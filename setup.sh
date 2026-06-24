#!/bin/bash
# 一键安装作品集依赖
# 需要 Python 3.8+

echo "📦 正在安装数据挖掘作品集依赖..."

python3 -m pip install --upgrade pip -q
python3 -m pip install pandas numpy matplotlib seaborn scikit-learn mlxtend jupyter -q

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 如何运行："
echo "  cd 项目1_电商用户行为分析"
echo "  jupyter notebook ecommerce_analysis.ipynb"
echo ""
echo "  cd 项目2_上市公司财务分析"
echo "  jupyter notebook financial_analysis.ipynb"
echo ""
echo "或者使用 VS Code 直接打开 .ipynb 文件运行"
