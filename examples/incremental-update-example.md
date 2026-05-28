# Incremental Update Example

Use this pattern when the workspace already contains a workbook and payload JSON, and the product requirement changes.

## Example Prompt

```text
需求有变更，请基于当前工作区已有的测试用例和 payload.json 找出受影响用例，
复制出新版本并完成修改。
```

## Example Change JSON

```json
{
  "change_type": "modify",
  "change_content": "将原先默认当前绑定单位改为下拉自选且必填",
  "source_name": "需求变更截图",
  "module_name": "长期聘用人员"
}
```
