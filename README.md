# Test Case XLSX Generator

从 PRD、截图、线框图或纯文本需求生成结构化测试用例，并导出为分类清晰的 `.xlsx` 工作簿。

Generate structured QA test cases from PRDs, screenshots, wireframes, or plain feature descriptions, then export them to categorized `.xlsx` workbooks.

这个仓库包含一个 Codex skill 和一个 Python 导出脚本，适合希望把需求输入稳定转换为 Excel 测试用例交付物的团队。

This repository contains a Codex skill plus a Python exporter script. It is designed for teams that want a repeatable workflow for turning requirement input into Excel-based test case deliverables.

## Version Notes

版本变更记录请参考 [版本介绍.md](./版本介绍.md)。

For release history and version-to-version changes, see [版本介绍.md](./版本介绍.md).

## What This Skill Does

- 将 PRD、截图、线框图或混合输入转换为结构化测试用例
- 在展开详细用例前先构建覆盖地图
- 按 `功能用例`、`表单校验`、`边界值`、`异常场景`、`界面交互`、`权限安全` 等分类整理用例
- 当需求中存在明确约束时，按系统化边界值策略生成测试点，而不只是笼统地测“特殊值”
- 用 `待确认项` 显式记录不确定信息
- 导出为格式化的 Excel 工作簿
- 默认输出到当前工作目录，并避免覆盖已有文件
- 如需执行版工作簿，可通过 `extra_columns` 追加 `实际结果` 等列，而不是修改默认列结构

- Turn PRDs, screenshots, wireframes, or mixed inputs into structured test cases
- Build a coverage map before writing detailed cases
- Classify cases into categories such as `功能用例`, `表单校验`, `边界值`, `异常场景`, `界面交互`, and `权限安全`
- When explicit constraints exist, generate boundary cases systematically instead of only checking vague "special values"
- Track uncertainty explicitly with `待确认项`
- Export the final result to a formatted Excel workbook
- Default to the current working directory and avoid accidental overwrites
- Keep execution-oriented columns such as `实际结果` optional through `extra_columns` instead of changing the default schema

## Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── execution-template-example.md
│   └── sample-prompt.md
├── references/
│   ├── classification-rules.md
│   ├── input-contract.md
│   └── workbook-schema.md
└── scripts/
    └── export_test_cases.py
