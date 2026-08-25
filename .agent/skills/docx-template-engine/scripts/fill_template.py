#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import time
from functools import wraps
from docxtpl import DocxTemplate
from jinja2 import Environment, DebugUndefined

def retry_io(max_retries=5, base_delay=1):
    """
    带有指数退避机制的 I/O 重试装饰器
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = base_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        print(f"I/O 操作失败，已达到最大重试次数 ({max_retries})")
                        raise e
                    print(f"I/O 错误: {e}。将在 {delay} 秒后重试 ({retries}/{max_retries})...")
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator

class TemplateFiller:
    def __init__(self, template_path, data_path, output_path):
        self.template_path = template_path
        self.data_path = data_path
        self.output_path = output_path

    @staticmethod
    def remove_empty_values(data):
        """
        递归清洗数据，剔除 None 和 ""，但保留 0 和 False。
        """
        if isinstance(data, dict):
            cleaned = {}
            for k, v in data.items():
                val = TemplateFiller.remove_empty_values(v)
                if val is not None and val != "":
                    cleaned[k] = val
            return cleaned
        elif isinstance(data, list):
            cleaned = []
            for item in data:
                val = TemplateFiller.remove_empty_values(item)
                if val is not None and val != "":
                    cleaned.append(val)
            return cleaned
        else:
            return data

    @retry_io(max_retries=5)
    def load_data(self):
        """加载 JSON 数据并支持重试"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @retry_io(max_retries=5)
    def load_template(self):
        """加载 Word 模板并支持重试"""
        return DocxTemplate(self.template_path)

    @retry_io(max_retries=5)
    def save_document(self, doc):
        """保存 Word 文档并支持重试"""
        doc.save(self.output_path)

    def run(self):
        print(f"正在加载数据: {self.data_path}")
        raw_data = self.load_data()
        
        print("正在清洗数据...")
        context = self.remove_empty_values(raw_data)
        
        print(f"正在加载模板: {self.template_path}")
        doc = self.load_template()
        
        print("正在渲染文档...")
        # 使用 DebugUndefined 保证空值保留
        env = Environment(undefined=DebugUndefined)
        doc.render(context, jinja_env=env)
        
        print(f"正在保存文档至: {self.output_path}")
        self.save_document(doc)
        print("文档渲染完成。")

def main():
    parser = argparse.ArgumentParser(description="根据 JSON 数据填充并渲染 Word (docx) 模板。")
    parser.add_argument("--template", required=True, help="输入的 Word 模板文件路径 (.docx)")
    parser.add_argument("--data", required=True, help="输入的数据文件路径 (.json)")
    parser.add_argument("--output", required=True, help="输出的 Word 文档路径 (.docx)")
    
    args = parser.parse_args()
    
    filler = TemplateFiller(
        template_path=args.template,
        data_path=args.data,
        output_path=args.output
    )
    filler.run()

if __name__ == "__main__":
    main()
