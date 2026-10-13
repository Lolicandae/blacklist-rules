# 通用规则合集 - 加速系列

**语言选择：[English](README.md)  | 简体中文**

## 类型 Ⅰ - 排除游戏且仅域名

 **如果您需要使用 `slowdomains_nogame_domainonly.yaml` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs)
- 镜像链接（可能会有24小时的延迟）：[YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs)

### 注意事项

**为了能够正常调用 `slowdomains_nogame_domainonly.yaml` 文件，`behavior` 属性应为 `domain` 字项。**

Mihomo 可使用上面的 MRS 链接：设置 `format: mrs`、`behavior: domain`，并把示例中的 URL 和缓存路径换成 `.mrs`。

### 示例代码:

```yaml
rule-providers:
  blacklistrules-boost:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml",
      path: "./ruleset/Paloexiz/slowdomains_nogame_domainonly.yaml",
    }
```

## 类型 Ⅱ - 仅游戏且仅域名

 **如果您需要使用 `slowdomains_gameonly_domainonly.yaml` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs)
- 镜像链接（可能会有24小时的延迟）：[YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs)

### 注意事项

**为了能够正常调用 `slowdomains_gameonly_domainonly.yaml` 文件，`behavior` 属性应为 `domain` 字项。**

Mihomo 可使用上面的 MRS 链接：设置 `format: mrs`、`behavior: domain`，并把示例中的 URL 和缓存路径换成 `.mrs`。

### 示例代码

```yaml
rule-providers:
  blacklistrules-unlock_game:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml",
      path: "./ruleset/Paloexiz/slowdomains_gameonly_domainonly.yaml",
    }
```
