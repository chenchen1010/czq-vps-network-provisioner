---
name: czq-vps-network-provisioner
description: 将用户提供的海外 Linux VPS 配置为可审计、可回滚的 x-ui/Xray 网络节点，首次交付可登录的面板信息、带国内外分流的个人 HTTPS Clash/Mihomo 订阅及真实联网验收，另提供本地 YAML 备份。用于新装或修复 3x-ui、VLESS TCP/RAW Reality Vision、端口与公网链路故障、Xray/Mihomo 兼容性、Google/YouTube/TikTok/Facebook/Instagram/Claude/ChatGPT/Gemini/Grok 连通性和出口 IP 验收。不要把服务启动、端口监听或 YAML 语法通过误报为端到端可用。
---

# VPS 配网与 Mac Clash 节点交付

把“服务器服务”“公网路径”“客户端协议”“规则分流”“目标网站”和“账号登录”作为独立验收层。只有最后一层实际通过，才能报告对应层完成。

## 首次交付的默认范围

用户要求“配置成 x-ui/VLESS Reality 节点”时，首次配置默认包含：可登录的 HTTPS 管理面板和私人登录信息交接、原生 Clash/Mihomo HTTPS 订阅、国内直连/海外走节点的统一分流，以及新建独立客户端的订阅联网验收。不能只交本地 YAML，等用户追问才开启订阅或提供面板信息。

用户明确只要本地文件、只排障或保留既有配置时，以其范围为准；已有环境先识别现状，保留其他账号、路径和服务。授权、预览和发布约束仍按当前会话执行。

## 使用边界

- 只用于用户拥有或明确授权管理的服务器和客户端。
- 支持正常访问海外网站、社媒和 AI 服务；不帮助绕过账号处罚、批量欺诈、平台安全控制或地区法律。
- 数据中心 VPS 只能提供固定机房出口，不能冒充住宅网络，也不能保证社媒或 AI 账号风控放行。
- 不在生产服务器编译 Xray、3x-ui 或前端。使用官方预编译产物，在本机下载和校验后上传。
- 不把服务器地址、SSH 密码、私钥、UUID、Reality 私钥、公钥、Short ID、面板凭证或分享链接写进本 Skill、Git、README、PROJECT_MEMORY 或聊天回复。

## 必需输入

先从用户请求和当前项目中解析，无法确定时才询问：

- VPS 地址、SSH 用户以及密码或密钥路径。
- VPS 是否承载其他生产服务，操作系统与 CPU 架构。
- 是否已有 3x-ui/x-ui、Xray、证书、域名或现有节点。
- 客户端：默认 macOS + Clash Verge Rev/Mihomo；其他客户端需单独适配。
- 目标流量：默认海外社媒、YouTube、Claude、ChatGPT/Codex、Gemini、Grok。
- 是否需要代为在用户 Mac 中导入和启用；默认交付订阅、备用 YAML 和使用说明，不自动切换系统网络。

## 凭证落盘

1. 优先使用项目已有 `.env.local`；没有约定时使用当前项目根目录 `.env.local`。
2. 写入前确认 `.env.local` 被 `.gitignore` 忽略；权限设为 `600`。
3. 推荐变量：
   - `VPS_SSH_HOST`
   - `VPS_SSH_USER`
   - `VPS_SSH_PASSWORD` 或 `VPS_SSH_KEY_PATH`
4. VLESS 分享链接保存在独立的 `client-share.env`，变量名为 `VLESS_SHARE_LINK`，权限 `600`。
5. 命令行、日志和最终回复不得输出凭证值。不要把完整分享链接放进 shell 参数、公开日志、进程列表或聊天。
6. 面板信息保存到同一 `.env.local`：`XUI_PANEL_URL`、`XUI_PANEL_USER`、`XUI_PANEL_PASSWORD`；客户端订阅另存 `XUI_TEST_SUB_ID`、`XUI_TEST_UUID`、`XUI_TEST_CLASH_SUB_URL`。
7. 创建 Git 忽略、权限 `600` 的私人交接文件，写入完整面板链接（含端口和随机路径）、用户名、密码及用途；实际验证 HTTPS 和登录后，最终回复提供该文件的可点击本地链接。不能以“不在聊天输出凭证”为由漏交面板信息。用户明确指定私密文档时才写入该目的地，不默认外发。

