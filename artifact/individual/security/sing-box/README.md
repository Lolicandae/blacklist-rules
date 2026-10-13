# CommonRules Collection - Security Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - DOMAIN ONLY

 **If you would like to use `anonymityservice_domainonly.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_domainonly.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_domainonly.json)

### Note

**To use `anonymityservice_domainonly.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Safe Browse` in the example is an existing outbound tag; replace it as needed.

### Example

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-security_domain",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_domainonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-security_domain"
        ],
        "outbound": "Safe Browse"
      }
    ]
  }
}
```

## Type Ⅱ - PROCESS NAME ONLY

 **If you would like to use `anonymityservice_processnameonly.json`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json)

### Note

**To use `anonymityservice_processnameonly.json`, the `format` property should be `source`.**

This file uses version 3 of the JSON rule-set format. `Safe Browse` in the example is an existing outbound tag; replace it as needed.

Source `PROCESS-NAME,...` entries become `process_name`. Matching requires local process information. Application package names use the separate `package_name` field and are not converted automatically here.

### Example

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "blacklistrules-security_process",
        "format": "source",
        "url": "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "blacklistrules-security_process"
        ],
        "outbound": "Safe Browse"
      }
    ]
  }
}
```
