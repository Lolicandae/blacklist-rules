# mihomo_override

**Select your Language: English | [简体中文](README.zh-cn.md)**

Please report problems or share suggestions in this repository's [Issues](https://github.com/Lolicandae/blacklist-rules/issues).

## Note

This file is mainly designed to proxy these following:

- Known IPs or domain that banned by the illegal Firewall you may know;
- Some application service that not available yet at your current region.
- Due to slow connection of some application service in current Internet provided by your ISP, cannot load all resources successfully for a long time.

## Script subscriptions

<table>
  <tr align="center">
    <td>
      <b>TYPE</b>
    </td>
    <td>
      <b>Original links</b>
    </td>
    <td>
      <b>CDN links</b>
    </td>
  </tr>
  <tr align="center">
    <td>
      <a href="mihomo_override.js">mihomo_override.js</a>
    </td>
    <td>
      <a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/client_conf/mihomo_override/mihomo_override.js">JavaScript</a>
    </td>
    <td>
      <a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/client_conf/mihomo_override/mihomo_override.js">JavaScript</a>
    </td>
  </tr>
</table>

## About "Proxy Groups"

- Node selection Groups
  - `Proxy`: Your main switch, choose a mode first to access most of IPs or domains that banned by the Firewall.
  - `All Nodes`: You can see all nodes of subscription(s), choose a node (or choose a node in other `[Region] Nodes`).
  - `HK/TW/JP/US/SG/UK Nodes`: You only can see HK/TW/JP/US/SG/UK nodes of subscription(s), choose a node (otherwise, choose a node in `All Nodes` or other `[Region] Nodes`).
  - `Minimum delay`: Automatically choose a node which has a minimum delay in `All Nodes`.
  - `Fallback`: Uses the first available node in `All Nodes`, following the node order. Automatically switches to another available node if the current one fails.
  - `Load Balancing (Hashing)`: It will assign requests with the same target address to the same proxy node within `All Nodes`.
  - `Load Balancing (Round Robin)`: It will distribute all requests among different proxy nodes within `All Nodes`.
- Contact
  - `Discord`: Include text, picture and game resources, exclude voice channel service. `Proxy` in default.
  - `Telegram`: `Proxy` in default.
- AI
  - `ChatGPT`: `Proxy` in default.
  - `Claude`: `Proxy` in default.
  - `Copilot`: `DIRECT` in default. Attention, if you choose proxy mode node in this proxy group, `www.bing.com` will be proxied. It will affect your experience when you search something in bing search engine.
  - `Gemini`: `Proxy` in default.
- Media
  - `Bilibili`: `DIRECT` in default.
  - `Disney`: `Proxy` in default.
  - `DMM`: `Proxy` in default.
  - `Netflix`: `Proxy` in default.
  - `Niconico`: `Proxy` in default.
  - `Pixiv`: `Proxy` in default.
  - `Spotify`: `Proxy` in default.
  - `Twitch`: `Proxy` in default.
  - `Youtube`: `Proxy` in default.
  - `Z-Library`: `Proxy` in default.
- Social
  - `Bluesky`: `Proxy` in default.
  - `LINUX DO`: `Proxy` in default.
  - `Twitter`: `Proxy` in default.
- Cloud Storage
  - `iCloud`: `DIRECT` in default.
  - `OneDrive`: `DIRECT` in default.
- Tech
  - `Aliyun`: `DIRECT` in default.
  - `Cloudflare`: `DIRECT` in default.
  - `Docker`: `DIRECT` in default.
  - `Homebrew`: `DIRECT` in default.
  - `Python`: `DIRECT` in default.
  - `GitHub`: `Proxy` in default.
  - `GitLab`: `Proxy` in default.
- Services Provider
  - `Apple`: `DIRECT` in default.
  - `Google`: `Proxy` in default.
  - `Microsoft`: `DIRECT` in default.
- Other Groups
  - `Steam`: `DIRECT` in default.
  - `Canva`: `Proxy` in default.
  - `Adobe Activation Service`: `REJECT` in default. You can choose `DIRECT` mode if you're using truly licensed Adobe software.
  - `AdBlock`: It will block spy connections and advertisements. `REJECT` in default.
  - `Domestic`: Include CN domains & IPs. `DIRECT` in default.
  - `Game Boosting`: Boost some game that may not stably connect to the internet provided by your ISP. `DIRECT` in default.
  - `Game Unlocking`: Unlock some game that not serve for some regions. `Proxy` in default.
  - `Google FCM`: `Proxy` in default.
  - `Others`: `DIRECT` in default. If you choose proxy mode in this proxy group, it will proxy all services that are not listed in above proxy groups. It won't affect domestic connections.
  - `Safe Browse`: `Proxy` in default.
