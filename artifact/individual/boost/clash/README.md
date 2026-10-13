# CommonRules Collection - Boost Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - NO GAME & DOMAIN ONLY

 **If you would like to use `slowdomains_nogame_domainonly.yaml`, you can get it with following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs)
- CDN(maybe 24-hour-delaying sync): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs)

### Note

**To use `slowdomains_nogame_domainonly.yaml`, `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

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

# CommonRules Collection - Boost Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅱ - GAME ONLY & DOMAIN ONLY

 **If you would like to use `slowdomains_gameonly_domainonly.yaml`, you can get it with following links:**

- Original: [YAML](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml) · [MRS](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs)
- CDN(maybe 24-hour-delaying sync): [YAML](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml) · [MRS](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs)

### Note

**To use `slowdomains_gameonly_domainonly.yaml`, `behavior` property should be `domain`.**

For Mihomo, use the MRS link with `format: mrs` and `behavior: domain`; change the example's URL and cache path to the `.mrs` file.

### Example

```yaml
rule-providers:
  blacklistrules-boost:
    {
      type: http,
      interval: 86400,
      format: yaml,
      behavior: domain,
      url: "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml",
      path: "./ruleset/Paloexiz/slowdomains_gameonly_domainonly.yaml",
    }
```
