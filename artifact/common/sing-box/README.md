# BlacklistRules Collection

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For sing-box Kernel

 **If you would like to use `blacklistrules_domainonly.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/sing-box/blacklistrules_domainonly.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/sing-box/blacklistrules_domainonly.json)

### Note

**To use `blacklistrules_domainonly.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Proxy` in the example is an existing outbound tag; replace it as needed.

### Example

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
