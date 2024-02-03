import docx
from docx import Document
from docx.shared import Inches, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX

import os
from docx.oxml.ns import qn  # 中文格式
from mod.docfun.table_plot import add_three_line
from mod.docfun.write_title import write_title
from mod.read_config import _load_yaml
from mod import parents_path

promts = _load_yaml(os.path.abspath(os.path.join(parents_path, 'config/promts.yaml')))



def write_docments(run_dir:str):
    # 创建一个新的Word文档对象
    document = Document()
    num = write_title(promts['title'],document)

    document.save(os.path.abspath(os.path.join(parents_path,f'run/{run_dir}/output_file/{run_dir}.docx')))


if __name__ == '__main__':
    write_docments('20240201_215030')
