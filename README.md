Sing-box Rule-set Generator
这是一个基于 Python 的自动规则转换工具，专为 sing-box 设计。它可以抓取远程链接或读取本地文本规则，并自动编译为高性能的二进制规则集 (.srs)。

✨ 功能特性
智能解析：自动识别 DOMAIN, DOMAIN-SUFFIX, IP-CIDR 等常见代理规则格式。

环境自适应：

GitHub Actions: 结果输出至 ./rules。

本地 Debian: 结果自动同步至 /etc/sing-box/rules。

高性能编译：利用 sing-box 官方工具链，生成加载速度极快的二进制 .srs 文件。

自动化同步：通过 GitHub Actions 每天定时更新规则，确保数据始终保持最新。

🛠️ 使用方法 (sing-box 远程引用)
您可以直接在 sing-box 配置文件（如 config.json）中引用本项目生成的二进制文件：

JSON

{
  "route": {
    "rule_set": [
      {
        "tag": "gfw",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/gfw.srs",
        "download_detour": "proxy"
      },
      {
        "tag": "adblock",
        "type": "remote",
        "format": "binary",
        "url": "https://raw.githubusercontent.com/libre0404/sing-box-geosite/main/rules/adblock_reject_domain.srs",
        "download_detour": "proxy"
      }
    ]
  }
}
📂 目录结构
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

根据fork项目修改自用，使用者请遵守原作者相关使用协议要求。
