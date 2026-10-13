# CommonRules Collection - Boost Series

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Type Ⅰ - NO GAME & DOMAIN ONLY

 **If you would like to use `slowdomains_nogame_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/surge/slowdomains_nogame_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_nogame_domainonly.list)

### Note

**To use `slowdomains_nogame_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules-boost_nogame
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_nogame_domainonly.list, Proxy, update-interval=86400
```

## Type Ⅱ - GAME ONLY & DOMAIN ONLY

 **If you would like to use `slowdomains_gameonly_domainonly.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/surge/slowdomains_gameonly_domainonly.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_gameonly_domainonly.list)

### Note

**To use `slowdomains_gameonly_domainonly.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > blacklistrules-boost_game
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_gameonly_domainonly.list, Game Boosting, update-interval=86400
```
