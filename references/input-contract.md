# Input Contract

## Required Input

Provide at least one of:

- `prd_path`
- `screenshots`
- `wireframes`
- `feature_description`

The skill should still work with mixed input.

## Recommended Prompt Parameters

- `module_name`
- `system_name`
- `output_dir`

## Optional Prompt Parameters

- `file_name`
- `extra_columns`
- `extra_categories`
- `output_format`
- `template_path`
- `test_focus`

## Parameter Meanings

- `module_name`
  Human-readable module scope, such as `登录模块` or `预警新增`
- `system_name`
  Product or system name, such as `WMS`
- `output_dir`
  Output folder for the workbook
- `file_name`
  Full workbook file name, including `.xlsx` when provided
- `extra_columns`
  Additional column names, such as `需求编号`, `实际结果`, or `是否自动化`
- `extra_categories`
  Additional case categories beyond the default set
- `output_format`
  Default is `xlsx`; other formats are optional future extensions
- `template_path`
  Optional workbook template path for future customization
- `test_focus`
  Priority direction such as `表单校验优先`

## Fallback Rules

- If `output_dir` is missing, default to the current working directory
- If `file_name` is missing, use the naming rules in `workbook-schema.md`
- If `system_name` is missing, omit it from the file name
- If `module_name` is missing, use a generic workbook name
- If `extra_columns` is missing, use the default columns only
- If `extra_categories` is missing, use the default categories only
- If the user wants an execution-ready workbook, keep the default columns and append execution-oriented fields through `extra_columns`

## Incomplete Information Rules

- Continue with high-confidence case generation
- Record unclear areas as `待确认项`
- Do not invent hidden business rules or role logic

## Implementation Notes

- Keep the payload schema simple and JSON-friendly so it can be passed to `scripts/export_test_cases.py`
- Prefer Chinese workbook field names unless the user explicitly asks for another schema
- If the input mixes PRD text and screenshots, combine them into a single coverage map before exporting
- Treat the current working directory as the default export location for open-source portability
