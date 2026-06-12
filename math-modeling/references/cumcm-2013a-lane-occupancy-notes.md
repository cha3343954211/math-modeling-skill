# CUMCM 2013A 车道被占用案例记录

## 适用场景

用户要求完成 2013 年国赛 A 题“车道被占用对城市道路通行能力的影响”，或其他依赖事故视频/交通流附件的道路通行能力、排队长度、瓶颈服务率建模题。

## 本次会话形成的关键经验

### 1. 附件缺失时的诚信处理

有些历史国赛题目录可能只含 `CUMCM2013A.doc` 和 `readme.doc`，readme 指向已失效或难访问的外部视频下载页，实际缺少：

- 附件1：视频1；
- 附件2：视频2；
- 附件3：视频1事故位置示意图；
- 附件4：上游路口交通组织方案图；
- 附件5：上游路口信号配时方案图。

此时禁止伪称“已从视频逐帧统计”或编造原始计数表。正确做法：

1. 在摘要、数据来源、readme、`frozen_numbers.json` 中明确写出“原题目录缺少视频/图片附件”。
2. 若仍需完成建模全过程，可构造**参数化重构数据**用于演示模型链，但必须标注：视频相关数值不是原始视频人工计数。
3. 支撑材料保留一键生成脚本，便于将来取得原视频后替换逐分钟到达量/通过量并重跑。
4. L2 门控应写为“有条件通过”：代码可复现、约束和数字自洽，但原始附件缺失限制了实测有效性。

### 2. 题面提取

`.doc` 题面可用 `antiword` 提取文本，保存到 `支撑材料/references/`：

```bash
antiword CUMCM2013A.doc > 支撑材料/references/CUMCM2013A.txt
antiword readme.doc > 支撑材料/references/readme.txt
```

题面核心小问：

1. 根据视频1描述事故发生至撤离期间事故横断面实际通行能力变化；
2. 结合视频2分析同一横断面事故所占车道不同对实际通行能力影响差异；
3. 构建排队长度与实际通行能力、事故持续时间、上游车流量的关系模型；
4. 当事故横断面距上游路口 140 m、上游流量 1500 pcu/h、初始排队为零且事故不撤离时，估算排队到达上游路口时间。

### 3. 可用模型链

推荐采用“瓶颈通行能力 + 排队守恒 + 位置修正 + 情景敏感性”的可解释链条：

#### 问题一：通行能力过程

- Baseline：事故期间固定平均能力。
- 主模型：信号调制瓶颈能力

```math
C_1(t)=C_{b,1}(t)s(t)+\varepsilon_t
```

其中 `s(t)` 表示上游信号放行调制，解释公开摘要中“随上游路口信号灯上下波动”的现象。

#### 问题二：占用位置差异

- Baseline：按被占车道数比例折减。
- 主模型：占用位置修正

```math
C_i(t)=\alpha_i C_0(t)s(t)+\varepsilon_i(t),\quad 0<\alpha_i\le 1
```

当中间/外侧车道被占用导致更强换道、靠边或非机动车冲突时，`alpha` 取更小值。

#### 问题三：排队长度关系

优先先写交通流守恒，再用回归作解释：

```math
N_{m+1}=\max\left\{0,N_m+\frac{q_m-C_m}{60}\right\},\quad L_m=\frac{N_m}{k_j}
```

经验解释式可用：

```math
L=\beta_0+\beta_1 C+\beta_2 T+\beta_3 q+u
```

验证指标：`R²`、RMSE、MAE、残差解释、非负约束检查。

#### 问题四：到达上游路口时间

若初始排队为零、事故不撤离、上游流量稳定：

```math
t^*=\frac{D k_j}{q-\bar C}
```

其中 `D=140 m`，`q=1500 pcu/h`，`\bar C` 可取问题一事故平均能力，`k_j` 为两车道等效拥堵排队密度。若 `q <= C`，队列不会持续增长到路口。

### 4. 外部资料参考方式

IMA 可能搜不到本题直接资料。可用公开网页摘要辅助方法选择，但不要照搬全文：

- CNKI 条目：李梦圆、陈亚男、戴辞源、朱家明《车道被占用对城市道路通行能力的影响》，贵州师范学院学报，2013(12)。公开摘要提到视频采集、标准化处理、R²/F/t 检验、实际通行能力变化、不同车道差异、多元线性回归、微分方程等。
- 爱发表公开摘要：贾文《车道被占用对城市道路通行能力的影响》，齐鲁工业大学学报，2014(01)。摘要提到用事故后单位时间路段滞留车辆 PCU 描述通行能力降低，并随上游信号灯上下波动；建立多元线性回归和 GM(1,3) 分析排队关系。

在 `支撑材料/references/external_resource_notes.md` 记录：资源名称、可借鉴点、如何转化为 baseline/主模型/验证、风险（只有摘要，无原始数据）。

### 5. 论文写作注意

- 摘要必须主动声明数据限制，避免评委误认为数值来自原视频。
- 论文中所有视频相关表述使用“重构”“参数化估计”“若取得原视频可替换重跑”等措辞。
- 三层审计建议：
  - L1：通过，若四问均有输出映射、baseline、模型公式和现实解释；
  - L2：有条件通过，若代码可复现但原视频缺失；
  - L3：通过，若 PDF 页数、图表解释、敏感性、附录齐全。

## 支撑材料推荐结构

```text
支撑材料/
├── papper/论文.tex, 论文.pdf
├── data/CUMCM2013A.doc, readme.doc
├── references/CUMCM2013A.txt, readme.txt, external_resource_notes.md
├── quest1/figures/q1_capacity_process.png, outputs/video1_reconstructed_capacity.csv
├── quest2/figures/q2_capacity_comparison.png, outputs/video2_reconstructed_capacity.csv
├── quest3/figures/q3_fit_scatter.png, q3_queue_evolution.png, outputs/q3_regression_dataset.csv
├── quest4/figures/q4_sensitivity.png, outputs/q4_sensitivity.csv
├── results/frozen_numbers.json
├── tables/final_results_summary.csv
├── run_modeling.py
└── readme.txt
```

## Pitfall

不要把“能构造一套合理参数化数据”写成“已根据视频统计得到”。这类历史附件缺失题最重要的质量点是诚实披露数据限制，同时保持模型、代码、图表和论文链条可复现。
