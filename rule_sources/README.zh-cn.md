# 规则源文件维护说明

**语言选择：[English](README.md) | 简体中文**

这里是手动维护规则条目的入口。需要改规则时，先改本目录里的 `*.rules`。PR 和其他分支的推送只校验生成结果，不写入文件，无需预先提交产物。变更进入 `main` 后，GitHub Actions 先校验，再构建 Clash / Surge / sing-box 产物并提交。

## 基本格式

```text
## ApplicationService
### google
cable.ua5v.com # Google Authenticator.
doodles.google # Currently blocked.
+.jotform.com # Form builder.

## Game
### pokemonmasters
! 3b8d4a717682c1cc5839b50bc93667cf.baas.nintendo.com # Disabled note.
```

## 写法约定

- `## <category>` 表示顶层分类，生成时会变成 `# /*<category>*/`。
- `### <group>` 表示分组，生成时会变成 `# <group>`。
- 普通行表示启用条目，支持域名、IP、`PROCESS-NAME,...`。
- `! <entry>` 表示禁用条目。
- 行尾 `# note` 是维护备注，只会输出到 Clash；Surge 只输出规则本体。
- `+.` 在 Clash 中原样保留，在 Surge 中会转换为 `.domain`。
- sing-box 输出原生 JSON，保留精确域名、后缀和单标签通配符语义；`PROCESS-NAME,...` 转换为 `process_name`。禁用条目及注释不输出。
- 在 `rules.build.json` 的 Clash 输出中设置 `"mrs": "domain"` 或 `"mrs": "ipcidr"`，会在 YAML 旁生成同名 `.mrs` 文件。进程规则保留 YAML；MRS 不包含注释和禁用条目。
- 不要直接手改生成产物；需要改规则就改这里的源文件。

## 本地校验

这些命令不是日常流程的必需步骤。推送前想检查生成结果，或排查构建问题时再运行。

构建使用 Mihomo v1.19.32。请将可执行文件加入 `PATH`，或先设置 `MIHOMO_BIN`：

```powershell
$env:MIHOMO_BIN = "C:\path\to\mihomo.exe"
python workflow_scripts/build_rules.py --self-test
python workflow_scripts/build_rules.py --validate
python workflow_scripts/build_rules.py
python workflow_scripts/build_rules.py --check
```

`--validate` 校验源文件生成的候选，包括 MRS 转换，不写文件，也不要求现有产物已同步。`--check` 则比较候选与已有产物是否一致。自动发布只在 `main` 执行，手动运行也遵循此限制；手动选择其他分支时只做校验。
