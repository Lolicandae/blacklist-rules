# 通用规则合集 - 解锁系列

**语言选择：[English](README.md)  | 简体中文**

## 类型 Ⅰ - 排除游戏且仅域名

 **如果您需要使用 `blockeddomains_nogame_domainonly.list` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list)

### 注意事项

**为了能够正常调用 `blockeddomains_nogame_domainonly.list` 文件，`behavior` 属性应为 `DOMAIN-SET` 字项。**

### 示例代码

```list
[Rule]
# > blacklistrules-unlock_nogame
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list, Proxy, update-interval=86400
```

## 类型 Ⅱ - 仅游戏且仅域名

 **如果您需要使用 `blockedgames_domainonly.list` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockedgames_domainonly.list)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockedgames_domainonly.list)

### 注意事项

**为了能够正常调用 `blockedgames_domainonly.list` 文件，`behavior` 属性应为 `DOMAIN-SET` 字项。**

### 示例代码

```list
[Rule]
# > blacklistrules-unlock_game
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockedgames_domainonly.list, Game Unlocking, update-interval=86400
```
