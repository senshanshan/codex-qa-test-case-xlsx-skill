---
name: test-case-xlsx-generator
description: Generate structured QA test cases from PRDs, screenshots, wireframes, or plain feature descriptions and export them to categorized `.xlsx` workbooks. Also use when a workspace already contains a test-case workbook and payload JSON, and Codex needs to revise the cases based on requirement changes without fully starting from zero.
---

# Test Case XLSX Generator

Generate structured test cases first, then export them to a categorized Excel workbook.

Keep the workflow conservative and evidence-based:

- Analyze the input before drafting cases
- Build a coverage map before expanding rows
- Prefer explicit evidence over guesswork
- Record unclear requirements as `待确认项`
- Export with consistent sheets, columns, and naming

## Modes

Support two stable modes.

### 1. First Generate

Use this mode when the user gives PRDs, screenshots, wireframes, or feature descriptions and wants a fresh workbook.

Core rules:

- Start from `templates/base_payload.json`
- Build the coverage map first
- Fill categorized cases into the payload
- Export with `scripts/export_test_cases.py`
- Save both workbook and payload JSON in the workspace

### 2. Incremental Update

Use this mode when the user says the requirement changed and the workspace already contains a workbook plus matching payload JSON.

Core rules:

- Treat the latest workbook + payload JSON pair as the baseline
- Do not overwrite the baseline files
- Copy the payload into the next revision
- Use the payload as the main source of truth for matching impacted cases
- Use `_meta.source_requirement`, `_meta.keywords`, case title, steps, and expected result to locate cases
- Export a new workbook after updating the new payload revision

## First Generate Workflow

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

- `功能用例`
- `表单校验`
- `边界值`
- `异常场景`
- `界面交互`
- `权限安全`

Allow prompt-level category extensions when they are useful. Read [references/classification-rules.md](./references/classification-rules.md) when category assignment is ambiguous.

### 3. Fill the Payload Instead of Rebuilding Structure

Create cases only after the coverage map is complete.

Use `templates/base_payload.json` as the fixed structure.

Default case columns:

- `用例编号`
- `模块`
- `用例标题`
- `前置条件`
- `测试步骤`
- `预期结果`
- `优先级`
- `类型`
- `备注`

Optional internal matching metadata may be kept in the payload only:

- `_meta.source_requirement`
- `_meta.keywords`

These `_meta` fields are for future matching and must not be shown in the exported workbook.

### 4. Handle Uncertainty Explicitly

If the input is incomplete or ambiguous:

- Generate only high-confidence cases
- Add `待确认项` in the summary
- Do not fabricate business rules, permissions, or hidden workflows

### 5. Export to `.xlsx`

Use the bundled exporter:

`scripts/export_test_cases.py`

Before exporting, keep the payload JSON in the workspace. This payload becomes the structured baseline for later revisions.

## Incremental Update Workflow

When the user provides new requirement-change evidence:

1. Find the latest workbook + payload JSON pair in the workspace
2. Read the baseline payload JSON
3. Create the next payload revision with `scripts/update_cases_from_change.py`
4. Match impacted cases through:
   - `_meta.source_requirement`
   - `_meta.keywords`
   - `用例标题`
   - `测试步骤`
   - `预期结果`
   - `模块`
5. Update, add, or remove cases in the new payload revision
6. Export a new workbook from the new payload revision

Versioning rules:

- Never overwrite the old workbook or old payload
- Append `_01`, `_02`, and so on to new revisions
- Increment `revision` in the payload JSON
- Record the prior workbook name in `based_on`

## Output Contract

Present results in this order unless the user asked for a different format:

1. Brief framing of the input and testing scope
2. Coverage map or impacted-case summary
3. Test case design or update summary
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
- [references/incremental-update-workflow.md](./references/incremental-update-workflow.md)
  Read when revising a case set from requirement changes.
- `templates/base_payload.json`
  Use as the starting structure for first-time generation.
- `scripts/export_test_cases.py`
  Use to export categorized case data to a formatted `.xlsx` workbook.
- `scripts/update_cases_from_change.py`
  Use to create the next payload revision from change evidence and an existing payload baseline.
