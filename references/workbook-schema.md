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

If the target file already exists, append `_01`, `_02`, and so on.

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

Each category item should contain:

- `name`
- `cases`

Each case should be a JSON object keyed by column name.

## Practical Notes

- Keep sheet names concise so they remain valid in Excel after sanitization
- Preserve the category order from the generated payload when possible
- Use `备注` for assumptions that should remain visible to reviewers
