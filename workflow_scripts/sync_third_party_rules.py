#!/usr/bin/env python3
"""Sync fixed upstream files and split mixed rules by matching type."""

from __future__ import annotations

import argparse
import base64
import contextlib
import errno
import hashlib
import html
import io
import ipaddress
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from time import sleep
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from build_rules import BuildError, Rule, render_items, render_json_rules, self_check


ROOT = Path(__file__).resolve().parents[1]
FORMATS = {"clash": ".yaml", "surge": ".list", "sing-box": ".json"}
SOURCE_AUTHORS = {
    "Cats-Team/AdRules": "cats-team",
    "MetaCubeX/meta-rules-dat": "metacubex",
    "peiyingyao/Rule-for-OCD": "peiyingyao",
    "Loyalsoldier/clash-rules": "loyalsoldier",
    "Loyalsoldier/surge-rules": "loyalsoldier",
    "blackmatrix7/ios_rule_script": "blackmatrix7",
    "coderbean/geosite2surge": "coderbean",
}


UPSTREAM_RULES: dict[str, tuple[str, str, str]] = {
    "adrules": ("adrules_Domain", "https://raw.githubusercontent.com/Cats-Team/AdRules/main/adrules_domainset.txt", "Domain"),
    "private_ip": ("private_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/private.yaml", "IP"),
    "private_domain": ("private_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/private.yaml", "Domain"),
    "steam": ("Steam_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Steam/Steam_OCD_Domain.txt", "Domain"),
    "copilot_ip": ("Copilot_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Copilot/Copilot_OCD_IP.txt", "IP"),
    "copilot_domain": ("Copilot_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Copilot/Copilot_OCD_Domain.txt", "Domain"),
    "gemini": ("google-gemini_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google-gemini.yaml", "Domain"),
    "adobeactivation": ("adobe-activation_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/adobe-activation.yaml", "Domain"),
    "googlefcm": ("googlefcm_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/googlefcm.yaml", "Domain"),
    "z-library": ("z-library_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/z-library.yaml", "Domain"),
    "linuxdo": ("linuxdo_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/linuxdo.yaml", "Domain"),
    "twitter_ip": ("twitter_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/twitter.yaml", "IP"),
    "twitter_domain": ("twitter_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitter.yaml", "Domain"),
    "github": ("github_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/github.yaml", "Domain"),
    "gitlab": ("gitlab_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gitlab.yaml", "Domain"),
    "onedrive": ("onedrive_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/onedrive.yaml", "Domain"),
    "microsoft": ("Microsoft_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Microsoft/Microsoft_OCD_Domain.txt", "Domain"),
    "openai": ("openai_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.yaml", "Domain"),
    "anthropic": ("anthropic_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/anthropic.yaml", "Domain"),
    "discord": ("discord_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/discord.yaml", "Domain"),
    "aliyun": ("aliyun_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/aliyun.yaml", "Domain"),
    "cloudflare": ("cloudflare_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cloudflare.yaml", "Domain"),
    "docker": ("docker_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/docker.yaml", "Domain"),
    "homebrew": ("homebrew_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/homebrew.yaml", "Domain"),
    "python": ("python_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/python.yaml", "Domain"),
    "icloud": ("icloud_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/icloud.yaml", "Domain"),
    "apple": ("apple_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/apple.yaml", "Domain"),
    "youtube": ("youtube_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.yaml", "Domain"),
    "google_ip": ("Google_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Google/Google_OCD_IP.txt", "IP"),
    "google_domain": ("Google_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Google/Google_OCD_Domain.txt", "Domain"),
    "twitch": ("twitch_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitch.yaml", "Domain"),
    "niconico": ("niconico_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/niconico.yaml", "Domain"),
    "pixiv": ("Pixiv_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Pixiv/Pixiv_OCD_Domain.txt", "Domain"),
    "netflix_ip": ("netflix_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/netflix.yaml", "IP"),
    "netflix_domain": ("netflix_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/netflix.yaml", "Domain"),
    "disney": ("disney_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/disney.yaml", "Domain"),
    "bilibili": ("bilibili_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/bilibili.yaml", "Domain"),
    "spotify": ("spotify_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/spotify.yaml", "Domain"),
    "dmm": ("dmm_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/dmm.yaml", "Domain"),
    "telegram_ip": ("Telegram_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Telegram/Telegram_OCD_IP.txt", "IP"),
    "telegram_domain": ("Telegram_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Telegram/Telegram_OCD_Domain.txt", "Domain"),
    "gfw": ("gfw_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gfw.yaml", "Domain"),
    "applications": ("applications", "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/applications.txt", "Process"),
    "cn_domain": ("cn_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.yaml", "Domain"),
    "surge_adrules": ("CatsTeam_AdRules", "https://raw.githubusercontent.com/Cats-Team/AdRules/main/adrules.list", "SurgeSplit"),
    "surge_blackmatrix7_lan": ("Blackmatrix7_Lan", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Lan/Lan.list", "SurgeSplit"),
    "surge_ruleforocd_steam": ("RuleForOCD_Steam", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Surge/Steam/Steam.list", "SurgeSplit"),
    "surge_blackmatrix7_adobeactivation": ("Blackmatrix7_AdobeActivation", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AdobeActivation/AdobeActivation.list", "SurgeSplit"),
    "surge_blackmatrix7_googlefcm": ("Blackmatrix7_GoogleFCM", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/GoogleFCM/GoogleFCM.list", "SurgeSplit"),
    "surge_geosite2surge_z-library": ("Geosite2Surge_z-library", "https://raw.githubusercontent.com/coderbean/geosite2surge/main/surge-rules/z-library.list", "SurgeSplit"),
    "surge_metacubex_linuxdo": ("MetaCubeX_linuxdo", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/linuxdo.list", "DomainSet"),
    "surge_blackmatrix7_twitter": ("Blackmatrix7_Twitter", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitter/Twitter.list", "SurgeSplit"),
    "surge_blackmatrix7_claude": ("Blackmatrix7_Claude", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Claude/Claude.list", "SurgeSplit"),
    "surge_blackmatrix7_openai": ("Blackmatrix7_OpenAI", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list", "SurgeSplit"),
    "surge_blackmatrix7_copilot": ("Blackmatrix7_Copilot", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Copilot/Copilot.list", "SurgeSplit"),
    "surge_metacubex_google-gemini": ("MetaCubeX_google-gemini", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google-gemini.list", "DomainSet"),
    "surge_blackmatrix7_github": ("Blackmatrix7_GitHub", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/GitHub/GitHub.list", "SurgeSplit"),
    "surge_metacubex_gitlab": ("MetaCubeX_gitlab", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gitlab.list", "DomainSet"),
    "surge_blackmatrix7_onedrive": ("Blackmatrix7_OneDrive", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OneDrive/OneDrive.list", "SurgeSplit"),
    "surge_blackmatrix7_microsoft": ("Blackmatrix7_Microsoft", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Microsoft/Microsoft.list", "SurgeSplit"),
    "surge_blackmatrix7_discord": ("Blackmatrix7_Discord", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Discord/Discord.list", "SurgeSplit"),
    "surge_metacubex_aliyun": ("MetaCubeX_aliyun", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/aliyun.list", "DomainSet"),
    "surge_metacubex_cloudflare": ("MetaCubeX_cloudflare", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cloudflare.list", "DomainSet"),
    "surge_blackmatrix7_docker": ("Blackmatrix7_Docker", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Docker/Docker.list", "SurgeSplit"),
    "surge_metacubex_homebrew": ("MetaCubeX_homebrew", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/homebrew.list", "DomainSet"),
    "surge_metacubex_python": ("MetaCubeX_python", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/python.list", "DomainSet"),
    "surge_blackmatrix7_icloud": ("Blackmatrix7_iCloud", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/iCloud/iCloud.list", "SurgeSplit"),
    "surge_blackmatrix7_apple_domainset": ("Blackmatrix7_AppleDomain", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_Domain.list", "DomainSet"),
    "surge_blackmatrix7_apple": ("Blackmatrix7_Apple", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple.list", "SurgeSplit"),
    "surge_blackmatrix7_youtube": ("Blackmatrix7_YouTube", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/YouTube/YouTube.list", "SurgeSplit"),
    "surge_blackmatrix7_google": ("Blackmatrix7_Google", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list", "SurgeSplit"),
    "surge_blackmatrix7_twitch": ("Blackmatrix7_Twitch", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitch/Twitch.list", "SurgeSplit"),
    "surge_blackmatrix7_niconico": ("Blackmatrix7_Niconico", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Niconico/Niconico.list", "SurgeSplit"),
    "surge_blackmatrix7_pixiv": ("Blackmatrix7_Pixiv", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Pixiv/Pixiv.list", "SurgeSplit"),
    "surge_blackmatrix7_netflix": ("Blackmatrix7_Netflix", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list", "SurgeSplit"),
    "surge_blackmatrix7_disney": ("Blackmatrix7_Disney", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Disney/Disney.list", "SurgeSplit"),
    "surge_blackmatrix7_bilibili": ("Blackmatrix7_BiliBili", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/BiliBili/BiliBili.list", "SurgeSplit"),
    "surge_blackmatrix7_spotify": ("Blackmatrix7_Spotify", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Spotify/Spotify.list", "SurgeSplit"),
    "surge_blackmatrix7_dmm": ("Blackmatrix7_DMM", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/DMM/DMM.list", "SurgeSplit"),
    "surge_blackmatrix7_telegram": ("Blackmatrix7_Telegram", "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Telegram/Telegram.list", "SurgeSplit"),
    "surge_loyalsoldier_gfw": ("Loyalsoldier_gfw", "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfw.txt", "DomainSet"),
    "surge_loyalsoldier_direct": ("Loyalsoldier_direct", "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt", "DomainSet"),
}

# Fixed native binary sources; selection never depends on client profiles.
UPSTREAM_RULES.update({
    "mrs_adrules": ("adrules_Domain", "https://raw.githubusercontent.com/Cats-Team/AdRules/main/adrules-mihomo.mrs", "MrsDomain"),
    "mrs_private_ip": ("private_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/private.mrs", "MrsIP"),
    "mrs_private_domain": ("private_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/private.mrs", "MrsDomain"),
    "mrs_steam": ("Steam_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Steam/Steam_OCD_Domain.mrs", "MrsDomain"),
    "mrs_copilot_ip": ("Copilot_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Copilot/Copilot_OCD_IP.mrs", "MrsIP"),
    "mrs_copilot_domain": ("Copilot_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Copilot/Copilot_OCD_Domain.mrs", "MrsDomain"),
    "mrs_gemini": ("google-gemini_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google-gemini.mrs", "MrsDomain"),
    "mrs_adobeactivation": ("adobe-activation_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/adobe-activation.mrs", "MrsDomain"),
    "mrs_googlefcm": ("googlefcm_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/googlefcm.mrs", "MrsDomain"),
    "mrs_z-library": ("z-library_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/z-library.mrs", "MrsDomain"),
    "mrs_linuxdo": ("linuxdo_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/linuxdo.mrs", "MrsDomain"),
    "mrs_twitter_ip": ("twitter_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/twitter.mrs", "MrsIP"),
    "mrs_twitter_domain": ("twitter_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitter.mrs", "MrsDomain"),
    "mrs_github": ("github_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/github.mrs", "MrsDomain"),
    "mrs_gitlab": ("gitlab_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gitlab.mrs", "MrsDomain"),
    "mrs_onedrive": ("onedrive_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/onedrive.mrs", "MrsDomain"),
    "mrs_microsoft": ("Microsoft_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Microsoft/Microsoft_OCD_Domain.mrs", "MrsDomain"),
    "mrs_openai": ("openai_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.mrs", "MrsDomain"),
    "mrs_anthropic": ("anthropic_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/anthropic.mrs", "MrsDomain"),
    "mrs_discord": ("discord_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/discord.mrs", "MrsDomain"),
    "mrs_aliyun": ("aliyun_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/aliyun.mrs", "MrsDomain"),
    "mrs_cloudflare": ("cloudflare_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cloudflare.mrs", "MrsDomain"),
    "mrs_docker": ("docker_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/docker.mrs", "MrsDomain"),
    "mrs_homebrew": ("homebrew_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/homebrew.mrs", "MrsDomain"),
    "mrs_python": ("python_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/python.mrs", "MrsDomain"),
    "mrs_icloud": ("icloud_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/icloud.mrs", "MrsDomain"),
    "mrs_apple": ("apple_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/apple.mrs", "MrsDomain"),
    "mrs_youtube": ("youtube_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs", "MrsDomain"),
    "mrs_google_ip": ("Google_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Google/Google_OCD_IP.mrs", "MrsIP"),
    "mrs_google_domain": ("Google_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Google/Google_OCD_Domain.mrs", "MrsDomain"),
    "mrs_twitch": ("twitch_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitch.mrs", "MrsDomain"),
    "mrs_niconico": ("niconico_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/niconico.mrs", "MrsDomain"),
    "mrs_pixiv": ("Pixiv_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Pixiv/Pixiv_OCD_Domain.mrs", "MrsDomain"),
    "mrs_netflix_ip": ("netflix_IP", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/netflix.mrs", "MrsIP"),
    "mrs_netflix_domain": ("netflix_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/netflix.mrs", "MrsDomain"),
    "mrs_disney": ("disney_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/disney.mrs", "MrsDomain"),
    "mrs_bilibili": ("bilibili_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/bilibili.mrs", "MrsDomain"),
    "mrs_spotify": ("spotify_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/spotify.mrs", "MrsDomain"),
    "mrs_dmm": ("dmm_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/dmm.mrs", "MrsDomain"),
    "mrs_telegram_ip": ("Telegram_IP", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Telegram/Telegram_OCD_IP.mrs", "MrsIP"),
    "mrs_telegram_domain": ("Telegram_Domain", "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/master/rule/Clash/Telegram/Telegram_OCD_Domain.mrs", "MrsDomain"),
    "mrs_gfw": ("gfw_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/gfw.mrs", "MrsDomain"),
    "mrs_cn_domain": ("cn_Domain", "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.mrs", "MrsDomain"),
})


SURGE_RULE_GROUPS = {
    "Domain": {"DOMAIN", "DOMAIN-SUFFIX"},
    "IP": {"IP-CIDR", "IP-CIDR6"},
    "Keyword": {"DOMAIN-KEYWORD"},
    "Process": {"PROCESS-NAME"},
    "ASN": {"IP-ASN"},
    "UserAgent": {"USER-AGENT"},
    "Logical": {"AND", "OR", "NOT"},
}
# Valid primitive sub-rules from https://manual.nssurge.com/rules/overview.html.
# These validate logical expressions; they do not cause extra output files.
SURGE_LOGICAL_LEAVES = set().union(*(types for group, types in SURGE_RULE_GROUPS.items() if group != "Logical")) | {
    "DOMAIN-WILDCARD", "DOMAIN-SET", "GEOIP", "URL-REGEX", "DEST-PORT", "SRC-PORT", "IN-PORT", "SRC-IP",
    "DEVICE-NAME", "MAC-ADDRESS", "PROTOCOL", "HOSTNAME-TYPE", "SUBNET", "CELLULAR-RADIO", "CELLULAR-CARRIER",
    "SCRIPT", "RULE-SET",
}

# Existing example-profile sections; this maps sources, never their output types.
SURGE_SECTIONS = {
    "CatsTeam_AdRules": "adrules", "Blackmatrix7_Lan": "lan", "RuleForOCD_Steam": "steam",
    "Blackmatrix7_AdobeActivation": "adobeactivation", "Blackmatrix7_GoogleFCM": "googlefcm",
    "Geosite2Surge_z-library": "z-library", "MetaCubeX_linuxdo": "linuxdo",
    "Blackmatrix7_Twitter": "twitter", "Blackmatrix7_Claude": "anthropic", "Blackmatrix7_OpenAI": "openai",
    "Blackmatrix7_Copilot": "copilot", "MetaCubeX_google-gemini": "gemini", "Blackmatrix7_GitHub": "github",
    "MetaCubeX_gitlab": "gitlab", "Blackmatrix7_OneDrive": "onedrive", "Blackmatrix7_Microsoft": "microsoft",
    "Blackmatrix7_Discord": "discord", "MetaCubeX_aliyun": "aliyun", "MetaCubeX_cloudflare": "cloudflare",
    "Blackmatrix7_Docker": "docker", "MetaCubeX_homebrew": "homebrew", "MetaCubeX_python": "python",
    "Blackmatrix7_iCloud": "icloud", "Blackmatrix7_AppleDomain": "apple_domain", "Blackmatrix7_Apple": "apple_classical",
    "Blackmatrix7_YouTube": "youtube", "Blackmatrix7_Google": "google", "Blackmatrix7_Twitch": "twitch",
    "Blackmatrix7_Niconico": "niconico", "Blackmatrix7_Pixiv": "pixiv", "Blackmatrix7_Netflix": "netflix",
    "Blackmatrix7_Disney": "disney", "Blackmatrix7_BiliBili": "bilibili", "Blackmatrix7_Spotify": "spotify",
    "Blackmatrix7_DMM": "dmm", "Blackmatrix7_Telegram": "telegram", "Loyalsoldier_gfw": "gfw",
    "Loyalsoldier_direct": "cn_domain",
}
SURGE_URL = "https://fastly.jsdelivr.net/gh/Lolicandae/blacklist-rules@main/third_party/"
TABLE_START = "<!-- synced-surge-rules:begin -->"
TABLE_END = "<!-- synced-surge-rules:end -->"


def targets() -> dict[str, tuple[str, str, str]]:
    result = dict(UPSTREAM_RULES)
    for index, (name, url, kind) in result.items():
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise BuildError(f"Unsafe output name: {index}")
        if kind not in {"Domain", "IP", "Process", "SurgeSplit", "DomainSet", "MrsDomain", "MrsIP"}:
            raise BuildError(f"Unsupported rule kind: {index}")
        if not url.startswith("https://raw.githubusercontent.com/"):
            raise BuildError(f"Unsupported upstream source: {index}")
    paths = [path.casefold() for name, url, kind in result.values() for path in possible_output_paths(name, kind, url).values()]
    if not result or len(set(paths)) != len(paths):
        raise BuildError("Empty or colliding third-party output names")
    return result


def download(url: str) -> str | bytes | None:
    request = Request(url, headers={"User-Agent": "blacklist-rules-sync"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                content = response.read(16 * 1024 * 1024 + 1)
            break
        except HTTPError as exc:
            if exc.code in {404, 410}:
                exc.close()
                return None
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise
            exc.close()
        except (URLError, TimeoutError, ConnectionError) as exc:
            reason = exc.reason if isinstance(exc, URLError) else exc
            temporary = isinstance(reason, (TimeoutError, ConnectionError)) or isinstance(reason, socket.gaierror) and reason.errno == socket.EAI_AGAIN or isinstance(reason, OSError) and reason.errno in {errno.ENETUNREACH, errno.EHOSTUNREACH}
            if not temporary or attempt == 2:
                raise
        sleep(attempt + 1)
    if len(content) > 16 * 1024 * 1024:
        raise BuildError(f"Source exceeds 16 MiB: {url}")
    return content if url.endswith(".mrs") else content.decode("utf-8-sig")


def download_self_test() -> None:
    url = "https://example.invalid/ai-agent-rules.txt"
    errors = [URLError(ConnectionResetError("reset")), URLError(TimeoutError("timeout")), TimeoutError("read timeout"), ConnectionResetError("read reset"), URLError(socket.gaierror(socket.EAI_AGAIN, "temporary DNS")), URLError(OSError(errno.ENETUNREACH, "network unreachable")), URLError(OSError(errno.EHOSTUNREACH, "host unreachable"))]
    errors.extend(HTTPError(url, status, "temporary", None, None) for status in (429, 500, 502, 503, 504))
    for error in errors:
        with patch(__name__ + ".urlopen", side_effect=[error, error, io.BytesIO(b"example.test\n")]) as request, patch(__name__ + ".sleep") as delay:
            assert download(url) == "example.test\n"
            assert request.call_count == 3 and [entry.args for entry in delay.call_args_list] == [(1,), (2,)]
        with patch(__name__ + ".urlopen", side_effect=error) as request, patch(__name__ + ".sleep") as delay:
            try:
                download(url)
            except type(error):
                pass
            else:
                raise AssertionError("Persistent download failure was ignored")
            assert request.call_count == 3 and delay.call_count == 2
    for status in (404, 410):
        with patch(__name__ + ".urlopen", side_effect=HTTPError(url, status, "missing", None, None)) as request, patch(__name__ + ".sleep") as delay:
            assert download(url) is None and request.call_count == 1
            delay.assert_not_called()
    for error in (HTTPError(url, 403, "forbidden", None, None), URLError(ValueError("invalid URL")), URLError(socket.gaierror(socket.EAI_NONAME, "unknown host"))):
        with patch(__name__ + ".urlopen", side_effect=error) as request, patch(__name__ + ".sleep") as delay:
            try:
                download(url)
            except type(error):
                pass
            else:
                raise AssertionError("Permanent download failure was ignored")
            assert request.call_count == 1
            delay.assert_not_called()
    for payload, expected_error in ((b"\xff", UnicodeError), (b"x" * (16 * 1024 * 1024 + 1), BuildError)):
        with patch(__name__ + ".urlopen", return_value=io.BytesIO(payload)) as request, patch(__name__ + ".sleep") as delay:
            try:
                download(url)
            except expected_error:
                pass
            else:
                raise AssertionError("Invalid download payload was accepted")
            assert request.call_count == 1
            delay.assert_not_called()
    with patch(__name__ + ".urlopen", return_value=io.BytesIO(b"\xff")):
        assert download(url + ".mrs") == b"\xff"
    print("Bounded download retry, missing upstream and permanent failure checks passed.")


@lru_cache(maxsize=64)
def validate_mrs(content: bytes, kind: str) -> bool:
    """Let Mihomo validate its native format; retain the original binary unchanged."""
    executable = os.environ.get("MIHOMO_BIN") or shutil.which("mihomo")
    if not executable:
        raise BuildError("MRS validation requires Mihomo; set MIHOMO_BIN to its executable path")
    with tempfile.TemporaryDirectory(prefix="ai-agent-third-party-mrs-") as temporary:
        source = Path(temporary) / "ai-agent-input.mrs"
        target = Path(temporary) / "ai-agent-output.txt"
        source.write_bytes(content)
        result = subprocess.run(
            [executable, "convert-ruleset", "domain" if kind == "MrsDomain" else "ipcidr", "mrs", str(source), str(target)],
            capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode:
            if result.stderr.startswith("panic: empty rule\n"):
                return False
            raise BuildError(f"Invalid {kind} file: {result.stderr.strip()}")
        if not target.is_file() or not target.read_text(encoding="utf-8").strip():
            raise BuildError(f"Invalid {kind} file: Mihomo returned no matching rules")
    return True


def convert(text: str, kind: str) -> dict[str, bytes]:
    items = []
    payload = False
    empty_payload = False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "//")):
            continue
        inline_empty = bool(re.fullmatch(r"payload:\s+\[\s*\](?:\s+#.*)?", line))
        if (line == "payload:" or inline_empty) and not items and not payload:
            payload = True
            empty_payload = inline_empty
            continue
        if empty_payload:
            raise BuildError("Inline empty YAML payload has additional content")
        if payload:
            if not line.startswith("- "):
                raise BuildError("Unsupported YAML payload")
            line = line[2:].strip()
            if line.startswith('"'):
                line = json.loads(line)
            elif line.startswith("'") and line.endswith("'"):
                line = line[1:-1].replace("''", "'")
        items.append(Rule(line))
    if not items:
        return {}
    content = render_json_rules(items)
    fields = {field for rule in json.loads(content)["rules"] for field in rule}
    allowed = {"Domain": {"domain", "domain_suffix", "domain_regex"}, "IP": {"ip_cidr"}, "Process": {"process_name"}}[kind]
    if not fields or not fields <= allowed:
        raise BuildError(f"Source does not contain only {kind} rules")
    if kind == "IP":
        surge = []
        for item in items:
            network = ipaddress.ip_network(item.raw, strict=False)
            surge.append(f"IP-CIDR{'6' if network.version == 6 else ''},{network},no-resolve")
    else:
        surge = render_items(items, "surge")
    yaml = ("\n".join(render_items(items, "clash")) + "\n").encode("utf-8")
    return {
        "clash": yaml,
        "surge": ("\n".join(surge) + "\n").encode("utf-8"),
        "sing-box": (content + "\n").encode("utf-8"),
    }


def closing_parenthesis(text: str) -> int:
    if not text.startswith("("):
        raise BuildError(f"Expected parenthesized Surge expression: {text}")
    balance, position = 0, 0
    quote = None
    previous = ""
    while position < len(text):
        char = text[position]
        if quote:
            if char == "\\":
                position += 2
                continue
            if char == quote:
                if position + 1 < len(text) and text[position + 1] == quote:
                    position += 2
                    continue
                quote = None
        elif char in {"'", '"'} and previous in {"(", ","}:
            quote = char
        elif char == "(":
            balance += 1
        elif char == ")":
            balance -= 1
            if balance == 0:
                return position
        if not char.isspace():
            previous = char
        position += 1
    raise BuildError(f"Unbalanced Surge expression: {text}")


def validate_logical(rule: str, depth: int = 1) -> None:
    rule_type, separator, value = rule.partition(",")
    rule_type, value = rule_type.strip(), value.strip()
    if not separator or not value:
        raise BuildError(f"Invalid Surge sub-rule: {rule}")
    if rule_type not in SURGE_RULE_GROUPS["Logical"]:
        if rule_type not in SURGE_LOGICAL_LEAVES:
            raise BuildError(f"Unsupported Surge sub-rule (not omitted): {rule}")
        return
    if depth > 10:
        raise BuildError("Surge logical nesting exceeds 10 levels")
    end = closing_parenthesis(value)
    suffix = value[end + 1:].strip()
    if suffix and (not suffix.startswith(",") or any(not option.strip() or option.strip() == "pre-matching" for option in suffix[1:].split(","))):
        raise BuildError(f"Invalid Surge logical options: {rule}")
    children, count = value[1:end].strip(), 0
    while children:
        end = closing_parenthesis(children)
        validate_logical(children[1:end].strip(), depth + 1)
        count += 1
        children = children[end + 1:].strip()
        if children:
            if not children.startswith(",") or not children[1:].strip():
                raise BuildError(f"Invalid Surge sub-rule separator: {rule}")
            children = children[1:].strip()
    if not count or (rule_type == "NOT" and count != 1):
        raise BuildError(f"Invalid Surge logical argument count: {rule}")


def split_surge(text: str, kind: str) -> dict[str, bytes]:
    """Keep every rule, grouped by type; never subtract another source's coverage."""
    if kind == "DomainSet":
        comments = ["# " + line.strip().lstrip("#/; ") for line in text.splitlines() if line.strip().startswith(("#", "//", ";"))]
        body = "\n".join(line for line in text.splitlines() if not line.strip().startswith(";"))
        prefix = ("\n".join(comments) + "\n").encode("utf-8") if comments else b""
        rules = convert(body, "Domain").get("surge")
        return {"Domain": prefix + rules} if rules else {}
    groups: dict[str, list[str]] = {}
    comments = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("#", "//", ";")):
            comments.append("# " + line.lstrip("#/; "))
            continue
        rule_type, separator, value = line.partition(",")
        value = value.strip()
        group = next((name for name, types in SURGE_RULE_GROUPS.items() if rule_type in types), None)
        if group is None or not separator or not value.strip():
            raise BuildError(f"Unsupported Surge rule (not omitted): {line}")
        if group == "Domain":
            if "," in value:
                raise BuildError(f"Domain-set cannot retain rule options: {line}")
            domain = value if rule_type == "DOMAIN" else "+." + value
            render_json_rules([Rule(domain)])
            line = value if rule_type == "DOMAIN" else "." + value
        elif group == "IP":
            network = ipaddress.ip_network(value.split(",")[0], strict=False)
            if network.version != (6 if rule_type == "IP-CIDR6" else 4):
                raise BuildError(f"Wrong Surge IP family: {line}")
            if any(option not in {"no-resolve"} for option in value.split(",")[1:]):
                raise BuildError(f"Unsupported Surge IP option: {line}")
        elif group == "ASN" and not re.fullmatch(r"\d+(?:,no-resolve)?", value):
            raise BuildError(f"Invalid Surge ASN: {line}")
        elif group == "Logical":
            validate_logical(line)
        groups.setdefault(group, []).append(line)
    return {group: ("\n".join(comments + rules) + "\n").encode("utf-8") for group, rules in groups.items()}


def source_layout(name: str, kind: str, url: str) -> tuple[str, str]:
    upstream = "/".join(url.split("/")[3:5])
    if upstream not in SOURCE_AUTHORS:
        raise BuildError(f"Unsupported upstream repository: {upstream}")
    author = SOURCE_AUTHORS[upstream]
    if kind in {"Domain", "IP", "Process", "MrsDomain", "MrsIP"}:
        service = name.removesuffix("_" + kind.removeprefix("Mrs")).lower()
    else:
        service = name.partition("_")[2].lower()
    if name == "Blackmatrix7_AppleDomain":
        service = "apple"
    if not re.fullmatch(r"[a-z0-9_-]+", service):
        raise BuildError(f"Unsafe service name: {name}")
    return author, service


def possible_output_paths(name: str, kind: str, url: str) -> dict[str, str]:
    """Allowed paths for collision checks and cleanup, not a list of files to emit."""
    author, service = source_layout(name, kind, url)
    folder = f"{author}/{service}"
    if kind in {"SurgeSplit", "DomainSet"}:
        types = SURGE_RULE_GROUPS if kind == "SurgeSplit" else {"Domain": set()}
        # Apple_Domain.list and Apple.list are distinct inputs for the same service.
        return {group: f"surge/{folder}/{service}_{'domainset' if name == 'Blackmatrix7_AppleDomain' else group.lower()}.list" for group in types}
    if kind in {"MrsDomain", "MrsIP"}:
        return {"mrs": f"clash/{folder}/{service}_{kind.removeprefix('Mrs').lower()}.mrs"}
    filename = f"{service}_{kind.lower()}"
    paths = {fmt: f"{fmt}/{folder}/{filename}{extension}" for fmt, extension in FORMATS.items()}
    if any(other_kind in {"SurgeSplit", "DomainSet"} and other_url.split("/")[3:5] == url.split("/")[3:5] and source_layout(other_name, other_kind, other_url) == (author, service) for other_name, other_url, other_kind in UPSTREAM_RULES.values()):
        paths.pop("surge")
    return paths


def render_surge_profile(text: str, mirrors: dict[str, dict]) -> str:
    """Update existing source sections using only types found in the downloaded rules."""
    for name, source in mirrors.items():
        heading = SURGE_SECTIONS[name]
        pattern = re.compile(r"(^# > " + re.escape(heading) + r"\n)(.*?)(?=^# > |^\[|\Z)", re.M | re.S)
        blocks = list(pattern.finditer(text))
        if len(blocks) != 1:
            raise BuildError(f"Missing or duplicate Surge profile section: {heading}")
        block = blocks[0]
        lines = block[2].splitlines(keepends=True)
        owned_urls = [SURGE_URL + path for path in possible_output_paths(name, source["kind"], source["source"]).values()]
        rule = re.compile(r"^(?:DOMAIN-SET|RULE-SET), (?:" + "|".join(re.escape(url) for url in owned_urls) + r"), (.+)\n?$")
        policies = [match[1] for line in lines if (match := rule.fullmatch(line))]
        marker = "# Sync policy: "
        policies += [line[len(marker):].rstrip("\n") for line in lines if line.startswith(marker)]
        if not policies or len(set(policies)) != 1:
            raise BuildError(f"Missing or inconsistent Surge policy: {name}")
        suffix = policies[0]
        generated = "".join(f"{'DOMAIN-SET' if group == 'Domain' else 'RULE-SET'}, {SURGE_URL}{path}, {suffix}\n" for group, path in source["outputs"].items())
        if not generated:
            # Keep the policy for a future nonempty sync without retaining a dead URL.
            generated = marker + suffix + "\n"
        owned = [i for i, line in enumerate(lines) if rule.fullmatch(line) or line.startswith(marker)]
        first = owned[0]
        rest = "".join(line for i, line in enumerate(lines) if i not in owned)
        insertion = sum(len(line) for i, line in enumerate(lines[:first]) if i not in owned)
        body = rest[:insertion] + generated + rest[insertion:]
        text = text[:block.start(2)] + body + text[block.end(2):]
    return text


def render_surge_table(text: str, mirrors: dict[str, dict], chinese: bool) -> str:
    if text.count(TABLE_START) != 1 or text.count(TABLE_END) != 1:
        raise BuildError("Missing or duplicate synced Surge table markers")
    labels = dict(zip(SURGE_RULE_GROUPS, ["仅域名", "仅 IP", "仅关键词", "仅进程", "仅 ASN", "仅 User-Agent", "仅逻辑规则"] if chinese else ["Domain Only", "IP Only", "Keyword Only", "Process Only", "ASN Only", "User-Agent Only", "Logical Only"]))
    rows = []
    for name, source in mirrors.items():
        if not source["outputs"]:
            continue
        cells = []
        for base in ("https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/", SURGE_URL):
            cells.append('<br>'.join(f'<a href="{base}{path}">{labels[group]}</a>' for group, path in source["outputs"].items()))
        rows.append(f'  <tr align="center">\n    <td>{name}</td>\n    <td>{cells[0]}</td>\n    <td>{cells[1]}</td>\n  </tr>\n')
    before, _, tail = text.partition(TABLE_START)
    _, separator, after = tail.partition(TABLE_END)
    if not separator:
        raise BuildError("Invalid synced Surge table markers")
    return before + TABLE_START + "\n" + "".join(rows) + TABLE_END + after


def render_legacy_table(table: str, fmt: str, selected: dict, sources: dict, chinese: bool) -> str:
    grouped = {}
    for index, (name, _, kind) in selected.items():
        if kind in {"Domain", "IP", "Process"}:
            stem = name.removesuffix("_" + kind)
            grouped.setdefault(stem.casefold(), []).append((index, kind))
    labels = dict(zip(("Domain", "IP", "Process"), ["仅域名", "仅 IP", "仅进程"] if chinese else ["Domain Only", "IP Only", "Process Only"]))
    row = re.compile(r'  <tr align="center">\n    <td>([^<>]+)</td>\n    <td>[^\n]*</td>\n    <td>[^\n]*</td>\n  </tr>\n')

    def replace(match: re.Match) -> str:
        entries = grouped.get(match[1].casefold())
        if entries is None:
            return match[0]
        if fmt == "surge" and all("surge" not in possible_output_paths(selected[index][0], kind, selected[index][1]) for index, kind in entries):
            return ""
        outputs = []
        for index, kind in entries:
            if fmt == "clash" and "mrs_" + index in sources:
                native = sources["mrs_" + index]["outputs"]
                if "mrs" in native:
                    outputs.append((native["mrs"], "MRS · " + labels[kind]))
            key = fmt
            if key in sources[index]["outputs"]:
                outputs.append((sources[index]["outputs"][key], ("YAML · " if fmt == "clash" else "") + labels[kind]))
        paths = re.findall(r"third_party/([^\"<>\s]+)", match[0])
        if sorted(paths) == sorted(path for path, _ in outputs for _ in range(2)):
            return match[0]
        cells = []
        for base in ("https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/", SURGE_URL):
            cells.append('<br>'.join(f'<a href="{base}{path}">{label}</a>' for path, label in outputs) or ("暂无规则" if chinese else "No rules"))
        return f'  <tr align="center">\n    <td>{match[1]}</td>\n    <td>{cells[0]}</td>\n    <td>{cells[1]}</td>\n  </tr>\n'

    return row.sub(replace, table)


def render_mihomo_references(text: str, selected: dict, sources: dict, javascript: bool) -> str:
    """Disable absent sources while keeping their original settings for restoration."""
    marker = "// Sync-disabled: " if javascript else "# Sync-disabled: "
    # These comments are inactive configuration templates, never sync inputs.
    text = re.sub(r"^([ \t]*)" + re.escape(marker) + r"(.*)$", r"\1\2", text, flags=re.M)

    def disable(content: str) -> str:
        return re.sub(r"^([ \t]*)(?=\S)", lambda match: match[1] + marker, content, flags=re.M)

    for index, (name, _, kind) in selected.items():
        if kind not in {"Domain", "IP", "Process"}:
            continue
        if javascript:
            pattern = r'^  "' + re.escape(index) + r'": \{\n(?:^    .*\n)*^  \},?\n'
        else:
            pattern = r'^  ' + re.escape(index) + r':\n(?:^    .*\n)+'
        provider = re.compile(pattern, re.M)
        blocks = list(provider.finditer(text))
        if len(blocks) != 1 or "third_party/clash/" not in blocks[0][0]:
            raise BuildError(f"Missing or ambiguous Mihomo provider template: {index}")
        native_index = "mrs_" + index
        native = native_index in selected
        outputs = sources[native_index if native else index]["outputs"]
        key = "mrs" if native else "clash"
        path = outputs.get(key)
        template = blocks[0][0]
        if path:
            template = template.replace("ruleProviderYaml", "ruleProviderMrs") if native else template.replace("ruleProviderMrs", "ruleProviderYaml")
            template = re.sub(r'((?:"url"|url):[ \t]*")[^"]*(")', lambda match: match[1] + SURGE_URL + path + match[2], template)
            cache = "./ruleset/paloexiz/third_party/" + path.removeprefix("clash/")
            template = re.sub(r'((?:"path"|path):[ \t]*")[^"]*(")', lambda match: match[1] + cache + match[2], template)
        text = provider.sub(lambda match: template if path else disable(template), text)
        if path:
            continue
        rule = re.compile(r'^[ \t]*(?:- |")RULE-SET,\s*' + re.escape(index) + r'\s*,[^\n]*\n', re.M)
        if not rule.search(text):
            raise BuildError(f"Missing Mihomo rule for absent provider: {index}")
        text = rule.sub(lambda match: disable(match[0]), text)
    return text


def reference_candidates(root: Path, selected: dict, sources: dict, only: Path | None = None) -> dict[Path, bytes]:
    mirrors = {name: sources[index] for index, (name, _, kind) in selected.items() if kind in {"SurgeSplit", "DomainSet"}}
    result = {}
    profile = root / "client_conf/surge_configuration/surge_configuration.conf"
    if (only is None or only == profile) and profile.is_file():
        result[profile] = render_surge_profile(profile.read_text(encoding="utf-8"), mirrors).encode("utf-8")
    for relative, javascript in (("client_conf/mihomo_configuration/mihomo_configuration.yaml", False), ("client_conf/mihomo_override/mihomo_override.js", True)):
        client = root / relative
        if (only is None or only == client) and client.is_file():
            result[client] = render_mihomo_references(client.read_text(encoding="utf-8"), selected, sources, javascript).encode("utf-8")
    for filename, chinese in (("README.md", False), ("README.zh-cn.md", True)):
        document = root / "third_party" / filename
        if (only is None or only == document) and document.is_file():
            text = document.read_text(encoding="utf-8")
            tables = list(re.finditer(r"<table>\n.*?</table>", text, re.S))
            if len(tables) != 3:
                raise BuildError("Expected the existing three client tables")
            for table, fmt in reversed(list(zip(tables, ("sing-box", "clash", "surge")))):
                text = text[:table.start()] + render_legacy_table(table[0], fmt, selected, sources, chinese) + text[table.end():]
            result[document] = render_surge_table(text, mirrors, chinese).encode("utf-8")
    return result


def notice_path(url: str) -> str:
    return {"MetaCubeX": "licenses/MetaCubeX/LICENSE", "peiyingyao": "licenses/Rule-for-OCD/LICENSE", "Loyalsoldier": "licenses/Loyalsoldier/LICENSE", "Cats-Team": "NOTICE.md", "blackmatrix7": "licenses/blackmatrix7-LICENSE", "coderbean": "NOTICE.md"}[url.split("/")[3]]


def read_repository_file(root: Path, relative: str) -> bytes:
    root = root.resolve()
    path = root / relative
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or getattr(part, "is_junction", lambda: False)():
            raise BuildError(f"{relative}: linked repository files are unsupported")
    if not path.resolve().is_relative_to(root):
        raise BuildError(f"{relative}: path resolves outside the repository")
    if not path.is_file():
        raise BuildError(f"{relative}: required file is missing")
    content = path.read_bytes()
    if not content.strip():
        raise BuildError(f"{relative}: file is empty")
    return content


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise BuildError(f"Duplicate JSON property: {key}")
        result[key] = value
    return result


def validate_rule_file(content: bytes, kind: str, key: str) -> None:
    if key == "mrs":
        if not validate_mrs(content, kind):
            raise BuildError("MRS contains no matching rules")
        return
    text = content.decode("utf-8")
    if key == "sing-box":
        data = json.loads(text, object_pairs_hook=unique_object)
        allowed = {"Domain": {"domain", "domain_suffix", "domain_regex"}, "IP": {"ip_cidr"}, "Process": {"process_name"}}[kind]
        if not isinstance(data, dict) or set(data) != {"version", "rules"} or data["version"] != 3 or not isinstance(data["rules"], list) or not data["rules"]:
            raise BuildError("Expected a nonempty sing-box version 3 ruleset")
        for rule in data["rules"]:
            if not isinstance(rule, dict) or not rule or not rule.keys() <= allowed:
                raise BuildError(f"sing-box rule contains fields outside {kind}")
            for field, values in rule.items():
                if not isinstance(values, list) or not values or any(not isinstance(value, str) or not value for value in values):
                    raise BuildError(f"sing-box {field} must be a nonempty string array")
                if field == "domain_regex":
                    for value in values:
                        re.compile(value)
                else:
                    converted = json.loads(render_json_rules([Rule("PROCESS-NAME," + value if field == "process_name" else value) for value in values]))["rules"]
                    canonical = {value for entry in converted for value in entry.get(field, [])}
                    if canonical != set(values):
                        raise BuildError(f"Invalid sing-box {field} values")
        return
    if key == "clash":
        body = [line.rstrip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if not body or body[0] != "payload:":
            raise BuildError("Expected the generated YAML payload")
        for line in body[1:]:
            entry = re.fullmatch(r"  - (\S.*)", line)
            if not entry:
                raise BuildError("Unsupported generated YAML payload indentation or entry")
            scalar = entry[1]
            if scalar.startswith('"'):
                if not isinstance(json.loads(scalar), str):
                    raise BuildError("YAML payload values must be strings")
            elif scalar.startswith("'"):
                if not re.fullmatch(r"'(?:[^']|'')*'", scalar):
                    raise BuildError("Invalid quoted YAML string")
            elif scalar[0] in "&*!{}[],|>@`%" or re.match(r"[-?:](?:\s|$)", scalar) or re.search(r":(?:\s|$)|(?:^|\s)#", scalar) or re.fullmatch(r"(?i:true|false|null|~|yes|no|on|off|[-+]?(?:0[xob][0-9a-f_]+|[0-9_]+(?:\.[0-9_]*)?(?:e[-+]?[0-9]+)?|\.[0-9_]+|\.inf|\.nan))|[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}", scalar):
                raise BuildError("YAML payload requires an unambiguous plain string or quoted string")
        converted = convert(text, kind)
        if not converted:
            raise BuildError("YAML contains no matching rules")
        if body != converted["clash"].decode("utf-8").splitlines():
            raise BuildError("YAML payload syntax disagrees with the generated string rules")
        return
    group = key if kind in {"SurgeSplit", "DomainSet"} else kind
    parsed = split_surge(text, "DomainSet" if group == "Domain" else "SurgeSplit")
    if set(parsed) != {group}:
        raise BuildError(f"Surge file must contain only nonempty {group} rules")
    if group == "Process":
        convert(text, "Process")


def validate_mihomo_references(text: str, selected: dict, sources: dict, javascript: bool) -> None:
    """Read only the scalar provider templates and rule list used by these profiles."""
    # ponytail: existing scalar templates only; use a real parser if profile syntax grows.
    marker = "// Sync-disabled: " if javascript else "# Sync-disabled: "
    lines = text.splitlines(keepends=True)
    disabled = []
    normalized = []
    for line in lines:
        prefix = line[:len(line) - len(line.lstrip())]
        flagged = line.lstrip().startswith(marker)
        disabled.append(flagged)
        normalized.append(prefix + line.lstrip()[len(marker):] if flagged else line)
    plain = "".join(normalized)

    def section(pattern: str, label: str) -> re.Match:
        matches = list(re.finditer(pattern, plain, re.M | re.S))
        if len(matches) != 1:
            raise BuildError(f"Missing or duplicate {label}")
        return matches[0]

    def inactive(match: re.Match) -> bool:
        first = plain.count("\n", 0, match.start())
        flags = disabled[first:first + len(match[0].splitlines())]
        if any(flags) and not all(flags):
            raise BuildError("Provider or rule is only partly Sync-disabled")
        return all(flags)

    def yaml_fields(body: str) -> dict:
        result = {}
        for field in body.splitlines():
            match = re.fullmatch(r'\s*([a-zA-Z_-]+):\s*("(?:[^"\\]|\\.)*"|[a-zA-Z0-9_-]+)\s*,?\s*', field)
            if not match or match[1] in result:
                raise BuildError(f"Unsupported or duplicate YAML provider field: {field.strip()}")
            value = match[2]
            result[match[1]] = json.loads(value) if value.startswith('"') else value
        return result

    templates = {}
    for name in ("ruleProviderYaml", "ruleProviderMrs"):
        if javascript:
            match = section(r'^const ' + name + r' = (\{\n.*?^\});\n', name)
            templates[name] = json.loads(match[1], object_pairs_hook=unique_object)
        else:
            match = section(r'^  ' + name + r': &' + name + r' \{ ([^\n{}]+) \}\n', name)
            templates[name] = yaml_fields("\n".join(match[1].split(",")))
        if not isinstance(templates[name], dict) or templates[name].get("type") != "http" or templates[name].get("format") != ("yaml" if name.endswith("Yaml") else "mrs"):
            raise BuildError(f"Invalid {name} type/format")
    container = section(r'^const ruleProviders = \{\n(.*?)^\};\n' if javascript else r'^rule-providers:\n(.*?)(?=^\S|\Z)', "rule-providers")
    pattern = r'^  "([A-Za-z0-9_-]+)": \{\n((?:^    [^\n]*\n)*)^  \},?\n' if javascript else r'^  ([A-Za-z0-9_-]+):\n    \{\n((?:^      [^\n]*\n)*)^    \}\n'
    providers = {}
    cursor = container.start(1)
    for match in re.finditer(pattern, plain, re.M):
        if not container.start(1) <= match.start() < container.end(1):
            continue
        if plain[cursor:match.start()].strip() or match[1] in providers:
            raise BuildError(f"Unsupported or duplicate provider template: {match[1]}")
        body = match[2]
        inheritance = re.fullmatch(r'    \.\.\.(ruleProviderYaml|ruleProviderMrs),\n' if javascript else r'      <<: \*(ruleProviderYaml|ruleProviderMrs),\n', body.splitlines(keepends=True)[0] if body else "")
        if not inheritance:
            raise BuildError(f"Unsupported provider inheritance: {match[1]}")
        fields = body[len(inheritance[0]):]
        attributes = json.loads("{" + re.sub(r',\s*\Z', '', fields) + "}", object_pairs_hook=unique_object) if javascript else yaml_fields(fields)
        providers[match[1]] = ({**templates[inheritance[1]], **attributes}, inactive(match))
        cursor = match.end()
    if plain[cursor:container.end(1)].strip():
        raise BuildError("Unsupported rule-providers template syntax")
    rules = section(r'^const rules = \[\n(.*?)^\];\n' if javascript else r'^rules:\n(.*?)(?=^\S|\Z)', "rules")
    references = {}
    cursor = rules.start(1)
    for match in re.finditer(r'^  "[^\n]+"[,]?\n' if javascript else r'^  - [^\n]+\n', plain, re.M):
        if not rules.start(1) <= match.start() < rules.end(1):
            continue
        if plain[cursor:match.start()].strip():
            raise BuildError("Unsupported rules template syntax")
        value = json.loads(match[0].strip().removesuffix(",")) if javascript else match[0].strip()[2:]
        fields = [field.strip() for field in value.split(",")]
        if fields[0] == "RULE-SET":
            if len(fields) < 3 or not fields[2] or fields[1] not in providers:
                raise BuildError(f"Invalid RULE-SET reference: {value}")
            references.setdefault(fields[1], []).append(inactive(match))
        cursor = match.end()
    if plain[cursor:rules.end(1)].strip():
        raise BuildError("Unsupported rules template syntax")
    legacy = {index for index, (_, _, kind) in selected.items() if kind in {"Domain", "IP", "Process"}}
    for index, (attributes, _) in providers.items():
        if "third_party/" in str(attributes.get("url", "")) and index not in legacy:
            raise BuildError(f"Unregistered third-party provider: {index}")
    for index in legacy:
        name, url, kind = selected[index]
        native = "mrs_" + index in selected
        target_index, key = ("mrs_" + index, "mrs") if native else (index, "clash")
        target_name, target_url, target_kind = selected[target_index]
        path = possible_output_paths(target_name, target_kind, target_url)[key]
        absent = key not in sources[target_index]["outputs"]
        expected = {"type": "http", "format": "mrs" if native else "yaml", "behavior": {"Domain": "domain", "IP": "ipcidr", "Process": "classical"}[kind], "url": SURGE_URL + path, "path": "./ruleset/paloexiz/third_party/" + path.removeprefix("clash/")}
        if index not in providers:
            raise BuildError(f"Missing third-party provider: {index}")
        attributes, off = providers[index]
        for field, value in expected.items():
            if attributes.get(field) != value:
                raise BuildError(f"{index}: incorrect {field}: expected {value}")
        if off != absent or not references.get(index) or any(flag != absent for flag in references[index]):
            raise BuildError(f"{index}: provider/rule enable state disagrees with outputs")


def validate_repository(root: Path, *, require_references: bool = True) -> None:
    """Validate committed third-party files offline, without changing the repository."""
    selected = targets()
    manifest = "third_party/sources.json"
    try:
        sources = json.loads(read_repository_file(root, manifest), object_pairs_hook=unique_object)
    except (ValueError, BuildError) as exc:
        raise BuildError(f"{manifest}: {exc}") from exc
    if not isinstance(sources, dict) or sources.keys() != selected.keys():
        raise BuildError(f"{manifest}: sources disagree with fixed inventory")
    registered = set()
    for index, (name, url, kind) in selected.items():
        source = sources[index]
        expected = possible_output_paths(name, kind, url)
        if not isinstance(source, dict) or set(source) != {"source", "sha256", "kind", "notices", "outputs"} or source.get("source") != url or source.get("kind") != kind or source.get("notices") != notice_path(url) or not isinstance(source.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            raise BuildError(f"{manifest}: {index}: invalid source/kind/notices/sha256 record")
        outputs = source["outputs"]
        if not isinstance(outputs, dict) or any(key not in expected or expected[key] != path for key, path in outputs.items()) or (kind not in {"SurgeSplit", "DomainSet"} and outputs not in ({}, expected)):
            raise BuildError(f"{manifest}: {index}: outputs disagree with allowed paths")
        read_repository_file(root, "third_party/" + source["notices"])
        for key, relative in outputs.items():
            path = "third_party/" + relative
            try:
                content = read_repository_file(root, path)
                validate_rule_file(content, kind, key)
                if key == "mrs" and hashlib.sha256(content).hexdigest() != source["sha256"]:
                    raise BuildError("Native MRS sha256 disagrees with source record")
            except (OSError, ValueError, UnicodeError, re.error, subprocess.SubprocessError, BuildError) as exc:
                raise BuildError(f"{path}: {index}/{key}: {exc}") from exc
            registered.add(path)
    for folder in ("clash", "surge", "sing-box"):
        base = root / "third_party" / folder
        if not base.resolve().is_relative_to(root.resolve()):
            raise BuildError(f"third_party/{folder}: path resolves outside the repository")
        for path in base.rglob("*"):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise BuildError(f"{relative}: linked rule artifacts are unsupported")
            if not path.resolve().is_relative_to(root.resolve()):
                raise BuildError(f"{relative}: path resolves outside the repository")
            if path.is_file() and relative not in registered:
                raise BuildError(f"{relative}: unregistered rule artifact")
    relatives = ("client_conf/mihomo_configuration/mihomo_configuration.yaml", "client_conf/mihomo_override/mihomo_override.js", "client_conf/surge_configuration/surge_configuration.conf", "third_party/README.md", "third_party/README.zh-cn.md")
    for relative in relatives:
        if not require_references and not (root / relative).exists():
            continue
        try:
            text = read_repository_file(root, relative).decode("utf-8").replace("\r\n", "\n")
            if relative.endswith((".yaml", ".js")):
                validate_mihomo_references(text, selected, sources, relative.endswith(".js"))
            elif relative.endswith(".conf"):
                surge = {path: group for index, (_, _, kind) in selected.items() if kind in {"SurgeSplit", "DomainSet"} for group, path in sources[index]["outputs"].items()}
                for line in text.splitlines():
                    if "third_party/" not in line or line.lstrip().startswith(("#", ";")):
                        continue
                    match = re.fullmatch(r'(DOMAIN-SET|RULE-SET), ([^, ]+), .+', line)
                    path = match[2].removeprefix(SURGE_URL) if match else ""
                    if not match or path not in surge or match[1] != ("DOMAIN-SET" if surge[path] == "Domain" else "RULE-SET"):
                        raise BuildError(f"Invalid or unregistered Surge reference: {line}")
            else:
                tables = re.findall(r"<table>\n.*?</table>", text, re.S)
                if len(tables) != 3:
                    raise BuildError("Expected the existing three client tables")
                for table, fmt in zip(tables, ("sing-box", "clash", "surge")):
                    legacy = table.split(TABLE_START)[0]
                    expected_rows = {name.removesuffix("_" + kind).casefold() for name, url, kind in selected.values() if kind in {"Domain", "IP", "Process"} and fmt in possible_output_paths(name, kind, url)}
                    rows = re.findall(r'<tr align="center">\n    <td>([^<>]+)</td>', legacy)
                    if {name.casefold() for name in rows} != expected_rows or len(rows) != len(expected_rows):
                        raise BuildError(f"{fmt}: missing, duplicate or unregistered generated row")
                allowed = {path for source in sources.values() for path in source["outputs"].values()}
                for anchor in re.findall(r'<a\b[^>]*>', text):
                    match = re.fullmatch(r'<a href="([^"]+)">', anchor)
                    if not match:
                        raise BuildError(f"Unsupported README reference syntax: {anchor}")
                    url = match[1]
                    path = next((url.removeprefix(base) for base in (SURGE_URL, "https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/") if url.startswith(base)), None)
                    if path not in allowed:
                        raise BuildError(f"Invalid or unregistered README reference: {url}")
            # Render one existing object so a render failure names the affected file.
            candidates = reference_candidates(root, selected, sources, only=root / relative)
            if candidates[root / relative].decode("utf-8").replace("\r\n", "\n") != text:
                raise BuildError("Generated references disagree with source outputs")
        except (ValueError, UnicodeError, BuildError) as exc:
            raise BuildError(f"{relative}: {exc}") from exc
    print(f"Validated {len(selected)} sources and {len(registered)} rule files offline.")


def publish(root: Path, candidates: dict[Path, bytes], obsolete: set[Path]) -> tuple[set[Path], set[Path]]:
    """Prepare all files first; restore prior files if a replacement or deletion fails."""
    changed = {path: content for path, content in candidates.items() if not path.is_file() or path.read_bytes() != content}
    removed = {path for path in obsolete if path.is_file()}
    if not changed and not removed:
        return set(), set()
    root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="ai-agent-third-party-publish-", dir=root))
    backups: dict[Path, Path | None] = {}
    prepared = {}
    touched = []
    retain_backup = False
    try:
        for number, path in enumerate(dict.fromkeys([*changed, *sorted(removed)])):
            backup = temporary / f"old-{number}-{path.name}" if path.is_file() else None
            if backup is not None:
                shutil.copy2(path, backup)
            backups[path] = backup
        for number, (path, content) in enumerate(changed.items()):
            staged = temporary / f"new-{number}-{path.name}"
            staged.write_bytes(content)
            if backups[path] is not None:
                shutil.copymode(backups[path], staged)
            prepared[path] = staged
        manifest = root / "third_party/sources.json"
        operations = [(path, staged) for path, staged in prepared.items() if path != manifest]
        operations += [(path, None) for path in sorted(removed)]
        if manifest in prepared:
            operations.append((manifest, prepared[manifest]))
        try:
            for path, staged in operations:
                if staged is None:
                    path.unlink()
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    staged.replace(path)
                touched.append(path)
        except BaseException:
            failed = []
            for path in reversed(touched):
                try:
                    backup = backups[path]
                    if backup is None:
                        path.unlink(missing_ok=True)
                    else:
                        backup.replace(path)
                except OSError as exc:
                    failed.append(f"{path.relative_to(root)}: {exc}")
            if failed:
                retain_backup = True
                raise BuildError(f"Publication rollback incomplete; backups retained at {temporary}: " + "; ".join(failed))
            raise
    finally:
        if not retain_backup:
            try:
                shutil.rmtree(temporary)
            except OSError as exc:
                print(f"[WARN] Could not remove publication temporary files at {temporary}: {exc}")
    return set(changed), removed


def report_retained(retained: list[tuple[str, str]]) -> None:
    if not retained or os.environ.get("GITHUB_ACTIONS") != "true":
        return
    for index, url in retained:
        message = f"{index}: upstream returned 404/410; retaining last successful files ({url})"
        escaped = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print("::warning::" + escaped)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as output:
            output.write("\n### Retained upstream sources\n\n<ul>\n")
            for index, url in retained:
                label = html.escape(" ".join(index.splitlines()))
                address = html.escape(" ".join(url.splitlines()))
                output.write(f"<li>{label}: {address} (HTTP 404/410; last successful files retained)</li>\n")
            output.write("</ul>\n")


def reporting_self_test() -> None:
    with tempfile.TemporaryDirectory(prefix="ai-agent-retained-summary-") as temporary:
        summary = Path(temporary) / "ai-agent-summary.md"
        captured = io.StringIO()
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false", "GITHUB_STEP_SUMMARY": str(summary)}), contextlib.redirect_stdout(captured):
            report_retained([("source", "https://example.invalid/rules")])
        assert not summary.exists() and not captured.getvalue()
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_STEP_SUMMARY": str(summary)}), contextlib.redirect_stdout(captured):
            report_retained([])
            assert not summary.exists() and not captured.getvalue()
            report_retained([("first", "https://example.invalid/first"), ("bad%name\n::error::injected", "https://example.invalid/<script>\r\nsecond")])
        warnings = captured.getvalue().splitlines()
        assert len(warnings) == 2 and all(line.startswith("::warning::") for line in warnings)
        assert "bad%25name%0A::error::injected" in warnings[1] and "%0D%0A" in warnings[1]
        text = summary.read_text(encoding="utf-8")
        assert text.count("<li>") == 2 and "&lt;script&gt;" in text and "<script>" not in text
        captured = io.StringIO()
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_STEP_SUMMARY": ""}), contextlib.redirect_stdout(captured):
            report_retained([("first", "https://example.invalid/first")])
        assert captured.getvalue().startswith("::warning::")
        summary.unlink()
        root = Path(temporary) / "ai-agent-repository"
        selected = {"adrules": UPSTREAM_RULES["adrules"]}
        captured = io.StringIO()
        with patch.dict(UPSTREAM_RULES, selected, clear=True), patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_STEP_SUMMARY": str(summary)}), contextlib.redirect_stdout(captured):
            sync(root, lambda url: "example.test\n")
            assert not summary.exists() and "::warning::" not in captured.getvalue()
            before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            sync(root, lambda url: None)
            assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
            assert "[KEEP] adrules" in captured.getvalue() and "::warning::adrules:" in captured.getvalue()
            assert "adrules" in summary.read_text(encoding="utf-8")
    print("Retained-source reporting, local execution and command escaping checks passed.")


def sync(root: Path, fetch=download) -> None:
    selected = targets()
    candidates: dict[Path, bytes] = {}
    obsolete: set[Path] = set()
    sources = {}
    previous_sources = None
    retained = []
    urls = list(dict.fromkeys(url for _, url, _ in selected.values()))
    # Validate every source and format before changing outputs; licenses remain fixed copies.
    with ThreadPoolExecutor(max_workers=4) as executor:
        downloaded = dict(zip(urls, executor.map(fetch, urls)))
    for index, (name, url, kind) in selected.items():
        text = downloaded[url]
        expected = possible_output_paths(name, kind, url)
        split = kind in {"SurgeSplit", "DomainSet"}
        if text is None:
            # The manifest is only a record of the last successful download, never the inventory.
            if previous_sources is None:
                previous_path = root / "third_party/sources.json"
                if not previous_path.is_file():
                    raise BuildError(f"Missing upstream has no successful source record: {index}")
                previous_sources = json.loads(previous_path.read_text(encoding="utf-8"))
            previous = previous_sources.get(index, {})
            outputs = previous.get("outputs", {})
            valid_outputs = isinstance(outputs, dict) and "outputs" in previous and all(expected.get(key) == path for key, path in outputs.items())
            complete = outputs in ({}, expected)
            if previous.get("source") != url or previous.get("kind") != kind or not valid_outputs or (not split and not complete) or not all((root / "third_party" / path).is_file() for path in outputs.values()):
                raise BuildError(f"Missing upstream has no matching published copy: {index}")
            sources[index] = previous
            retained.append((index, url))
            print(f"[KEEP] {index}: upstream missing; retaining last successful files")
            continue
        notice = notice_path(url)
        native = kind in {"MrsDomain", "MrsIP"}
        if native:
            if not isinstance(text, bytes):
                raise BuildError(f"Expected native MRS bytes: {index}")
            converted = {"mrs": text} if validate_mrs(text, kind) else {}
        else:
            if not isinstance(text, str):
                raise BuildError(f"Expected text rules: {index}")
            converted = split_surge(text, kind) if split else convert(text, kind)
            converted = {key: content for key, content in converted.items() if key in expected}
        obsolete.update(root / "third_party" / path for group, path in expected.items() if group not in converted)
        sources[index] = {"source": url, "sha256": hashlib.sha256(text if native else text.encode("utf-8")).hexdigest(), "kind": kind, "notices": notice, "outputs": {key: expected[key] for key in converted}}
        for key, content in converted.items():
            if not native and (split or key != "sing-box"):
                content = f"# Converted by blacklist-rules; matching rules retain upstream ownership.\n# Source: {url}\n# Notices: third_party/{notice}\n".encode("utf-8") + content
            candidates[root / "third_party" / expected[key]] = content
    rule_count = len(candidates)
    candidates.update(reference_candidates(root, selected, sources))
    manifest = root / "third_party/sources.json"
    candidates[manifest] = (json.dumps(sources, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    written, removed = publish(root, candidates, obsolete)
    for path in candidates:
        if path in written and path != manifest:
            print(f"[OK] {path.relative_to(root)}")
    for path in sorted(removed):
        print(f"[REMOVE] {path.relative_to(root)}: type no longer contains rules")
    print(f"Checked {len(selected)} sources; generated {rule_count} rule files.")
    report_retained(retained)


@patch.dict(os.environ, {"GITHUB_ACTIONS": "false"})
def self_test() -> None:
    self_check()
    download_self_test()
    reporting_self_test()
    domain = convert('payload:\n  - "+.example.com"\n  - exact.test\n', "Domain")
    assert json.loads(domain["sing-box"])["rules"][0]["domain"] == ["example.com", "exact.test"]
    assert domain["surge"] == b".example.com\nexact.test\n"
    assert convert("192.0.2.1/24\n2001:db8::/32", "IP")["surge"] == b"IP-CIDR,192.0.2.0/24,no-resolve\nIP-CIDR6,2001:db8::/32,no-resolve\n"
    assert json.loads(convert("payload:\n - PROCESS-NAME,App.exe", "Process")["sing-box"])["rules"] == [{"process_name": ["App.exe"]}]
    classical = "# Upstream notice\nDOMAIN,exact.test\nDOMAIN-SUFFIX,example.com\nDOMAIN-KEYWORD,example\nIP-CIDR,192.0.2.0/24,no-resolve\nIP-CIDR6,2001:db8::/32\nIP-ASN,64500\nUSER-AGENT,Example*\nPROCESS-NAME,App\nOR,((DOMAIN,example.com),(IP-CIDR6,2001:db8::/32))\n"
    grouped = split_surge(classical, "SurgeSplit")
    assert set(grouped) == set(SURGE_RULE_GROUPS)
    assert grouped["Domain"] == b"# Upstream notice\nexact.test\n.example.com\n"
    assert grouped["IP"] == b"# Upstream notice\nIP-CIDR,192.0.2.0/24,no-resolve\nIP-CIDR6,2001:db8::/32\n"
    assert grouped["Logical"].endswith(b"OR,((DOMAIN,example.com),(IP-CIDR6,2001:db8::/32))\n")
    for expression in (
        "AND,((NOT,((SRC-IP,192.168.1.110))),(DOMAIN-SUFFIX,example.com))",
        "OR,((IP-ASN,44907,no-resolve),(IP-ASN,59930,no-resolve))",
        'OR,((URL-REGEX,"^https://example.com/(,foo"),(PROTOCOL,UDP))',
        "OR,((USER-AGENT,'Example,(foo'),(DEST-PORT,443))",
    ):
        assert split_surge(expression, "SurgeSplit")["Logical"] == (expression + "\n").encode("utf-8")
    nested = "DOMAIN,example.com"
    for _ in range(10):
        nested = f"NOT,(({nested}))"
    validate_logical(nested)
    for invalid in ("OR,((UNKNOWN,example.com))", "AND,((NOT,((FINAL,DIRECT))),(DOMAIN,example.com))", "NOT,((DOMAIN,a.test),(DOMAIN,b.test))", "OR,()", "OR,((DOMAIN,example.com),)", "NOT,((" + nested + "))"):
        try:
            split_surge(invalid, "SurgeSplit")
        except BuildError:
            pass
        else:
            raise AssertionError(f"Invalid logical sub-rule was accepted: {invalid}")
    assert sum(len([line for line in content.splitlines() if not line.startswith(b"#")]) for content in grouped.values()) == 9
    assert split_surge("# All rules removed", "SurgeSplit") == {}
    assert split_surge("# No domains\n", "DomainSet") == {}
    assert split_surge(".example.com\nexact.test", "DomainSet")["Domain"] == b".example.com\nexact.test\n"
    assert split_surge("DOMAIN-SUFFIX, example.com", "SurgeSplit")["Domain"] == b".example.com\n"
    assert convert("# All rules removed", "Domain") == {}
    assert convert("", "IP") == {}
    for kind in ("Domain", "IP", "Process"):
        for empty in ("payload: []\n", "payload: [ ] # All rules removed\n# Upstream note\n"):
            assert convert(empty, kind) == convert("", kind)
    for text, kind in [("<html>error</html>", "Domain"), ("example.com", "IP"), ("192.0.2.0/24", "Domain"), ("payload:\nother: value", "Domain"), ("payload: []\n - example.com", "Domain")]:
        try:
            convert(text, kind)
        except BuildError:
            continue
        raise AssertionError(f"Invalid {kind} source accepted")
    for text in ["<html>error</html>", "IP-CIDR,2001:db8::/32", "IP-ASN,invalid", "DOMAIN,example.com,extended-matching", "OR,((DOMAIN,example.com)", "UNKNOWN,example"]:
        try:
            split_surge(text, "SurgeSplit")
        except (ValueError, BuildError):
            continue
        raise AssertionError("Unsupported Surge content was silently accepted")
    with patch.object(Path, "read_text", side_effect=AssertionError("Rule inventory must not read client profiles or generated manifests")):
        selected = targets()
    assert selected["steam"][0] == "Steam_Domain" and selected["google_ip"][0] == "Google_IP"
    assert all(path == path.lower() for name, url, kind in selected.values() for path in possible_output_paths(name, kind, url).values())
    assert all(source_layout(name, kind, url)[0] == url.split("/")[3].lower() for name, url, kind in selected.values())
    assert {"openai", "cn_domain", "applications", "adrules"} <= selected.keys()
    assert all("_OCD_" not in name for name, _, _ in selected.values())
    mrs_domain = base64.b64decode("KLUv/QQA9QEAxAJNUlMBAAKwAAEAAGtVVVVVVAAAABdtdG9zY2UudGUubHRwY21hYXh4ZWUuKwYAIKBOcisjahJgIZfMaQF3VE62")
    mrs_ip = base64.b64decode("KLUv/QQAZQEARAFNUlMBAQACAAAAAP//wP8gAQ24/wkAOBMQwOcAYOhMEobaNM2JKpgxODhxl4bq")
    assert validate_mrs(mrs_domain, "MrsDomain") and validate_mrs(mrs_ip, "MrsIP")
    for content, kind in ((b"Not an MRS file", "MrsDomain"), (mrs_domain, "MrsIP")):
        try:
            validate_mrs(content, kind)
        except BuildError:
            pass
        else:
            raise AssertionError("Invalid native MRS file was accepted")
    samples = {url: {"Domain": "+.example.com", "IP": "192.0.2.0/24", "Process": "PROCESS-NAME,App.exe", "SurgeSplit": classical, "DomainSet": ".example.com", "MrsDomain": mrs_domain, "MrsIP": mrs_ip}[kind] for _, url, kind in selected.values()}

    def changed_sample(url: str, value: str) -> str | bytes:
        sample = samples[url]
        return sample if isinstance(sample, bytes) else sample.replace("example.com", value)
    with tempfile.TemporaryDirectory(prefix="ai-agent-third-party-") as temporary:
        publication = Path(temporary) / "ai-agent-publication"
        publication.mkdir()
        old_rule = publication / "third_party/surge/old.list"
        old_rule.parent.mkdir(parents=True)
        config = publication / "profile.conf"
        manifest = publication / "third_party/sources.json"
        original = {old_rule: b"old rules\n", config: b"old configuration\n", manifest: b"old manifest\n"}
        for path, content in original.items():
            path.write_bytes(content)
        new_rule = publication / "third_party/surge/new.list"
        candidates = {new_rule: b"new rules\n", config: b"new configuration\n", manifest: b"new manifest\n"}
        write_bytes, replace, unlink = Path.write_bytes, Path.replace, Path.unlink

        def fail_prepare(path: Path, content: bytes) -> int:
            if path.name.startswith("new-") and path.name.endswith("sources.json"):
                raise OSError("Simulated staging failure")
            return write_bytes(path, content)

        def fail_manifest(path: Path, target: Path) -> Path:
            if target == manifest:
                raise OSError("Simulated manifest replacement failure")
            return replace(path, target)

        def fail_delete(path: Path, *args, **kwargs) -> None:
            if path == old_rule:
                raise OSError("Simulated obsolete-file deletion failure")
            return unlink(path, *args, **kwargs)

        for method, failure in (("write_bytes", fail_prepare), ("replace", fail_manifest), ("unlink", fail_delete)):
            with patch.object(Path, method, failure):
                try:
                    publish(publication, candidates, {old_rule})
                except OSError:
                    pass
                else:
                    raise AssertionError("Publication failure was ignored")
            assert {path: path.read_bytes() for path in publication.rglob("*") if path.is_file()} == original
            assert not list(publication.glob("ai-agent-third-party-publish-*"))
        written, removed = publish(publication, candidates, {old_rule})
        assert written == set(candidates) and removed == {old_rule}
        assert {path: path.read_bytes() for path in publication.rglob("*") if path.is_file()} == candidates
        assert publish(publication, candidates, {old_rule}) == (set(), set())
        publish(publication, original, {new_rule})

        def fail_rollback(path: Path, target: Path) -> Path:
            if target == manifest or (path.name.startswith("old-") and target == config):
                raise OSError("Simulated replacement and rollback failure")
            return replace(path, target)

        with patch.object(Path, "replace", fail_rollback):
            try:
                publish(publication, candidates, {old_rule})
            except BuildError as exc:
                assert "rollback incomplete" in str(exc)
            else:
                raise AssertionError("Incomplete rollback was ignored")
        retained, = publication.glob("ai-agent-third-party-publish-*")
        backup, = retained.glob("old-*-profile.conf")
        assert backup.read_bytes() == original[config]
        backup.replace(config)
        shutil.rmtree(retained)
        assert {path: path.read_bytes() for path in publication.rglob("*") if path.is_file()} == original

        root = Path(temporary) / "ai-agent-existing"
        cold = Path(temporary) / "ai-agent-new-type"
        steam_key = "surge_ruleforocd_steam"
        profile = cold / "client_conf/surge_configuration/surge_configuration.conf"
        profile.parent.mkdir(parents=True)
        profile.write_text(f"[Rule]\n# > steam\nDOMAIN-SET, {SURGE_URL}surge/peiyingyao/steam/steam_domain.list, Custom Steam, update-interval=600\n# > next\nFINAL,Others\n", encoding="utf-8")
        for filename in ("README.md", "README.zh-cn.md"):
            document = cold / "third_party" / filename
            document.parent.mkdir(parents=True, exist_ok=True)
            document.write_text(f"<table>\n</table>\n<table>\n</table>\n<table>\n{TABLE_START}\n{TABLE_END}\n</table>\n", encoding="utf-8")
        with patch.dict(UPSTREAM_RULES, {steam_key: selected[steam_key]}, clear=True):
            sync(cold, lambda url: "DOMAIN-SUFFIX,example.com\n")
            process_path = cold / "third_party/surge/peiyingyao/steam/steam_process.list"
            assert not process_path.exists()
            assert len(list((cold / "third_party/surge").rglob("*.list"))) == 1
            assert "_process.list" not in profile.read_text(encoding="utf-8")
            sync(cold, lambda url: "DOMAIN-SUFFIX,example.com\nPROCESS-NAME,NewApp\n")
            assert process_path.read_bytes().endswith(b"PROCESS-NAME,NewApp\n")
            assert "_process.list, Custom Steam, update-interval=600" in profile.read_text(encoding="utf-8")
            assert "Process Only" in (cold / "third_party/README.md").read_text(encoding="utf-8")
            assert "仅进程" in (cold / "third_party/README.zh-cn.md").read_text(encoding="utf-8")
            before_missing = {path: path.read_bytes() for path in cold.rglob("*") if path.is_file()}
            sync(cold, lambda url: None)
            assert before_missing == {path: path.read_bytes() for path in cold.rglob("*") if path.is_file()}
            sync(cold, lambda url: "# All rules removed\n")
            assert not list((cold / "third_party/surge").rglob("*.list"))
            assert "third_party/surge/" not in profile.read_text(encoding="utf-8")
            assert "# Sync policy: Custom Steam, update-interval=600" in profile.read_text(encoding="utf-8")
            assert "RuleForOCD_Steam" not in (cold / "third_party/README.md").read_text(encoding="utf-8")
            sync(cold, lambda url: "IP-ASN,64500\n")
            assert len(list((cold / "third_party/surge").rglob("*.list"))) == 1
            assert "_asn.list, Custom Steam, update-interval=600" in profile.read_text(encoding="utf-8")
            assert "_domain.list" not in profile.read_text(encoding="utf-8")
            stable = {path: path.read_bytes() for path in cold.rglob("*") if path.is_file()}
            sync(cold, lambda url: "IP-ASN,64500\n")
            assert stable == {path: path.read_bytes() for path in cold.rglob("*") if path.is_file()}
        for index in ("adrules", "private_ip", "applications"):
            legacy = Path(temporary) / ("ai-agent-empty-" + index)
            name, source_url, kind = selected[index]
            stem = name.removesuffix("_" + kind)
            with patch.dict(UPSTREAM_RULES, {index: selected[index]}, clear=True):
                fixture_paths = possible_output_paths(name, kind, source_url)
            for relative, javascript in (("client_conf/mihomo_configuration/mihomo_configuration.yaml", False), ("client_conf/mihomo_override/mihomo_override.js", True)):
                client = legacy / relative
                client.parent.mkdir(parents=True, exist_ok=True)
                url = SURGE_URL + fixture_paths["clash"]
                text = f'const ruleProviders = {{\n  "{index}": {{\n    "url": "{url}"\n  }},\n}};\nconst rules = [\n  "RULE-SET, {index}, Custom Policy",\n];\n' if javascript else f'rules:\n  - RULE-SET, {index}, Custom Policy\nrule-providers:\n  {index}:\n    {{\n      url: "{url}"\n    }}\n'
                client.write_text(text, encoding="utf-8")
            for filename, chinese in (("README.md", False), ("README.zh-cn.md", True)):
                tables = []
                label = {"Domain": "仅域名", "IP": "仅 IP", "Process": "仅进程"}[kind] if chinese else kind + " Only"
                for fmt in ("sing-box", "clash", "surge"):
                    path = fixture_paths[fmt]
                    display = ("YAML · " if fmt == "clash" else "") + label
                    cells = [f'<a href="{base}{path}">{display}</a>' for base in ("https://raw.githubusercontent.com/Lolicandae/blacklist-rules/main/third_party/", SURGE_URL)]
                    row = f'  <tr align="center">\n    <td>{stem}</td>\n    <td>{cells[0]}</td>\n    <td>{cells[1]}</td>\n  </tr>\n'
                    tables.append("<table>\n" + row + (f"{TABLE_START}\n{TABLE_END}\n" if fmt == "surge" else "") + "</table>\n")
                document = legacy / "third_party" / filename
                document.parent.mkdir(parents=True, exist_ok=True)
                document.write_text("".join(tables), encoding="utf-8")
            with patch.dict(UPSTREAM_RULES, {index: selected[index]}, clear=True):
                sync(legacy, lambda url: samples[url])
                original = {path: path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
                sync(legacy, lambda url: "payload: []\n")
                assert all(not (legacy / "third_party" / path).exists() for path in possible_output_paths(name, kind, source_url).values())
                for relative, javascript in (("client_conf/mihomo_configuration/mihomo_configuration.yaml", False), ("client_conf/mihomo_override/mihomo_override.js", True)):
                    text = (legacy / relative).read_text(encoding="utf-8")
                    assert "Sync-disabled:" in text
                    active = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith(("#", "//")))
                    assert "RULE-SET" not in active and "third_party/clash/" not in active
                for filename in ("README.md", "README.zh-cn.md"):
                    assert '<a href=' not in (legacy / "third_party" / filename).read_text(encoding="utf-8")
                empty = {path: path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
                sync(legacy, lambda url: None)
                assert empty == {path: path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
                sync(legacy, lambda url: samples[url])
                assert original == {path: path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
        license_file = root / "third_party/licenses/AdRules/SCRIPT-LICENSE"
        license_file.parent.mkdir(parents=True)
        license_file.write_bytes(b"Fixed license copy\n")
        sync(root, samples.__getitem__)
        assert (root / "third_party/clash/cats-team/adrules/adrules_domain.mrs").read_bytes() == mrs_domain
        assert (root / "third_party/clash/cats-team/adrules/adrules_domain.yaml").is_file()
        assert (root / "third_party/surge/cats-team/adrules/adrules_domain.list").read_bytes().endswith(b"exact.test\n.example.com\n")
        assert license_file.read_bytes() == b"Fixed license copy\n"
        assert {path for path in (root / "third_party/licenses").rglob("*") if path.is_file()} == {license_file}
        before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        assert len(before) == sum(len(possible_output_paths(name, kind, url)) for name, url, kind in selected.values()) + 2
        assert not list((root / "third_party/clash").glob("*.yaml"))
        assert "surge" not in json.loads((root / "third_party/sources.json").read_text(encoding="utf-8"))["adrules"]["outputs"]

        try:
            sync(root, lambda url: b"Invalid native MRS" if url == selected["mrs_adrules"][1] else changed_sample(url, "changed.test"))
        except BuildError:
            pass
        else:
            raise AssertionError("Invalid native MRS did not stop publication")
        assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}

        with patch(__name__ + ".validate_mrs", return_value=False):
            sync(root, samples.__getitem__)
        assert not list((root / "third_party/clash").rglob("*.mrs"))
        assert all(json.loads((root / "third_party/sources.json").read_text(encoding="utf-8"))[index]["outputs"] == {} for index in selected if index.startswith("mrs_"))
        empty_native = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        sync(root, lambda url: None)
        assert empty_native == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        sync(root, samples.__getitem__)
        assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}

        sync(root, lambda url: "payload: []\n" if url == selected["adrules"][1] else samples[url])
        assert all(not (root / "third_party" / path).exists() for path in possible_output_paths("adrules_Domain", "Domain", selected["adrules"][1]).values())
        assert json.loads((root / "third_party/sources.json").read_text(encoding="utf-8"))["adrules"]["outputs"] == {}

        reduced = "# Upstream notice\nDOMAIN-KEYWORD,example\n"
        missing_url = selected["surge_ruleforocd_steam"][1]
        sync(root, lambda url: reduced if url == missing_url else samples[url])
        mirrored = root / "third_party/surge/peiyingyao/steam/steam_keyword.list"
        assert mirrored.read_text(encoding="utf-8").split("\n", 3)[3] == reduced
        cleared = root / "third_party/surge/peiyingyao/steam/steam_process.list"
        assert not cleared.exists()
        sync(root, lambda url: "# All rules removed" if url == missing_url else samples[url])
        assert not mirrored.exists()
        old_source = json.loads((root / "third_party/sources.json").read_text(encoding="utf-8"))["surge_ruleforocd_steam"]
        assert old_source["outputs"] == {}
        sync(root, lambda url: None if url == missing_url else changed_sample(url, "updated.test"))
        assert not mirrored.exists()
        assert json.loads((root / "third_party/sources.json").read_text(encoding="utf-8"))["surge_ruleforocd_steam"] == old_source
        assert b"updated.test" in (root / "third_party/clash/cats-team/adrules/adrules_domain.yaml").read_bytes()
        before = {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
        sync(root, lambda url: None)
        assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}

        unpublished = root / "ai-agent-unpublished"
        try:
            sync(unpublished, lambda url: None)
        except BuildError:
            pass
        else:
            raise AssertionError("Missing source without a published copy was accepted")
        assert not unpublished.exists()

        def fail_one(url: str) -> str:
            if url == selected["openai"][1]:
                raise OSError("Simulated download failure")
            return changed_sample(url, "changed.test")

        try:
            sync(root, fail_one)
        except OSError:
            pass
        else:
            raise AssertionError("Download failure was ignored")
        assert before == {path: path.read_bytes() for path in root.rglob("*") if path.is_file()}
    repository_self_test()
    print("Fixed inventory, three-format conversion, complete type splitting, upstream deletion and missing-source retention passed.")


@patch.dict(os.environ, {"GITHUB_ACTIONS": "false"})
def repository_self_test() -> None:
    for text in ("payload:\n  - exact.test\n  - .example.com\n", '# Rules\r\npayload:\r\n  # Wildcard\r\n  - "*.example.com"\r\n'):
        validate_rule_file(text.encode("utf-8"), "Domain", "clash")
    for text, kind in (("payload:\n  - *.example.com\n", "Domain"), ("payload:\n- example.com\n", "Domain"), ("payload:\n    - example.com\n", "Domain"), ("payload:\n  - true\n", "Domain"), ("payload:\n  - null\n", "Domain"), ("payload:\n  - 123\n", "Domain"), ("payload:\n  - 0x12\n", "Domain"), ("payload:\n  - .inf\n", "Domain"), ("payload:\n  - 2026-10-06\n", "Domain"), ("payload:\n  - [example.com]\n", "Domain"), ("payload:\n  - {domain: example.com}\n", "Domain"), ("payload:\n  - &name example.com\n", "Domain"), ("payload:\n  - !!str example.com\n", "Domain"), ("payload:\n  - PROCESS-NAME,App: Name\n", "Process"), ("payload:\n  - PROCESS-NAME,App # note\n", "Process")):
        try:
            validate_rule_file(text.encode("utf-8"), kind, "clash")
        except BuildError:
            pass
        else:
            raise AssertionError(f"Invalid original YAML syntax accepted: {text}")
    selected = {index: UPSTREAM_RULES[index] for index in ("private_domain", "mrs_private_domain", "private_ip", "applications", "surge_ruleforocd_steam")}
    mrs = base64.b64decode("KLUv/QQA9QEAxAJNUlMBAAKwAAEAAGtVVVVVVAAAABdtdG9zY2UudGUubHRwY21hYXh4ZWUuKwYAIKBOcisjahJgIZfMaQF3VE62")
    samples = {url: {"Domain": ".example.com", "IP": "192.0.2.0/24", "Process": "PROCESS-NAME,App.exe", "SurgeSplit": "DOMAIN-SUFFIX,example.com\nDOMAIN-KEYWORD,example\n", "MrsDomain": mrs}[kind] for _, url, kind in selected.values()}
    native_links = True
    with tempfile.TemporaryDirectory(prefix="ai-agent-repository-check-") as temporary, patch.dict(UPSTREAM_RULES, selected, clear=True), patch(__name__ + ".urlopen", side_effect=AssertionError("Offline checks must not download")), contextlib.redirect_stdout(io.StringIO()):
        root = Path(temporary)
        for notice in {notice_path(url) for _, url, _ in selected.values()}:
            path = root / "third_party" / notice
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Fixture upstream notice\n", encoding="utf-8")
        for javascript, relative in ((False, "client_conf/mihomo_configuration/mihomo_configuration.yaml"), (True, "client_conf/mihomo_override/mihomo_override.js")):
            providers, rules = [], []
            for index, (name, url, kind) in selected.items():
                if kind not in {"Domain", "IP", "Process"}:
                    continue
                native = "mrs_" + index in selected
                target_name, target_url, target_kind = selected["mrs_" + index] if native else (name, url, kind)
                path = possible_output_paths(target_name, target_kind, target_url)["mrs" if native else "clash"]
                template = "ruleProviderMrs" if native else "ruleProviderYaml"
                behavior = {"Domain": "domain", "IP": "ipcidr", "Process": "classical"}[kind]
                cache = "./ruleset/paloexiz/third_party/" + path.removeprefix("clash/")
                if javascript:
                    providers.append(f'  "{index}": {{\n    ...{template},\n    "behavior": "{behavior}",\n    "url": "{SURGE_URL}{path}",\n    "path": "{cache}"\n  }},\n')
                    rules.append(f'  "RULE-SET, {index}, Custom Policy",\n')
                else:
                    providers.append(f'  {index}:\n    {{\n      <<: *{template},\n      behavior: {behavior},\n      url: "{SURGE_URL}{path}",\n      path: "{cache}",\n    }}\n')
                    rules.append(f'  - RULE-SET, {index}, Custom Policy\n')
            text = ('const ruleProviderYaml = {\n  "type": "http",\n  "format": "yaml",\n  "interval": 86400\n};\nconst ruleProviderMrs = {\n  "type": "http",\n  "format": "mrs",\n  "interval": 86400\n};\nconst ruleProviders = {\n' + "".join(providers) + '};\nconst rules = [\n' + "".join(rules) + '];\n') if javascript else ('rules:\n' + "".join(rules) + 'rule-anchor:\n  ruleProviderYaml: &ruleProviderYaml { type: http, interval: 86400, format: yaml }\n  ruleProviderMrs: &ruleProviderMrs { type: http, interval: 86400, format: mrs }\nrule-providers:\n' + "".join(providers))
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_text(text, encoding="utf-8")
        profile = root / "client_conf/surge_configuration/surge_configuration.conf"
        profile.parent.mkdir(parents=True)
        profile.write_text(f"[Rule]\n# > steam\nDOMAIN-SET, {SURGE_URL}surge/peiyingyao/steam/steam_domain.list, Custom Steam\n", encoding="utf-8")
        stems = dict.fromkeys(name.removesuffix("_" + kind) for name, _, kind in selected.values() if kind in {"Domain", "IP", "Process"})
        for filename in ("README.md", "README.zh-cn.md"):
            table = "<table>\n" + "".join(f'  <tr align="center">\n    <td>{stem}</td>\n    <td></td>\n    <td></td>\n  </tr>\n' for stem in stems)
            (root / "third_party" / filename).write_text(table + "</table>\n" + table + "</table>\n" + table + TABLE_START + "\n" + TABLE_END + "\n</table>\n", encoding="utf-8")
        sync(root, samples.__getitem__)

        def snapshot() -> dict:
            return {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}

        def check() -> None:
            before = snapshot()
            validate_repository(root)
            assert snapshot() == before, "Offline validation changed repository files"

        def reject(relative: str, content: bytes | None) -> None:
            path = root / relative
            original = path.read_bytes() if path.is_file() else None
            if content is None:
                path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            before = snapshot()
            try:
                validate_repository(root)
            except BuildError as exc:
                assert relative in str(exc), (relative, str(exc))
            else:
                raise AssertionError(f"Invalid repository accepted: {relative}")
            assert snapshot() == before, "Failed validation changed repository files"
            if original is None:
                path.unlink()
            else:
                path.write_bytes(original)

        check()
        for relative in ("client_conf/mihomo_configuration/mihomo_configuration.yaml", "client_conf/mihomo_override/mihomo_override.js", "client_conf/surge_configuration/surge_configuration.conf", "third_party/README.md", "third_party/README.zh-cn.md"):
            path = root / relative
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        check()
        yaml = "third_party/clash/metacubex/private/private_domain.yaml"
        reject(yaml, None)
        reject(yaml, b"")
        reject(yaml, b"payload:\n  - 192.0.2.0/24\n")
        reject(yaml, b"payload:\n  - *.example.com\n")
        reject(yaml, b"payload:\n  - -\n")
        reject("third_party/sing-box/metacubex/private/private_domain.json", b'{"version":3,"rules":[{"ip_cidr":["192.0.2.0/24"]}]}')
        reject("third_party/surge/peiyingyao/steam/steam_keyword.list", b"IP-ASN,64500\n")
        reject("third_party/clash/metacubex/private/private_domain.mrs", b"Invalid native MRS\n")
        reject("third_party/clash/unregistered.yaml", b"payload:\n  - example.com\n")
        path = root / yaml
        original = path.read_bytes()
        target = root / "ai-agent-valid-domain.yaml"
        target.write_bytes(original)
        path.unlink()
        try:
            path.symlink_to(target)
        except OSError:
            native_links = False
            path.write_bytes(original)
        before = snapshot()
        is_symlink = Path.is_symlink
        with contextlib.nullcontext() if native_links else patch.object(Path, "is_symlink", autospec=True, side_effect=lambda checked: checked == path or is_symlink(checked)):
            try:
                validate_repository(root)
            except BuildError as exc:
                assert yaml in str(exc) and "linked" in str(exc)
            else:
                raise AssertionError("Linked committed rule file was accepted")
        assert snapshot() == before, "Linked-file validation changed repository files"
        path.unlink()
        path.write_bytes(original)
        target.unlink()
        manifest = "third_party/sources.json"
        original_sources = json.loads((root / manifest).read_text(encoding="utf-8"))
        for field, value in (("source", "https://example.com/invalid"), ("kind", "IP"), ("notices", "../outside"), ("sha256", "invalid"), ("outputs", {"clash": "../outside.yaml"})):
            changed = json.loads(json.dumps(original_sources))
            changed["private_domain"][field] = value
            reject(manifest, json.dumps(changed).encode("utf-8"))
        changed = json.loads(json.dumps(original_sources))
        changed["surge_ruleforocd_steam"]["outputs"] = {"unknown": None}
        reject(manifest, json.dumps(changed).encode("utf-8"))
        changed = json.loads(json.dumps(original_sources))
        changed.pop("applications")
        reject(manifest, json.dumps(changed).encode("utf-8"))
        changed = json.loads(json.dumps(original_sources))
        changed["mrs_private_domain"]["sha256"] = "0" * 64
        # MRS failures name the actual binary and the mismatched record.
        (root / manifest).write_text(json.dumps(changed), encoding="utf-8")
        before = snapshot()
        try:
            validate_repository(root)
        except BuildError as exc:
            assert "private_domain.mrs" in str(exc) and "mrs_private_domain" in str(exc)
        else:
            raise AssertionError("MRS hash mismatch was accepted")
        assert snapshot() == before, "Failed MRS validation changed repository files"
        (root / manifest).write_text(json.dumps(original_sources), encoding="utf-8")
        for relative in ("client_conf/mihomo_configuration/mihomo_configuration.yaml", "client_conf/mihomo_override/mihomo_override.js"):
            original = (root / relative).read_bytes()
            for before, after in ((b"private_domain.mrs", b"wrong.mrs"), (b"behavior: domain", b"behavior: ipcidr") if relative.endswith(".yaml") else (b'"behavior": "domain"', b'"behavior": "ipcidr"'), (b"format: mrs", b"format: yaml") if relative.endswith(".yaml") else (b'"format": "mrs"', b'"format": "yaml"')):
                reject(relative, original.replace(before, after, 1))
            reject(relative, original.replace(b"RULE-SET, private_domain, Custom Policy", b"RULE-SET, unknown_provider, Custom Policy", 1))
            reject(relative, None)
        relative = "client_conf/surge_configuration/surge_configuration.conf"
        reject(relative, (root / relative).read_bytes().replace(b"DOMAIN-SET", b"RULE-SET", 1))
        reject("third_party/README.md", (root / "third_party/README.md").read_bytes().replace(b"https://raw.githubusercontent.com/", b"https://example.com/", 1))
        reject("third_party/README.zh-cn.md", None)
        sync(root, samples.__getitem__)
        old = snapshot()
        sync(root, lambda url: None)
        check()
        assert snapshot() == old, "Valid retained upstream copies changed"
        with patch(__name__ + ".validate_mrs", return_value=False):
            sync(root, lambda url: "payload: []\n" if url == selected["private_domain"][1] else "# All rules removed\n" if url == selected["surge_ruleforocd_steam"][1] else samples[url])
        check()
    print("Offline repository checks passed: files, manifest, native MRS, references, CRLF, empty outputs and retained copies.")
    if not native_links:
        print("Native symlink creation unavailable; linked-file rejection tested with a controlled path predicate.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--check", action="store_true", help="Validate committed files and references offline without writing")
    mode.add_argument("--check-self-test", action="store_true", help="Run isolated offline-validation checks")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        elif args.check_self_test:
            repository_self_test()
        elif args.check:
            validate_repository(ROOT)
        else:
            sync(ROOT)
    except (OSError, UnicodeError, ValueError, BuildError) as exc:
        parser.exit(1, f"[ERROR] {exc}\n")


if __name__ == "__main__":
    main()
