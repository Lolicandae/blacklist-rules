# Other Rules - Bluesky

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For sing-box Kernel Only

 **If you would like to use `bluesky.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/sing-box/bluesky/bluesky.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/sing-box/bluesky/bluesky.json)

### Note

**To use `bluesky.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Bluesky` in the example is an existing outbound tag; replace it as needed.

### Example

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "bluesky",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/sing-box/bluesky/bluesky.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "bluesky"
        ],
        "outbound": "Bluesky"
      }
    ]
  }
}
```
