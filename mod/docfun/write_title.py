import docx
from docx.shared import RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn  # 中文格式


def write_title(title:str,document,intial_counts=0):
    # 添加标题
    title = document.add_heading(title, level=1)
    run = title.runs[0]
    run.font.color.rgb = RGBColor(0, 0, 0)  # 设置文本颜色为红色
    # title.text = "仿真分析报告"
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # 居中对齐
    # 设置西体格式
    run.font.name = '宋体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    run.font.size = docx.shared.Pt(16)  # 设置第一个运行的字体大小为15磅
    intial_counts = intial_counts+1
    return intial_counts
