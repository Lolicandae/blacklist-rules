# CommonRules Collection - Unlock Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - DOMAIN ONLY

 **If you would like to use `anonymityservice_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_domainonly.list)

### Note

**To use `anonymityservice_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules-security_domain
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_domainonly.list, Safe Browse, update-interval=86400
```

## Type Ⅱ - PROCESS NAME ONLY

 **If you would like to use `anonymityservice_processnameonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_processnameonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_processnameonly.list)

### Note

**To use `anonymityservice_processnameonly.list`, `behavior` property should be `RULE-SET`.**

### Example

```list
[Rule]
# > blacklistrules-security_process
RULE-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_processnameonly.list, Safe Browse, update-interval=86400
```
