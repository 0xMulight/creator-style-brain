"""Local writing style extraction + draft checking. No network calls, stdlib only."""
import argparse
from collections import Counter
from pathlib import Path
import json
import re
import statistics

MAX_FILE=2*1024*1024
WORDS=['旨在','赋能','打造','范式','路径','痛点','说白了','不可否认','值得一提的是','综上所述','这种']
WORD_RX=re.compile(r'[\u4e00-\u9fff]|[A-Za-z]+|\d+')
PUNCT_RX=re.compile(r'[。！？!?；;]+|(?<!\d)\.(?!\d)')
EMOJI_RX=re.compile(r'[\U0001F300-\U0001FAFF]')


def safe_text(path):
    p=Path(path)
    if not p.is_file(): raise ValueError(f'文件不存在: {p}')
    if p.stat().st_size>MAX_FILE: raise ValueError(f'文件超过2MB: {p}')
    return p.read_text(encoding='utf-8-sig').strip()


def split_paragraphs(text):
    return [s.strip() for s in re.split(r'\n\s*\n|\n',text) if s.strip()]


def char_count(s): return len(WORD_RX.findall(s))


def analyze_texts(files):
    samples=[]
    for f in files:
        t=safe_text(f)
        if t: samples.append({'file':str(f),'text':t})
    if not samples: raise ValueError('请提供至少一个非空TXT/MD样本')
    chunks=[p for o in samples for p in split_paragraphs(o['text'])]
    first=[split_paragraphs(o['text'])[0][:110] for o in samples]
    units=[x.strip() for o in samples for x in PUNCT_RX.split(o['text']) if x.strip()]
    alltext='\n'.join(o['text'] for o in samples)
    lines=[char_count(p) for p in chunks]
    stats={
        'file_count':len(samples),'text_units':char_count(alltext),
        'paragraphs':len(chunks),'average_paragraph_units':round(statistics.mean(lines),1),
        'median_sentence_units':round(statistics.median([char_count(x) for x in units]),1) if units else 0,
        'question_marks':alltext.count('?')+alltext.count('？'),
        'exclamations':alltext.count('!')+alltext.count('！'),
        'emoji_count':len(EMOJI_RX.findall(alltext)),
        'hashtags':len(re.findall(r'(?<!\w)#[^\s#]+',alltext)),
        'url_count':len(re.findall(r'https?://[^\s]+',alltext)),
        'overused_phrases':{w:alltext.count(w) for w in WORDS if alltext.count(w)},
    }
    return {'version':'1.0','statistical_profile_only':True,'metrics':stats,'opening_examples':first[:8],
            'source_files':[Path(s['file']).name for s in samples]}


def profile_guide(profile):
    m=profile['metrics']; openers=profile['opening_examples']
    x=[
      '# 创作风格档案（本地样本提取）','',
      f"- 样本：{m['file_count']}篇；统计约{m['text_units']}字词单位。",
      f"- 段落平均长度：{m['average_paragraph_units']}字词单位；句子中位长度：{m['median_sentence_units']}。",
      f"- 疑问句符号：{m['question_marks']}；感叹号：{m['exclamations']}；emoji：{m['emoji_count']}。",
      '- 以下开头只用于总结习惯，不要照抄原文或未经许可复刻他人风格。','', '## 原始开头例子',
    ]
    x += [f'- {a.replace(chr(10)," ")}' for a in openers]
    x += ['', '## 推荐的 Agent 行为',
       '- 用以上长度、段落习惯作参考，优先保持作者提供的主题与事实。',
       '- 先询问用途、受众和字数，再给出初稿；不凭空发明经历、数字或来源。',
       '- 接到用户修改意见后，精确调整被指出的部分，保留用户认可的写法。',
       '- 先输出1个版本；未经要求不要提供三套营销话术。',
       '- 只在取得明确同意后保存个人私密样本或分享文件。',
       '', '## 需要人工补充',
       '- 个人长期禁用词、偏爱的句式、常用结尾、代表作品请自行核对补充。',
       '- 本工具只做可复现的文本统计，不会自动“训练模型”或理解作者的完整人格。',
    ]
    if m['overused_phrases']:
        x.insert(6, '- 样本中出现的模板词（仅统计，不判定作者喜欢与否）：'+ '、'.join(f'{k}×{v}' for k,v in m['overused_phrases'].items()))
    return '\n'.join(x)+'\n'


def draft_check(profile,text):
    ps=split_paragraphs(text)
    lengths=[char_count(p) for p in ps]
    m=profile['metrics']
    flags=[]
    for w in WORDS:
        if w in text:flags.append(f'发现模板表达「{w}」×{text.count(w)}，请按个人习惯判断是否删掉。')
    if lengths and max(lengths)>max(100,round(m['average_paragraph_units']*2.5)):
        flags.append(f'最长段落{max(lengths)}字词单位，明显超过历史平均{m["average_paragraph_units"]}，可考虑拆段。')
    if len(ps)==1 and char_count(text)>160: flags.append('长篇单段，可考虑拆成短段落。')
    if not flags: flags.append('未触发本地启发式规则；仍需人工确认事实与自然度。')
    return '# 草稿风格检查\n\n'+f'- 草稿约{char_count(text)}字词单位，共{len(ps)}段。\n'+'\n'.join(f'- {a}' for a in flags)+'\n\n> 这些是本地统计提醒，不代表AI质量评分。\n'


def main(argv=None):
    ap=argparse.ArgumentParser(description='Creator Style Brain: 本地写作风格分析')
    subs=ap.add_subparsers(dest='cmd',required=True)
    a=subs.add_parser('analyze');a.add_argument('--input',required=True);a.add_argument('--output',default='reports')
    b=subs.add_parser('check');b.add_argument('--profile',required=True);b.add_argument('--draft',required=True);b.add_argument('--output',default='reports/draft-check.md')
    c=subs.add_parser('prompt');c.add_argument('--profile',required=True);c.add_argument('--output',default='reports/agent-prompt.md')
    args=ap.parse_args(argv)
    if args.cmd=='analyze':
        source=Path(args.input); files=sorted([p for p in source.rglob('*') if p.is_file() and p.suffix.lower() in ('.md','.txt')]) if source.is_dir() else [source]
        prof=analyze_texts(files);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
        (out/'style-profile.json').write_text(json.dumps(prof,ensure_ascii=False,indent=2),encoding='utf-8')
        (out/'style-guide.md').write_text(profile_guide(prof),encoding='utf-8')
        print('生成：',out/'style-profile.json','、',out/'style-guide.md')
    elif args.cmd=='check':
        prof=json.loads(safe_text(args.profile)); report=draft_check(prof,safe_text(args.draft));o=Path(args.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(report,encoding='utf-8');print('生成：',o)
    elif args.cmd=='prompt':
        prof=json.loads(safe_text(args.profile)); content=('请参考以下由我授权作品提取的风格摘要写稿；不要复刻原文，不要捏造事实。\n\n'+profile_guide(prof)+'\n先询问受众、篇幅和主题，输出一个自然版本；用户反馈后精准修改。\n')
        o=Path(args.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(content,encoding='utf-8');print('生成：',o)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:raise SystemExit(f'错误：{e}')
