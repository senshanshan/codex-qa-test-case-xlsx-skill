# 示例提示词

使用 `$test-case-xlsx-generator` 从 PRD 或截图生成分类测试用例。

推荐参数：

- `output_dir`: `C:\Users\YourName\Desktop\TestCases`

常用可选参数：

- `system_name`: `Demo System`
- `module_name`: `Login`
- `extra_categories`: `兼容性`, `性能`
- `extra_columns`: `需求编号`, `是否自动化`

标准示例：

```text
使用 $test-case-xlsx-generator 根据这张登录页截图生成分类测试用例。

system_name: Demo System
module_name: Login
output_dir: C:\Users\YourName\Desktop\TestCases
extra_categories: 兼容性, 性能
extra_columns: 需求编号, 是否自动化

请：
1. 先构建覆盖地图。
2. 只生成高置信度测试用例。
3. 如果存在明确的输入限制，请系统化覆盖边界值。
4. 最终导出为 xlsx。
```

精简版本：

```text
使用 $test-case-xlsx-generator 根据这份 PRD 生成测试用例，并将 xlsx 保存到：
C:\Users\YourName\Desktop\TestCases
```

如果你想看执行版工作簿模板示例，也可以参考 `examples/execution-template-example.md`。
