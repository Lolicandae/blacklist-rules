# Other Rules - Bluesky

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For Clash Kernel Only

**If you would like to use `bluesky.yaml`, you can get it with the following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/clash/bluesky/bluesky.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/clash/bluesky/bluesky.mrs)
- CDN (may have a 24-hour sync delay): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/clash/bluesky/bluesky.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/clash/bluesky/bluesky.mrs)

### Note

**To use `bluesky.yaml`, the `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

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
