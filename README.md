# CZQ VPS Network Provisioner

把一台海外 VPS 交付成真正可用、可回滚、可验收的 Mac Clash 节点。

这个 Codex Skill 不止安装 x-ui。它会继续检查 Xray 与 Mihomo 是否兼容、公网端口是否被机房重定向、Google/YouTube 是否真实可达、出口 IP 是否正确，以及 TikTok、Facebook、Instagram、Claude、ChatGPT、Gemini、Grok 是否按规则走海外节点。

> 核心原则：`服务已启动`、`端口在监听`、`Configuration OK` 和 `YAML 语法通过`，都不等于用户真的能打开网站。

## 适合谁

- 已经有一台海外 Linux VPS，希望在 Mac 上稳定使用 Clash Verge 的个人用户。
- 需要登录和运营海外社媒的创作者、出海团队与运营人员。
- 经常遇到 Reality 认证失败、Google/YouTube 打不开或 443 明明监听却不可用的开发者。
- 希望每次部署都有备份、回滚和验收证据，而不是依赖一键脚本输出“成功”的维护者。

## 它解决什么

| 技术概念 | 用户能感知的含义 | 实际结果 |
| --- | --- | --- |
| x-ui / Xray | 在自己的服务器上管理海外网络节点 | 节点归自己管理，可备份和迁移 |
| VLESS Reality | 用普通 HTTPS 外观建立加密连接 | 在兼容客户端中获得稳定的海外出口 |
| Xray/Mihomo 版本矩阵 | 防止服务端和 Mac 客户端“参数都对却握手失败” | 避免反复修改 UUID、公钥和规则 |
| 公网端口 A/B 测试 | 区分服务器配置错误与机房端口重定向 | 找到外部真正可连接的正式端口 |
| Clash YAML 分流 | 国内流量直连，社媒与 AI 服务走 VPS | 不需要每次手动切换全局代理 |
| 分层验收 | 分别检查服务、端口、协议、网站、出口 IP 和登录 | 不再把半成品当作完成交付 |

## 主要能力

- 新装或复用 3x-ui，并在改动前备份数据库、Xray 二进制和配置。
- 配置 VLESS TCP/RAW Reality Vision 节点。
- 检查已知的 Xray/Mihomo Reality 兼容问题。
- 诊断 `REALITY authentication failed`、真实证书重定向和公网端口超时。
- 从安全保存的 VLESS 分享信息生成 Mac Clash Verge YAML。
- 自动配置 TikTok、Facebook、Instagram、X、YouTube 和海外流量规则。
- 自动配置 Claude、ChatGPT/Codex、Gemini、Grok 规则。
- 用独立 Mihomo 端口验证 Google/YouTube、目标网站和出口 IP，不打断当前系统代理。
- 区分网页可达、HTTP 403、登录跳转和真实账号登录。

## 安装

```bash
git clone https://github.com/chenchen1010/czq-vps-network-provisioner.git \
  ~/.codex/skills/czq-vps-network-provisioner
```

重新打开或刷新 Codex 任务后，使用：

```text
使用 $czq-vps-network-provisioner，把这台海外 VPS 配置成 x-ui/VLESS Reality 节点，
为 Mac Clash Verge 生成海外社媒与 AI 工具分流 YAML，并完成真实联网验收。
```

需要向 Codex 提供：

- VPS 地址。
- SSH 用户。
- SSH 密码或密钥路径。
- 服务器是否承载其他业务。
- 客户端类型；默认支持 macOS + Clash Verge Rev。

Skill 会要求把凭证保存到被 Git 忽略的本地 `.env.local`，并设置为仅当前用户可读。凭证不会写入仓库、README 或最终报告。

## 单独生成 Clash YAML

先创建权限为 `600` 的分享文件：

```dotenv
VLESS_SHARE_LINK=vless://...
```

生成正式配置：

```bash
node scripts/generate_clash_profile.mjs \
  --env /secure/path/client-share.env \
  --out /secure/path/Mac-Clash-Verge-x-ui.yaml
```

生成不会修改系统代理的测试配置：

```bash
node scripts/generate_clash_profile.mjs \
  --env /secure/path/client-share.env \
  --out /secure/path/Mac-Clash-Verge-x-ui-test.yaml \
  --test \
  --mixed-port 17900
```

验证 YAML：

```bash
scripts/validate_mihomo_profile.sh /secure/path/Mac-Clash-Verge-x-ui.yaml
```

在测试 Mihomo 已启动的情况下检查目标网站：

```bash
scripts/probe_proxy.sh http://127.0.0.1:17900 EXPECTED_EXIT_IP
```

## 为什么要检查版本和公网端口

真实事故中，Xray `26.7.11` 与 Mihomo `1.19.28`/`1.19.29` 的 VLESS Reality 出现持续认证失败。回退兼容版本后，还发现服务器本机 443 完全正常，但 Mac 通过公网 443 会收到真实证书重定向；8443 同样超时，只有现场验证过的其他端口能够工作。

因此本 Skill 强制执行两层判断：

1. 协议实现是否兼容。
2. 公网端口路径是否真实可达。

完整案例见 [Reality/Mihomo 双重故障复盘](references/reality-mihomo-port-path-incident.md)。上游兼容问题见 [XTLS/Xray-core#6477](https://github.com/XTLS/Xray-core/issues/6477)。

## 验收标准

Skill 会分别报告：

1. x-ui 安装、复用和备份。
2. Xray 版本、配置测试和 systemd 状态。
3. 正式公网端口监听。
4. Mac 外部 Mihomo Reality 握手。
5. Google、YouTube、社媒和 AI 网站响应。
6. 出口 IP 是否等于 VPS 地址。
7. Clash YAML 是否生成、导入和启用。
8. 浏览器账号是否真实登录成功。

其中任何一层未验证，都不会被包装成端到端完成。

## 安全边界

- 仅用于你拥有或获授权管理的服务器和设备。
- 不帮助绕过账号处罚、欺诈检测、平台安全控制或当地法律。
- 数据中心 VPS 能解决网络连通，不等于住宅 IP，也不能保证社媒和 AI 平台放行登录。
- YAML 包含节点访问参数，应设置为 `600`，不要上传公开仓库、公开网盘或发送给无关人员。
- 生产服务器不进行源码构建；使用经过校验的官方预编译产物和可回滚替换。

## 项目结构

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/
│   └── reality-mihomo-port-path-incident.md
├── scripts/
│   ├── generate_clash_profile.mjs
│   ├── probe_proxy.sh
│   └── validate_mihomo_profile.sh
└── tests/
    └── fixture.env.example
```

## 参考资料

- [3x-ui 官方安装文档](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [Xray Reality 官方配置](https://xtls.github.io/en/config/transports/reality.html)
- [Mihomo VLESS 配置](https://wiki.metacubex.one/en/config/proxies/vless/)
- [Xray 26.7.11 与 Mihomo Reality 兼容问题](https://github.com/XTLS/Xray-core/issues/6477)

## License

[MIT](LICENSE)
