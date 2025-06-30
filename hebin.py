import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 合并与页码删除工具")
        self.pdf_files = []

        # 按钮
        tk.Button(root, text="选择PDF文件", command=self.select_files).pack(pady=5)
        tk.Button(root, text="设置输出文件名", command=self.set_output_file).pack(pady=5)
        tk.Button(root, text="开始合并", command=self.merge_pdfs).pack(pady=5)

        # 页面删除功能
        self.delete_var = tk.BooleanVar()
        tk.Checkbutton(root, text="是否删除页码", variable=self.delete_var).pack()

        tk.Label(root, text="（如：2,4 表示删除第2、第4页）").pack()
        self.page_entry = tk.Entry(root)
        self.page_entry.pack()

        # 输出路径默认值
        self.output_file = "merged_output.pdf"

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_files = list(files)
            messagebox.showinfo("文件选择成功", f"已选择 {len(self.pdf_files)} 个PDF文件")

    def set_output_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.output_file = file

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("错误", "请先选择PDF文件")
            return

        # 合并
        temp_file = "temp_merge.pdf"
        merger = PdfMerger()
        for pdf in self.pdf_files:
            merger.append(pdf)
        merger.write(temp_file)
        merger.close()

        # 处理删除页码
        if self.delete_var.get():
            try:
                input_pages = self.page_entry.get().strip()
                if input_pages:
                    page_indices = sorted(set(int(i.strip()) - 1 for i in input_pages.split(",") if i.strip().isdigit()))
                else:
                    page_indices = []

                reader = PdfReader(temp_file)
                writer = PdfWriter()
                total_pages = len(reader.pages)

                for i, page in enumerate(reader.pages):
                    if i not in page_indices:
                        writer.add_page(page)

                with open(self.output_file, "wb") as f:
                    writer.write(f)
                os.remove(temp_file)

                messagebox.showinfo("完成", f"PDF合并并删除页面成功！\n共删除 {len(page_indices)} 页")
            except Exception as e:
                messagebox.showerror("删除页面失败", str(e))
        else:
            os.rename(temp_file, self.output_file)
            messagebox.showinfo("完成", f"PDF合并成功！\n输出文件：{self.output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
