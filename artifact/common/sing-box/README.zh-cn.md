# 黑名单规则合集

**语言选择：[English](README.md)  | 简体中文**

## 适用于 sing-box 内核的类型

 **如果您需要使用 `blacklistrules_domainonly.json` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/sing-box/blacklistrules_domainonly.json)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/sing-box/blacklistrules_domainonly.json)

### 注意事项

**为了能够正常调用 `blacklistrules_domainonly.json` 文件，`format` 属性应为 `source` 字项。**

该文件使用版本 3 的 JSON 规则集格式。示例中的 `Proxy` 是已配置的出口标签，请按需替换。

### 示例代码

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/sing-box/blacklistrules_domainonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules"
        ],
        "outbound": "Proxy"
      }
    ]
  }
}
```
