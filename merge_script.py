import fitz
import os
import sys

def get_pdf_files():
    """获取当前目录所有PDF文件并按文件名排序"""
    files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    return sorted(files)

def vertical_merge(file1, file2, output):
    """上下分栏合并PDF（顶格对齐版）"""
    pdf1 = fitz.open(file1)
    pdf2 = fitz.open(file2)
    new_pdf = fitz.open()
    
    # 创建A4页面
    page = new_pdf.new_page(width=595, height=842)
    half_h = 842 / 2  # 每个分栏高度

    # 处理上半部分
    def process_section(pdf, y_start):
        src_page = pdf.load_page(0)
        src_rect = src_page.rect
        
        # 计算宽度撑满的缩放比例
        scale = 595 / src_rect.width
        required_src_h = (half_h) / scale  # 需要截取的源文件高度
        
        # 设置源文件截取区域（从顶部开始）
        clip_rect = fitz.Rect(0, 0, src_rect.width, min(required_src_h, src_rect.height))
        
        # 目标区域定位
        dest_rect = fitz.Rect(0, y_start, 595, y_start + half_h)
        
        # 绘制到目标区域（保持宽高比）
        page.show_pdf_page(
            dest_rect,
            pdf,
            0,
            clip=clip_rect,
            keep_proportion=True
        )

    # 处理第一个文件到上半栏
    process_section(pdf1, 0)
    # 处理第二个文件到下半栏
    process_section(pdf2, half_h)

    new_pdf.save(output)

def merge_multiple_pdfs(files, output):
    """常规多PDF合并（逻辑不变）"""
    merged = fitz.open()
    for f in files:
        pdf = fitz.open(f)
        merged.insert_pdf(pdf)
        pdf.close()
    merged.save(output)

if __name__ == "__main__":
    try:
        pdf_files = get_pdf_files()
        
        if len(pdf_files) < 2:
            print("需要至少2个PDF文件")
            sys.exit(1)

        output_name = "merged.pdf" if len(pdf_files)==2 else "combined.pdf"
        
        if len(pdf_files) == 2:
            print("执行上下分栏合并...")
            vertical_merge(pdf_files[0], pdf_files[1], output_name)
        else:
            print("执行多文件合并...")
            merge_multiple_pdfs(pdf_files, output_name)
            
        print(f"成功生成：{output_name}")

    except Exception as e:
        print(f"错误：{str(e)}")
        sys.exit(1)