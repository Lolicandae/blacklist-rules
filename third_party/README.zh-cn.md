# 第三方规则

**语言选择：[English](README.md) | 简体中文**

## 项目介绍

按固定清单同步上游文件，并按 Domain、IP、Keyword、Process、ASN、UserAgent、Logical 等类型拆分规则。规则按作者和服务分目录存放，文件名统一使用小写；自有规则仍位于原有 `artifact/` 目录。

**使用方式**：在下方选择适合客户端的规则链接，并在客户端配置中指定对应的分流策略，例如直连、代理或拦截。规则文件只包含匹配条件，具体流量如何处理由你的客户端配置决定。第三方规则内容由本仓库定期从上游同步更新。

**更新频率**：每天定时同步一次，计划在香港时间（UTC+8，与北京时间相同）凌晨 **03:23** 触发，对应前一天 UTC **19:23**。

定时配置随 [Workflow](../.github/workflows/sync-third-party-rules.yml) 发布到 `main` 后生效。03:23 是计划触发时间；[GitHub Actions 调度可能延迟](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows#scheduled-workflows-running-at-unexpected-times)，实际开始与完成时间以 Actions 运行记录为准，不能保证规则文件在 03:23 已更新完成。

## 维护方式

同步清单固定在 `workflow_scripts/sync_third_party_rules.py` 的 `UPSTREAM_RULES` 中，不从客户端配置中读取。每项明确上游地址、输入类型和产物名称；修改同步范围时编辑该清单。`third_party/sources.json` 记录下载结果和产物路径。Workflow 将 Domain/IP/Process 来源转换为 Clash YAML、Surge 和 sing-box 格式，同时原样同步上游 MRS 文件。同一来源、服务已有 Surge 规则时，直接使用上游 Surge 文件，不再生成转换副本。MRS 由 Mihomo 校验；本地运行同步脚本时，通过 `MIHOMO_BIN` 指定内核程序，Workflow 已配置。Surge 来源按全部匹配类型分别输出，保留 Surge 专有语法，链接放在下方 Surge 表格中；不同上游各自存放、更新。遇到尚不支持的规则时验证失败，不会静默漏掉。许可文件保留固定副本，变更需人工审核。

成功同步时，规则按上游当前内容更新，上游删除的规则也会一并移除。上游仓库或文件返回 HTTP 404/410 时，保留该来源的现有文件和最后成功的来源记录，其他来源继续同步。缺失来源没有匹配的本地副本、其他下载错误或内容无效时，Workflow 失败且不提交新规则，已发布文件继续保留。全部可用来源验证成功后才更新产物。内容不变时不生成提交。可在 Actions 中手动运行 Sync Third-Party Rules。

只生成有规则的分类文件。上游某一类已没有规则时，删除对应文件，并移除下载链接和示例配置中的引用。同步哪些上游文件由固定清单决定，客户端配置只用于更新引用。

## 第三方许可

规则沿用各来源的版权与许可，仓库自身的许可证不替代第三方许可。完整说明及原文见 [NOTICE.zh-cn.md](NOTICE.zh-cn.md) 和 [licenses/](licenses/)。AdRules 的生成规则是多来源聚合；其脚本的 0BSD 许可不能作为全部规则数据的许可。原始来源表中未明确许可的条目按上游声明保留，不另行指定许可。

## 相关文档与链接

**提示**：CDN 镜像可能因为缓存而滞后。需要最新文件时，请优先使用原始链接。

### 适用于 sing-box 内核 - 选择您的类型

远程规则集填写原始链接，设置 `type: remote`、`format: source`。applications 是客户端进程规则，需使用支持进程识别的运行环境。

<table>
  <tr align="center">
    <td><b>类型</b></td>
    <td><b>通过原始链接以查看或下载</b></td>
    <td><b>通过镜像链接以查看或下载</b></td>
  </tr>
  <tr align="center">
    <td>adrules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/cats-team/adrules/adrules_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/cats-team/adrules/adrules_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/private/private_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/private/private_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/private/private_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/private/private_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/steam/steam_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/steam/steam_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/copilot/copilot_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/copilot/copilot_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/copilot/copilot_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/copilot/copilot_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/google-gemini/google-gemini_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/google-gemini/google-gemini_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/adobe-activation/adobe-activation_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/adobe-activation/adobe-activation_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/googlefcm/googlefcm_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/googlefcm/googlefcm_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/z-library/z-library_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/z-library/z-library_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/linuxdo/linuxdo_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/linuxdo/linuxdo_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitter/twitter_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitter/twitter_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitter/twitter_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitter/twitter_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/github/github_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/github/github_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/gitlab/gitlab_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/gitlab/gitlab_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/onedrive/onedrive_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/onedrive/onedrive_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/microsoft/microsoft_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/microsoft/microsoft_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/openai/openai_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/openai/openai_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/anthropic/anthropic_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/anthropic/anthropic_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/discord/discord_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/discord/discord_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/aliyun/aliyun_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/aliyun/aliyun_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/cloudflare/cloudflare_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/cloudflare/cloudflare_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/docker/docker_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/docker/docker_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/homebrew/homebrew_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/homebrew/homebrew_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/python/python_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/python/python_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/icloud/icloud_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/icloud/icloud_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/apple/apple_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/apple/apple_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/youtube/youtube_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/youtube/youtube_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/google/google_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/google/google_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/google/google_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/google/google_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitch/twitch_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitch/twitch_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/niconico/niconico_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/niconico/niconico_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/pixiv/pixiv_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/pixiv/pixiv_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/netflix/netflix_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/netflix/netflix_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/netflix/netflix_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/netflix/netflix_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/disney/disney_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/disney/disney_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/bilibili/bilibili_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/bilibili/bilibili_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/spotify/spotify_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/spotify/spotify_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/dmm/dmm_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/dmm/dmm_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/telegram/telegram_ip.json">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/telegram/telegram_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/telegram/telegram_ip.json">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/telegram/telegram_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/gfw/gfw_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/gfw/gfw_domain.json">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/loyalsoldier/applications/applications_process.json">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/loyalsoldier/applications/applications_process.json">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/cn/cn_domain.json">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/cn/cn_domain.json">仅域名</a></td>
  </tr>
</table>

### 适用于 Clash 内核 - 选择您的类型

Domain 文件使用 `behavior: domain`，IP 文件使用 `behavior: ipcidr`，applications 使用 `behavior: classical`。MRS 使用 `format: mrs`，YAML 使用 `format: yaml`；MRS 适用于 Mihomo 的域名和 IP 规则，进程规则使用 YAML。

MRS、YAML 均放在 `clash/作者/服务/` 下，例如 `clash/peiyingyao/steam/steam_domain.mrs`。

<table>
  <tr align="center">
    <td><b>类型</b></td>
    <td><b>通过原始链接以查看或下载</b></td>
    <td><b>通过镜像链接以查看或下载</b></td>
  </tr>
  <tr align="center">
    <td>adrules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/cats-team/adrules/adrules_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/cats-team/adrules/adrules_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/cats-team/adrules/adrules_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/cats-team/adrules/adrules_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/steam/steam_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/steam/steam_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/steam/steam_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/steam/steam_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/google-gemini/google-gemini_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/google-gemini/google-gemini_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/google-gemini/google-gemini_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/google-gemini/google-gemini_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/googlefcm/googlefcm_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/googlefcm/googlefcm_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/googlefcm/googlefcm_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/googlefcm/googlefcm_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/z-library/z-library_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/z-library/z-library_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/z-library/z-library_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/z-library/z-library_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/linuxdo/linuxdo_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/linuxdo/linuxdo_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/linuxdo/linuxdo_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/linuxdo/linuxdo_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/github/github_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/github/github_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/github/github_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/github/github_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gitlab/gitlab_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gitlab/gitlab_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gitlab/gitlab_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gitlab/gitlab_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/onedrive/onedrive_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/onedrive/onedrive_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/onedrive/onedrive_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/onedrive/onedrive_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/microsoft/microsoft_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/microsoft/microsoft_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/microsoft/microsoft_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/microsoft/microsoft_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/openai/openai_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/openai/openai_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/openai/openai_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/openai/openai_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/anthropic/anthropic_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/anthropic/anthropic_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/anthropic/anthropic_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/anthropic/anthropic_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/discord/discord_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/discord/discord_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/discord/discord_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/discord/discord_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/aliyun/aliyun_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/aliyun/aliyun_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/aliyun/aliyun_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/aliyun/aliyun_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cloudflare/cloudflare_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cloudflare/cloudflare_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cloudflare/cloudflare_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cloudflare/cloudflare_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/docker/docker_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/docker/docker_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/docker/docker_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/docker/docker_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/homebrew/homebrew_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/homebrew/homebrew_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/homebrew/homebrew_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/homebrew/homebrew_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/python/python_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/python/python_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/python/python_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/python/python_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/icloud/icloud_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/icloud/icloud_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/icloud/icloud_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/icloud/icloud_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/apple/apple_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/apple/apple_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/apple/apple_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/apple/apple_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/youtube/youtube_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/youtube/youtube_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/youtube/youtube_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/youtube/youtube_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitch/twitch_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitch/twitch_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitch/twitch_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitch/twitch_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/niconico/niconico_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/niconico/niconico_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/niconico/niconico_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/niconico/niconico_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/pixiv/pixiv_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/pixiv/pixiv_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/pixiv/pixiv_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/pixiv/pixiv_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/disney/disney_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/disney/disney_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/disney/disney_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/disney/disney_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/bilibili/bilibili_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/bilibili/bilibili_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/bilibili/bilibili_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/bilibili/bilibili_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/spotify/spotify_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/spotify/spotify_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/spotify/spotify_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/spotify/spotify_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/dmm/dmm_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/dmm/dmm_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/dmm/dmm_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/dmm/dmm_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_ip.mrs">MRS · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_ip.yaml">YAML · 仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_ip.mrs">MRS · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_ip.yaml">YAML · 仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gfw/gfw_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gfw/gfw_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gfw/gfw_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gfw/gfw_domain.yaml">YAML · 仅域名</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/loyalsoldier/applications/applications_process.yaml">YAML · 仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/loyalsoldier/applications/applications_process.yaml">YAML · 仅进程</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cn/cn_domain.mrs">MRS · 仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cn/cn_domain.yaml">YAML · 仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cn/cn_domain.mrs">MRS · 仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cn/cn_domain.yaml">YAML · 仅域名</a></td>
  </tr>
</table>

### 适用于 Surge 内核 - 选择您的类型

Domain 文件使用 `DOMAIN-SET`，其他类型使用 `RULE-SET`。原有 IP 转换产物添加 `no-resolve`，拆分出的 Surge IP 文件保留上游选项。下表只列出上游实际包含规则的分类；没有规则的分类不生成文件。上游新增分类或删除某类全部规则时，同步更新分类文件、下方链接和仓库内的 Surge 示例配置。

<table>
  <tr align="center">
    <td><b>类型</b></td>
    <td><b>通过原始链接以查看或下载</b></td>
    <td><b>通过镜像链接以查看或下载</b></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/private/private_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/private/private_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/private/private_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/private/private_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/copilot/copilot_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/copilot/copilot_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/copilot/copilot_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/copilot/copilot_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/adobe-activation/adobe-activation_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/adobe-activation/adobe-activation_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/googlefcm/googlefcm_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/googlefcm/googlefcm_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/z-library/z-library_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/z-library/z-library_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitter/twitter_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitter/twitter_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitter/twitter_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitter/twitter_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/github/github_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/github/github_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/onedrive/onedrive_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/onedrive/onedrive_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/microsoft/microsoft_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/microsoft/microsoft_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/openai/openai_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/openai/openai_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/anthropic/anthropic_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/anthropic/anthropic_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/discord/discord_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/discord/discord_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/docker/docker_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/docker/docker_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/icloud/icloud_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/icloud/icloud_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/apple/apple_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/apple/apple_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/youtube/youtube_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/youtube/youtube_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/google/google_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/google/google_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/google/google_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/google/google_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitch/twitch_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitch/twitch_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/niconico/niconico_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/niconico/niconico_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/pixiv/pixiv_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/pixiv/pixiv_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/netflix/netflix_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/netflix/netflix_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/netflix/netflix_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/netflix/netflix_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/disney/disney_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/disney/disney_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/bilibili/bilibili_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/bilibili/bilibili_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/spotify/spotify_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/spotify/spotify_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/dmm/dmm_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/dmm/dmm_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/telegram/telegram_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/telegram/telegram_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/telegram/telegram_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/telegram/telegram_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/gfw/gfw_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/gfw/gfw_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/applications/applications_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/applications/applications_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/cn/cn_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/cn/cn_domain.list">仅域名</a></td>
  </tr>
<!-- synced-surge-rules:begin -->
  <tr align="center">
    <td>CatsTeam_AdRules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/cats-team/adrules/adrules_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/cats-team/adrules/adrules_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Lan</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/lan/lan_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/lan/lan_ip.list">仅 IP</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/lan/lan_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/lan/lan_ip.list">仅 IP</a></td>
  </tr>
  <tr align="center">
    <td>RuleForOCD_Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/steam/steam_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/steam/steam_keyword.list">仅关键词</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/steam/steam_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/steam/steam_keyword.list">仅关键词</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_AdobeActivation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_ip.list">仅 IP</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_ip.list">仅 IP</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_GoogleFCM</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/googlefcm/googlefcm_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/googlefcm/googlefcm_ip.list">仅 IP</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/googlefcm/googlefcm_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/googlefcm/googlefcm_ip.list">仅 IP</a></td>
  </tr>
  <tr align="center">
    <td>Geosite2Surge_z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/coderbean/z-library/z-library_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/coderbean/z-library/z-library_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/linuxdo/linuxdo_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/linuxdo/linuxdo_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_ip.list">仅 IP</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_ip.list">仅 IP</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Claude</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/claude/claude_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/claude/claude_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_OpenAI</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_asn.list">仅 ASN</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_asn.list">仅 ASN</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_asn.list">仅 ASN</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_asn.list">仅 ASN</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/google-gemini/google-gemini_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/google-gemini/google-gemini_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_GitHub</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/github/github_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/github/github_keyword.list">仅关键词</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/github/github_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/github/github_keyword.list">仅关键词</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/gitlab/gitlab_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/gitlab/gitlab_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_OneDrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/discord/discord_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/discord/discord_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/aliyun/aliyun_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/aliyun/aliyun_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/cloudflare/cloudflare_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/cloudflare/cloudflare_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/docker/docker_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/docker/docker_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/homebrew/homebrew_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/homebrew/homebrew_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/python/python_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/python/python_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_iCloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/icloud/icloud_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/icloud/icloud_keyword.list">仅关键词</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/icloud/icloud_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/icloud/icloud_keyword.list">仅关键词</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_AppleDomain</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_domainset.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_domainset.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_YouTube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_useragent.list">仅 User-Agent</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_useragent.list">仅 User-Agent</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/niconico/niconico_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/niconico/niconico_useragent.list">仅 User-Agent</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/niconico/niconico_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/niconico/niconico_useragent.list">仅 User-Agent</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/pixiv/pixiv_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/pixiv/pixiv_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_BiliBili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_useragent.list">仅 User-Agent</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_process.list">仅进程</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_useragent.list">仅 User-Agent</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_process.list">仅进程</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_DMM</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/dmm/dmm_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/dmm/dmm_ip.list">仅 IP</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/dmm/dmm_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/dmm/dmm_ip.list">仅 IP</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_domain.list">仅域名</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_keyword.list">仅关键词</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_ip.list">仅 IP</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_asn.list">仅 ASN</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_process.list">仅进程</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_logical.list">仅逻辑规则</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_domain.list">仅域名</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_keyword.list">仅关键词</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_ip.list">仅 IP</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_asn.list">仅 ASN</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_process.list">仅进程</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_logical.list">仅逻辑规则</a></td>
  </tr>
  <tr align="center">
    <td>Loyalsoldier_gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/gfw/gfw_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/gfw/gfw_domain.list">仅域名</a></td>
  </tr>
  <tr align="center">
    <td>Loyalsoldier_direct</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/direct/direct_domain.list">仅域名</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/direct/direct_domain.list">仅域名</a></td>
  </tr>
<!-- synced-surge-rules:end -->
</table>
