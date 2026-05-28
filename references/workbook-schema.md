# Workbook Schema

## Default Workbook Structure

Recommended sheets:

- `说明`
- `功能用例`
- `表单校验`
- `边界值`
- `异常场景`
- `界面交互`
- `权限安全`

Additional sheets may be added for prompt-defined categories.

## Default Columns

- `用例编号`
- `模块`
- `用例标题`
- `前置条件`
- `测试步骤`
- `预期结果`
- `优先级`
- `类型`
- `备注`

Append prompt-defined extra columns after the default columns.

## Payload-Only Internal Metadata

The payload JSON may contain case-level internal metadata under `_meta`, for example:

- `_meta.source_requirement`
- `_meta.keywords`

These fields exist to help later incremental updates match impacted cases more accurately.

Do not show `_meta` fields in the exported workbook.

## Execution-Oriented Optional Columns

The default workbook stays focused on test case design, not execution records.

If the user wants an execution-ready workbook, recommend adding extra columns such as:

- `实际结果`
- `执行人`
- `执行日期`
- `是否通过`
- `需求编号`
- `是否自动化`

These columns should usually be passed through `extra_columns` instead of being added to the default schema.

## Summary Sheet

The `说明` sheet should include:

- 系统名
- 模块名
- 输入来源
- 生成时间
- 输出格式
- 用例总数
- 分类统计
- 待确认项

## Naming Rules

Priority order:

1. Use `file_name` if the user provides it
2. `{system_name}_{module_name}_测试用例_{YYYY-MM-DD}.xlsx`
3. `{module_name}_测试用例_{YYYY-MM-DD}.xlsx`
4. `测试用例_{YYYY-MM-DD}.xlsx`

For later revisions, append `_01`, `_02`, and so on to both workbook and payload file names.

## Formatting Expectations

- Freeze the header row in each case sheet
- Bold the header row
- Use wrap text for long steps and expected results
- Auto-adjust widths within a reasonable cap
- Keep the workbook readable rather than overly styled

## Data Model for the Export Script

The export script expects a JSON object with:

- `system_name`
- `module_name`
- `input_summary`
- `generated_at`
- `output_format`
- `uncertainties`
- `extra_columns`
- `categories`

The payload may also contain metadata such as:

- `schema_version`
- `source_name`
- `file_name`
- `output_dir`
- `revision`
- `based_on`
- `extra_categories`

These metadata fields support workflow stability and future incremental updates, but do not need to appear in the workbook.

Each category item should contain:

- `name`
- `cases`

Each case should be a JSON object keyed by workbook column name, and may optionally include `_meta`.

## Practical Notes

- Keep sheet names concise so they remain valid in Excel after sanitization
- Preserve the category order from the generated payload when possible
- Use `备注` for assumptions that should remain visible to reviewers
- If execution-oriented columns are requested, append them after the default columns so the base schema remains stable across teams
