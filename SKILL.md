---
name: test-case-xlsx-generator
description: Generate structured QA test cases from PRDs, screenshots, wireframes, or plain feature descriptions and export them to categorized `.xlsx` workbooks. Use when Codex needs a repeatable workflow for coverage mapping, case classification, uncertainty tracking, Excel delivery, or Windows-friendly test case export from visible UI or written requirements.
---

# Test Case XLSX Generator

Generate structured test cases first, then export them to a categorized Excel workbook.

Keep the workflow conservative and evidence-based:

- Analyze the input before drafting cases
- Build a coverage map before expanding rows
- Prefer explicit evidence over guesswork
- Record unclear requirements as `待确认项`
- Export with consistent sheets, columns, and naming

## Workflow

Follow these steps in order. Do not jump straight to workbook generation.

### 1. Identify the Available Evidence

Accept one or more of these sources:

- PRD or requirement document
- UI screenshot
- Wireframe or prototype image
- Plain-text feature description
- Mixed input, such as PRD plus screenshots

List only what is directly knowable from the input:

- Visible controls
- Labels and messages
- Navigation structure
- Input constraints
- User flow steps
- Business rules explicitly stated in the PRD

Do not infer hidden backend behavior unless the input clearly supports it.

If the material is partial, continue with the high-confidence portion and track the gaps as `待确认项`.

### 2. Build a Coverage Map First

Before generating any case rows, create a concise coverage map from the available evidence.

Default coverage categories:

- 功能用例
- 表单校验
- 边界值
- 异常场景
- 界面交互
- 权限安全

Allow prompt-level category extensions when they are useful. Read [references/classification-rules.md](./references/classification-rules.md) when category assignment is ambiguous.

Coverage map goals:

- Identify the main flows worth testing
- Identify the controls and states visible in the input
- Identify likely validation points
- Identify explicit boundaries such as min/max length, numeric ranges, thresholds, required fields, and selectable states
- Identify missing information that should remain unconfirmed

### 3. Generate Cases from the Coverage Map

Create cases only after the coverage map is complete.

Default output columns:

- 用例编号
- 模块
- 用例标题
- 前置条件
- 测试步骤
- 预期结果
- 优先级
- 类型
- 备注

Allow prompt-level extra columns when requested. Read [references/workbook-schema.md](./references/workbook-schema.md) for workbook structure and default naming rules.

Generation rules:

- Prefer concrete, testable steps
- Prefer observable expected results
- Avoid duplicate cases with only wording differences
- Use the visible page structure when working from screenshots
- Use explicit PRD rules when working from documents
- When the input defines a length, range, threshold, count, or enumeration rule, generate boundary cases systematically instead of only using a vague "special value" case
- Default boundary coverage should include: one normal valid value, the minimum valid value, minimum minus one when meaningful, the maximum valid value, maximum plus one when meaningful, and empty value when applicable
- If the exact boundary is not stated, do not invent a number. Keep the related point in `待确认项` and only generate high-confidence cases supported by the evidence
- Keep execution-oriented columns such as `实际结果` optional through `extra_columns` unless the user explicitly asks for an execution-ready workbook
- Mark uncertain assumptions in `备注` or in the summary sheet

### 4. Handle Uncertainty Explicitly

If the input is incomplete or ambiguous:

- Generate only high-confidence cases
- Add `待确认项` in the summary
- Do not fabricate business rules, permissions, or hidden workflows

Examples:

- Screenshot text is blurry
- The PRD names a button but does not describe failure behavior
- A page is visible but role-based access is not specified

### 5. Export to `.xlsx`

Default to `xlsx`.

Use prompt-level values when provided:

- output directory
- file name
- module name
- system name
- extra columns
- extra categories
- output format

Prioritize `xlsx` for stable delivery. Treat other formats as optional extensions instead of the default path.

Use the bundled exporter:

`scripts/export_test_cases.py`

Read [references/input-contract.md](./references/input-contract.md) before assembling exporter inputs.

### 6. Perform a Final QA Pass

Before finishing:

- Confirm the workbook path
- Confirm the file name
- Confirm the sheet split matches the case categories
- Confirm required columns are present
- Confirm any requested execution-oriented columns such as `实际结果` were appended correctly
- Confirm there are no obviously empty critical fields
- Confirm uncertain items are called out rather than hidden

## Output Contract

Present results in this order unless the user asked for a different format:

1. Brief framing of the input and testing scope
2. Coverage map
3. Test case design summary
4. Export confirmation
5. Final workbook path

Do not bury the result in raw logs.

## Output Defaults

This skill is Windows-first.

- Prefer a user-provided `output_dir`
- If `output_dir` is missing, default to the current working directory
- Create missing directories automatically
- Avoid overwriting an existing workbook by appending a numeric suffix

Use the default Chinese workbook labels unless the user clearly wants another schema.

## Resources

- [references/input-contract.md](./references/input-contract.md)
  Read when deciding which prompt parameters are available and how defaults should behave.
- [references/classification-rules.md](./references/classification-rules.md)
  Read when choosing categories or adding custom classification buckets.
- [references/workbook-schema.md](./references/workbook-schema.md)
  Read when building workbook columns, summary content, sheet names, and file naming.
- `scripts/export_test_cases.py`
  Use to export categorized case data to a formatted `.xlsx` workbook.
