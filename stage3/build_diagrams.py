from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

OUT = Path('stage3')
OUT.mkdir(exist_ok=True)

try:
    FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
    BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    if not Path(FONT).exists():
        FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
except Exception:
    FONT = BOLD = None

def f(size, bold=False):
    try: return ImageFont.truetype(BOLD if bold else FONT, size)
    except Exception: return ImageFont.load_default()

def svg_text(x, y, text, size=16, bold=False, anchor='middle', fill='#182A3A'):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}px" font-weight="{"700" if bold else "400"}" text-anchor="{anchor}" fill="{fill}">{escape(text)}</text>'

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0),test,font=font)[2] <= maxw: cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def actor_svg(x,y,label):
    return f'<g stroke="#243B53" stroke-width="2" fill="none"><circle cx="{x}" cy="{y-20}" r="12" fill="#E7F0F8"/><line x1="{x}" y1="{y-8}" x2="{x}" y2="{y+28}"/><line x1="{x-18}" y1="{y+3}" x2="{x+18}" y2="{y+3}"/><line x1="{x}" y1="{y+28}" x2="{x-16}" y2="{y+52}"/><line x1="{x}" y1="{y+28}" x2="{x+16}" y2="{y+52}"/></g>{svg_text(x,y+75,label,15,True)}'