## Gate 1：只读勘察

任何安装或改动前先记录：

```bash
uname -m
cat /etc/os-release
systemctl is-active x-ui || true
ss -lntp
df -h
free -h
```

同时检查防火墙、已有 3x-ui/x-ui 数据库、Xray 二进制版本、面板端口、订阅端口和现有业务端口。不得覆盖已有服务或数据库。

若服务器已有 x-ui，优先复用并备份，不重复安装。

## Gate 2：安装或复用 3x-ui

官方安装资料：<https://github.com/MHSanaei/3x-ui/wiki/Installation>

### 新装

- 只使用官方发布源。
- 面板用户名、密码、路径和端口使用随机值。
- 面板凭证仅保存到服务器 root-only 文件和项目 `.env.local` 及私人交接文件。
- 启用 systemd，重启后检查 `systemctl is-active x-ui`。

### 已安装

备份至少包括：

- x-ui 数据库。
- 当前 Xray 二进制与 SHA-256。
- 当前生成的 Xray 配置。
- 面板证书和必要设置。

备份文件使用显式、可审计的名称，不覆盖上一个备份。数据库修改前停止 x-ui，失败时恢复数据库并重启。

## Gate 3：Xray/Mihomo 版本兼容

同时读取：

```bash
/path/to/xray version
/Applications/Clash\ Verge.app/Contents/MacOS/verge-mihomo -v
```

已知事故：Xray `26.7.11` 与 Mihomo `1.19.28`/`1.19.29` 的 VLESS Reality 可能持续报 `REALITY authentication failed`。相关上游报告：<https://github.com/XTLS/Xray-core/issues/6477>

处理原则：

1. 不把最新版等同于兼容版。
2. 先查看上游发行说明和兼容问题，再选版本。
3. 对上述组合，优先使用已验证的 Xray `26.6.27`，直到新的组合完成真实回归。
4. 官方压缩包必须在本机下载，同时下载 `.dgst`，SHA-256 一致后解压上传。
5. 上传为 `.new` 文件，先执行版本和配置测试，再备份旧二进制、原子替换、重启和健康检查。
6. 新版本不健康时立即恢复旧二进制。不要删除回滚备份。
7. 禁止仅凭 GitHub issue 或版本号宣布修复；还必须完成 Gate 7 的真实 Mihomo 测试。

## Gate 4：创建 VLESS Reality 节点

默认兼容配置：

- 协议：VLESS。
- 传输：TCP/RAW。
- 安全：Reality。
- Flow：`xtls-rprx-vision`。
- UDP：开启。
- 客户端指纹：`chrome`。
- 独立 UUID、Reality 密钥和偶数长度 Short ID。

Reality 官方字段规范：<https://xtls.github.io/en/config/transports/reality.html>

Reality `target` 和 `serverNames` 必须匹配目标站点证书行为。使用 `xray tls ping <target>` 检查，不要随意选择 Cloudflare 等可能让服务器成为公共回落转发器的目标。

`mldsa65Seed` 是可选字段。诊断时检查值是否非空，不要因为 JSON 中存在这个键就认定已启用。空字符串等同未启用。

## Gate 5：端口与公网路径

端口监听不代表公网可用。候选端口必须避开 SSH、面板、订阅和其他业务。

依次验证：

1. Xray 配置测试通过。
2. 服务端本机监听。
3. 服务端本机通过 Reality 回环访问 Google/YouTube。
4. Mac 从外部网络访问同一端口。

关键判断：

- 若服务端回环成功、Mac 外部失败并出现 `received real certificate`、`potential MITM or redirection` 或 Reality 认证失败，优先判断公网端口路径被机房、防火墙、运营商或中间设备重定向。
- 不要继续反复改 UUID、公钥和规则。
- 使用临时端口做 A/B 测试；每次只改变端口，其他配置保持一致。
- `443`、`8443` 或任何常见端口都不能假定可用。选择实际外部测试成功且防火墙允许的端口。
- 临时监听验证后必须关闭，清理临时配置和 PID 文件。

