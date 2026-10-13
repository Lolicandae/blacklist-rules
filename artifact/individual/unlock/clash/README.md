# CommonRules Collection - Unlock Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - NO GAME & DOMAIN ONLY

 **If you would like to use `blockeddomains_nogame_domainonly.yaml`, you can get it with following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.mrs)
- CDN(maybe 24-hour-delaying sync): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.mrs)

### Note

**To use `blockeddomains_nogame_domainonly.yaml`, `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

```yaml
rule-providers:
  blacklistrules-unlock_nogame:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.yaml",
      path: "./ruleset/Paloexiz/blockeddomains_nogame_domainonly.yaml",
    }
```

## Type Ⅱ - GAME ONLY & DOMAIN ONLY

 **If you would like to use `blockedgames_domainonly.yaml`, you can get it with following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockedgames_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockedgames_domainonly.mrs)
- CDN(maybe 24-hour-delaying sync): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockedgames_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockedgames_domainonly.mrs)

### Note

**To use `blockedgames_domainonly.yaml`, `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

```yaml
rule-providers:
  blacklistrules-unlock_game:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockedgames_domainonly.yaml",
      path: "./ruleset/Paloexiz/blockedgames_domainonly.yaml",
    }
```
