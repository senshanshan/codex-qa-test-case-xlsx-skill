# Input Contract

## First Generate Required Input

Provide at least one of:

- `prd_path`
- `screenshots`
- `wireframes`
- `feature_description`

The skill should still work with mixed input.

## Incremental Update Required Input

Provide requirement-change evidence as one or more of:

- changed PRD text
- screenshot
- feature-change description
- document excerpt

The workspace should already contain:

- a baseline workbook
- a baseline payload JSON

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
  Optional payload template path for future customization
- `test_focus`
  Priority direction such as `表单校验优先`

## First Generate Rules

- Start from `templates/base_payload.json`
- Fill metadata first, then fill categories and cases
- Save both workbook and payload JSON together

## Incremental Update Rules

- Use the latest matching workbook + payload JSON pair as the baseline unless the user explicitly points to another pair
- Never overwrite the old baseline files
- Create a new payload revision first
- Export a new workbook from the new payload revision

## Fallback Rules

- If `output_dir` is missing, default to the current working directory
- If `file_name` is missing, use the naming rules in `workbook-schema.md`
- If `system_name` is missing, omit it from the file name
- If `module_name` is missing, use a generic workbook name
- If `extra_columns` is missing, use the default columns only
- If `extra_categories` is missing, use the default categories only
- If the user wants an execution-ready workbook, keep the default columns and append execution-oriented fields through `extra_columns`

## Incomplete Information Rules

- Continue with high-confidence case generation or updates
- Record unclear areas as `待确认项`
- Do not invent hidden business rules or role logic
- If incremental matching is weak, leave the uncertainty visible instead of forcing a broad rewrite

## Implementation Notes

- Keep the payload schema simple and JSON-friendly so it can be passed to `scripts/export_test_cases.py`
- Prefer Chinese workbook field names unless the user explicitly asks for another schema
- Treat the current working directory as the default export location for open-source portability
- Keep `_meta` fields in the payload JSON only; they are for agent matching, not for workbook display
