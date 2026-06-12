# 竞赛课程报告（竞赛过程记录）写作指南

## 适用场景

大学生数学建模课程要求提交"竞赛过程记录"——回顾一次参赛经历，描述选题、建模、编程、写作全过程。常见于课程期末作业、模块化课程记录本。

## 标准结构（8段式）

1. **竞赛基本信息**：竞赛名称、时间、选题、队伍编号、队员、指导教师
2. **选题过程**：三题初读比较 → 选题决策理由（3-4条）
3. **问题分析**：题目理解、子问题逻辑关系、建模难点识别
4. **模型建立**：总体框架 + 每问的核心思路、方法、关键结果数字
5. **编程实现**：开发环境、代码结构、关键挑战与解决方案
6. **论文撰写**：论文结构、撰写分工（用户填写）、撰写过程
7. **获奖情况**：用户填写
8. **赛后反思**：做得好的地方（3条）、不足与改进（3条）、总体收获

## 工作流程

### A. 信息收集（必须先做）

1. **读取已有论文**：PDF 或 docx，提取标题、摘要、三问方法和关键数字
2. **读取课程模板**：确认格式要求（封面、打印方式、装订方式）
3. **检查目录结构**：了解提交了什么（论文、代码、支撑材料）
4. **搜索历史会话**：如有之前的建模会话，搜索获取选题讨论、过程细节

### B. 内容生成

- 从论文中提取：方法名称、关键公式、核心结果数字、图表描述
- 从目录结构推断：代码组织、支撑材料完整度
- 基于论文内容合理推断：选题理由、建模难点、编程挑战
- **红色占位符**标记用户必须填写的内容：姓名、分工、获奖、个人感受

### C. 格式输出

优先使用 `python-docx` 生成 Word 文档（方便打印），同时保留 Markdown 草稿。

## python-docx 中文文档生成模板

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

doc = Document()

# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
style.paragraph_format.line_spacing = 1.5

# 标题（黑体）
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('标题文字')
run.font.size = Pt(22)
run.font.bold = True
run.font.name = '黑体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

# 正文（宋体，首行缩进）
p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Pt(24)
p.paragraph_format.line_spacing = 1.5
run = p.add_run('正文内容')
run.font.size = Pt(12)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 红色占位符（用户填写项）
p = doc.add_paragraph()
p.paragraph_format.first_line_indent = Pt(24)
run = p.add_run('[请填写xxx]')
run.font.size = Pt(12)
run.font.name = '宋体'
run._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
run.font.color.rgb = RGBColor(255, 0, 0)
```

## ⚠️ 常见坑

| 坑 | 解决方案 |
|---|---|
| python-docx 中文显示方框 | 必须设置 `rFonts` 的 `w:eastAsia` 属性为中文字体名 |
| 黑体/宋体标题不生效 | `run.font.name` 和 `run._element.rPr.rFonts.set(qn('w:eastAsia'), ...)` 两个都要设 |
| 首行缩进不生效 | 用 `paragraph_format.first_line_indent = Pt(24)` 而非手动加空格 |
| 行距不生效 | 在 `style.paragraph_format.line_spacing = 1.5` 设全局，或逐段设置 |
| 红色文字打印前需删除 | 在文档中统一用 RGBColor(255,0,0) 标记，提醒用户打印前删除 |

## 内容填充原则

- **基于论文提取**：方法名、公式、数字结果直接从已有论文中提取，不编造
- **合理推断**：编程挑战、建模难点可基于论文内容合理推断，但用词留有余地
- **用户必填项**：姓名学号、团队分工、获奖情况、个人感受必须用红色占位符
- **语言风格**：第一人称复数（"我们"），回忆性叙述，适当使用"首先/其次/因此"等连接词
- **数字一致**：报告中的所有数字必须与原始论文一致（如AUC=0.9743、7类方案、1523.65元等）
