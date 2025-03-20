import fitz
import os
import sys

def get_pdf_files():
    """获取当前目录所有PDF文件并按文件名排序"""
    files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    return sorted(files)

def vertical_merge(file1, file2, output):
    """上下合并两个PDF到单页"""
    pdf1 = fitz.open(file1)
    pdf2 = fitz.open(file2)
    new_pdf = fitz.open()
    
    # 创建A4页面
    new_page = new_pdf.new_page(width=595, height=842)
    half_h = 842 / 2

    # 合并第一个PDF
    page = pdf1.load_page(0)
    r = page.rect
    scale = min(595/r.width, half_h/r.height)
    new_w = r.width * scale
    new_h = r.height * scale
    new_page.show_pdf_page(
        fitz.Rect((595-new_w)/2, (half_h-new_h)/2, 
                 (595+new_w)/2, (half_h+new_h)/2),
        pdf1, 0)

    # 合并第二个PDF
    page = pdf2.load_page(0)
    r = page.rect
    scale = min(595/r.width, half_h/r.height)
    new_w = r.width * scale
    new_h = r.height * scale
    new_page.show_pdf_page(
        fitz.Rect((595-new_w)/2, half_h + (half_h-new_h)/2,
                 (595+new_w)/2, half_h + (half_h+new_h)/2),
        pdf2, 0)

    new_pdf.save(output)

def merge_multiple_pdfs(files, output):
    """合并多个PDF到多页文档"""
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
            print("发现PDF文件数量不足，请至少放入2个PDF文件")
            sys.exit(1)

        if len(pdf_files) == 2:
            print("检测到2个PDF，执行上下合并...")
            vertical_merge(pdf_files[0], pdf_files[1], "merged.pdf")
        else:
            print(f"检测到{len(pdf_files)}个PDF，执行多页合并...")
            merge_multiple_pdfs(pdf_files, "combined.pdf")
            
        print("操作成功完成！输出文件：", "merged.pdf" if len(pdf_files)==2 else "combined.pdf")

    except Exception as e:
        print(f"操作失败：{str(e)}")
        sys.exit(1)