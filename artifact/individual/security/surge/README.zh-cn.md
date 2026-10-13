# 通用规则合集 - 安全系列

**语言选择：[English](README.md)  | 简体中文**

## 类型 Ⅰ - 仅域名

 **如果您需要使用 `anonymityservice_domainonly.list` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_domainonly.list)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_domainonly.list)

### 注意事项

**为了能够正常调用 `anonymityservice_domainonly.list` 文件，`behavior` 属性应为 `DOMAIN-SET` 字项。**

### 示例代码

```list
[Rule]
# > blacklistrules-security_domain
DOMAIN-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_domainonly.list, Safe Browse, update-interval=86400
```

## 类型 Ⅱ - 仅程序名

 **如果您需要使用 `anonymityservice_processnameonly.list` 文件，您可以通过如下超链接进行获取：**

- 原始链接：[查看或下载](https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_processnameonly.list)
- 镜像链接（可能会有24小时的延迟）：[查看或下载](https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_processnameonly.list)

### 注意事项

**为了能够正常调用 `anonymityservice_processnameonly.list` 文件，`behavior` 属性应为 `RULE-SET` 字项。**

### 示例代码

```list
[Rule]
# > blacklistrules-security_process
RULE-SET, https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_processnameonly.list, Safe Browse, update-interval=86400
```
