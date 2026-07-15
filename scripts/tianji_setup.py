#!/usr/bin/env python3
"""天玑 · 初始化工具

为小白准备的配置向导:
1. 检查Python环境
2. 创建数据目录
3. 引导配置API keys
"""

import os, json, sys
from datetime import datetime

HOME = os.path.expanduser("~")
DATA_DIR = os.path.join(HOME, "tianji-data")
CONFIG_FILE = os.path.join(HOME, ".hermes", "secrets", "tianji_config.json")

def check_environment():
    print("\n📋 检查运行环境...")
    print(f"   Python: {sys.version}")
    print(f"   数据目录: {DATA_DIR}")
    
    # 创建数据目录
    for d in ["exchange-rates", "social-signals", "ecommerce", "regulatory", "reports"]:
        os.makedirs(os.path.join(DATA_DIR, d), exist_ok=True)
    print(f"✅ 数据目录已创建")
    
    return True

def setup_config():
    print("\n🔑 API Keys 配置")
    print("   以下服务需要API key才能工作：")
    print("")
    
    config = {}
    
    # ExchangeRate-API
    print("1. ExchangeRate-API (汇率数据, 免费1000次/月)")
    key = input("   输入API key (留空跳过): ").strip()
    if key:
        config["exchange_rate_api_key"] = key
    
    # FRED
    print("\n2. FRED (美联储经济数据, 免费)")
    key = input("   输入API key (留空跳过): ").strip()
    if key:
        config["fred_api_key"] = key
    
    if config:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n✅ 配置已保存: {CONFIG_FILE}")
    else:
        print("\n⏳ 暂未配置API key，采集器会以降级模式运行")

def main():
    print("🌍 天玑 · 初始化向导")
    print("=" * 40)
    print(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    check_environment()
    setup_config()
    
    print("\n" + "=" * 40)
    print("✅ 天玑初始化完成!")
    print("   下一步: python tianji_runner.py")
    print("=" * 40)

if __name__ == "__main__":
    main()
