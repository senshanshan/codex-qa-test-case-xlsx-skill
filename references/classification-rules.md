# Classification Rules

## Default Categories

- `功能用例`
  Use for main user flows, successful operations, navigation, and expected business behavior clearly supported by the input.

- `表单校验`
  Use for required-field checks, format checks, prompt behavior, and submit-blocking logic.

- `边界值`
  Use for min/max length, value thresholds, empty combinations, and limit-related input behavior.

- `异常场景`
  Use for invalid input, failed submission, error prompts, broken flow handling, or graceful fallback expectations.

- `界面交互`
  Use for layout, control visibility, clickability, focus movement, keyboard actions, checkbox behavior, and readable UI feedback.

- `权限安全`
  Use for visible permission boundaries, masked password behavior, restricted entry points, and sensitive feedback exposure that is actually supported by the input.

## Adding Extra Categories

Prompt-provided categories may be added when useful, for example:

- `兼容性`
- `易用性`
- `状态切换`
- `性能感知`

Keep categories practical. Do not create tiny one-case categories unless the user explicitly wants them.

## Assignment Rules

- Put each case in the single best-fit category by default
- If a case genuinely spans multiple dimensions, keep one main category and note the overlap in `备注`
- Do not duplicate the same case across many sheets unless the user explicitly asks for repeated placement
- Keep category names short enough to work as Excel sheet names

## Screenshot-Specific Guidance

When only screenshots are available:

- Prefer `界面交互`, `表单校验`, and visible `功能用例`
- Use `权限安全` only when there is visible evidence, such as a password mask or a restricted entry element
- Treat hidden backend assumptions as out of scope

## PRD-Specific Guidance

When a PRD is available:

- Expand the main flow into `功能用例`
- Expand rule checks into `表单校验`
- Expand limits into `边界值`
- Expand failure handling into `异常场景`
- Expand UI obligations into `界面交互`

## Mixed-Input Guidance

When both documents and screenshots are available:

- Use the PRD to anchor business intent
- Use screenshots to anchor visible controls and page structure
- Prefer screenshot evidence when PRD wording and visible UI differ
- Move unresolved mismatches into `待确认项`
