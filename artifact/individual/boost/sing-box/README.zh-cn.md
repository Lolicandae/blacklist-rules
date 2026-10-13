# 通用规则合集 - 加速系列

**语言选择：[English](README.md)  | 简体中文**

## 类型 Ⅰ - 排除游戏且仅域名

 **如果您需要使用 `slowdomains_nogame_domainonly.json` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json)

### 注意事项

**为了能够正常调用 `slowdomains_nogame_domainonly.json` 文件，`format` 属性应为 `source` 字项。**

该文件使用版本 3 的 JSON 规则集格式。示例中的 `Proxy` 是已配置的出口标签，请按需替换。

### 示例代码

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-boost_nogame",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-boost_nogame"
        ],
        "outbound": "Proxy"
      }
    ]
  }
}
```

## 类型 Ⅱ - 仅游戏且仅域名

 **如果您需要使用 `slowdomains_gameonly_domainonly.json` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json)

### 注意事项

**为了能够正常调用 `slowdomains_gameonly_domainonly.json` 文件，`format` 属性应为 `source` 字项。**

该文件使用版本 3 的 JSON 规则集格式。示例中的 `Game Boosting` 是已配置的出口标签，请按需替换。

### 示例代码

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-boost_game",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-boost_game"
        ],
        "outbound": "Game Boosting"
      }
    ]
  }
}
```
