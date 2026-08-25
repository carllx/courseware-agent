import re
import os
import time
import random
from pathlib import Path
from typing import List, Tuple
from imgur_uploader import main as upload_image

class MarkdownImageConverter:
    def __init__(self, markdown_file: str):
        self.markdown_file = Path(markdown_file).resolve()
        self.base_dir = self.markdown_file.parent
        self.total_images = 0
        self.processed_images = 0
        
    def is_local_image(self, path: str) -> bool:
        """判断是否为本地图片路径"""
        # 排除 http/https 链接
        if re.match(r'^https?://', path):
            return False
        
        # 检查文件扩展名
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        return Path(path).suffix.lower() in image_extensions
    
    def get_absolute_path(self, relative_path: str) -> str:
        """获取图片的绝对路径"""
        try:
            image_path = Path(relative_path)
            
            # 处理相对路径
            if not image_path.is_absolute():
                # 尝试多个可能的基础路径
                possible_paths = [
                    self.base_dir / image_path,  # 相对于markdown文件的路径
                    Path(relative_path),  # 原始路径
                    Path.cwd() / image_path  # 相对于当前工作目录
                ]
                
                for path in possible_paths:
                    try:
                        resolved_path = path.resolve()
                        if resolved_path.exists():
                            return str(resolved_path)
                    except Exception:
                        continue
                
                # 如果所有尝试都失败，返回相对于markdown文件的路径
                return str((self.base_dir / image_path).resolve())
            
            return str(image_path.resolve())
            
        except Exception as e:
            print(f"警告: 解析路径失败 - {relative_path}: {str(e)}")
            return relative_path
    
    def find_images(self, content: str) -> List[Tuple[str, str, int, int]]:
        """查找 Markdown 中的图片链接"""
        images = []
        # 匹配更多的 Markdown 图片语法变体
        patterns = [
            r'!\[([^\]]*)\]\(([^)]+)\)',  # 标准语法
            r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>',  # HTML 语法
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                full_match = match.group(0)
                # 根据不同模式获取图片路径
                if pattern.startswith('!'):
                    image_path = match.group(2)
                else:
                    image_path = match.group(1)
                
                # 清理路径
                image_path = image_path.split(' ')[0].strip()
                image_path = image_path.replace('file://', '')
                
                if self.is_local_image(image_path):
                    images.append((
                        full_match,
                        image_path,
                        match.start(),
                        match.end()
                    ))
        
        return images

    def count_images(self, content: str) -> int:
        """统计需要处理的图片数量"""
        return len(self.find_images(content))
    
    def process_file(self) -> None:
        try:
            print(f"\n正在处理文件: {self.markdown_file}")
            
            # 创建临时文件路径
            temp_file = self.markdown_file.with_suffix('.md.temp')
            print(f"临时文件位置: {temp_file}")
            
            # 读取文件内容
            with open(self.markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找所有本地图片
            images = self.find_images(content)
            self.total_images = len(images)
            
            if self.total_images == 0:
                print("未找到本地图片链接")
                return
            
            print(f"找到 {self.total_images} 张本地图片")
            
            # 处理每个图片
            new_content = content
            offset = 0
            
            for full_match, image_path, start, end in images:
                self.processed_images += 1
                print(f"\n正在处理markdown文件: {self.markdown_file}")
                print(f"\n处理第 {self.processed_images}/{self.total_images} 张图片")
                
                abs_path = self.get_absolute_path(image_path)
                
                if not os.path.exists(abs_path):
                    print(f"警告: 图片不存在 - {abs_path}")
                    print(f"尝试查找的位置:")
                    print(f"1. Markdown文件目录: {self.base_dir}")
                    print(f"2. 当前工作目录: {os.getcwd()}")
                    print(f"3. 原始路径: {image_path}")
                    continue
                
                # 上传到 Imgur (添加重试机制)
                start_time = time.time()
                retry_count = 0
                max_retry_time = 3600  # 1小时最大重试时间
                
                while True:
                    try:
                        imgur_url = upload_image(abs_path)
                        if not imgur_url.startswith('Error:'):
                            break  # 只有上传成功才跳出循环
                        
                        if time.time() - start_time >= max_retry_time:
                            print(f"上传失败 - {image_path}: 超过最大重试时间(1小时)")
                            break
                        
                        # 所有错误情况（包括速率限制）统一处理
                        retry_count += 1
                        wait_time = random.randint(30, 120)  # 随机等待60-120秒
                        print(f"上传失败（{imgur_url}），等待 {wait_time} 秒后进行第 {retry_count} 次重试...")
                        time.sleep(wait_time)
                        continue
                        
                    except Exception as e:
                        if time.time() - start_time >= max_retry_time:
                            print(f"上传失败 - {image_path}: {str(e)}")
                            break
                        retry_count += 1
                        wait_time = max(60, 120)
                        print(f"发生错误: {str(e)}，等待 {wait_time} 秒后进行第 {retry_count} 次重试...")
                        time.sleep(wait_time)
                        continue
                
                # 如果上传失败，跳过当前图片
                if imgur_url.startswith('Error:'):
                    print(f"跳过图片 {image_path}: {imgur_url}")
                    continue
                
                # 创建新的 Markdown 图片链接，保持原始路径作为图片描述
                original_path = image_path
                if '\\' in original_path:  # 处理 Windows 路径分隔符
                    original_path = original_path.replace('\\', '/')
                new_match = f'![{original_path}]({imgur_url})'
                
                # 替换内容
                start_pos = start + offset
                end_pos = end + offset
                new_content = new_content[:start_pos] + new_match + new_content[end_pos:]
                
                # 更新偏移量
                offset += len(new_match) - (end - start)
                print(f"已上传并替换: {image_path} -> {imgur_url}")
                print(f"进度: {self.processed_images}/{self.total_images}")
                
                # 每次成功替换后就更新临时文件
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"已更新临时文件: {temp_file}")
                            
            # 保存最终文件
            backup_file = self.markdown_file.with_suffix('.md.bak')
            try:
                # 先创建备份
                if backup_file.exists():
                    backup_file.unlink()  # 如果已存在备份文件，先删除
                os.rename(self.markdown_file, backup_file)
                
                # 保存新文件
                with open(self.markdown_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # 处理完成后删除临时文件
                if temp_file.exists():
                    temp_file.unlink()
                
                print(f"处理完成! 原文件已备份为: {backup_file}")
                
            except Exception as e:
                # 如果保存过程中出错，尝试恢复原文件
                if backup_file.exists() and not self.markdown_file.exists():
                    os.rename(backup_file, self.markdown_file)
                print(f"保存文件时出错: {str(e)}")
                raise
        
        except Exception as e:
            print(f"处理文件时出错: {str(e)}")


def main():
    import sys
    if len(sys.argv) != 2:
        print("使用方法: python convert_local_images.py <markdown_file>")
        return 0
    
    markdown_file = sys.argv[1]
    converter = MarkdownImageConverter(markdown_file)
    converter.process_file()
    return converter.total_images  # 返回处理的图片总数

if __name__ == "__main__":
    result = main()
    print(result)  # 输出总图片数

