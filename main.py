import os
import json
import requests
import yaml
import ipaddress
import subprocess
import glob

# 核心映射字典
MAP_DICT = {
    'DOMAIN-SUFFIX': 'domain_suffix',
    'DOMAIN': 'domain',
    'DOMAIN-KEYWORD': 'domain_keyword',
    'IP-CIDR': 'ip_cidr',
    'IP-CIDR6': 'ip_cidr',
    'SRC-IP-CIDR': 'source_ip_cidr',
    'GEOIP': 'geoip',
    'DST-PORT': 'port',
    'SRC-PORT': 'source_port',
    'DOMAIN-REGEX': 'domain_regex'
}

# --- 路径配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LINKS_FILE = os.path.join(BASE_DIR, "links.txt")

# 自动判断输出目录：如果是 GitHub Actions 环境则输出到当前目录的 rules，否则输出到系统目录
if os.environ.get('GITHUB_ACTIONS') == 'true':
    OUTPUT_DIR = os.path.join(BASE_DIR, "rules")
else:
    OUTPUT_DIR = "/etc/sing-box/rules"

def is_ipv4_or_ipv6(address):
    """验证是否为合法 IP 格式"""
    try:
        ipaddress.ip_network(address, strict=False)
        return True
    except ValueError:
        return False

def get_content(path):
    """兼容远程 URL 和本地绝对路径"""
    if path.startswith(('http://', 'https://')):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(path, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  ❌ 网络抓取失败: {e}")
            return None
    elif os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"  ❌ 本地读取失败: {e}")
            return None
    return None

def parse_rules(content, path):
    rules_data = {v: set() for v in MAP_DICT.values()}
    
    if path.endswith(('.yaml', '.yml')) or 'payload:' in content:
        try:
            data = yaml.safe_load(content)
            items = data.get('payload', []) if isinstance(data, dict) else content.splitlines()
        except:
            items = content.splitlines()
    else:
        items = content.splitlines()

    for line in items:
        line = line.strip().strip('"').strip("'").strip(',')
        if not line or line.startswith(('#', '//', ';')):
            continue
        
        parts = line.split(',')
        if len(parts) >= 2:
            raw_type = parts[0].strip().upper().replace('HOST', 'DOMAIN')
            val = parts[1].strip().strip('"').strip("'")
        else:
            val = parts[0].strip().strip('"').strip("'")
            if is_ipv4_or_ipv6(val):
                raw_type = 'IP-CIDR'
            elif val.startswith('.'):
                raw_type = 'DOMAIN-SUFFIX'
                val = val[1:]
            elif val.startswith('+.'):
                raw_type = 'DOMAIN-SUFFIX'
                val = val[2:]
            elif val.startswith('*.'):
                raw_type = 'DOMAIN-SUFFIX'
                val = val[2:]
            else:
                raw_type = 'DOMAIN'

        target_type = MAP_DICT.get(raw_type)
        if target_type in rules_data:
            rules_data[target_type].add(val)

    return rules_data

def main():
    if not os.path.exists(LINKS_FILE):
        print(f"❌ 找不到 {LINKS_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(LINKS_FILE, 'r') as f:
        raw_links = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            raw_links.append(line.split(' ')[-1])

    expanded_links = []
    for path in raw_links:
        if '*' in path:
            full_glob_path = os.path.join(BASE_DIR, path) if not os.path.isabs(path) else path
            files = glob.glob(full_glob_path)
            if files:
                expanded_links.extend(files)
            else:
                print(f"⚠️ 未找到匹配通配符的文件: {path}")
        else:
            expanded_links.append(path)

    for url_or_path in expanded_links:
        name = os.path.basename(url_or_path).split('.')[0]
        print(f"➡️ 正在处理: {name}")
        
        content = get_content(url_or_path)
        if content:
            rules_data = parse_rules(content, url_or_path)
            
            final_json = {"version": 2, "rules": []}
            
            combined_rule = {}
            for key in sorted(rules_data.keys()):
                values = rules_data[key]
                if values:
                    combined_rule[key] = sorted(list(values))
            
            if combined_rule:
                final_json["rules"].append(combined_rule)

            json_path = os.path.join(OUTPUT_DIR, f"{name}.json")
            srs_path = os.path.join(OUTPUT_DIR, f"{name}.srs")

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(final_json, f, indent=2, ensure_ascii=False)

            try:
                subprocess.run(
                    ["sing-box", "rule-set", "compile", "--output", srs_path, json_path],
                    check=True,
                    capture_output=True
                )
                print(f"  ✅ 成功生成: {name}.srs")
            except Exception as e:
                print(f"  ❌ 编译失败: {name}")

if __name__ == "__main__":
    main()