不得把一次事故中成功的 `24443` 硬编码为所有服务器默认端口；它只是候选值，必须现场验证。

## Gate 6：默认启用原生 HTTPS 订阅与统一分流

首次配置必做，按 [面板交接与原生订阅](references/panel-and-subscription.md) 完成：

- 核对实际版本，启用订阅总开关和 Clash/Mihomo 输出；为独立订阅监听器配置有效 HTTPS、空闲端口和外部可达路径，不能把面板 HTTPS 当成订阅 HTTPS。
- 配置统一分流模板：局域网/国内直连，社媒、YouTube、AI 和其他海外走节点。模板不含 `proxies`、UUID 或个人订阅 ID；每个账号的节点由面板生成。默认规则模式不代表已配置分流。
- 保存并按该版本要求重启，回读持久化设置，核对面板客户端信息中可复制的 CLASH/Mihomo 地址；客户端自动识别可作为补充，不代替专用地址验收。
- 先登录面板确认可用，再交付私人登录信息；不要让用户反复索要链接、用户名和密码。

生成不含节点凭证的统一分流模板：

```bash
node scripts/generate_clash_profile.mjs \
  --subscription-template \
  --out /secure/path/subscription-routing.yaml
```

将模板用于面板的 Clash/Mihomo 全局路由配置。此命令只生成本地文件，不连接面板或保存服务器设置；仍须完成上述配置与 Gate 7。

### 本地 YAML 作为备份或明确要求的文件交付

从 root-only 的 VLESS 分享文件生成，不手抄公钥或 UUID：

```bash
node scripts/generate_clash_profile.mjs \
  --env /secure/path/client-share.env \
  --out /secure/path/Mac-Clash-Verge-x-ui.yaml
```

生成独立测试配置时：

```bash
node scripts/generate_clash_profile.mjs \
  --env /secure/path/client-share.env \
  --out /secure/path/Mac-Clash-Verge-x-ui-test.yaml \
  --test \
  --mixed-port 17900
```

生成器会创建以下规则组：

- `节点选择`
- `海外社媒`
- `YouTube`
- `AI 工具`
- `其他海外`

默认分流：局域网与中国大陆直连；TikTok、Facebook、Instagram、X、YouTube、Claude、OpenAI/ChatGPT/Codex、Gemini 和 Grok 走 VPS；其他海外流量走 VPS。

YAML 含节点凭证，权限必须是 `600`，不得上传公共网盘或 Git。

## Gate 7：真实 Mihomo 验收

默认新建一个明确命名的独立验收客户端，使用独立 UUID/订阅 ID，关联已有正式入站；流量额度按用户要求，未指定时可用 50 GB 的有限额度并记录有效期策略。不要借用管理员设备账号替代新员工流程，也不要重置其流量。测试账号的最终状态应告知用户；不要擅自删除或重新启用用户已停用的账号。

从该账号的公网 HTTPS CLASH/Mihomo 地址下载实际订阅，不关闭证书验证。确认只含该账号节点、代理组引用有效、国内直连及海外规则存在；若启用自动识别，另外测试标准 SUB 地址。以这份下载内容进行以下语法与联网测试，不能拿另行生成或手修节点参数的 YAML 冒充订阅验收。

测试副本仅调整本地监听端口、关闭 TUN、必要的日志/测试网络绑定；记录差异，不把设备网卡名写入通用订阅。核对测试账号在 Xray 实际配置中已生效。

### 语法

```bash
scripts/validate_mihomo_profile.sh /secure/path/Mac-Clash-Verge-x-ui.yaml
```

`configuration test is successful` 只表示语法与字段可加载，不表示节点可用。

### 外部链路

原生订阅使用下载内容的测试副本；仅本地文件任务可使用生成器的 `--test` 配置。在独立端口启动 Mihomo，不切换用户现有系统代理：

