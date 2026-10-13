# CommonRules Collection - Boost Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - NO GAME & DOMAIN ONLY

 **If you would like to use `slowdomains_nogame_domainonly.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json)

### Note

**To use `slowdomains_nogame_domainonly.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Proxy` in the example is an existing outbound tag; replace it as needed.

### Example

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

## Type Ⅱ - GAME ONLY & DOMAIN ONLY

 **If you would like to use `slowdomains_gameonly_domainonly.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json)

### Note

**To use `slowdomains_gameonly_domainonly.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Game Boosting` in the example is an existing outbound tag; replace it as needed.

### Example

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
