"""Append current statutory texts from recorded metadata and original official JSON responses, offline."""
import os,json,subprocess,csv,io,hashlib,re,argparse
from datetime import datetime,timezone
from pathlib import Path
from current_text_2010_2017 import render
for key,value in {'GIT_AUTHOR_NAME':'Lexifina','GIT_AUTHOR_EMAIL':'russia-law@lexifina.com','GIT_COMMITTER_NAME':'Lexifina','GIT_COMMITTER_EMAIL':'russia-law@lexifina.com'}.items():os.environ[key]=value
REPO=None
def run(args,input=None):
 process=subprocess.Popen(args,stdin=subprocess.PIPE if input is not None else None,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**({'creationflags':subprocess.BELOW_NORMAL_PRIORITY_CLASS} if os.name=='nt' else {}))
 out,err=process.communicate(input)
 if process.returncode:raise RuntimeError(err.decode('utf-8',errors='replace'))
 return out
def git(*args):return run(['git','-c','gc.auto=0','-C',str(REPO),*args]).decode('utf-8')
def blob(base,path):return run(['git','-C',str(REPO),'show',base+':'+path])
def timestamp(day):
 # Use the source calendar date at noon in the historical Moscow time zone.
 from zoneinfo import ZoneInfo
 d=datetime.fromisoformat(day+'T12:00:00').replace(tzinfo=ZoneInfo('Europe/Moscow'))
 return f'{int(d.timestamp())} {d.strftime("%z")}'
def data(raw):return b'data '+str(len(raw)).encode()+b'\n'+raw+b'\n'
def commit(ref,parent,author,committer,message,files,mark=None):
 out=b'commit refs/heads/'+ref.encode()+b'\n'+(b'mark :'+str(mark).encode()+b'\n' if mark is not None else b'')+b'author '+author.encode()+b'\n'+b'committer '+committer.encode()+b'\n'+data(message.encode('utf-8'))+b'from '+parent.encode()+b'\n'
 for path,raw in sorted(files.items()):out+=b'M 100644 inline '+path.encode()+b'\n'+data(raw)
 return out+b'\n'
