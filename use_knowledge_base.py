#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式向量知识库使用脚本
"""

import sys
import os
from advanced_vector_kb import AdvancedVectorKnowledgeBase

def print_banner():
    """打印欢迎横幅"""
    print("=" * 60)
    print("           🧠 向量知识库查询系统 🧠")
    print("=" * 60)
    print("支持功能：")
    print("1. 搜索知识库内容")
    print("2. 查看知识库统计信息")
    print("3. 导出搜索结果")
    print("4. 退出系统")
    print("=" * 60)

def search_knowledge_base(kb):
    """搜索知识库"""
    print("\n🔍 知识库搜索")
    print("-" * 30)
    
    while True:
        query = input("请输入搜索关键词 (输入 'back' 返回主菜单): ").strip()
        
        if query.lower() == 'back':
            break
            
        if not query:
            print("请输入有效的搜索关键词")
            continue
            
        try:
            n_results = int(input("显示结果数量 (默认5): ") or "5")
        except ValueError:
            n_results = 5
            
        print(f"\n正在搜索: '{query}'...")
        results = kb.search(query, n_results)
        
        if not results:
            print("❌ 未找到相关结果")
            continue
            
        print(f"\n✅ 找到 {len(results)} 个相关结果:")
        print("-" * 50)
        
        for i, result in enumerate(results, 1):
            print(f"\n📄 结果 {i}:")
            print(f"   文件: {result['metadata']['file_name']}")
            print(f"   类型: {result['metadata']['file_type']}")
            print(f"   相似度: {1 - result['distance']:.3f}" if result['distance'] else "   相似度: N/A")
            print(f"   内容: {result['text'][:200]}...")
            
        # 询问是否导出结果
        export = input("\n是否导出搜索结果到文件? (y/n): ").lower()
        if export == 'y':
            filename = input("请输入文件名 (默认: search_results.json): ").strip() or "search_results.json"
            kb.export_search_results(query, n_results, filename)
            print(f"✅ 搜索结果已导出到: {filename}")

def show_statistics(kb):
    """显示知识库统计信息"""
    print("\n📊 知识库统计信息")
    print("-" * 30)
    
    info = kb.get_collection_info()
    if info:
        print(f"集合名称: {info.get('collection_name', 'N/A')}")
        print(f"文档总数: {info.get('total_documents', 0)}")
    else:
        print("❌ 无法获取知识库信息")

def export_results(kb):
    """导出搜索结果"""
    print("\n📤 导出搜索结果")
    print("-" * 30)
    
    query = input("请输入搜索关键词: ").strip()
    if not query:
        print("请输入有效的搜索关键词")
        return
        
    try:
        n_results = int(input("导出结果数量 (默认10): ") or "10")
    except ValueError:
        n_results = 10
        
    filename = input("请输入输出文件名 (默认: exported_results.json): ").strip() or "exported_results.json"
    
    print(f"\n正在搜索并导出: '{query}'...")
    kb.export_search_results(query, n_results, filename)
    print(f"✅ 搜索结果已导出到: {filename}")

def main():
    """主函数"""
    print_banner()
    
    # 初始化知识库
    print("\n🔄 正在初始化知识库...")
    try:
        kb = AdvancedVectorKnowledgeBase()
        print("✅ 知识库初始化成功!")
    except Exception as e:
        print(f"❌ 知识库初始化失败: {e}")
        print("请确保已安装所需的依赖包: pip install chromadb sentence-transformers")
        return
    
    # 主菜单循环
    while True:
        print("\n" + "=" * 60)
        print("请选择操作:")
        print("1. 🔍 搜索知识库")
        print("2. 📊 查看统计信息")
        print("3. 📤 导出搜索结果")
        print("4. 🚪 退出系统")
        print("=" * 60)
        
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == '1':
            search_knowledge_base(kb)
        elif choice == '2':
            show_statistics(kb)
        elif choice == '3':
            export_results(kb)
        elif choice == '4':
            print("\n👋 感谢使用向量知识库系统!")
            break
        else:
            print("❌ 无效选项，请重新选择")

if __name__ == "__main__":
    main()
