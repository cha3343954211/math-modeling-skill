# 球面方位投影（光源投影）建模案例

## 适用场景
题目涉及球面方位投影、地图投影、航线投影、盲区分析时参考。

## 投影公式（关键区分）

### 光源在对跖点（本题类型）
光源 S 在投影点 P 的对跖点（antipode），光线从 S 穿过球面打到切平面。

**正确公式**：
```
r = R · tan(c/2)
x = r · (P×X)_x / |P×X|
y = r · (P×X)_y / |P×X|
```
其中 c = arccos(P⃗·X⃗ / R²) 是投影中心 P 与被投影点 X 的球面角距离。

**推导**：
- 光线参数方程: L(t) = S + t·(X - S)，S = -R·P̂
- 切平面 z = R（以 P 为极轴）
- 求交: t = 2R/(X_z + R)
- 投影距离: r = R·sin(c)/(1+cos(c)) = R·tan(c/2)

### ⚠️ 常见错误：混淆为 gnomonic 投影
- **Gnomonic**（光源在球心）：r = R·tan(c) ← 错误用于本题！
- **Stereographic**（光源在对跖点）：r = 2R·tan(c/2) ← 也有因子2错误
- **本题正确**：r = R·tan(c) ← 不对！
- **本题正确**：r = R·sin(c)/(1+cos(c)) = R·tan(c/2)

注意：gnomonic 的分母是 cos(c)，本题的分母是 1+cos(c)。两者在 c→0 时都退化为 R·c，但在 c=90° 时完全不同（gnomonic→∞，本题=R）。

## 盲区判定
盲区 = 距光源 S 球面角距离 ≤ 45° 的区域。
等价于距投影点 P 角距离 ≥ 135° 的区域。

```python
S_dir = -normalize(ll_to_xyz(proj_lon, proj_lat, R=1.0))
cos_c = np.dot(point_dir, S_dir)
c = np.arccos(np.clip(cos_c, -1, 1))
is_blind = np.rad2deg(c) <= 45
```

## 盲区边界在投影平面上的形状
盲区边界（距 S 恰好 45° 的小圆）投影后在切平面上仍是一个圆。
经过仿射变换后变为椭圆。

## 逆投影公式
给定投影平面坐标 (x, y) 和投影点 P：
1. 计算 r = sqrt(x² + y²)
2. c = 2·arctan(r/R)
3. 方向角 φ = arctan2(y, x)（在投影平面内）
4. 从 P 沿方向 φ 走角距离 c 得到原像点

## 图像坐标提取工作流（从带噪投影图读取数据）

### 步骤1：轴标定
从图像中提取轴刻度位置（像素），建立像素↔图面坐标(km)映射：
```python
# 找轴刻度：在底部行/左侧列搜索暗像素组
# X轴: pixel_left → -30000km, pixel_right → 30000km
# Y轴: pixel_top → 20000km, pixel_bottom → -20000km（或反过来，看标签）
x_km = x_min + (px - px_left) / (px_right - px_left) * (x_max - x_min)
y_km = y_max - (py - py_top) / (py_bottom - py_top) * (y_max - y_min)
```

### 步骤2：提取城市/特征点像素坐标
```python
# 方法1：视觉分析工具（vision_analyze）
# 方法2：颜色聚类（找特定颜色的像素簇）
dark_mask = (r < 30) & (g < 30) & (b < 30) & (a > 200)
# 方法3：手动读图 + 轴交叉验证
```

### 步骤3：仿射逆变换 + 逆投影
```python
A_inv = np.linalg.inv(A)
xy_ideal = A_inv @ (xy_observed - d)  # 逆仿射
lon, lat = azimuthal_unproject(xy_ideal[0], xy_ideal[1], proj_lon, proj_lat)  # 逆投影
```

### 步骤4：验证
正投影→仿射变换→像素，与观测对比：
```python
xy_check = azimuthal_project(lon, lat, proj_lon, proj_lat)
xy_check_noisy = A @ xy_check + d
px_check, py_check = map_to_pixel(xy_check_noisy[0], xy_check_noisy[1])
err = sqrt((px_check - px_obs)**2 + (py_check - py_obs)**2)
```

## 多目标飞行路径优化模式

### 目标函数
1. 通信静默时间（航段在盲区内的弧长 / 巡航速度）
2. 投影形变方差（各航段投影长度比的方差）
3. 总航程（TSP距离）

### 求解策略
1. 最近邻 + 2-opt 求 TSP 基准解
2. 网格搜索 + Nelder-Mead 优化投影点
3. 变异 + 2-opt 进一步优化路线+投影点组合

### 静默时间计算
```python
def compute_blackout_time(route, proj_lon, proj_lat, speed=900):
    S_dir = -normalize(ll_to_xyz(proj_lon, proj_lat, R=1.0))
    total_blind_km = 0
    for i in range(len(route) - 1):
        arc = great_circle_arc(xyz[route[i]], xyz[route[i+1]], n_pts=200)
        for j in range(len(arc) - 1):
            mid = (arc[j] + arc[j+1]) / 2
            cos_c = np.dot(normalize(mid), S_dir)
            if np.rad2deg(np.arccos(np.clip(cos_c,-1,1))) <= 45:
                total_blind_km += great_circle_distance(arc[j], arc[j+1])
    return total_blind_km / speed
```

## LaTeX 编译经验
- 42页论文用 xelatex 编译3遍，耗时约8分钟
- ctexart 文档类 + SimHei/SimSun 字体
- tikz/pgfplots 可用于绘制投影几何示意图
- 不需要 \\usepackage{fontspec}（ctex 已处理字体）
