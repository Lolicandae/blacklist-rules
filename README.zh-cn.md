# 黑名单规则

**语言选择：[English](README.md)  | 简体中文**

## 项目介绍

用于进行出站分流的规则。

**更新频率**：任何时候。

## 免责声明

请只在合法且已获授权的场景下使用本仓库。这里的规则用于网络分流、过滤、研究和维护，不应用于违法活动、违反服务条款或侵犯第三方权益。

你需要自行确认使用、分发或修改这些规则是否符合所在地和具体场景的要求。维护者不承担滥用产生的责任。本仓库按现状提供，不作担保；许可条款见 [GNU General Public License v3.0](LICENSE)。

## 仓库维护方式

手动维护规则时，只改 `rule_sources/*.rules`。生成产物位于 `artifact/common/`、`artifact/individual/` 和 `artifact/other/`。

维护流程：

1. 修改 `rule_sources/` 中对应的源文件。
2. 提交并推送源文件改动。
3. 变更进入 `main` 后，GitHub Actions 先校验，再生成并提交规则产物。

Pull Request 中，GitHub Actions 校验源文件生成的候选结果，不写入产物，无需预先提交生成文件。推送前可在本地运行 `python workflow_scripts/build_rules.py --validate`；如需检查现有产物是否与源文件一致，使用 `--check`。

源文件格式与维护约定见 [rule_sources/README.zh-cn.md](rule_sources/README.zh-cn.md)。

第三方规则每天同步，并提供 Clash、Surge 和 sing-box 三种格式。订阅链接与维护说明见 [third_party/README.zh-cn.md](third_party/README.zh-cn.md)，上游许可见 [third_party/NOTICE.zh-cn.md](third_party/NOTICE.zh-cn.md)。

## 相关文档与链接

**提示**：CDN 镜像链接可能因为缓存而滞后。需要最新文件时，请优先使用原始链接。

### 适用于 Clash 内核 - 选择您的类型

域名规则提供 YAML 和 MRS 两种格式。Mihomo 可使用 MRS，设置 `format: mrs` 和 `behavior: domain`；程序名规则使用 YAML，设置 `behavior: classical`。

<table>
  <tr align="center">
    <th rowspan="2" scope="col">
      类型
    </th>
    <th colspan="2" scope="colgroup">
      原始链接
    </th>
    <th colspan="2" scope="colgroup">
      镜像链接
    </th>
  </tr>
  <tr align="center">
    <th scope="col">YAML</th>
    <th scope="col">MRS</th>
    <th scope="col">YAML</th>
    <th scope="col">MRS</th>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/common/clash/README.zh-cn.md">自定义规则合集</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/clash/blacklistrules_domainonly.yaml">仅域名</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/clash/blacklistrules_domainonly.mrs">仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/clash/blacklistrules_domainonly.yaml">仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/clash/blacklistrules_domainonly.mrs">仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/boost/clash/README.zh-cn.md">通用-加速</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.yaml">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.yaml">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_nogame_domainonly.mrs">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/clash/slowdomains_gameonly_domainonly.mrs">仅游戏且仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/security/clash/README.zh-cn.md">通用-安全</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/clash/anonymityservice_domainonly.yaml">仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/clash/anonymityservice_processnameonly.yaml">仅程序名</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/clash/anonymityservice_domainonly.mrs">仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/clash/anonymityservice_domainonly.yaml">仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/clash/anonymityservice_processnameonly.yaml">仅程序名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/clash/anonymityservice_domainonly.mrs">仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/unlock/clash/README.zh-cn.md">通用-解锁</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.yaml">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockedgames_domainonly.yaml">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.mrs">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/clash/blockedgames_domainonly.mrs">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.yaml">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockedgames_domainonly.yaml">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockeddomains_nogame_domainonly.mrs">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/clash/blockedgames_domainonly.mrs">仅游戏且仅域名</a>
    </td>
  </tr>
</table>

### 适用于 sing-box 内核 - 选择您的类型

<table>
  <tr align="center">
    <td>
      <b>类型</b>
    </td>
    <td>
      <b>通过原始链接以查看或下载</b>
    </td>
    <td>
      <b>通过镜像链接以查看或下载</b>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/common/sing-box/README.zh-cn.md">自定义规则合集</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/sing-box/blacklistrules_domainonly.json">仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/sing-box/blacklistrules_domainonly.json">仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/boost/sing-box/README.zh-cn.md">通用-加速</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_nogame_domainonly.json">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/sing-box/slowdomains_gameonly_domainonly.json">仅游戏且仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/security/sing-box/README.zh-cn.md">通用-安全</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_domainonly.json">仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json">仅程序名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_domainonly.json">仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/sing-box/anonymityservice_processnameonly.json">仅程序名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/blob/main/artifact/individual/unlock/sing-box/README.zh-cn.md">通用-解锁</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/sing-box/blockeddomains_nogame_domainonly.json">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/sing-box/blockedgames_domainonly.json">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/sing-box/blockeddomains_nogame_domainonly.json">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/sing-box/blockedgames_domainonly.json">仅游戏且仅域名</a>
    </td>
  </tr>
</table>

### 适用于 Surge 内核 - 选择您的类型

<table>
  <tr align="center">
    <td>
      <b>类型</b>
    </td>
    <td>
      <b>通过原始链接以查看或下载</b>
    </td>
    <td>
      <b>通过镜像链接以查看或下载</b>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/tree/main/artifact/common/surge">自定义规则合集</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/common/surge/blacklistrules_domainonly.list">仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/common/surge/blacklistrules_domainonly.list">仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/tree/main/artifact/individual/boost/surge">通用-加速</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/surge/slowdomains_nogame_domainonly.list">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/boost/surge/slowdomains_gameonly_domainonly.list">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_nogame_domainonly.list">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/boost/surge/slowdomains_gameonly_domainonly.list">仅游戏且仅域名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/tree/main/artifact/individual/security/surge">通用-安全</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_domainonly.list">仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/security/surge/anonymityservice_processnameonly.list">仅程序名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_domainonly.list">仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/security/surge/anonymityservice_processnameonly.list">仅程序名</a>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="https://github.com/Lolicandae/blacklist-rules/tree/main/artifact/individual/unlock/surge">通用-解锁</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list">排除游戏且仅域名</a>
      <br>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/artifact/individual/unlock/surge/blockedgames_domainonly.list">仅游戏且仅域名</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockeddomains_nogame_domainonly.list">排除游戏且仅域名</a>
      <br>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/artifact/individual/unlock/surge/blockedgames_domainonly.list">仅游戏且仅域名</a>
    </td>
  </tr>
</table>
