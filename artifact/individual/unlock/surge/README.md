# CommonRules Collection - Unlock Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - NO GAME & DOMAIN ONLY

 **If you would like to use `blockeddomains_nogame_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list)

### Note

**To use `blockeddomains_nogame_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules-unlock_nogame
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list, Proxy, update-interval=86400
```

## Type Ⅱ - GAME ONLY & DOMAIN ONLY

 **If you would like to use `blockedgames_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockedgames_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockedgames_domainonly.list)

### Note

**To use `blockedgames_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules-unlock_game
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockedgames_domainonly.list, Game Unlocking, update-interval=86400
```
