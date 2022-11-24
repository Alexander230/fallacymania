#!/usr/bin/python3
from math import ceil

from os import path, makedirs

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame, KeepInFrame, Flowable


class Fallacy:
    def __init__(self, name, png_path, description, example, number, icon, bg_color, pdf_coords,
                 pdf_coords_st_single, pdf_coords_st_double1, pdf_coords_st_double2):
        self.name = name
        self.png_path = png_path
        self.description = description
        self.example = example
        self.number = number
        self.icon = icon
        self.bg_color = bg_color
        self.pdf_coords = pdf_coords
        self.pdf_coords_st_single = pdf_coords_st_single
        self.pdf_coords_st_double1 = pdf_coords_st_double1
        self.pdf_coords_st_double2 = pdf_coords_st_double2


class PdfImage(Flowable):
    def __init__(self, filename_or_object, width=None, height=None, kind='direct'):
        super().__init__()
        if hasattr(filename_or_object, 'read'):
            filename_or_object.seek(0)
        self.page = PdfReader(filename_or_object, decompress=False).pages[0]
        self.xobj = pagexobj(self.page)

        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth) / self.imageHeight
        if kind in ['direct', 'absolute'] or width is None or height is None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound', 'proportional']:
            factor = min(float(width) / self._w, float(height) / self._h)
            self.drawWidth = self._w * factor
            self.drawHeight = self._h * factor

    def wrap(self, available_width, available_height):
        return self.drawWidth, self.drawHeight

    def drawOn(self, canvas, x, y, _sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5 * _sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        xobj_name = makerl(canvas, self.xobj)

        xscale = self.drawWidth / self._w
        yscale = self.drawHeight / self._h

        x -= self.xobj.BBox[0] * xscale
        y -= self.xobj.BBox[1] * yscale

        canvas.saveState()
        canvas.translate(x, y)
        canvas.scale(xscale, yscale)
        canvas.doForm(xobj_name)
        canvas.restoreState()


def draw_fallacy_box(conf, styles, canvas, fallacy, sheet_type):
    if sheet_type == 'game':
        block_x0 = fallacy.pdf_coords[0] * mm
        block_y0 = fallacy.pdf_coords[1] * mm
        block_w = conf['block_size_x'] * mm
        block_h = conf['block_size_y'] * mm
        text_pad_x = conf['card_left_pad'] * mm
        text_pad_y = 0.0
        bg_pad = 0.0
        number_x0 = block_x0 + text_pad_x + conf['fallacy_number_x'] * mm
        number_y0 = block_y0 + text_pad_y + conf['fallacy_number_y'] * mm
        fallacy_name_x = conf['fallacy_name_x']
        fallacy_name_y = conf['fallacy_name_y']
        fallacy_name_w = conf['fallacy_name_w']
        fallacy_name_h = conf['fallacy_name_h']
        fallacy_desc_x = conf['fallacy_desc_x']
        fallacy_desc_y = conf['fallacy_desc_y']
        fallacy_desc_w = conf['fallacy_desc_w']
        fallacy_desc_h = conf['fallacy_desc_h']
        fallacy_example_x = conf['fallacy_example_x']
        fallacy_example_y = conf['fallacy_example_y']
        fallacy_example_w = conf['fallacy_example_w']
        fallacy_example_h = conf['fallacy_example_h']
        fallacy_icon_x = conf['fallacy_icon_x']
        fallacy_icon_y = conf['fallacy_icon_y']
        fallacy_icon_size = conf['fallacy_icon_size']
    else:
        if sheet_type == 'st_single':
            block_x0 = fallacy.pdf_coords_st_single[0] * mm
            block_y0 = fallacy.pdf_coords_st_single[1] * mm
        elif sheet_type == 'st_double1':
            block_x0 = fallacy.pdf_coords_st_double1[0] * mm
            block_y0 = fallacy.pdf_coords_st_double1[1] * mm
        else:
            block_x0 = fallacy.pdf_coords_st_double2[0] * mm
            block_y0 = fallacy.pdf_coords_st_double2[1] * mm
        block_w = conf['st_block_size_x'] * mm
        block_h = conf['st_block_size_y'] * mm
        text_pad_x = conf['card_left_pad'] * mm
        text_pad_y = conf['st_bottom_pad'] * mm
        bg_pad = conf['st_bg_color_pad'] * mm
        number_x0 = block_x0 + bg_pad + conf['st_number_x'] * mm
        number_y0 = block_y0 + bg_pad + conf['st_number_y'] * mm
        fallacy_name_x = conf['st_fallacy_name_x']
        fallacy_name_y = conf['st_fallacy_name_y']
        fallacy_name_w = conf['st_fallacy_name_w']
        fallacy_name_h = conf['st_fallacy_name_h']
        fallacy_desc_x = conf['st_fallacy_desc_x']
        fallacy_desc_y = conf['st_fallacy_desc_y']
        fallacy_desc_w = conf['st_fallacy_desc_w']
        fallacy_desc_h = conf['st_fallacy_desc_h']
        fallacy_example_x = conf['st_fallacy_example_x']
        fallacy_example_y = conf['st_fallacy_example_y']
        fallacy_example_w = conf['st_fallacy_example_w']
        fallacy_example_h = conf['st_fallacy_example_h']
        fallacy_icon_x = conf['st_fallacy_icon_x']
        fallacy_icon_y = conf['st_fallacy_icon_y']
        fallacy_icon_size = conf['st_fallacy_icon_size']

    canvas.saveState()
    canvas.setFillColor(HexColor(fallacy.bg_color))
    canvas.rect(block_x0 + bg_pad, block_y0 + bg_pad, block_w - bg_pad * 2, block_h - bg_pad * 2, stroke=0, fill=1)
    canvas.restoreState()

    name_x0 = block_x0 + text_pad_x + fallacy_name_x * mm
    name_y0 = block_y0 + text_pad_y + fallacy_name_y * mm
    name_w = fallacy_name_w * mm
    name_h = fallacy_name_h * mm
    draw_frame(canvas, fallacy.name, styles['name'], name_x0, name_y0, name_w, name_h)

    desc_x0 = block_x0 + text_pad_x + fallacy_desc_x * mm
    desc_y0 = block_y0 + text_pad_y + fallacy_desc_y * mm
    desc_w = fallacy_desc_w * mm
    desc_h = fallacy_desc_h * mm
    draw_frame(canvas, fallacy.description, styles['desc'], desc_x0, desc_y0, desc_w, desc_h)

    example_x0 = block_x0 + text_pad_x + fallacy_example_x * mm
    example_y0 = block_y0 + text_pad_y + fallacy_example_y * mm
    example_w = fallacy_example_w * mm
    example_h = fallacy_example_h * mm
    draw_frame(canvas, fallacy.example, styles['example'], example_x0, example_y0, example_w, example_h)

    number_w = conf['fallacy_number_w'] * mm
    number_h = conf['fallacy_number_h'] * mm
    draw_frame(canvas, str(fallacy.number), styles['number'], number_x0, number_y0, number_w, number_h)

    icon_x0 = block_x0 + text_pad_x + fallacy_icon_x * mm
    icon_y0 = block_y0 + text_pad_y + fallacy_icon_y * mm
    icon_size = fallacy_icon_size * mm
    icon_in_frame = KeepInFrame(icon_size, icon_size, [fallacy.icon])
    frame = Frame(icon_x0, icon_y0, icon_size, icon_size,
                  leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary=0)
    frame.add(icon_in_frame, canvas)


def draw_frame(canvas, text, style, x0, y0, w, h):
    paragraph = Paragraph(text, style)
    paragraph_in_frame = KeepInFrame(w, h, [paragraph])
    paragraph_in_frame.canv = canvas
    real_w, real_h = paragraph_in_frame.wrap(w, h)
    y0_fixed = y0 - (h - real_h) / 2
    frame = Frame(x0, y0_fixed, w, h, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary=0)
    frame.add(paragraph_in_frame, canvas)


def init_data():
    page_size = (210.0, 297.0)
    page_border = 2.0
    stickers_gap = 2.0
    fallacies_num = 45
    table_grid_size = (3, 5)
    sticker_table_grid_size = (3, 3)
    conf = {
        'fallacies_num': fallacies_num,
        'page_size': A4,
        'page_size_x': page_size[0] - page_border * 2,
        'page_size_y': page_size[1] - page_border * 2,
        'table_grid_x': table_grid_size[0],
        'table_grid_y': table_grid_size[1],
        'st_table_grid_x': sticker_table_grid_size[0],
        'st_table_grid_y': sticker_table_grid_size[1],
        'block_size_x': (page_size[0] - page_border * 2) / table_grid_size[0],
        'block_size_y': (page_size[1] - page_border * 2) / table_grid_size[1],
        'st_block_size_x': (page_size[0] - page_border * 2) / sticker_table_grid_size[0],
        'st_block_size_y': (page_size[1] - page_border * 2) / sticker_table_grid_size[1],
        'game_pages': ceil(fallacies_num / (table_grid_size[0] * table_grid_size[1])),
        'st_pages_single': ceil(fallacies_num / (sticker_table_grid_size[0] * sticker_table_grid_size[1])),
        'st_pages_double': ceil(fallacies_num * 2 / (sticker_table_grid_size[0] * sticker_table_grid_size[1])),
        'page_border': page_border,
        'card_size_x': 56.6,
        'card_left_pad': stickers_gap / 2,
        'card_size_y': 46.222,
        'st_size_x': 64,
        'st_bg_color_pad': stickers_gap / 2,
        'st_size_y': 81.2,
        'st_bottom_pad': 17.489,
        'st_fallacy_name_x': 0.0,
        'st_fallacy_name_y': 65.476,
        'st_fallacy_name_w': 65.6,
        'st_fallacy_name_h': 6.0,
        'st_fallacy_desc_x': 1.8,
        'st_fallacy_desc_y': 48.347,
        'st_fallacy_desc_w': 62.0,
        'st_fallacy_desc_h': 12.674,
        'st_fallacy_icon_x': 15,
        'st_fallacy_icon_y': 12,
        'st_fallacy_icon_size': 35.0,
        'st_fallacy_example_x': 0.0,
        'st_fallacy_example_y': -10.0,
        'st_fallacy_example_w': 65.1,
        'st_fallacy_example_h': 24.1,
        'st_fallacy_number_x': 51.0,
        'st_fallacy_number_y': 0.7,
        'fallacy_name_x': 0.0,
        'fallacy_name_y': 49.476,
        'fallacy_name_w': 65.6,
        'fallacy_name_h': 6.0,
        'fallacy_desc_x': 1.8,
        'fallacy_desc_y': 35.347,
        'fallacy_desc_w': 62.0,
        'fallacy_desc_h': 12.674,
        'fallacy_icon_x': -1.5,
        'fallacy_icon_y': 3,
        'fallacy_icon_size': 33.0,
        'fallacy_example_x': 27.5,
        'fallacy_example_y': 8.0,
        'fallacy_example_w': 37.1,
        'fallacy_example_h': 24.1,
        'fallacy_number_x': 62.0,
        'fallacy_number_y': 0.7,
        'st_number_x': 62.0,
        'st_number_y': 1.0,
        'fallacy_number_w': 4.0,
        'fallacy_number_h': 2.237,
        'input_file_prefix': 'fallacies-',
        'input_file_suffix': '.txt',
        'output_file_prefix': 'fallacies-',
        'output_file_suffix': '.pdf',
        'stickers_folder': 'stickers/',
        'st_output_file_prefix': 'stickers-',
        'st_single': '-single.pdf',
        'st_double': '-double.pdf',
        'icons_path': 'icons/vector/',
        'icons_suffix': '.pdf'
    }

    fonts_dir = '/usr/share/fonts/'
    font_dejavu_dir = fonts_dir + 'truetype/dejavu/'
    font_liberation_dir = fonts_dir + 'truetype/liberation/'
    registerFont(TTFont('DejaVuSans', font_dejavu_dir + 'DejaVuSans.ttf'))
    registerFont(TTFont('DejaVuSans-Bold', font_dejavu_dir + 'DejaVuSans-Bold.ttf'))
    registerFont(TTFont('DejaVuSans-Italic', font_dejavu_dir + 'DejaVuSans-Oblique.ttf'))
    registerFont(TTFont('DejaVuSans-BoldItalic', font_dejavu_dir + 'DejaVuSans-BoldOblique.ttf'))
    registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold',
                       italic='DejaVuSans-Italic', boldItalic='DejaVuSans-BoldItalic')
    registerFont(TTFont('LiberationSans', font_liberation_dir + 'LiberationSans-Regular.ttf'))
    registerFont(TTFont('LiberationSans-Bold', font_liberation_dir + 'LiberationSans-Bold.ttf'))
    registerFont(TTFont('LiberationSans-Italic', font_liberation_dir + 'LiberationSans-Italic.ttf'))
    registerFont(TTFont('LiberationSans-BoldItalic', font_liberation_dir + 'LiberationSans-BoldItalic.ttf'))
    registerFontFamily('LiberationSans', normal='LiberationSans', bold='LiberationSans-Bold',
                       italic='LiberationSans-Italic', boldItalic='LiberationSans-BoldItalic')

    name_font = 'DejaVuSans-Bold'
    desc_font = name_font
    example_font = 'LiberationSans-BoldItalic'
    number_font = name_font
    name_font_size = 11
    desc_font_size = 8
    example_font_size = 7
    number_font_size = 8
    styles = {
        'name': ParagraphStyle(
            name='name',
            fontName=name_font,
            fontSize=name_font_size,
            alignment=TA_CENTER,
            leading=name_font_size,
            textColor=white
        ),
        'desc': ParagraphStyle(
            name='desc',
            fontName=desc_font,
            fontSize=desc_font_size,
            alignment=TA_CENTER,
            leading=desc_font_size,
            textColor=white
        ),
        'example': ParagraphStyle(
            name='example',
            fontName=example_font,
            fontSize=example_font_size,
            alignment=TA_CENTER,
            leading=example_font_size,
            textColor=white
        ),
        'number': ParagraphStyle(
            name='number',
            fontName=number_font,
            fontSize=number_font_size,
            alignment=TA_CENTER,
            textColor=white
        )
    }

    colors = {
        0: '#3CAFEE', 1: '#28A8EC', 2: '#159FEA', 3: '#1492D6', 4: '#1285C2',
        5: '#1078AF', 6: '#0E6A9C', 7: '#0D5C88', 8: '#0B5075',
        9: '#DE4549', 10: '#DA3236', 11: '#CF2529', 12: '#BB2226', 13: '#A81E21',
        14: '#951A1D', 15: '#81161A', 16: '#6C1315', 17: '#581012',
        18: '#AC6C3E', 19: '#9C6338', 20: '#8C5933', 21: '#7D4F2D', 22: '#6D4527',
        23: '#5E3C22', 24: '#4F311C', 25: '#3F2616', 26: '#301D10',
        27: '#9593BB', 28: '#8D8BB6', 29: '#8482B0', 30: '#7A78AB', 31: '#7370A5',
        32: '#69669F', 33: '#625F98', 34: '#5C598E', 35: '#555386',
        36: '#5BB9AB', 37: '#4DB3A4', 38: '#46A496', 39: '#409588', 40: '#39867A',
        41: '#33776C', 42: '#2D6860', 43: '#265953', 44: '#204A45'
    }

    languages = ('rus', 'eng')

    return conf, styles, colors, languages


