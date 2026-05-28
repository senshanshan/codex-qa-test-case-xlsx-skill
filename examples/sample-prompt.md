# 示例提示词 | Sample Prompts

使用 `$test-case-xlsx-generator` 从 PRD、截图或功能描述生成分类测试用例，或基于已有 payload/workbook 做增量修改。

Use `$test-case-xlsx-generator` to generate categorized test cases from PRDs, screenshots, or feature descriptions, or to revise an existing payload/workbook pair when requirements change.

## 首次生成示例 | First Generate Example

```text
使用 $test-case-xlsx-generator 根据这份 PRD 生成测试用例。

system_name: Demo System
module_name: Login
output_dir: C:\Users\YourName\Desktop\TestCases

请：
1. 先构建覆盖地图。
2. 只生成高置信度测试用例。
3. 最终导出为 xlsx，并保留 payload.json。
```

```text
Use $test-case-xlsx-generator to generate test cases from this PRD.

system_name: Demo System
module_name: Login
output_dir: C:\Users\YourName\Desktop\TestCases

Please:
1. build a coverage map first,
2. generate only high-confidence test cases,
3. export the final result as xlsx and keep payload.json beside it.
```

## 增量修改示例 | Incremental Update Example

```text
需求有变更，请基于当前工作区已有的测试用例和 payload.json 找出受影响用例，
复制出新版本并完成修改。
```

```text
The requirement changed. Please use the existing test cases and payload.json in the current workspace
to find impacted cases, copy a new revision, and complete the update.
```
