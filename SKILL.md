---
name: czq-vps-network-provisioner
description: 将用户提供的海外 Linux VPS 配置为可审计、可回滚的 x-ui/Xray 网络节点，并为 macOS Clash Verge/Mihomo 生成带海外社媒与 AI 工具分流规则的 VLESS Reality YAML。用于新装或修复 3x-ui、VLESS TCP/RAW Reality Vision、端口与公网链路故障、Xray/Mihomo 兼容性、Google/YouTube/TikTok/Facebook/Instagram/Claude/ChatGPT/Gemini/Grok 连通性和出口 IP 验收。不要把服务启动、端口监听或 YAML 语法通过误报为端到端可用。
---

# VPS 配网与 Mac Clash 节点交付

把“服务器服务”“公网路径”“客户端协议”“规则分流”“目标网站”和“账号登录”作为独立验收层。只有最后一层实际通过，才能报告对应层完成。

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
- 是否仅交付 YAML，还是还要在用户 Mac 中导入和启用。

## 凭证落盘

1. 优先使用项目已有 `.env.local`；没有约定时使用当前项目根目录 `.env.local`。
2. 写入前确认 `.env.local` 被 `.gitignore` 忽略；权限设为 `600`。
3. 推荐变量：
   - `VPS_SSH_HOST`
   - `VPS_SSH_USER`
   - `VPS_SSH_PASSWORD` 或 `VPS_SSH_KEY_PATH`
4. VLESS 分享链接保存在独立的 `client-share.env`，变量名为 `VLESS_SHARE_LINK`，权限 `600`。
5. 命令行、日志和最终回复不得输出凭证值。不要把完整分享链接放进 shell 参数、URL、进程列表或聊天。

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
- 面板凭证仅保存到服务器 root-only 文件和项目 `.env.local`。
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
7. 禁止仅凭 GitHub issue 或版本号宣布修复；还必须完成 Gate 6 的真实 Mihomo 测试。

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

## Gate 6：生成 Clash Verge YAML

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

### 语法

```bash
scripts/validate_mihomo_profile.sh /secure/path/Mac-Clash-Verge-x-ui.yaml
```

`configuration test is successful` 只表示语法与字段可加载，不表示节点可用。

### 外部链路

用 `--test` 配置在独立端口启动 Mihomo，不切换用户现有系统代理：

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
- Mihomo 日志是否仍有 `REALITY authentication failed`、`received real certificate`、超时或连接错误。

状态解释：

- HTTP `200`、`204`、正常 `3xx`：链路可达。
- HTTP `403`：通常已成功到站，但可能被访客、机器人或数据中心 IP 风控；不能报告账号登录成功。
- HTTP `000`、TLS 错误、超时：链路未通过。
- 只有浏览器中实际完成登录并保持会话，才能报告“账号登录成功”。

## Gate 8：Mac 导入与启用

若用户只要文件，到此交付 YAML 和导入步骤，不修改系统网络。

若用户要求代为导入：

1. 使用 Computer Use 检查 Clash Verge 当前配置，保留旧配置作为回退。
2. 导入新 YAML，但不要覆盖用户其他订阅。
3. 切换配置、启用 TUN 或系统代理属于网络设置变更；按 Computer Use 规则在动作发生前请求确认。
4. 切换后重新执行目标站点和出口 IP 测试。
5. 新配置失败时切回旧配置，不删除用户原配置。

## 停止条件

出现以下任一项不得报告完成：

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
7. Mac YAML 文件和导入状态。
8. 浏览器账号登录状态。

列出保留的回滚备份，但不要暴露任何凭证、完整 URL 或节点参数。