def main():
    conf, styles, colors, languages = init_data()
    for language in languages:
        input_file_name = ''.join((conf['input_file_prefix'], language, conf['input_file_suffix']))
        with open(input_file_name) as input_file:
            lines = input_file.readlines()
        lines.append('')
        fallacies = []
        fallacy_read_completed = False
        current_name = ''
        current_png_path = ''
        current_icon = None
        current_bg_color = ''
        current_pdf_coords = (0, 0, 0)
        current_pdf_coords_st_single = (0, 0)
        current_pdf_coords_st_double1 = (0, 0)
        current_pdf_coords_st_double2 = (0, 0)
        current_description = ''
        current_example = ''
        for i, line in enumerate(lines):
            if i % 4 == 0:
                if fallacy_read_completed:
                    fallacies.append(Fallacy(current_name, current_png_path, current_description, current_example,
                                             i // 4 - 1, current_icon, current_bg_color, current_pdf_coords,
                                             current_pdf_coords_st_single,
                                             current_pdf_coords_st_double1, current_pdf_coords_st_double2))
                    fallacy_read_completed = False
                current_name = line.strip().replace('\\\\n', '<br/>')
            elif i % 4 == 1:
                current_png_path = line.strip()
            elif i % 4 == 2:
                current_description = line.strip().replace('\\\\n', '<br/>')
            elif i % 4 == 3:
                current_example = line.strip().replace('\\\\n', '<br/>')
                current_icon_fname = ''.join((conf['icons_path'], str(i // 4).rjust(2, '0'), conf['icons_suffix']))
                current_icon = PdfImage(current_icon_fname)
                current_bg_color = colors[i // 4]
                current_gx = (i // 4) % (conf['table_grid_x'] *  conf['game_pages'])
                current_x = current_gx % conf['table_grid_x']
                current_page = current_gx // conf['table_grid_x']
                current_y = (i // 4) // (conf['table_grid_x'] *  conf['game_pages'])
                current_pdf_coords = (current_x * conf['block_size_x'] + conf['page_border'],
                                      conf['page_size_y'] + conf['page_border']
                                      - (current_y + 1) * conf['block_size_y'], current_page)
                st_single_position = (i // 4) % (conf['st_table_grid_x'] * conf['st_table_grid_y'])
                st_double1_position = ((i // 4) * 2) % (conf['st_table_grid_x'] * conf['st_table_grid_y'])
                st_double2_position = ((i // 4) * 2 + 1) % (conf['st_table_grid_x'] * conf['st_table_grid_y'])
                current_pdf_coords_st_single, current_pdf_coords_st_double1, current_pdf_coords_st_double2 = map(
                    lambda position: (position % conf['st_table_grid_x'] * conf['st_block_size_x']
                                      + conf['page_border'],
                                      conf['page_size_y'] + conf['page_border']
                                      - (position // conf['st_table_grid_x'] + 1) * conf['st_block_size_y']),
                    (st_single_position, st_double1_position, st_double2_position))
                fallacy_read_completed = True

        output_file_name = ''.join((conf['output_file_prefix'], language, conf['output_file_suffix']))
        canvas_game = Canvas(output_file_name, pagesize=conf['page_size'])
        stickers_folder = path.dirname(conf['stickers_folder'])
        if not path.exists(stickers_folder):
            makedirs(stickers_folder)
        st_single_out_file_name = ''.join((conf['stickers_folder'], conf['st_output_file_prefix'], language,
                                 conf['st_single']))
        st_double_out_file_name = ''.join((conf['stickers_folder'], conf['st_output_file_prefix'], language,
                                 conf['st_double']))
        st_single_out_canv = Canvas(filename=st_single_out_file_name, pagesize=conf['page_size'])
        st_double_out_canv = Canvas(filename=st_double_out_file_name, pagesize=conf['page_size'])

        for page in range(conf['st_pages_single']):
            for y in range(conf['st_table_grid_y']):
                for x in range(conf['st_table_grid_x']):
                    fallacy_num = (page * conf['st_table_grid_y'] + y) * conf['st_table_grid_x'] + x
                    fallacy = fallacies[fallacy_num]
                    draw_fallacy_box(conf, styles, st_single_out_canv, fallacy, 'st_single')
            st_single_out_canv.showPage()

        for page in range(conf['st_pages_double']):
            for y in range(conf['st_table_grid_y']):
                for x in range(conf['st_table_grid_x']):
                    fallacy_num2 = (page * conf['st_table_grid_y'] + y) * conf['st_table_grid_x'] + x
                    fallacy_num = fallacy_num2 // 2
                    fallacy = fallacies[fallacy_num]
                    ty = 'st_double1' if fallacy_num2 % 2 == 0 else 'st_double2'
                    draw_fallacy_box(conf, styles, st_double_out_canv, fallacy, ty)
            st_double_out_canv.showPage()

        for page in range(conf['game_pages']):
            for fallacy in fallacies:
                if fallacy.pdf_coords[2] == page:
                    draw_fallacy_box(conf, styles, canvas_game, fallacy, 'game')
            canvas_game.showPage()

        canvas_game.save()
        st_single_out_canv.save()
        st_double_out_canv.save()


if __name__ == "__main__":
    main()
