# BlacklistRules Collection

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For Surge Kernel

 **If you would like to use `blacklistrules_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/surge/blacklistrules_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/surge/blacklistrules_domainonly.list)

### Note

**To use `blacklistrules_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/surge/blacklistrules_domainonly.list, Proxy, update-interval=86400
```
