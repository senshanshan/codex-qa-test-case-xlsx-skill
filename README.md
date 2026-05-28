# Test Case XLSX Generator

基于 PRD、截图、线框图或纯文字需求生成结构化 QA 测试用例，并导出为分类 `.xlsx` 工作簿。

Generate structured QA test cases from PRDs, screenshots, wireframes, or plain feature descriptions, then export them to categorized `.xlsx` workbooks.

## 简介 | Overview

这个仓库包含一个 Codex skill 和配套 Python 脚本，支持两类核心场景：

- 首次根据需求生成 Excel 测试用例
- 当需求变更时，基于已有 workbook 和 payload JSON 做版本化修改

This repository contains a Codex skill plus Python scripts for two core workflows:

- first-time generation of Excel test cases from requirements
- revision-based updates when requirements change and an existing workbook plus payload JSON already exists

## 能力说明 | What This Skill Does

- 将 PRD、截图、线框图或混合输入转为结构化测试用例
- 在展开详细用例前先构建覆盖地图
- 导出格式化 Excel 测试用例工作簿
- 在 workbook 旁边保留结构化 `payload.json`，方便后续修改
- 基于旧 `payload.json + workbook` 进行增量修订，而不是每次从零重建

- Turn PRDs, screenshots, wireframes, or mixed inputs into structured test cases
- Build a coverage map before writing detailed cases
- Export the final result to a formatted Excel workbook
- Save a structured `payload.json` beside the workbook for later updates
- Reuse the old payload JSON plus workbook to revise cases instead of fully starting over

## 仓库结构 | Repository Structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── examples/
│   ├── execution-template-example.md
│   ├── incremental-update-example.md
│   └── sample-prompt.md
├── references/
│   ├── classification-rules.md
│   ├── incremental-update-workflow.md
│   ├── input-contract.md
│   └── workbook-schema.md
├── scripts/
│   ├── export_test_cases.py
│   └── update_cases_from_change.py
└── templates/
    └── base_payload.json
```

## 首次生成流程 | First Generate Workflow

1. 读取输入，只提取有证据支持的信息。
2. 先构建覆盖地图，再写详细用例。
3. 使用 `templates/base_payload.json` 作为固定骨架。
4. 导出 `.xlsx` 工作簿。
5. 将 `payload.json` 与 workbook 一起保留在工作区。

1. Read the input and identify only what is directly supported by the evidence.
2. Build a coverage map before writing detailed rows.
3. Fill `templates/base_payload.json`.
4. Export the result to `.xlsx`.
5. Keep the payload JSON beside the workbook.

## 增量修改流程 | Incremental Update Workflow

1. 用户提供需求变更证据。
2. 在工作区中定位最新的 workbook + payload JSON 基线对。
3. 创建下一版 payload 修订文件。
4. 基于 payload 里的 `_meta`、标题、步骤和预期结果命中受影响用例。
5. 导出修订后的 workbook。

1. The user provides requirement-change evidence.
2. Locate the latest workbook + payload JSON pair in the workspace.
3. Create the next payload revision.
4. Match impacted cases from payload `_meta`, titles, steps, and expected results.
5. Export the revised workbook.

## Payload 模板 | Payload Template

skill 内置固定模板：

- `templates/base_payload.json`

这个模板用于稳定结构，减少每次重新组织 JSON schema 的成本。

The skill includes a fixed template at:

- `templates/base_payload.json`

The template keeps the structure stable and reduces repeated schema reconstruction work.

## 内部匹配元数据 | Internal Matching Metadata

`payload.json` 中的单条用例可包含：

- `_meta.source_requirement`
- `_meta.keywords`

这些字段用于后续需求变更时提高命中精度，但不会出现在导出的 workbook 中。

Cases in the payload JSON may include:

- `_meta.source_requirement`
- `_meta.keywords`

These metadata fields help future updates locate impacted cases more accurately, but they do not appear in the exported workbook.

## 安装 | Install

```bash
pip install -r requirements.txt
```

## 版本说明 | Version Notes

版本历史请参考 [版本介绍.md](./版本介绍.md)。

For release history, see [版本介绍.md](./版本介绍.md).
