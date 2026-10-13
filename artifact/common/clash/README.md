# BlacklistRules Collection

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For Clash Kernel

 **If you would like to use `blacklistrules_domainonly.yaml`, you can get it with following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/clash/blacklistrules_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/clash/blacklistrules_domainonly.mrs)
- CDN(maybe 24-hour-delaying sync): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/clash/blacklistrules_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/clash/blacklistrules_domainonly.mrs)

### Note

**To use `blacklistrules_domainonly.yaml`, `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

```yaml
rule-providers:
  blacklistrules:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/clash/blacklistrules_domainonly.yaml",
      path: "./ruleset/Paloexiz/blacklistrules_domainonly.yaml",
    }
```
