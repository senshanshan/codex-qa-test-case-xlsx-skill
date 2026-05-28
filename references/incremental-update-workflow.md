# Incremental Update Workflow

## Goal

Revise an existing test-case set without fully rebuilding it from zero.

## Baseline Pair

The preferred baseline is a file pair already present in the workspace:

- workbook: `.xlsx`
- structured payload: `payload.json`

The payload JSON is the primary source of truth for later updates. The workbook is the user-facing deliverable.

## High-Level Flow

1. User provides requirement-change evidence
2. Locate the latest matching workbook + payload JSON pair
3. Copy the payload into the next revision
4. Match impacted cases using payload data
5. Update the new payload revision
6. Export a new workbook from the new payload revision

## Matching Priority

Use this order when locating impacted cases:

1. `_meta.source_requirement`
2. `_meta.keywords`
3. `用例标题`
4. `测试步骤`
5. `预期结果`
6. `模块`

Favor precision over broad rewrites.

## Revisioning Rules

- Never overwrite the old workbook or old payload
- Create the next revision with `_01`, `_02`, and so on
- Increment `revision` in the new payload
- Fill `based_on` with the prior workbook file name

## Change Handling

### Modify

- Update the matched cases first
- Preserve existing case IDs
- Refresh `_meta.source_requirement` and `_meta.keywords`

### Add

- Add only the new cases needed by the change
- Put them in the best-fit category
- Generate new case IDs

### Delete

- Remove only high-confidence matched cases from the new payload revision
- If confidence is weak, leave the item in `待确认项` instead of deleting aggressively

## Output

At the end of an incremental update, produce:

- a new payload JSON revision
- a new workbook revision
- a short change summary
