"""Render official response HTML, preserving verbal text, tables and superscripts."""
import re
import html as stdhtml
from lxml import html
BLOCKS={'p','div','br','tr','table','h1','h2','h3','h4','h5','h6','li','ul','ol','section','article','blockquote','pre'}
def normalize(s):return re.sub(r'[\s\u200b\ufeff]+',' ',s.replace('\u00ad','')).strip()
def render(raw):
 root=html.fromstring(raw.encode('utf-8'),parser=html.HTMLParser(encoding='utf-8'))
 body=root.find('.//body');root=body if body is not None else root
 out=[];tables=[]
 def inline(e):
  if not isinstance(e.tag,str):return ''
  tag=e.tag.lower()
  if tag in {'script','style','input','label','img','image'}:return ''
  if tag=='table':return table(e)
  value=stdhtml.escape(e.text or '',quote=False)
  for child in e:
   if isinstance(child.tag,str) and child.tag.lower() in BLOCKS:value+=' '
   if isinstance(child.tag,str) and child.tag.lower()=='br':value+=' '
   else:value+=inline(child)
   if isinstance(child.tag,str) and child.tag.lower() in BLOCKS:value+=' '
   value+=stdhtml.escape(child.tail or '',quote=False)
  if tag in {'sup','sub'}:value='<'+tag+'>'+value+'</'+tag+'>'
  elif tag=='span' and 'W9' in (e.get('class') or '').split():value='<sup>'+value+'</sup>'
  return value
 def table(e):
  pieces=['<table>']
  def contents(container):
   if container.text and container.text.strip():pieces.append(stdhtml.escape(container.text,quote=False))
   for child in container:
    if not isinstance(child.tag,str):continue
    tag=child.tag.lower()
    if tag=='tr':
     cells=[]
     for cell in child:
      if not isinstance(cell.tag,str) or cell.tag.lower() not in {'td','th'}:continue
      attrs=''.join(' '+key+'="'+stdhtml.escape(cell.get(key),quote=True)+'"' for key in ['rowspan','colspan'] if cell.get(key))
      cells.append('<'+cell.tag.lower()+attrs+'>'+normalize(inline(cell))+'</'+cell.tag.lower()+'>')
     pieces.append('<tr>'+''.join(cells)+'</tr>')
    elif tag=='caption':pieces.append('<caption>'+normalize(inline(child))+'</caption>')
    elif tag in {'thead','tbody','tfoot'}:
     pieces.append('<'+tag+'>');contents(child);pieces.append('</'+tag+'>')
    elif child.text_content().strip():pieces.append(normalize(inline(child)))
    if child.tail and child.tail.strip():pieces.append(stdhtml.escape(child.tail,quote=False))
  contents(e);pieces.append('</table>');return '\n'.join(pieces)
 def walk(e):
  if not isinstance(e.tag,str):return
  tag=e.tag.lower()
  if tag in {'script','style','input','label','img','image'}:return
  if tag=='table':
   token='\x00TABLE'+str(len(tables))+'\x00';tables.append(table(e));out.extend(['\n',token,'\n']);return
  if tag in {'sup','sub'} or (tag=='span' and 'W9' in (e.get('class') or '').split()):out.append(inline(e));return
  if tag in BLOCKS:out.append('\n')
  if e.text:out.append(stdhtml.escape(e.text,quote=False))
  for child in e:
   walk(child)
   if child.tail:out.append(stdhtml.escape(child.tail,quote=False))
   if isinstance(child.tag,str) and child.tag.lower() in {'td','th'}:out.append(' ')
  if tag in BLOCKS:out.append('\n')
 walk(root)
 rendered='\n\n'.join(t for line in ''.join(out).split('\n') if (t:=normalize(line)))+'\n'
 for index,value in enumerate(tables):rendered=rendered.replace('\x00TABLE'+str(index)+'\x00',value)
 return rendered