def build(part,base,ref):
 old=int(git('show','-s','--format=%ct',base).strip())
 existing={r['path'].rstrip('/') for r in csv.DictReader(io.StringIO(blob(base,'laws.csv').decode('utf-8')))}
 existing_count=len(existing)
 parent=base;new_rows=[];commits=[];streams=[]
 for i,act in enumerate(part['acts'],1):
  path=act['act_path'];v=act['versions'][0]
  if path in existing:raise RuntimeError('Published path collision: '+path)
  existing.add(path)
  msg=act['title']+' — oldest version available\n\n'+'\n'.join(['Kind: baseline','In-force: '+v['from'],'In-force-basis: '+v['in_force_basis'],'Enacted: '+act['enacted'],'First-law: null',f"Edition: {act['docid']} {v['redid']}",'Act-path: '+path,'Files: '+path+'/text.md','Source: '+v['source_url'],'Source-sha256: '+v['sha256']])+'\n'
  streams.append(commit(ref,parent,'Official Internet Portal of Legal Information <actual@pravo.gov.invalid> '+timestamp(v['from']),'Lexifina <russia-law@lexifina.com> '+str(old+i)+' +0000',msg,{path+'/text.md':v['units']['text']['text'].encode('utf-8')},mark=i))
  parent=':'+str(i);commits.append({'act':path,'in_force':v['from'],'docid':act['docid'],'redid':v['redid']})
  new_rows.append({'nd':act['docid'],'type':act['kind'],'title':act['title'],'adoption':act['adoption'],'enacted':act['enacted'],'state':act['state'],'editions':1,'texts':1,'path':path+'/','source':act['url']})
 run(['git','-c','gc.auto=0','-C',str(REPO),'fast-import','--quiet','--done'],b''.join(streams)+b'done\n')
 hashes=git('rev-list','--reverse',base+'..'+ref).splitlines()
 if len(hashes)!=len(commits):raise RuntimeError('Appended commit count differs')
 for entry,sha in zip(commits,hashes):entry['sha']=sha
 parent=hashes[-1]
 old_csv=blob(base,'laws.csv').decode('utf-8');header=next(csv.reader(io.StringIO(old_csv)))
 out=io.StringIO();w=csv.DictWriter(out,fieldnames=header,lineterminator='\n');w.writerows(new_rows)
 law_csv=(old_csv.rstrip('\r\n')+'\n'+out.getvalue()).encode('utf-8')
 readme=re.sub(r'The Constitution and \d+ current-text federal instruments are covered.','The Constitution and '+str(existing_count+len(part['acts']))+' current-text federal instruments are covered.',blob(base,'README.md').decode('utf-8'))
 readme+='\n\n## Federal acts signed 2010–2017\n\n'+str(len(part['acts']))+' additional acts each contain the current official verbal text, including explanatory notes and textual annexes. Each act is one file (`text.md`); earlier editions are not recorded for these additions. The source edition date and amending instrument identify the edition in force. Initial editions are dated by their commencement clause and official publication evidence.\n\nImage material remains deferred for separate integration. These additions make no assertion of image completeness.\n\n| Folder | Act | Current text applies from |\n| --- | --- | --- |\n'
 for a in part['acts']:readme+='| `'+a['act_path']+'/` | '+a['title'].replace('|','\\|')+' | '+a['versions'][0]['from']+' |\n'
 jurisdiction=json.loads(blob(base,'jurisdiction.json'))
 jurisdiction['build']=jurisdiction.get('build','')+'; '+str(len(part['acts']))+' current-text acts signed 2010–2017'
 jurisdiction['register_date']='2026-11-04'
 reproduce=blob(base,'REPRODUCE.md').decode('utf-8')
 reproduce+='\n\n## Current editions signed 2010–2017\n\nOne official current edition per added act. Source response SHA-256 and edition references are recorded in `data/signed-2010-2017.json` and the law commits. All legal wording comes from official HTML. Source notes remain in the text. In-force-basis identifies the edition and its amending instrument or the original commencement clause. GPT-6 wrote the collection, parsing, and verification code; no model wrote or corrected legal text.\n'
 reproduce+='\nThe exact offline renderer and appender are `tools/current_text_2010_2017.py` and `tools/append_signed_2010_2017.py`. The appender accepts the recorded metadata and original official JSON response files named by SHA-256, checks their hashes, and reconstructs the appended history from the recorded baseline.\n'
 thin=[]
 for act in part['acts']:
  copy={key:value for key,value in act.items() if key!='versions'}
  copy['versions']=[{key:value for key,value in v.items() if key!='units'}|{'files':[act['act_path']+'/text.md']} for v in act['versions']]
  thin.append(copy)
 metadata=json.dumps({'acts':thin,'commits':commits,'baseline_sha':base,'record_date':'2026-11-04','first_law':None,'history':'current-only','image_status':'deferred'},ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n'
 files={'README.md':readme.encode('utf-8'),'jurisdiction.json':json.dumps(jurisdiction,ensure_ascii=False,indent=2).encode()+b'\n','laws.csv':law_csv,'data/laws.csv':law_csv,'data/signed-2010-2017.json':metadata,'REPRODUCE.md':reproduce.encode('utf-8')}
 for name in ['append_signed_2010_2017.py','current_text_2010_2017.py','check_words.py']:files['tools/'+name]=(Path(__file__).resolve().parent/name).read_bytes()
 msg='Russia: current federal acts signed 2010–2017\n\nKind: documentation\nSource: http://actual.pravo.gov.ru/\n'
 stream=commit(ref,parent,'Lexifina <russia-law@lexifina.com> 1793782800 +0000','Lexifina <russia-law@lexifina.com> '+str(old+len(part['acts'])+1)+' +0000',msg,files)+b'done\n'
 run(['git','-c','gc.auto=0','-C',str(REPO),'fast-import','--quiet','--done'],stream)
 return {'head':git('rev-parse',ref).strip(),'commits':commits}

def main():
 global REPO
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('repository',type=Path)
 parser.add_argument('metadata',type=Path)
 parser.add_argument('responses',type=Path)
 parser.add_argument('--branch',default='current-text-review')
 args=parser.parse_args();REPO=args.repository
 metadata=json.loads(args.metadata.read_text(encoding='utf-8'))
 for act in metadata['acts']:
  for version in act['versions']:
   raw=(args.responses/(version['sha256']+'.json')).read_bytes()
   if hashlib.sha256(raw).hexdigest()!=version['sha256']:raise ValueError('Official response hash differs')
   version['units']={'text':{'label':act['short'],'kind':'whole-act','text':render(json.loads(raw)['redtext'])}}
 result=build({'acts':metadata['acts']},metadata['baseline_sha'],args.branch)
 print(json.dumps({'head':result['head'],'acts':len(metadata['acts'])}))
if __name__=='__main__':main()
