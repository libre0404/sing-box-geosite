<div align="center">

# 🛠️ Sing-box Rule-set Generator

**一个高性能、自动化的 sing-box 规则集编译工具**

[![Auto Sync](https://img.shields.io/github/actions/workflow/status/libre0404/sing-box-geosite/sync.yml?style=flat-square&logo=github-actions&logoColor=white&label=Auto%20Update)](https://github.com/libre0404/sing-box-geosite/actions)
[![Last Update](https://img.shields.io/github/last-commit/libre0404/sing-box-geosite?style=flat-square&logo=git&label=Last%20Update)](https://github.com/libre0404/sing-box-geosite/commits/main)
[![License](https://img.shields.io/github/license/libre0404/sing-box-geosite?style=flat-square&color=blue&label=License)](LICENSE)

[功能特性](#-功能特性) • [使用方法](#-使用方法-sing-box-远程引用) • [目录结构](#-目录结构) • [本地部署](#️-本地部署-debianubuntu)

</div>

---

## 🚀 功能特性

- **✨ 智能解析**：自动识别并转换 `DOMAIN`, `DOMAIN-SUFFIX`, `IP-CIDR` 等主流代理规则格式。
- **🌍 环境自适应**：
    - **GitHub Actions**: 自动输出至 `./rules` 目录。
    - **Debian 本地**: 自动同步至 `/etc/sing-box/rules`，无缝对接系统服务。
- **⚡ 二进制编译**：调用官方工具链生成 `.srs` 文件，大幅提升 sing-box 加载与匹配效率。
- **📅 自动化同步**：预设 GitHub Actions 工作流，每日定时更新，告警失效规则。

---

## 🛠️ 使用方法 (sing-box 远程引用)

在你的 sing-box `config.json` 中，通过 `remote` 方式引用生成的二进制文件：

```jsonc
{
  "route": {
    "rule_set": [
      {
        "tag": "gfw",
        "type": "remote",
        "format": "binary",
        "url": "[https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/gfw.srs](https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/gfw.srs)",
        "download_detour": "proxy"
      },
      {
        "tag": "adblock",
        "type": "remote",
        "format": "binary",
        "url": "[https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/adblock_reject_domain.srs](https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/adblock_reject_domain.srs)",
        "download_detour": "proxy"
      }
    ]
  }
}
# 📂 目录结构
Bash

.
├── main.py           # 转换核心脚本 (支持去重与格式转换)
├── links.txt         # 规则源列表 (支持远程 URL 和本地通配符)
├── local_rules/      # 存放手动上传的自定义规则文本 (*.txt)
├── rules/            # [自动生成] 存放 .json 和 .srs 规则文件
└── update_rules.sh   # 本地环境一键更新脚本
⚙️ 本地部署 (Debian/Ubuntu)
如果您希望在自己的服务器上运行转换逻辑：

环境准备：

Bash

sudo apt update && sudo apt install python3-venv sing-box -y
配置并执行：

Bash

# 赋予脚本执行权限
chmod +x update_rules.sh

# 执行更新 (自动创建虚拟环境并输出结果至 /etc/sing-box/rules)
./update_rules.sh
📅 更新统计
最后更新时间: 2026-01-01 17:28:30

规则仓库: libre0404/sing-box-geosite

📜 免责声明与协议
本项目系根据其他项目修改而来的自用版本。

使用者请务必遵守原作者的相关使用协议要求。

本项目仅供技术交流与学习使用。