```bash
/Applications/Clash\ Verge.app/Contents/MacOS/verge-mihomo \
  -d /secure/test-data \
  -f /secure/path/Mac-Clash-Verge-x-ui-test.yaml
```

另一终端执行：

```bash
scripts/probe_proxy.sh http://127.0.0.1:17900 EXPECTED_EXIT_IP
```

必须检查：

- Google `generate_204`。
- YouTube `generate_204`。
- TikTok、Facebook、Instagram。
- ChatGPT、Claude、Gemini、Grok。
- 实际出口 IP 是否等于 VPS 公网 IP。
- 至少一个国内网站的请求确实命中 `DIRECT`，不能只看页面打开。
- 新验收客户端上传/下载计数是否增长，不能只看入站总流量。
- Mihomo 日志是否仍有 `REALITY authentication failed`、`received real certificate`、超时或连接错误。

若本机已有 TUN，先检查到 VPS 的系统路由：独立测试程序可能被已有代理再次接管。对比原有已验收配置，必要时仅在测试副本中绑定实际物理网卡；不要立即改服务器密钥、端口或用户系统代理。测试后停止独立进程。详见订阅参考中的诊断顺序。

状态解释：

- HTTP `200`、`204`、正常 `3xx`：链路可达。
- HTTP `403`：通常已成功到站，但可能被访客、机器人或数据中心 IP 风控；不能报告账号登录成功。
- HTTP `000`、TLS 错误、超时：链路未通过。
- 只有浏览器中实际完成登录并保持会话，才能报告“账号登录成功”。

## Gate 8：Mac 导入与启用

若用户只要文件，到此交付 YAML 和导入步骤，不修改系统网络。

若用户要求代为导入：

1. 使用 Computer Use 检查 Clash Verge 当前配置，保留旧配置作为回退。
2. 优先导入已验收的个人 HTTPS 订阅；明确的文件任务导入备用 YAML。不要覆盖用户其他订阅。
3. 切换配置、启用 TUN 或系统代理属于网络设置变更；按 Computer Use 规则在动作发生前请求确认。
4. 切换后重新执行目标站点和出口 IP 测试。
5. 新配置失败时切回旧配置，不删除用户原配置。

## 停止条件

出现以下任一项不得报告完整首次交付完成（明确缩小范围的任务按其范围报告）：

- 面板信息未安全交接，或未验证面板 HTTPS 和登录。
- 原生订阅未启用、未通过公网 HTTPS 验收，或面板没有可复制的个人 CLASH/Mihomo 链接。
- 订阅缺少分流，或使用手工修过的节点 YAML 代替服务器实际输出。
- 未用独立客户端确认个人节点隔离、真实联网及流量计数。
- Xray/Mihomo 版本未知或兼容性未验证。
- 分享链接与服务器当前配置不一致。
- `REALITY authentication failed`。
- `received real certificate` 或 `potential MITM or redirection`。
- 服务端回环通过但外部端口未测试。
- 出口 IP 不匹配。
- 只通过 YAML 语法检查。
- 只看到端口监听、HTTP 403 或应用启动。
- 用户导入的是旧端口的本地配置快照。

## 故障案例

遇到 Reality 认证、443/8443 不通或“本机正常、外部失败”时，先读：

- [Reality/Mihomo 双重故障复盘](references/reality-mihomo-port-path-incident.md)

## 交付报告

按以下层级分别报告，禁止混称：

1. 服务器安装/复用和备份。
2. Xray 版本、配置测试和服务状态。
3. 正式公网端口与监听。
4. 外部 Mihomo Reality 握手。
5. Google/YouTube/社媒/AI 网站响应。
6. 出口 IP。
7. 面板 HTTPS、登录验证及私人交接文件位置。
8. 个人 HTTPS Clash/Mihomo 订阅、分流和独立验收账号的状态、额度、流量证据。
9. Mac 订阅或备用 YAML 的实际导入、启用状态（独立内核测试不等于已替用户导入）。
10. 浏览器账号登录状态。

列出保留的回滚备份，但不要暴露任何凭证、完整 URL 或节点参数。
