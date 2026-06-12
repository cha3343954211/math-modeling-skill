# 球面方位投影航线识别案例记录（校赛B）

## 适用场景

当数学建模题涉及地图投影、球面几何、大圆航线、投影盲区、图像读点反推、飞行路径规划与投影点联合优化时参考。

## 建模路线

### 正向球面方位投影

1. 经纬度转三维单位向量：
   \[
   q=(\cos\varphi\cos\lambda,\cos\varphi\sin\lambda,\sin\varphi).
   \]
2. 投影点单位向量为 `P`，光源点为 `S=-P`，切平面为 `P·X=R`。
3. 光源点 `-RP` 到球面点 `Rq` 的射线与切平面交点：
   \[
   X=-RP+\frac{2R}{1+P\cdot q}(q+P).
   \]
4. 构造切平面东向/北向基，得到平面坐标 `(x,y)`。
5. 盲区判别：`angular_distance(q, S) <= 45°`，盲区内城市点和航线采样点不显示。
6. 大圆航线用 SLERP 采样，不要用经纬度平面直线或投影平面直线替代。

### 带噪观测反投影

- 题给误差模型通常形如 `p' = A p + d + ε`，先用 `p = inv(A)(p'-d)` 做一阶系统误差校正。
- 平面点反投影：切平面点 `X=RP+x e+y n`，从光源点 `-RP` 向 `X` 连线，解 `|-RP+u(X+RP)|=R` 的正根，再转经纬度。
- 图像读点只能作为证据链的一部分；若未人工精确读点，必须在论文中说明像素标定/读点误差，并把结论表述为“带噪估计”。
- 不得用海岸线形状或现实地理轮廓猜测城市身份，除非题目允许。

### 路径规划与投影点优化

1. 先计算节点两两大圆距离。
2. 用最近邻 + 2-opt 生成可复现的 TSP baseline/可行路线。
3. 固定路线后优化连续投影点，目标可包含：
   - 总通信静默比例；
   - 最大单段静默弧长/时间；
   - 投影长度畸变方差；
   - 总航程（若路线也参与迭代）。
4. 静默弧长可用大圆采样近似：每段总长度 × 落入盲区采样点比例。
5. 必做 baseline：固定投影点方案 vs 优化投影点方案，报告静默比例和静默时间变化。

## Windows/中文路径实现坑

### OpenCV 读取中文路径图片

`cv2.imread(str(path))` 在 Windows 中文路径下可能返回 `None`。稳定写法：

```python
import cv2, numpy as np
from pathlib import Path

img_path = Path('E:/含中文路径/附件2_带噪球面方位投影图.png')
raw = np.fromfile(str(img_path), dtype=np.uint8)
img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
if img is None:
    raise FileNotFoundError(str(img_path))
```

### OpenCV 保存中文路径图片

`cv2.imwrite()` 也可能受中文路径影响。稳定写法：

```python
cv2.imencode('.png', img)[1].tofile(str(output_path))
```

## 论文表述注意

- 对图像反推问题，不要把自动读图的粗估结果写成“精确识别”；需写清读点误差、噪声容许范围和结果边界。
- 若正式论文页数低于 skill 的正文 15 页门槛，只能视为“校赛快速交付版/短论文”，最终回复要主动说明；若用户要求正式完整论文，应继续扩充到门槛后再发送。
- 摘要数字必须来自 `frozen_numbers.json`，不要从运行日志临时复制。

## 最小支撑材料

- `quest1/figures/q1_projected_route.png`
- `quest2/figures/q2_red_components_debug.png`
- `quest2/outputs/q2_red_components.csv`
- `quest3/outputs/q3_segment_results.csv`
- `results/frozen_numbers.json`
- `papper/论文.tex` 与 `papper/论文.pdf`
