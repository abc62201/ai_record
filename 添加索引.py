#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_record 目录索引自动生成脚本
用法: python gen_index.py 或双击 gen_index.bat
功能: 扫描指定目录, 自动生成 record.txt (给AI读) 和 README.md (给人读)
"""

import os
import sys

# ==================== 配置区 ====================

# Gitee 仓库基础 URL
# 给AI直接获取的 -> raw 链接, AI可以下载文件内容
给AI直接获取的 = 'https://gitee.com/abc62201/ai_record/raw/master/'

# 写到README的 -> tree 链接, 人类在浏览器查看目录
写到README的 = 'https://gitee.com/abc62201/ai_record/tree/master/'

# 指定扫描的文件夹目录
指定文件夹目录 = {'ai', 'git日记仓库'}

# 指定添加的文件类型
指定文件类型 = {'.txt', '.md'}

# 排除的路径(目录名)
排除的路径 = {'.git', '.obsidian'}

# 每个扫描目录内部放一个给AI阅读的索引文件
record文件名 = 'record.txt'

# 项目根目录放一个给自己阅读的索引文件
readme文件名 = 'README.md'

# ==================== 核心逻辑 ====================

# 获取脚本所在目录作为项目根目录
script_dir = os.path.dirname(os.path.abspath(__file__))

def 扫描目录(scan_dir_name):
    """扫描指定子目录, 返回文件列表"""
    scan_path = os.path.join(script_dir, scan_dir_name)
    
    if not os.path.isdir(scan_path):
        print(f"  [警告] 目录不存在, 跳过: {scan_dir_name}")
        return []
    
    files = []
    for entry in os.listdir(scan_path):
        # 跳过索引文件自身
        if entry == record文件名 or entry == readme文件名:
            continue
        
        # 检查文件扩展名
        ext = os.path.splitext(entry)[1].lower()
        if ext not in 指定文件类型:
            continue
        
        # 检查是否在排除路径中
        full_path = os.path.join(scan_path, entry)
        skip = False
        for excluded in 排除的路径:
            if excluded in entry:
                skip = True
                break
        if skip:
            continue
        
        # 读取文件第一行非空文字作为描述
        desc = entry.rsplit('.', 1)[0]  # 默认用文件名(去扩展名)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        desc = line
                        break
        except Exception as e:
            print(f"  [读取失败] {entry}: {e}")
        
        relative_path = os.path.join(scan_dir_name, entry)
        
        # 构建两种URL
        ai_url = 给AI直接获取的 + relative_path.replace('\\', '/')
        readme_url = 写到README的 + relative_path.replace('\\', '/')
        
        files.append({
            'file': entry,
            'desc': desc,
            'ai_url': ai_url,
            'readme_url': readme_url,
            'relative_path': relative_path
        })
    
    # 按文件名排序
    files.sort(key=lambda x: x['file'])
    return files

def 生成record_txt(scan_dir_name, files):
    """生成给AI阅读的 record.txt"""
    record_path = os.path.join(script_dir, scan_dir_name, record文件名)
    
    with open(record_path, 'w', encoding='utf-8') as f:
        f.write(f"# {scan_dir_name} 目录索引\n")
        f.write(f"# 自动生成, 请勿手动修改\n\n")
        
        for i, file_info in enumerate(files, 1):
            # 格式: 序号.描述：raw_url
            f.write(f"{i}.{file_info['desc']}:{file_info['ai_url']}\n")
    
    print(f"  [生成] {record_path}")

def 生成readme_md(all_dir_files):
    """生成给人阅读的 README.md"""
    readme_path = os.path.join(script_dir, readme文件名)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# ai_record 项目目录索引\n\n")
        f.write(f"> 自动生成, 请勿手动修改\n\n")
        
        for scan_dir_name, files in all_dir_files:
            if not files:
                continue
            
            f.write(f"## {scan_dir_name}\n\n")
            
            for i, file_info in enumerate(files, 1):
                # Markdown 链接格式
                f.write(f"{i}. [{file_info['desc']}]({file_info['readme_url']})\n")
            
            f.write("\n")
    
    print(f"  [生成] {readme_path}")

# ==================== 主流程 ====================

print("=" * 50)
print("ai_record 目录索引生成工具")
print("=" * 50)

all_dir_files = []
total_files = 0

for scan_dir in sorted(指定文件夹目录):
    print(f"\n扫描目录: {scan_dir}")
    files = 扫描目录(scan_dir)
    
    if files:
        print(f"  找到 {len(files)} 个文件")
        for fi in files:
            print(f"    - {fi['file']}")
        total_files += len(files)
    
    all_dir_files.append((scan_dir, files))

# 生成每个子目录的 record.txt
for scan_dir_name, files in all_dir_files:
    if files:
        生成record_txt(scan_dir_name, files)

# 生成根目录的 README.md
if total_files > 0:
    生成readme_md(all_dir_files)
else:
    print("\n[提示] 未找到任何文件, 未生成 README.md")

print("\n" + "=" * 50)
print(f"完成! 共处理 {total_files} 个文件")
print("=" * 50)

# 暂停(双击运行时可见)
if len(sys.argv) == 1:
    input("按回车键退出...")
