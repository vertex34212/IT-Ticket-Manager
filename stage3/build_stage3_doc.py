from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT=Path('stage3'); doc=Document(); sec=doc.sections[0]
sec.top_margin=Inches(.65); sec.bottom_margin=Inches(.6); sec.left_margin=Inches(.7); sec.right_margin=Inches(.7)
for s in ['Normal','Body Text']:
    st=doc.styles[s]; st.font.name='Aptos'; st.font.size=Pt(10.2); st.font.color.rgb=RGBColor(0,0,0); st.paragraph_format.space_after=Pt(5); st.paragraph_format.line_spacing=1.08
for n,sz in [(1,16),(2,13),(3,11)]:
    st=doc.styles[f'Heading {n}']; st.font.name='Aptos Display'; st.font.size=Pt(sz); st.font.bold=True; st.font.color.rgb=RGBColor(0,0,0); st.paragraph_format.keep_with_next=True
doc.styles['Title'].font.name='Aptos Display'; doc.styles['Title'].font.size=Pt(25); doc.styles['Title'].font.bold=True; doc.styles['Title'].font.color.rgb=RGBColor(0,0,0)
doc.styles['Subtitle'].font.name='Aptos Display'; doc.styles['Subtitle'].font.size=Pt(13); doc.styles['Subtitle'].font.color.rgb=RGBColor(0,0,0)
header=sec.header.paragraphs[0]; header.text='IT Ticket Manager  |  Этап 3  |  UML'; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for r in header.runs: r.font.name='Aptos'; r.font.size=Pt(8); r.font.color.rgb=RGBColor(90,90,90)
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER; footer.add_run('Tcacenco Dmitrii  •  P2524r  •  '); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)
NAVY='17365D'; PALE='F3F6F9'; GRAY='D9D9D9'
def shade(c,fill):
    p=c._tc.get_or_add_tcPr(); x=OxmlElement('w:shd'); x.set(qn('w:fill'),fill); p.append(x)
def border(t):
    b=OxmlElement('w:tblBorders')
    for e in ['top','left','bottom','right','insideH','insideV']:
        x=OxmlElement('w:'+e); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),GRAY); b.append(x)
    t._tbl.tblPr.append(b)
def table(head,rows,widths=None,size=8.8):
    t=doc.add_table(rows=1,cols=len(head)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False; border(t)
    trPr=t.rows[0]._tr.get_or_add_trPr(); rep=OxmlElement('w:tblHeader'); rep.set(qn('w:val'),'true'); trPr.append(rep)
    for i,v in enumerate(head):
        c=t.rows[0].cells[i]; c.text=''; r=c.paragraphs[0].add_run(str(v)); r.bold=True; r.font.size=Pt(size); r.font.name='Aptos'; r.font.color.rgb=RGBColor(255,255,255); shade(c,NAVY); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for ri,row in enumerate(rows):
        cs=t.add_row().cells
        for i,v in enumerate(row):
            cs[i].text=''; p=cs[i].paragraphs[0]; p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2); r=p.add_run(str(v)); r.font.name='Aptos'; r.font.size=Pt(size); cs[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri%2: shade(cs[i],PALE)
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Inches(w)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)
def h(x,n=1): doc.add_heading(x,level=n)
def p(x): doc.add_paragraph(x,style='Body Text')
def bullets(xs):
    for x in xs: doc.add_paragraph(x,style='List Bullet')

