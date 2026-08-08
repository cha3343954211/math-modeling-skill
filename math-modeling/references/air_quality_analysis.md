# 空气质量分析与预测实践案例

> 日期：2026年5月27日  
> 难度：入门基础  
> 用时：1天  

## 问题背景

某市环保部门在城区范围内布设了8个空气质量监测站，覆盖城区、工业区、交通区、居民区、生态区、文教区和郊区等不同功能区域，每日监测PM2.5、PM10、SO2、NO2、CO、O3等污染物浓度，并计算空气质量指数（AQI）。

## 数据说明

### 附件1：空气质量监测数据
- 8个监测站 × 60天 = 480条记录
- 字段：日期、监测站编号/名称、区域类型、PM2.5、PM10、SO2、NO2、CO、O3浓度、AQI、空气质量等级、首要污染物

### 附件2：气象数据
- 60天逐日数据 = 60条记录
- 字段：日期、天气状况、最高/最低温度、相对湿度、风速、风向、气压

## 问题分解

### 问题一：空气质量数据统计
1. 计算各监测站60天的PM2.5和AQI平均值，按AQI从高到低排序
2. 绘制各区域类型的AQI平均值对比柱状图
3. 统计各空气质量等级的天数占比，绘制饼图

### 问题二：AQI与气象因素的关系
1. 计算AQI与各气象变量的皮尔逊相关系数
2. 选取相关性最强的2个气象变量，绘制散点图并添加趋势线
3. 建立多元线性回归模型，给出回归方程和R²值

### 问题三：AQI预测与简单预警
1. 使用前40天训练，后20天测试，计算MAPE和RMSE
2. 预测第61天的AQI值
3. 判断空气质量等级并给出建议

## 关键代码片段

### 数据加载
```python
import pandas as pd

df_air = pd.read_excel('附件1_空气质量监测数据.xlsx')
df_air['日期'] = pd.to_datetime(df_air['日期'])

df_weather = pd.read_excel('附件2_气象数据.xlsx')
df_weather['日期'] = pd.to_datetime(df_weather['日期'])
```

### AQI分级函数
```python
def get_aqi_level(aqi):
    if aqi <= 50: return '优'
    elif aqi <= 100: return '良'
    elif aqi <= 150: return '轻度污染'
    elif aqi <= 200: return '中度污染'
    elif aqi <= 300: return '重度污染'
    else: return '严重污染'
```

### 相关系数计算
```python
from scipy import stats

corr, p_value = stats.pearsonr(df['AQI'], df['风速(m/s)'])
```

### 多元线性回归
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"R²: {model.score(X, y):.4f}")
print(f"回归方程: AQI = {model.intercept_:.4f}", end="")
for i, var in enumerate(features):
    print(f" + {model.coef_[i]:.4f} × {var}", end="")
```

### 评价指标
```python
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import numpy as np

mape = mean_absolute_percentage_error(y_test, y_pred) * 100
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
```

## 实践结果

### 问题一结果
- 工业区和交通区AQI最高（>140），属于轻度污染
- 生态区和郊区AQI最低（<65），空气质量良好
- 约77%的天数空气质量为"良"或"轻度污染"

### 问题二结果
- 风速与AQI呈显著正相关（r=0.260, p<0.05）
- 回归方程：AQI = 100.43 + 1.27 × 风速 - 0.81 × 最低温度
- R² = 0.108（模型解释力较弱）

### 问题三结果
- 测试集MAPE = 12.22%，RMSE = 14.63
- 第61天预测AQI = 110.50，属于轻度污染
- 建议：减少户外运动时间，敏感人群应避免户外活动

## 图表清单

| 文件名 | 内容 |
|--------|------|
| 问题1_区域AQI对比.png | 各区域类型AQI平均值柱状图 |
| 问题1_空气质量等级分布.png | 空气质量等级饼图 |
| 问题1_监测站AQI排名.png | 各监测站AQI排名条形图 |
| 问题2_散点图.png | AQI与气象变量散点图 |
| 问题2_回归分析.png | 回归模型预测vs实际值 |
| 问题2_相关系数热力图.png | 相关系数热力图 |
| 问题3_测试集预测.png | 测试集预测效果 |
| 问题3_预测结果.png | 第61天AQI预测可视化 |

## 关键发现

1. **空气质量分布**：工业区和交通区空气质量最差，生态区和郊区最好
2. **气象影响**：风速与AQI呈显著正相关，其他气象因素影响不显著
3. **模型局限**：线性回归模型解释力较弱（R²仅10.8%），说明AQI受多种因素影响

## 改进方向

1. 增加更多特征变量（如首要污染物、天气状况等）
2. 使用非线性模型（如随机森林、XGBoost）
3. 增加时间序列特征（如滞后变量、移动平均）
