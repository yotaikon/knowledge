import os
import chromadb
from chromadb.utils import embedding_functions
import hashlib
import re
from typing import List, Dict, Any
import logging
import json

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedVectorKnowledgeBase:
    def __init__(self, db_path: str = "./local_db"):
        """初始化向量知识库"""
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        self.embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="my_knowledge_base",
            embedding_function=self.embedding
        )
        
    def extract_text_from_txt(self, file_path: str) -> str:
        """从文本文件中提取文本"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"处理文本文件 {file_path} 时出错: {e}")
                return ""
        except Exception as e:
            logger.error(f"处理文本文件 {file_path} 时出错: {e}")
            return ""
    
    def extract_text_from_pdf_simple(self, file_path: str) -> str:
        """从PDF文件中提取文本（简化版本，使用系统命令）"""
        try:
            # 尝试使用系统命令提取PDF文本
            import subprocess
            result = subprocess.run(['pdftotext', file_path, '-'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout
            else:
                logger.warning(f"PDF文本提取失败，尝试其他方法: {file_path}")
                return self.extract_text_from_pdf_fallback(file_path)
        except Exception as e:
            logger.warning(f"PDF处理失败，使用备用方法: {e}")
            return self.extract_text_from_pdf_fallback(file_path)
    
    def extract_text_from_pdf_fallback(self, file_path: str) -> str:
        """PDF文本提取的备用方法"""
        try:
            # 尝试使用PyPDF2（如果可用）
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            logger.warning("PyPDF2未安装，无法处理PDF文件")
            return f"[PDF文件: {os.path.basename(file_path)} - 需要安装PyPDF2或pdftotext工具]"
        except Exception as e:
            logger.error(f"PDF备用方法也失败: {e}")
            return f"[PDF文件: {os.path.basename(file_path)} - 处理失败]"
    
    def extract_text_from_docx_simple(self, file_path: str) -> str:
        """从DOCX文件中提取文本（简化版本）"""
        try:
            # 尝试使用python-docx
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            logger.warning("python-docx未安装，无法处理DOCX文件")
            return f"[DOCX文件: {os.path.basename(file_path)} - 需要安装python-docx]"
        except Exception as e:
            logger.error(f"处理DOCX文件 {file_path} 时出错: {e}")
            return f"[DOCX文件: {os.path.basename(file_path)} - 处理失败]"
    
    def extract_text_from_image_simple(self, file_path: str) -> str:
        """从图片文件中提取文本（简化版本）"""
        try:
            # 尝试使用pytesseract
            import pytesseract
            from PIL import Image
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text if text.strip() else f"[图片文件: {os.path.basename(file_path)} - 未检测到文本]"
        except ImportError:
            logger.warning("pytesseract或PIL未安装，无法处理图片文件")
            return f"[图片文件: {os.path.basename(file_path)} - 需要安装pytesseract和Pillow]"
        except Exception as e:
            logger.error(f"处理图片文件 {file_path} 时出错: {e}")
            return f"[图片文件: {os.path.basename(file_path)} - 处理失败]"
    
    def extract_metadata_from_file(self, file_path: str) -> Dict[str, Any]:
        """提取文件元数据"""
        try:
            stat = os.stat(file_path)
            return {
                'file_size': stat.st_size,
                'created_time': stat.st_ctime,
                'modified_time': stat.st_mtime,
                'file_extension': os.path.splitext(file_path)[1].lower()
            }
        except Exception as e:
            logger.error(f"提取文件元数据失败: {e}")
            return {}
    
    def clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符，保留中文、英文、数字和基本标点
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()（）\-_]', '', text)
        return text.strip()
    
    def split_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """将长文本分割成小块"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
            
        return chunks
    
    def generate_file_id(self, file_path: str) -> str:
        """生成文件ID"""
        return hashlib.md5(file_path.encode()).hexdigest()
    
    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """处理单个文件并返回文档块"""
        file_ext = os.path.splitext(file_path)[1].lower()
        file_id = self.generate_file_id(file_path)
        
        # 根据文件类型提取文本
        if file_ext == '.txt':
            text = self.extract_text_from_txt(file_path)
        elif file_ext == '.pdf':
            text = self.extract_text_from_pdf_simple(file_path)
        elif file_ext == '.docx':
            text = self.extract_text_from_docx_simple(file_path)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            text = self.extract_text_from_image_simple(file_path)
        else:
            logger.warning(f"不支持的文件类型: {file_ext}")
            return []
        
        if not text:
            logger.warning(f"无法从文件 {file_path} 提取文本")
            return []
        
        # 清理文本
        text = self.clean_text(text)
        
        # 分割文本
        chunks = self.split_text(text)
        
        # 提取文件元数据
        file_metadata = self.extract_metadata_from_file(file_path)
        
        # 创建文档块
        documents = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # 只添加非空块
                documents.append({
                    'id': f"{file_id}_chunk_{i}",
                    'text': chunk,
                    'metadata': {
                        'file_path': file_path,
                        'file_name': os.path.basename(file_path),
                        'file_type': file_ext,
                        'chunk_index': i,
                        'total_chunks': len(chunks),
                        **file_metadata
                    }
                })
        
        return documents
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """添加文档到向量数据库"""
        if not documents:
            return
        
        texts = [doc['text'] for doc in documents]
        ids = [doc['id'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        try:
            self.collection.add(
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            logger.info(f"成功添加 {len(documents)} 个文档块到向量数据库")
        except Exception as e:
            logger.error(f"添加文档到向量数据库时出错: {e}")
    
    def process_directory(self, directory_path: str):
        """处理目录中的所有支持的文件"""
        supported_extensions = {'.txt', '.pdf', '.docx', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        
        processed_files = 0
        total_chunks = 0
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in supported_extensions:
                    logger.info(f"处理文件: {file_path}")
                    documents = self.process_file(file_path)
                    if documents:
                        self.add_documents(documents)
                        processed_files += 1
                        total_chunks += len(documents)
        
        logger.info(f"处理完成: {processed_files} 个文件，{total_chunks} 个文档块")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """搜索向量数据库"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # 格式化结果
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"搜索时出错: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            logger.error(f"获取集合信息时出错: {e}")
            return {}
    
    def export_search_results(self, query: str, n_results: int = 10, output_file: str = "search_results.json"):
        """导出搜索结果到JSON文件"""
        results = self.search(query, n_results)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"搜索结果已导出到: {output_file}")
        except Exception as e:
            logger.error(f"导出搜索结果失败: {e}")

def create_sample_files():
    """创建示例文件用于测试"""
    # 创建示例文本文件
    sample_texts = [
        {
            'filename': '汽车零部件研究.txt',
            'content': '''
            汽车零部件线圈生产线停机时间研究
            本研究主要关注汽车零部件生产过程中线圈生产线的停机时间问题。
            通过分析生产数据，我们发现停机时间主要来源于设备故障、维护保养和人员操作等因素。
            为了减少停机时间，我们提出了以下改进措施：
            1. 定期设备维护和预防性保养
            2. 操作人员技能培训
            3. 生产流程优化
            4. 备件库存管理优化
            这些措施的实施预计可以将停机时间减少30%以上。
            '''
        },
        {
            'filename': '豆包MarsCode介绍.txt',
            'content': '''
            豆包MarsCode是一个强大的AI编程助手，能够帮助开发者提高编程效率。
            它支持多种编程语言，包括Python、JavaScript、Java等。
            主要功能包括：
            - 代码生成和补全
            - 代码审查和优化建议
            - 问题诊断和解决方案
            - 文档生成
            使用豆包MarsCode可以显著提高开发效率，减少编程错误。
            '''
        }
    ]
    
    for sample in sample_texts:
        with open(sample['filename'], 'w', encoding='utf-8') as f:
            f.write(sample['content'])
        print(f"创建示例文件: {sample['filename']}")

def main():
    """主函数 - 演示如何使用高级向量知识库"""
    print("=== 高级向量知识库系统 ===")
    
    # 创建示例文件
    print("\n1. 创建示例文件...")
    create_sample_files()
    
    # 初始化向量知识库
    print("\n2. 初始化向量知识库...")
    kb = AdvancedVectorKnowledgeBase()
    
    # 处理当前目录中的所有文档
    print("\n3. 处理文档...")
    kb.process_directory(".")
    
    # 显示集合信息
    info = kb.get_collection_info()
    print(f"\n4. 向量知识库信息: {info}")
    
    # 演示搜索功能
    print("\n5. 演示搜索功能:")
    queries = ["汽车零部件", "豆包MarsCode", "停机时间", "编程助手"]
    
    for query in queries:
        print(f"\n搜索查询: '{query}'")
        results = kb.search(query, n_results=3)
        
        for i, result in enumerate(results, 1):
            print(f"  结果 {i}:")
            print(f"    文件: {result['metadata']['file_name']}")
            print(f"    类型: {result['metadata']['file_type']}")
            print(f"    文本片段: {result['text'][:150]}...")
            if result['distance']:
                print(f"    相似度: {1 - result['distance']:.3f}")
    
    # 导出搜索结果
    print("\n6. 导出搜索结果...")
    kb.export_search_results("汽车零部件", 5, "汽车零部件搜索结果.json")
    
    print("\n=== 向量知识库系统运行完成 ===")

if __name__ == "__main__":
    main()