```

## Best Fit

适合以下场景：

- 从 PRD 生成测试用例
- 从截图或线框图生成测试用例
- 导出分类测试用例到 Excel
- 生成适合 Windows 交付流程复用的测试用例工作簿

Use this skill when you want Codex to:

- Generate test cases from a PRD
- Generate test cases from screenshots or wireframes
- Export categorized QA cases to Excel
- Produce a reusable test case workbook for Windows-based delivery

## Workflow

1. 阅读输入内容，只提取有明确证据支持的信息。
2. 先构建覆盖地图，再写详细用例。
3. 生成高置信度测试用例。
4. 如存在明确限制条件，按系统化边界值策略补充测试点。
5. 将缺失或模糊需求标记为 `待确认项`。
6. 导出为 `.xlsx`。
   如未指定输出目录，则默认输出到当前工作目录。

1. Read the input and identify only what is directly supported by the evidence.
2. Build a coverage map before writing detailed rows.
3. Generate high-confidence test cases.
4. When explicit limits exist, cover boundary values systematically.
5. Mark missing or ambiguous requirements as `待确认项`.
6. Export the result to `.xlsx`.
   If no output directory is provided, export to the current working directory.

## Output Format

默认工作簿使用中文 sheet 名和列名：

- Sheets: `说明`, `功能用例`, `表单校验`, `边界值`, `异常场景`, `界面交互`, `权限安全`
- Columns: `用例编号`, `模块`, `用例标题`, `前置条件`, `测试步骤`, `预期结果`, `优先级`, `类型`, `备注`

The default workbook uses Chinese sheet names and columns:

- Sheets: `说明`, `功能用例`, `表单校验`, `边界值`, `异常场景`, `界面交互`, `权限安全`
- Columns: `用例编号`, `模块`, `用例标题`, `前置条件`, `测试步骤`, `预期结果`, `优先级`, `类型`, `备注`

你也可以通过 prompt 参数扩展额外分类或字段列。

如果你希望把生成结果直接当执行单使用，建议通过 `extra_columns` 追加 `实际结果`、`执行人`、`执行日期`、`是否通过` 等字段，而不是直接修改默认列。

You can extend the workbook with additional categories or extra columns through prompt parameters.

If you want an execution-ready workbook, add columns such as `实际结果`, `执行人`, `执行日期`, and `是否通过` through `extra_columns` instead of changing the default columns.

## Install

### 1. Place the skill in your Codex skills directory

将本目录放到你的 Codex skills 路径下，例如：

Put this folder under your Codex skills path, for example:

```text
$CODEX_HOME/skills/test-case-xlsx-generator
```

如果没有设置 `CODEX_HOME`，常见默认目录是：

If `CODEX_HOME` is not set, a common default is:

```text
~/.codex/skills/test-case-xlsx-generator
```

### 2. Install Python dependency

安装 Python 依赖：

```bash
pip install -r requirements.txt
```

如果不传 `output_dir`，生成的工作簿会默认保存在你运行命令时所在的当前目录。

If you do not pass `output_dir`, the generated workbook will be saved in the current working directory where the command runs.

## Example Prompt

示例提示词：

```text
Use $test-case-xlsx-generator to generate categorized QA test cases from this PRD and these screenshots. Focus on login and password reset. Save the workbook to C:\Users\me\Documents\TestCases.
```

如果你想要更贴近团队执行习惯的模板示例，请参考 [examples/execution-template-example.md](./examples/execution-template-example.md)。

If you want a more execution-oriented example, see [examples/execution-template-example.md](./examples/execution-template-example.md).

## Export Script

仓库内置 `scripts/export_test_cases.py`，用于将结构化 JSON 导出为 Excel 工作簿。

The repository includes `scripts/export_test_cases.py` for exporting structured JSON into an Excel workbook.

### Script Usage

脚本用法：

```bash
python scripts/export_test_cases.py --input-json payload.json
```

```bash
python scripts/export_test_cases.py --input-json payload.json --output-dir ./exports
```

### Expected Payload Shape

JSON 载荷建议包含以下字段：

- `system_name`
- `module_name`
- `input_summary`
- `generated_at`
- `output_format`
- `uncertainties`
- `extra_columns`
- `categories`

The JSON payload should include fields such as:

- `system_name`
- `module_name`
- `input_summary`
- `generated_at`
- `output_format`
- `uncertainties`
- `extra_columns`
- `categories`

每个分类对象应包含：

- `name`
- `cases`

Each category should contain:

- `name`
- `cases`

每条用例应是一个以工作簿列名为 key 的 JSON 对象。

Each case should be a JSON object keyed by workbook column name.

完整结构请参考 [references/input-contract.md](./references/input-contract.md) 和 [references/workbook-schema.md](./references/workbook-schema.md)。

See [references/input-contract.md](./references/input-contract.md) and [references/workbook-schema.md](./references/workbook-schema.md) for the full structure.

## Design Principles

- 优先基于证据生成用例，而不是做推测性覆盖
- 对明确存在的边界规则，优先做系统化边界覆盖，而不是只补一个“异常值”
- 让不确定信息可见，而不是隐藏起来
- 保持流程稳定、可复用
- 优先优化 Excel 交付效果，而不只是文本输出

- Prefer evidence-based cases over speculative coverage
- For explicit limit rules, prefer systematic boundary coverage instead of a single vague "invalid value" case
- Make uncertainty visible instead of hiding it
- Keep the workflow stable and reusable
- Optimize for practical Excel delivery, not just raw text output

## Notes

- 当前版本虽然仍偏向中文 QA 交付结构，但默认输出路径已经改为当前工作目录，更适合开源共享。
- 工作簿默认结构更适合中文 QA 交付场景。
- 如果你想适配其他语言或企业模板，建议同时修改 `references/workbook-schema.md` 和导出脚本。

- This version still favors Chinese QA deliverables, but the default export path now uses the current working directory for better open-source portability.
- The workbook defaults are optimized for Chinese QA deliverables.
- If you want to adapt the schema for another language or company template, update `references/workbook-schema.md` and the exporter script together.
