# Reality/Mihomo 双重故障复盘

## 事故概况

一台海外 VPS 使用 3x-ui 和 VLESS TCP Reality Vision。官方 Xray 客户端曾经通过，但交付给 macOS Clash Verge/Mihomo 的 YAML 只能通过语法测试，Google 和 YouTube 实际不可用。

## 第一层：版本兼容

现场组合：

- 服务端 Xray 26.7.11。
- 客户端 Mihomo 1.19.29。
- 日志持续出现 `REALITY authentication failed`。

上游已有相同问题报告：<https://github.com/XTLS/Xray-core/issues/6477>

处理：

- 在本机下载 Xray 26.6.27 和官方 `.dgst`。
- 校验 SHA-256 后上传为新文件。
- 用服务器当前配置执行 `run -test`。
- 备份 26.7.11，原子替换，重启 x-ui。

教训：不能把最新 Xray 与当前 Mihomo 默认视为兼容，必须建立版本矩阵并进行真实握手。

## 第二层：公网端口路径

回退版本后，外部 443 仍失败。进一步 A/B 测试发现：

- 服务器本机通过 `127.0.0.1:443` 使用同一 UUID、公钥、Short ID、SNI 和目标站点时，Google 和 YouTube 均返回 204。
- Mac 通过公网 IP 的 443 连接时，官方 Xray 报 `received real certificate (potential MITM or redirection)`，Mihomo 报 Reality 认证失败。
- 临时 8443 公网连接超时。
- 临时高端口在完全相同配置下通过 Mihomo，Google 和 YouTube 返回 204。

结论：正式配置参数正确，但机房或公网链路对部分端口发生阻断或重定向。最终端口必须通过外部实测选择，不能假设 443 或 8443 可用。

## 排除项

- `mldsa65Seed` 键存在，但实际值为空。不能因为键存在就判断 ML-DSA 已启用。
- YAML 语法测试成功不代表 Reality 握手成功。
- `systemctl active`、端口监听和 Xray `Configuration OK` 均不是公网端到端证据。

## 正确验证顺序

1. 对分享链接与服务器当前配置做字段级比对，但只输出相等/不相等，不输出秘密值。
2. Xray 配置测试。
3. 服务状态和端口监听。
4. 服务器回环 Reality 测试。
5. 外部 Xray 客户端测试。
6. 外部 Mihomo 测试。
7. Google/YouTube `generate_204`。
8. 社媒和 AI 网站状态。
9. 出口 IP 匹配。
10. 浏览器账号登录。

## HTTP 状态解释

- Google/YouTube 204 是良好的传输证据。
- TikTok/Facebook/Instagram/Grok 200 表示网页链路可达。
- Gemini 302 通常表示到达登录跳转。
- ChatGPT/Claude 403 表示请求已到站，但可能被数据中心 IP、机器人检测或访客策略拒绝；不能包装成登录成功，也不能简单归类为网络断开。

## 安全与清理

- 旧 Xray 二进制和 x-ui 数据库使用显式文件名备份。
- 临时端口验证完成后关闭临时进程并删除临时服务器配置。
- 客户端分享链接和 YAML 权限设为 600。
- 不在复盘、Skill 或最终回复中保存服务器 IP、UUID、Reality 密钥、Short ID、面板凭证或 SSH 凭证。
