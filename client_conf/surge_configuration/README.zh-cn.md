# surge_configuration

**语言选择：[English](README.md) | 简体中文**

如果发现问题或有改进建议，请在本仓库的 [Issues](https://github.com/Lolicandae/blacklist-rules/issues) 中反馈。

## 说明

此文件主要用于代理以下内容：

- 受您可能知晓的非法防火墙屏蔽的已知 IP 或域名；
- 当前所在地区尚不可用的部分应用服务；
- 由于当前 ISP 提供的互联网连接缓慢，长时间无法完整加载全部资源的部分应用服务。

## 配置订阅

<table>
  <tr align="center">
    <td>
      <b>类型</b>
    </td>
    <td>
      <b>原始链接</b>
    </td>
    <td>
      <b>镜像链接</b>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="surge_configuration.conf">surge_configuration.conf</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/client_conf/surge_configuration/surge_configuration.conf">CONF</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/client_conf/surge_configuration/surge_configuration.conf">CONF</a>
    </td>
  </tr>
</table>

## 关于“代理组”

- 节点选择组
  - `Proxy`：主开关。请先选择一种模式，以访问大多数受防火墙屏蔽的 IP 或域名。
  - `All Nodes`：显示订阅中的全部节点，可直接选择节点，也可选择其他 `[Region] Nodes` 中的节点。
  - `HK/TW/JP/US/SG/UK Nodes`：仅显示对应地区的订阅节点；也可在 `All Nodes` 或其他 `[Region] Nodes` 中选择节点。
  - `Minimum delay`：自动选择 `All Nodes` 中延迟最低的节点。
  - `Fallback`：按节点顺序使用 `All Nodes` 中第一个可用节点；当前节点不可用时，自动切换到其他可用节点。
  - `Load Balancing (Hashing)`：将目标地址相同的请求分配到 `All Nodes` 中的同一代理节点。
  - `Load Balancing (Round Robin)`：将所有请求轮流分配到 `All Nodes` 中的不同代理节点。
- 通讯
  - `Discord`：包含文本、图片和游戏资源，不包含语音频道服务；默认为 `Proxy`。
  - `Telegram`：默认为 `Proxy`。
- AI
  - `ChatGPT`：默认为 `Proxy`。
  - `Claude`：默认为 `Proxy`。
  - `Copilot`：默认为 `DIRECT`。注意：若在此代理组中选择代理节点，`www.bing.com` 也会被代理，这会影响使用 Bing 搜索引擎时的体验。
  - `Gemini`：默认为 `Proxy`。
- 媒体
  - `Bilibili`：默认为 `DIRECT`。
  - `Disney`：默认为 `Proxy`。
  - `DMM`：默认为 `Proxy`。
  - `Netflix`：默认为 `Proxy`。
  - `Niconico`：默认为 `Proxy`。
  - `Pixiv`：默认为 `Proxy`。
  - `Spotify`：默认为 `Proxy`。
  - `Twitch`：默认为 `Proxy`。
  - `Youtube`：默认为 `Proxy`。
  - `Z-Library`：默认为 `Proxy`。
- 社交
  - `Bluesky`：默认为 `Proxy`。
  - `LINUX DO`：默认为 `Proxy`。
  - `Twitter`：默认为 `Proxy`。
- 云存储
  - `iCloud`：默认为 `DIRECT`。
  - `OneDrive`：默认为 `DIRECT`。
- 技术服务
  - `Aliyun`：默认为 `DIRECT`。
  - `Cloudflare`：默认为 `DIRECT`。
  - `Docker`：默认为 `DIRECT`。
  - `Homebrew`：默认为 `DIRECT`。
  - `Python`：默认为 `DIRECT`。
  - `GitHub`：默认为 `Proxy`。
  - `GitLab`：默认为 `Proxy`。
- 服务提供商
  - `Apple`：默认为 `DIRECT`。
  - `Google`：默认为 `Proxy`。
  - `Microsoft`：默认为 `DIRECT`。
- 其他代理组
  - `Steam`：默认为 `DIRECT`。
  - `Adobe Activation Service`：默认为 `REJECT`。如果您使用的是正版 Adobe 软件，可选择 `DIRECT` 模式。
  - `AdBlock`：用于阻止跟踪连接和广告；默认为 `REJECT`。
  - `Domestic`：包含中国大陆域名和 IP；默认为 `DIRECT`。
  - `Game Boosting`：加速部分无法通过当前 ISP 稳定联网的游戏；默认为 `DIRECT`。
  - `Game Unlocking`：解锁部分未向某些地区提供服务的游戏；默认为 `Proxy`。
  - `Google FCM`：默认为 `Proxy`。
  - `Others`：默认为 `DIRECT`。若在此代理组中选择代理模式，将代理未被上述代理组列出的全部服务，但不会影响国内连接。
  - `Safe Browse`：默认为 `Proxy`。
