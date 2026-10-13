# 通用规则合集 - 安全系列

**语言选择：[English](README.md)  | 简体中文**

## 类型 Ⅰ - 仅域名

 **如果您需要使用 `anonymityservice_domainonly.json` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_domainonly.json)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_domainonly.json)

### 注意事项

**为了能够正常调用 `anonymityservice_domainonly.json` 文件，`format` 属性应为 `source` 字项。**

该文件使用版本 3 的 JSON 规则集格式。示例中的 `Safe Browse` 是已配置的出口标签，请按需替换。

### 示例代码

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-security_domain",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_domainonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-security_domain"
        ],
        "outbound": "Safe Browse"
      }
    ]
  }
}
```

## 类型 Ⅱ - 仅程序名

 **如果您需要使用 `anonymityservice_processnameonly.json` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json)

### 注意事项

**为了能够正常调用 `anonymityservice_processnameonly.json` 文件，`format` 属性应为 `source` 字项。**

该文件使用版本 3 的 JSON 规则集格式。示例中的 `Safe Browse` 是已配置的出口标签，请按需替换。

程序名按源文件中的 `PROCESS-NAME,...` 转换为 `process_name`。匹配需要运行环境提供本机进程信息；应用包名规则使用不同的 `package_name` 字段，不会在此自动转换。

### 示例代码

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-security_process",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-security_process"
        ],
        "outbound": "Safe Browse"
      }
    ]
  }
}
```
