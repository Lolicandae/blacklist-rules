# 其它规则 - Bluesky

**语言选择：[English](README.md) | 简体中文**

## 仅适用于 Clash 内核

**如果您需要使用 `bluesky.yaml` 文件，可以通过以下链接获取：**

- 原始链接：[YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/clash/bluesky/bluesky.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/clash/bluesky/bluesky.mrs)
- 镜像链接（同步可能延迟 24 小时）：[YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/clash/bluesky/bluesky.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/clash/bluesky/bluesky.mrs)

### 注意事项

**为了正常调用 `bluesky.yaml` 文件，`behavior` 属性应为 `domain`。**

Mihomo 可使用上面的 MRS 链接：设置 `format: mrs`、`behavior: domain`，并把示例中的 URL 和缓存路径换成 `.mrs`。

### 示例代码

```yaml
rule-providers:
  bluesky:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/clash/bluesky/bluesky.yaml",
      path: "./ruleset/paloexiz/bluesky.yaml",
    }
```
