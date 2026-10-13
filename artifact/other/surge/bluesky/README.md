# Other Rules - Bluesky

**Select your Language: English | [简体中文](README.zh-cn.md)**

## For Surge Kernel Only

 **If you would like to use `bluesky.list`, you can get it with following links:**

- Original: [View or Download](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/other/surge/bluesky/bluesky.list)
- CDN(maybe 24-hour-delaying sync): [View or Download](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/surge/bluesky/bluesky.list)

### Note

**To use `bluesky.list`, `behavior` property should be `DOMAIN-SET`.**

### Example

```list
[Rule]
# > bluesky
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/other/surge/bluesky/bluesky.list, Bluesky, update-interval=86400
```