def usecase_svg():
    W,H=1500,900; parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#FFFFFF"/><style>.line{{stroke:#6B7C93;stroke-width:2;fill:none}}.uc{{fill:#F4F8FC;stroke:#2F5D7E;stroke-width:2}}</style>',svg_text(750,48,'IT Ticket Manager — диаграмма вариантов использования',28,True)]
    parts.append('<rect x="290" y="90" width="930" height="750" rx="8" fill="#FBFCFE" stroke="#6B7C93" stroke-width="2"/>')
    parts.append(svg_text(755,124,'Система IT Ticket Manager',20,True))
    parts.append(actor_svg(120,370,'Пользователь'))
    parts.append(actor_svg(1380,370,'IT-техник'))
    ucs=[('Авторизоваться',520,190),('Создать заявку',520,300),('Просмотреть свои заявки',520,410),('Проверить статус',520,520),('Добавить комментарий',520,630),('Подтвердить решение',520,740),('Сообщить о нерешённой проблеме',830,740),('Просмотреть очередь заявок',1000,190),('Принять заявку в работу',1000,300),('Изменить статус',1000,410),('Указать результат решения',1000,520),('Закрыть заявку',1000,630)]
    for label,x,y in ucs:
        parts.append(f'<ellipse class="uc" cx="{x}" cy="{y}" rx="170" ry="36"/>'); parts.append(svg_text(x,y+6,label,15))
    # associations
    edges=[(150,350,350,190),(150,350,350,300),(150,350,350,410),(150,350,350,520),(150,350,350,630),(150,350,350,740),(150,350,660,740),(1350,350,1170,190),(1350,350,1170,300),(1350,350,1170,410),(1350,350,1170,520),(1350,350,1170,630)]
    for x1,y1,x2,y2 in edges: parts.append(f'<line class="line" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    parts.append(f'<line class="line" x1="690" y1="190" x2="830" y2="190" stroke-dasharray="7 6"/><text x="760" y="180" font-family="Arial" font-size="13" text-anchor="middle" fill="#52606D">email-события</text>')
    parts.append(svg_text(755,875,'Email-события проектируются; фактическая SMTP-доставка не входит в этап.',14,False,'middle','#52606D'))
    parts.append('</svg>'); return ''.join(parts)

def activity_svg():
    W,H=1600,1450; p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#FFFFFF"/><style>.a{{fill:#F6F9FC;stroke:#2F5D7E;stroke-width:2}}.d{{fill:#FFF7E6;stroke:#B7791F;stroke-width:2}}.l{{stroke:#52606D;stroke-width:2;fill:none;marker-end:url(#arr)}}.lane{{stroke:#AAB7C4;stroke-width:2;fill:#FBFCFE}}</style><defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L9,3 L0,6 z" fill="#52606D"/></marker></defs>',svg_text(800,48,'IT Ticket Manager — диаграмма активности',28,True)]
    lanes=[(0,520,'Пользователь'),(520,1060,'Система'),(1060,1600,'IT-техник')]
    for x1,x2,label in lanes:
        p.append(f'<rect class="lane" x="{x1}" y="80" width="{x2-x1}" height="1320"/>'); p.append(svg_text((x1+x2)//2,112,label,19,True))
    def box(x,y,w,h,text,cls='a'):
        p.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>')
        lines=text.split('\n')
        for i,line in enumerate(lines): p.append(svg_text(x+w/2,y+h/2+6+(i-(len(lines)-1)/2)*20,line,16))
    def line(x1,y1,x2,y2): p.append(f'<line class="l" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    # main path
    box(130,145,260,64,'Создать заявку'); box(650,145,300,64,'Проверить данные'); box(1140,145,300,64,'Принять заявку в работу')
    box(650,300,300,64,'Зарегистрировать\nстатус «Открыта»'); box(1140,300,300,64,'Решить проблему и\nуказать результат')
    box(130,455,260,64,'Проверить результат'); box(650,455,300,64,'Сохранить решение\nи создать email-событие'); box(1140,455,300,64,'Перевести в «Решена»')
    box(130,610,260,64,'Подтвердить или\nотклонить решение','d'); box(650,610,300,64,'Записать событие\nподтверждения/отказа'); box(1140,610,300,64,'Закрыть заявку\nпосле подтверждения')
    box(650,765,300,64,'Вернуть статус\n«В работе» при отказе','d'); box(1140,765,300,64,'Уточнить описание\nи продолжить работу','d')
    box(650,920,300,64,'Создать email-событие\nоб изменении статуса'); box(1140,920,300,64,'Повторно обработать\nзаявку')
    # arrows
    for a in [(390,177,650,177),(950,177,1140,177),(1290,209,1290,300),(1140,332,950,332),(650,332,520,332),(520,332,520,487),(390,487,650,487),(950,487,1140,487),(1290,519,1290,610),(390,642,650,642),(950,642,1140,642),(650,674,520,765),(950,797,1140,797),(1290,829,1290,920),(950,952,1290,952)]: line(*a)
    p.append(svg_text(800,1035,'Развилка: подтверждение фиксируется как событие, а не как отдельный статус.',16,False,'middle','#7B4A00'))
    p.append('<circle cx="140" cy="1100" r="20" fill="#243B53"/><line class="l" x1="160" y1="1100" x2="650" y2="1100"/>')
    box(650,1060,300,64,'Заявка закрыта'); p.append('<circle cx="1300" cy="1100" r="20" fill="#FFFFFF" stroke="#243B53" stroke-width="5"/>')
    p.append('</svg>'); return ''.join(p)

def svg_to_png(kind, path, size):
    im=Image.new('RGB', size, 'white'); d=ImageDraw.Draw(im)
    navy='#182A3A'; blue='#2F5D7E'; pale='#F4F8FC'; gray='#6B7C93'; gold='#B7791F'
    d.text((size[0]//2,25), 'IT Ticket Manager — ' + ('варианты использования' if kind=='use' else 'диаграмма активности'), font=f(28,True), fill=navy, anchor='ma')
    if kind=='use':
        d.rounded_rectangle((290,90,1220,840),radius=8,outline=gray,width=2,fill='#FBFCFE')
        d.text((755,105),'Система IT Ticket Manager',font=f(20,True),fill=navy,anchor='ma')
        def actor(x,y,label):
            d.ellipse((x-12,y-32,x+12,y-8),fill='#E7F0F8',outline=navy,width=2); d.line((x,y-8,x,y+28),fill=navy,width=2); d.line((x-18,y+3,x+18,y+3),fill=navy,width=2); d.line((x,y+28,x-16,y+52),fill=navy,width=2); d.line((x,y+28,x+16,y+52),fill=navy,width=2); d.text((x,y+75),label,font=f(15,True),fill=navy,anchor='ma')
        actor(120,370,'Пользователь'); actor(1380,370,'IT-техник')
        ucs=[('Авторизоваться',520,190),('Создать заявку',520,300),('Просмотреть свои заявки',520,410),('Проверить статус',520,520),('Добавить комментарий',520,630),('Подтвердить решение',520,740),('Сообщить о нерешённой проблеме',830,740),('Просмотреть очередь заявок',1000,190),('Принять заявку в работу',1000,300),('Изменить статус',1000,410),('Указать результат решения',1000,520),('Закрыть заявку',1000,630)]
        for label,x,y in ucs:
            d.ellipse((x-170,y-36,x+170,y+36),fill=pale,outline=blue,width=2); d.text((x,y),label,font=f(15),fill=navy,anchor='mm')
        edges=[(150,350,350,190),(150,350,350,300),(150,350,350,410),(150,350,350,520),(150,350,350,630),(150,350,350,740),(150,350,660,740),(1350,350,1170,190),(1350,350,1170,300),(1350,350,1170,410),(1350,350,1170,520),(1350,350,1170,630)]
        for e in edges: d.line(e,fill=gray,width=2)
        d.text((755,875),'Email-события проектируются; фактическая SMTP-доставка не входит в этап.',font=f(14),fill='#52606D',anchor='ma')
    else:
        lanes=[(0,520,'Пользователь'),(520,1060,'Система'),(1060,1600,'IT-техник')]
        for x1,x2,label in lanes: d.rectangle((x1,80,x2,1400),fill='#FBFCFE',outline='#AAB7C4',width=2); d.text(((x1+x2)//2,95),label,font=f(19,True),fill=navy,anchor='ma')
        def box(x,y,w,h,text,fill=pale,outline=blue):
            d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill=fill,outline=outline,width=2)
            lines=text.split('\n'); yy=y+h/2-(len(lines)-1)*10
            for line in lines: d.text((x+w/2,yy),line,font=f(16),fill=navy,anchor='mm'); yy+=20
        def arr(a,b): d.line((a[0],a[1],b[0],b[1]),fill='#52606D',width=2)
        boxes=[(130,145,260,64,'Создать заявку'),(650,145,300,64,'Проверить данные'),(1140,145,300,64,'Принять заявку в работу'),(650,300,300,64,'Зарегистрировать\nстатус «Открыта»'),(1140,300,300,64,'Решить проблему и\nуказать результат'),(130,455,260,64,'Проверить результат'),(650,455,300,64,'Сохранить решение\nи создать email-событие'),(1140,455,300,64,'Перевести в «Решена»'),(130,610,260,64,'Подтвердить или\nотклонить решение'),(650,610,300,64,'Записать событие\nподтверждения/отказа'),(1140,610,300,64,'Закрыть заявку\nпосле подтверждения'),(650,765,300,64,'Вернуть статус\n«В работе» при отказе'),(1140,765,300,64,'Уточнить описание\nи продолжить работу'),(650,920,300,64,'Создать email-событие\nоб изменении статуса'),(1140,920,300,64,'Повторно обработать\nзаявку')]
        for x,y,w,h,t in boxes: box(x,y,w,h,t, '#FFF7E6' if 'откл' in t or 'Вернуть' in t or 'Уточнить' in t else pale, gold if ('откл' in t or 'Вернуть' in t or 'Уточнить' in t) else blue)
        for a,b in [((390,177),(650,177)),((950,177),(1140,177)),((1290,209),(1290,300)),((1140,332),(950,332)),((650,332),(520,332)),((520,332),(520,487)),((390,487),(650,487)),((950,487),(1140,487)),((1290,519),(1290,610)),((390,642),(650,642)),((950,642),(1140,642)),((650,674),(520,765)),((950,797),(1140,797)),((1290,829),(1290,920)),((950,952),(1290,952))]: arr(a,b)
        d.text((800,1035),'Развилка: подтверждение фиксируется как событие, а не как отдельный статус.',font=f(16),fill='#7B4A00',anchor='ma')
        d.ellipse((120,1080,160,1120),fill=navy); d.line((160,1100,650,1100),fill='#52606D',width=2); box(650,1060,300,64,'Заявка закрыта'); d.ellipse((1280,1080,1320,1120),fill='white',outline=navy,width=5)
    im.save(path)

use=usecase_svg(); act=activity_svg()
(OUT/'use_case_diagram.svg').write_text(use,encoding='utf-8')
(OUT/'activity_diagram.svg').write_text(act,encoding='utf-8')
svg_to_png('use',OUT/'use_case_diagram.png',(1500,900)); svg_to_png('activity',OUT/'activity_diagram.png',(1600,1450))

(OUT/'use_case_diagram.puml').write_text('''@startuml\ntitle IT Ticket Manager - Диаграмма вариантов использования\nleft to right direction\nactor "Пользователь" as User\nactor "IT-техник" as Tech\nrectangle "Система IT Ticket Manager" {\n  usecase "Авторизоваться" as U01\n  usecase "Создать заявку" as U02\n  usecase "Просмотреть свои заявки" as U03\n  usecase "Проверить статус" as U04\n  usecase "Добавить комментарий" as U05\n  usecase "Подтвердить решение" as U06\n  usecase "Сообщить о нерешённой проблеме" as U07\n  usecase "Просмотреть очередь заявок" as T01\n  usecase "Принять заявку в работу" as T02\n  usecase "Изменить статус" as T03\n  usecase "Указать результат решения" as T04\n  usecase "Закрыть заявку" as T05\n}\nUser --> U01\nUser --> U02\nUser --> U03\nUser --> U04\nUser --> U05\nUser --> U06\nUser --> U07\nTech --> U01\nTech --> T01\nTech --> T02\nTech --> T03\nTech --> T04\nTech --> T05\nnote bottom of T05\nЗакрытие разрешено только после\nподтверждения автора заявки.\nend note\nnote right of U07\nОтказ автора возвращает заявку\nв состояние «В работе».\nend note\n@enduml\n''',encoding='utf-8')
(OUT/'activity_diagram.puml').write_text('''@startuml\ntitle IT Ticket Manager - Диаграмма активности\n|Пользователь|\nstart\n:Создать заявку;\n|Система|\n:Проверить данные;\nif (Данные корректны?) then (да)\n  :Зарегистрировать заявку;\n  :Установить статус «Открыта»;\nelse (нет)\n  :Показать ошибки формы;\n  |Пользователь|\n  :Исправить данные;\n  |Система|\n  :Повторить проверку;\nendif\n|IT-техник|\n:Принять заявку в работу;\n:Решить проблему и указать результат;\n|Система|\n:Сохранить решение;\n:Установить статус «Решена»;\n:Создать проектируемое email-событие;\n|Пользователь|\n:Проверить результат;\nif (Решение подтверждено?) then (да)\n  |Система|\n  :Записать событие подтверждения;\n  |IT-техник|\n  :Закрыть заявку;\n  |Система|\n  :Создать email-событие о закрытии;\n  stop\nelse (нет)\n  :Указать причину отказа;\n  |Система|\n  :Записать событие отказа;\n  :Вернуть статус «В работе»;\n  :Создать email-событие;\n  |IT-техник|\n  :Уточнить данные и повторно обработать;\n  |Пользователь|\n  :Проверить результат повторно;\nendif\n@enduml\n''',encoding='utf-8')
print('created diagrams')
