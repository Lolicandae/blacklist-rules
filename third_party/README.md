# Third-Party Rules

**Select your Language: English | [简体中文](README.zh-cn.md)**

## Introduction

Synchronizes a fixed list of upstream files and separates their rules by type, including Domain, IP, Keyword, Process, ASN, UserAgent and Logical. Rules are grouped into author and service directories with lowercase filenames. Custom rules remain in the existing `artifact/` directories.

**Usage**: Choose a rule link for your client from the tables below, then assign a routing policy in your client configuration, such as direct, proxy or reject. Rule files contain only matching conditions; your client configuration determines how matching traffic is handled. This repository regularly synchronizes third-party rule content from upstream.

**Update frequency**: one scheduled sync per day, at **03:23** Hong Kong time (UTC+8, the same as Beijing time), corresponding to **19:23 UTC on the previous day**.

The schedule takes effect after the [workflow](../.github/workflows/sync-third-party-rules.yml) is published to `main`. 03:23 is the scheduled trigger time; [GitHub Actions scheduling can be delayed](https://docs.github.com/en/actions/how-tos/troubleshoot-workflows#scheduled-workflows-running-at-unexpected-times). Check the Actions run history for actual start and completion times; updated rule files are not guaranteed to be available at 03:23.

## Repository Maintenance

The sync inventory is fixed in `UPSTREAM_RULES` in `workflow_scripts/sync_third_party_rules.py`; it is not read from client profiles. Each entry specifies its upstream URL, input type and output name. Edit this list to change the sync scope. `third_party/sources.json` records each download and its output paths. The workflow converts Domain/IP/Process sources into Clash YAML, Surge and sing-box formats, and copies upstream MRS files unchanged. When the same repository and service already provide Surge rules, the upstream Surge file is used without generating another converted copy. Mihomo validates the MRS files. Set `MIHOMO_BIN` to the core executable when running the sync script locally; the workflow already configures it. Surge sources are split into separate files for every matching type, retaining Surge-specific syntax, and appear in the Surge table below. Different upstreams are stored and updated separately. Unsupported rules fail validation rather than being silently omitted. License files remain fixed copies and are maintained through manual review.

Successful syncs use the current upstream content and remove rules deleted upstream. If an upstream repository or file returns HTTP 404/410, its existing files and last successful source record remain unchanged while other sources continue syncing. A missing source without a matching local copy, other download failures, or invalid content prevent publication and preserve the previously published files. All available sources are validated before outputs are updated. Unchanged contents create no commit. Run Sync Third-Party Rules manually from Actions when needed.

Files are generated only for categories that contain upstream rules. When a category has no rules, its files, download links and references in the example profiles are removed. A fixed list specifies which upstream files to sync; client profiles are read only to update references.

## Third-Party Licenses

Rules retain their upstream copyright and license terms; this repository does not replace those terms. See [NOTICE.md](NOTICE.md) and [licenses/](licenses/) for complete notices and original texts. AdRules aggregates multiple sources; its 0BSD script license does not license all rule data. Entries without a stated license retain the upstream declaration.

## Related documents and links

**Note**: CDN links can lag because of caching. Use the original links for the latest files.

### For sing-box Kernel - Choose your TYPE

Remote rule sets use the original URL with `type: remote` and `format: source`. The applications provider contains process rules and requires an environment that supports process identification.

<table>
  <tr align="center">
    <td><b>TYPE</b></td>
    <td><b>View or Download by an Original Link</b></td>
    <td><b>View or Download by a CDN Link</b></td>
  </tr>
  <tr align="center">
    <td>adrules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/cats-team/adrules/adrules_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/cats-team/adrules/adrules_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/private/private_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/private/private_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/private/private_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/private/private_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/steam/steam_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/steam/steam_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>canva</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/canva/canva_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/canva/canva_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/copilot/copilot_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/copilot/copilot_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/copilot/copilot_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/copilot/copilot_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/google-gemini/google-gemini_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/google-gemini/google-gemini_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/adobe-activation/adobe-activation_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/adobe-activation/adobe-activation_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/googlefcm/googlefcm_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/googlefcm/googlefcm_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/z-library/z-library_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/z-library/z-library_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/linuxdo/linuxdo_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/linuxdo/linuxdo_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitter/twitter_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitter/twitter_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitter/twitter_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitter/twitter_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/github/github_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/github/github_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/gitlab/gitlab_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/gitlab/gitlab_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/onedrive/onedrive_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/onedrive/onedrive_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/microsoft/microsoft_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/microsoft/microsoft_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/openai/openai_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/openai/openai_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/anthropic/anthropic_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/anthropic/anthropic_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/discord/discord_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/discord/discord_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/aliyun/aliyun_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/aliyun/aliyun_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/cloudflare/cloudflare_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/cloudflare/cloudflare_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/docker/docker_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/docker/docker_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/homebrew/homebrew_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/homebrew/homebrew_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/python/python_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/python/python_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/icloud/icloud_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/icloud/icloud_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/apple/apple_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/apple/apple_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/youtube/youtube_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/youtube/youtube_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/google/google_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/google/google_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/google/google_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/google/google_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/twitch/twitch_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/twitch/twitch_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/niconico/niconico_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/niconico/niconico_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/pixiv/pixiv_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/pixiv/pixiv_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/netflix/netflix_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/netflix/netflix_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/netflix/netflix_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/netflix/netflix_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/disney/disney_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/disney/disney_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/bilibili/bilibili_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/bilibili/bilibili_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/spotify/spotify_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/spotify/spotify_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/dmm/dmm_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/dmm/dmm_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/telegram/telegram_ip.json">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/peiyingyao/telegram/telegram_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/telegram/telegram_ip.json">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/peiyingyao/telegram/telegram_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/gfw/gfw_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/gfw/gfw_domain.json">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/loyalsoldier/applications/applications_process.json">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/loyalsoldier/applications/applications_process.json">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/sing-box/metacubex/cn/cn_domain.json">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/sing-box/metacubex/cn/cn_domain.json">Domain Only</a></td>
  </tr>
</table>

### For Clash Kernel - Choose your TYPE

Use `behavior: domain` for Domain files, `behavior: ipcidr` for IP files and `behavior: classical` for applications. Set `format: mrs` for MRS files and `format: yaml` for YAML files. MRS supports Mihomo Domain and IP rules; Process rules use YAML.

MRS and YAML files share `clash/author/service/` directories, for example `clash/peiyingyao/steam/steam_domain.mrs`.

<table>
  <tr align="center">
    <td><b>TYPE</b></td>
    <td><b>View or Download by an Original Link</b></td>
    <td><b>View or Download by a CDN Link</b></td>
  </tr>
  <tr align="center">
    <td>adrules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/cats-team/adrules/adrules_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/cats-team/adrules/adrules_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/cats-team/adrules/adrules_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/cats-team/adrules/adrules_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/private/private_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/private/private_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/steam/steam_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/steam/steam_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/steam/steam_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/steam/steam_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>canva</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/canva/canva_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/canva/canva_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/canva/canva_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/canva/canva_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/copilot/copilot_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/copilot/copilot_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/google-gemini/google-gemini_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/google-gemini/google-gemini_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/google-gemini/google-gemini_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/google-gemini/google-gemini_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/adobe-activation/adobe-activation_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/googlefcm/googlefcm_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/googlefcm/googlefcm_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/googlefcm/googlefcm_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/googlefcm/googlefcm_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/z-library/z-library_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/z-library/z-library_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/z-library/z-library_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/z-library/z-library_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/linuxdo/linuxdo_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/linuxdo/linuxdo_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/linuxdo/linuxdo_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/linuxdo/linuxdo_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitter/twitter_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitter/twitter_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/github/github_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/github/github_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/github/github_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/github/github_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gitlab/gitlab_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gitlab/gitlab_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gitlab/gitlab_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gitlab/gitlab_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/onedrive/onedrive_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/onedrive/onedrive_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/onedrive/onedrive_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/onedrive/onedrive_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/microsoft/microsoft_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/microsoft/microsoft_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/microsoft/microsoft_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/microsoft/microsoft_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/openai/openai_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/openai/openai_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/openai/openai_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/openai/openai_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/anthropic/anthropic_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/anthropic/anthropic_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/anthropic/anthropic_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/anthropic/anthropic_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/discord/discord_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/discord/discord_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/discord/discord_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/discord/discord_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/aliyun/aliyun_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/aliyun/aliyun_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/aliyun/aliyun_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/aliyun/aliyun_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cloudflare/cloudflare_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cloudflare/cloudflare_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cloudflare/cloudflare_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cloudflare/cloudflare_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/docker/docker_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/docker/docker_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/docker/docker_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/docker/docker_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/homebrew/homebrew_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/homebrew/homebrew_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/homebrew/homebrew_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/homebrew/homebrew_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/python/python_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/python/python_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/python/python_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/python/python_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/icloud/icloud_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/icloud/icloud_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/icloud/icloud_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/icloud/icloud_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/apple/apple_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/apple/apple_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/apple/apple_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/apple/apple_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/youtube/youtube_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/youtube/youtube_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/youtube/youtube_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/youtube/youtube_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/google/google_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/google/google_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitch/twitch_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/twitch/twitch_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitch/twitch_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/twitch/twitch_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/niconico/niconico_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/niconico/niconico_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/niconico/niconico_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/niconico/niconico_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/pixiv/pixiv_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/pixiv/pixiv_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/pixiv/pixiv_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/pixiv/pixiv_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/netflix/netflix_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/netflix/netflix_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/disney/disney_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/disney/disney_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/disney/disney_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/disney/disney_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/bilibili/bilibili_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/bilibili/bilibili_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/bilibili/bilibili_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/bilibili/bilibili_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/spotify/spotify_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/spotify/spotify_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/spotify/spotify_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/spotify/spotify_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/dmm/dmm_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/dmm/dmm_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/dmm/dmm_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/dmm/dmm_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_ip.mrs">MRS · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_ip.yaml">YAML · IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/peiyingyao/telegram/telegram_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_ip.mrs">MRS · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_ip.yaml">YAML · IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/peiyingyao/telegram/telegram_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gfw/gfw_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/gfw/gfw_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gfw/gfw_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/gfw/gfw_domain.yaml">YAML · Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/loyalsoldier/applications/applications_process.yaml">YAML · Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/loyalsoldier/applications/applications_process.yaml">YAML · Process Only</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cn/cn_domain.mrs">MRS · Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/clash/metacubex/cn/cn_domain.yaml">YAML · Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cn/cn_domain.mrs">MRS · Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/clash/metacubex/cn/cn_domain.yaml">YAML · Domain Only</a></td>
  </tr>
</table>

### For Surge Kernel - Choose your TYPE

Use `DOMAIN-SET` for Domain files and `RULE-SET` for the other types. Existing IP conversions add `no-resolve`; split Surge IP files preserve upstream options. The table lists only categories that contain upstream rules; empty categories produce no files. When upstream adds a category or removes its last rule, the sync updates the category files, links below and the repository's Surge example profile.

<table>
  <tr align="center">
    <td><b>TYPE</b></td>
    <td><b>View or Download by an Original Link</b></td>
    <td><b>View or Download by a CDN Link</b></td>
  </tr>
  <tr align="center">
    <td>private</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/private/private_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/private/private_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/private/private_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/private/private_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/copilot/copilot_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/copilot/copilot_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/copilot/copilot_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/copilot/copilot_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>adobe-activation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/adobe-activation/adobe-activation_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/adobe-activation/adobe-activation_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>googlefcm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/googlefcm/googlefcm_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/googlefcm/googlefcm_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/z-library/z-library_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/z-library/z-library_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitter/twitter_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitter/twitter_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitter/twitter_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitter/twitter_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>github</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/github/github_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/github/github_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>onedrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/onedrive/onedrive_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/onedrive/onedrive_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/microsoft/microsoft_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/microsoft/microsoft_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>openai</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/openai/openai_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/openai/openai_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>anthropic</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/anthropic/anthropic_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/anthropic/anthropic_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/discord/discord_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/discord/discord_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/docker/docker_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/docker/docker_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>icloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/icloud/icloud_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/icloud/icloud_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/apple/apple_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/apple/apple_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>youtube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/youtube/youtube_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/youtube/youtube_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/google/google_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/google/google_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/google/google_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/google/google_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/twitch/twitch_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/twitch/twitch_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/niconico/niconico_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/niconico/niconico_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/pixiv/pixiv_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/pixiv/pixiv_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/netflix/netflix_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/netflix/netflix_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/netflix/netflix_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/netflix/netflix_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/disney/disney_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/disney/disney_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>bilibili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/bilibili/bilibili_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/bilibili/bilibili_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/spotify/spotify_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/spotify/spotify_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>dmm</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/dmm/dmm_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/dmm/dmm_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/telegram/telegram_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/telegram/telegram_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/telegram/telegram_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/telegram/telegram_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/gfw/gfw_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/gfw/gfw_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>applications</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/applications/applications_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/applications/applications_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>cn</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/cn/cn_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/cn/cn_domain.list">Domain Only</a></td>
  </tr>
<!-- synced-surge-rules:begin -->
  <tr align="center">
    <td>CatsTeam_AdRules</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/cats-team/adrules/adrules_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/cats-team/adrules/adrules_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Lan</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/lan/lan_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/lan/lan_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/lan/lan_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/lan/lan_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>RuleForOCD_Steam</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/steam/steam_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/steam/steam_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/peiyingyao/steam/steam_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/steam/steam_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/steam/steam_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/peiyingyao/steam/steam_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_canva</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/canva/canva_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/canva/canva_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_AdobeActivation</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/adobeactivation/adobeactivation_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_GoogleFCM</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/googlefcm/googlefcm_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/googlefcm/googlefcm_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/googlefcm/googlefcm_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/googlefcm/googlefcm_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>Geosite2Surge_z-library</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/coderbean/z-library/z-library_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/coderbean/z-library/z-library_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_linuxdo</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/linuxdo/linuxdo_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/linuxdo/linuxdo_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Twitter</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitter/twitter_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitter/twitter_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Claude</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/claude/claude_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/claude/claude_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_OpenAI</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/openai/openai_asn.list">ASN Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/openai/openai_asn.list">ASN Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Copilot</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/copilot/copilot_asn.list">ASN Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/copilot/copilot_asn.list">ASN Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_google-gemini</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/google-gemini/google-gemini_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/google-gemini/google-gemini_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_GitHub</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/github/github_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/github/github_keyword.list">Keyword Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/github/github_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/github/github_keyword.list">Keyword Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_gitlab</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/gitlab/gitlab_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/gitlab/gitlab_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_OneDrive</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/onedrive/onedrive_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/onedrive/onedrive_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Microsoft</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/microsoft/microsoft_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/microsoft/microsoft_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Discord</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/discord/discord_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/discord/discord_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_aliyun</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/aliyun/aliyun_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/aliyun/aliyun_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_cloudflare</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/cloudflare/cloudflare_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/cloudflare/cloudflare_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Docker</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/docker/docker_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/docker/docker_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_homebrew</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/homebrew/homebrew_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/homebrew/homebrew_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>MetaCubeX_python</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/metacubex/python/python_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/metacubex/python/python_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_iCloud</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/icloud/icloud_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/icloud/icloud_keyword.list">Keyword Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/icloud/icloud_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/icloud/icloud_keyword.list">Keyword Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_AppleDomain</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_domainset.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_domainset.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Apple</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/apple/apple_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/apple/apple_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_YouTube</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/youtube/youtube_useragent.list">User-Agent Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/youtube/youtube_useragent.list">User-Agent Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Google</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/google/google_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/google/google_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Twitch</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/twitch/twitch_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/twitch/twitch_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Niconico</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/niconico/niconico_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/niconico/niconico_useragent.list">User-Agent Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/niconico/niconico_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/niconico/niconico_useragent.list">User-Agent Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Pixiv</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/pixiv/pixiv_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/pixiv/pixiv_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Netflix</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/netflix/netflix_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/netflix/netflix_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Disney</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/disney/disney_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/disney/disney_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_BiliBili</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/bilibili/bilibili_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/bilibili/bilibili_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Spotify</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_useragent.list">User-Agent Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/spotify/spotify_process.list">Process Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_useragent.list">User-Agent Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/spotify/spotify_process.list">Process Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_DMM</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/dmm/dmm_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/dmm/dmm_ip.list">IP Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/dmm/dmm_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/dmm/dmm_ip.list">IP Only</a></td>
  </tr>
  <tr align="center">
    <td>Blackmatrix7_Telegram</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_domain.list">Domain Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_keyword.list">Keyword Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_ip.list">IP Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_asn.list">ASN Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_process.list">Process Only</a><br><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/blackmatrix7/telegram/telegram_logical.list">Logical Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_domain.list">Domain Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_keyword.list">Keyword Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_ip.list">IP Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_asn.list">ASN Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_process.list">Process Only</a><br><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/blackmatrix7/telegram/telegram_logical.list">Logical Only</a></td>
  </tr>
  <tr align="center">
    <td>Loyalsoldier_gfw</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/gfw/gfw_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/gfw/gfw_domain.list">Domain Only</a></td>
  </tr>
  <tr align="center">
    <td>Loyalsoldier_direct</td>
    <td><a href="https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/surge/loyalsoldier/direct/direct_domain.list">Domain Only</a></td>
    <td><a href="https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/surge/loyalsoldier/direct/direct_domain.list">Domain Only</a></td>
  </tr>
<!-- synced-surge-rules:end -->
</table>