doc.add_paragraph().paragraph_format.space_after=Pt(50)
x=doc.add_paragraph(style='Title'); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.add_run('IT Ticket Manager')
x=doc.add_paragraph(style='Subtitle'); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.add_run('UML диаграммы и пояснение  |  Этап 3')
x=doc.add_paragraph(); x.alignment=WD_ALIGN_PARAGRAPH.CENTER; x.add_run('Учебный проект настольного приложения').bold=True
doc.add_paragraph().paragraph_format.space_after=Pt(35)
table(['Параметр','Значение'],[['Студент','Tcacenco Dmitrii'],['Группа','P2524r'],['Преподаватель','Natalia Gairunova'],['Основа','SRS этапа 2 и планирование этапа 1'],['Статус','Проектная UML-модель']],[2.0,4.0],10)
p('Документ содержит Use Case Diagram и Activity Diagram для IT Ticket Manager. Диаграммы согласованы со сценариями UC-01–UC-06, функциональными требованиями FR-001–FR-031 и бизнес-правилом: подтверждение решения является событием, а не отдельным статусом. Реальная SMTP-доставка не заявляется как реализованная.')
h('Состав материалов')
table(['Материал','Назначение'],[['Use Case Diagram','Роли и доступные действия пользователя и IT-техника.'],['Activity Diagram','Процесс от создания заявки до закрытия с альтернативной ветвью отказа.'],['PlantUML .puml','Исходники диаграмм для дальнейшего редактирования и рендера.'],['PNG и SVG','Растровое и векторное представления диаграмм.']],[1.8,4.2],9.2)
doc.add_page_break()
h('1. Use Case Diagram')
p('Диаграмма вариантов использования показывает внешних акторов и доступные им действия в границах системы. Обе роли проходят авторизацию, но права после входа различаются.')
doc.add_picture(str(OUT/'use_case_diagram.png'),width=Inches(6.5)); cap=doc.add_paragraph('Рисунок 1 — Диаграмма вариантов использования IT Ticket Manager'); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
h('1.1 Согласование со сценариями и требованиями',2)
table(['Элемент диаграммы','Сценарии SRS','Требования'],[['Авторизоваться','Общее предусловие UC-01–UC-06','FR-001–006'],['Создать заявку','UC-01','FR-007–011'],['Очередь и приём в работу','UC-02','FR-012–018'],['Результат решения','UC-03','FR-018, FR-024'],['Подтверждение или отказ','UC-04','FR-019–020'],['Закрытие заявки','UC-05','FR-021–022'],['История и комментарии','UC-06 и карточка','FR-016, FR-023, FR-026–028'],['Email-события','UC-01–UC-05','FR-029–031']],[2.25,2.1,1.65],8.3)
p('В диаграмму не добавлена административная роль: SRS определяет обязательными только пользователя и техника. Email-события показаны как проектируемая интеграционная граница, а не как самостоятельная роль с подтверждённой доставкой.')
doc.add_page_break()
h('2. Activity Diagram')
p('Диаграмма активности описывает основной поток обработки одной заявки и ответственность участников. Дорожки разделяют действия пользователя, системы и IT-техника.')
doc.add_picture(str(OUT/'activity_diagram.png'),width=Inches(6.55)); cap=doc.add_paragraph('Рисунок 2 — Диаграмма активности с дорожками ответственности'); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
h('2.1 Основной поток',2)
table(['Шаг','Ответственный','Результат'],[['1','Пользователь','Заполняет и отправляет заявку.'],['2','Система','Проверяет данные и регистрирует статус «Открыта».'],['3','IT-техник','Принимает заявку в работу и указывает результат.'],['4','Система','Переводит заявку в «Решена» и создаёт email-событие.'],['5','Пользователь','Проверяет результат.'],['6','IT-техник','Закрывает заявку после подтверждения автора.']],[.55,1.5,3.95],8.7)
h('2.2 Альтернативные ветви',2)
bullets(['Ошибка заполнения: система не создаёт заявку, сообщает о проблемах и возвращает пользователя к исправлению данных.','Отказ автора: пользователь указывает причину, система сохраняет событие отказа и возвращает заявку в «В работе».','Повторная обработка: техник уточняет описание и повторно выполняет решение.','Подтверждение решения: фиксируется в истории как событие; отдельный статус «Подтверждена» не вводится.'])
h('3. Проверка соответствия SRS')
table(['Правило / требование','Отражение в диаграммах','Результат'],[['Две роли: пользователь и техник','Акторы Use Case и три дорожки Activity','Согласовано'],['UC-01–UC-06','Use Case содержит все шесть сценариев','Согласовано'],['FR-001–031','Таблица трассировки связывает действия и FR','Согласовано'],['Подтверждение не является статусом','Событие подтверждения в Activity и пояснительная заметка','Согласовано'],['Закрытие только после подтверждения','Предусловие явно указано в Use Case и Activity','Согласовано'],['Отказ возвращает в работу','Альтернативная ветвь Activity','Согласовано'],['Email проектируется','Подписи email-событий без утверждения SMTP-доставки','Согласовано']],[2.2,3.25,1.0],8.2)
h('4. Артефакты и воспроизводимость')
p('Исходные файлы PlantUML находятся рядом с изображениями. Они используют стандартные конструкции actor, usecase, rectangle, swimlanes, if/then/else и start/stop и предназначены для рендера в PlantUML-совместимом инструменте. SVG является векторным представлением для отчёта, PNG — готовым изображением для вставки в текстовый документ.')
h('5. Вывод')
p('Этап 3 подготовлен как согласованный комплект UML-материалов. Use Case фиксирует границы функциональности и права двух ролей. Activity показывает полный жизненный цикл заявки, контроль корректности данных, решение, подтверждение, возврат в работу и закрытие. Диаграммы не вводят функций, статусов или интеграций, отсутствующих в SRS.')
doc.save(OUT/'IT_Ticket_Manager_Etap_3_UML.docx'); print((OUT/'IT_Ticket_Manager_Etap_3_UML.docx').resolve())
