from docx.table import _Cell
from docx.oxml import OxmlElement
from docx.oxml.ns import qn  # 中文格式
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_ALIGN_PARAGRAPH
from docx.shared import RGBColor


# 定义一个函数，设置单元格的边框颜色，这里主要是把表格转换为三线表
def set_cell_border(cell: _Cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('left', 'top', 'right', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))


def add_three_line(v_cell_num, h_cell_num, table):
    line_width = 16
    color = RGBColor(0, 0, 0)
    for i in range(v_cell_num):
        for j in range(h_cell_num):
            table.cell(i, j).paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            if ((i == 0) | (i == 1)): # 第0列和第一列
                if j == 0:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width, "val": "single"},
                                    bottom={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0)},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})
                elif j == h_cell_num - 1:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width, "val": "single"},
                                    bottom={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0), "val": "single"},
                                    right={"color": RGBColor(0, 0, 0)})
                else:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width, "val": "single"},
                                    bottom={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0), "val": "single"},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})

            elif i == (v_cell_num - 1):  # 最后一列
                if j == 0:
                    set_cell_border(table.cell(i, j), bottom={"color": color, "sz": line_width, "val": "single"},
                                    top={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0)},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})
                elif j == h_cell_num - 1:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width},
                                    bottom={"color": color, "sz": line_width, "val": "single"},
                                    left={"color": RGBColor(0, 0, 0), "val": "single"},
                                    right={"color": RGBColor(0, 0, 0)})
                else:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width},
                                    bottom={"color": color, "sz": line_width, "val": "single"},
                                    left={"color": RGBColor(0, 0, 0), "val": "single"},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})
            else:
                if j == 0:
                    set_cell_border(table.cell(i, j), bottom={"color": color, "sz": line_width},
                                    top={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0)},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})
                elif j == h_cell_num - 1:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width},
                                    bottom={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0)},
                                    right={"color": RGBColor(0, 0, 0)})
                else:
                    set_cell_border(table.cell(i, j), top={"color": color, "sz": line_width},
                                    bottom={"color": RGBColor(255, 0, 0)},
                                    left={"color": RGBColor(0, 0, 0)},
                                    right={"color": RGBColor(0, 0, 0), "val": "single"})

    return table
