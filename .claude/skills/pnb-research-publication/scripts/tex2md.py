"""Regenerate paper.md from main.tex + main.aux + main.bbl (Rule H: main.tex is source of truth)."""
import re, sys
D = sys.argv[1]
tex = open(f'{D}/main.tex', encoding='utf-8').read()
aux = open(f'{D}/main.aux', encoding='utf-8').read()
bbl = open(f'{D}/main.bbl', encoding='utf-8').read()

# citation numbers in bbl order
keys = re.findall(r'\\bibitem\{([^}]+)\}', bbl)
num = {k: i + 1 for i, k in enumerate(keys)}
# label -> number
labels = {}
for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}', aux):
    labels[m.group(1)] = re.sub(r'\\mbox\s*\{','',m.group(2))

body = tex[tex.index('\\begin{document}'):tex.index('\\bibliographystyle')]
title = re.search(r'\\title\{\\textcolor\{darkblue\}\{(.*?)\}\}', body).group(1)
abstract = re.search(r'Abstract\\,---\}\}~(.*?)\n', body).group(1)
kw = re.search(r'Index Terms\\,---\\,\}\}(.*?)\n', body).group(1)
main = body[body.index('\\section{'):]

def strip_comments(s):
    return re.sub(r'(?<!\\)%[^\n]*', '', s)

def cites(m):
    ns = sorted(num[k.strip()] for k in m.group(1).split(','))
    return ', '.join(f'[{n}]' for n in ns)

def inline(s):
    s = re.sub(r'~?\\cite\{([^}]*)\}', lambda m: ' ' + cites(m), s)
    s = re.sub(r'\\ref\{([^}]*)\}', lambda m: labels.get(m.group(1), '??'), s)
    s = s.replace('\\hacof{}', 'HACOF').replace('\\hacof', 'HACOF')
    for _ in range(3):
        s = re.sub(r'\\textcolor\{[^}]*\}\{([^{}]*)\}', r'\1', s)
        s = re.sub(r'\\textbf\{([^{}]*)\}', r'**\1**', s)
        s = re.sub(r'\\(?:textit|emph)\{([^{}]*)\}', r'*\1*', s)
    s = re.sub(r'\\IEEEPARstart\{(\w)\}\{(\w+)\}', r'\1\2', s)
    s = s.replace('$\\circ$', '○').replace('\\checkmark', '✓')   # comparison-table marks
    s = s.replace('\\textasciitilde', '≈').replace('\\S', '§').replace('{,}', ',')
    s = re.sub(r'\\mbox\s*\{([^}]*)\}', r'\1', s)
    s = s.replace('---', '—').replace('--', '–').replace('``', '"').replace("''", '"')
    s = s.replace('\\%', '%').replace('\\$', '$').replace('\\&', '&').replace('\\,', ' ')
    s = s.replace('\\ ', ' ').replace('\\-', '').replace('~', ' ').replace('\\_', '_')
    s = re.sub(r'\\noindent', '', s)
    s = re.sub(r' +', ' ', s)
    s = re.sub(r' ([.,;:])', r'\1', s)
    return s.strip()

def table(block):
    cap = re.search(r'\\caption\{(.*?)\}\n', block).group(1)
    lab = re.search(r'\\label\{([^}]*)\}', block).group(1)
    rows = re.search(r'\\midrule(.*?)\\bottomrule', block, re.S).group(1)
    head = re.search(r'\\toprule(.*?)\\midrule', block, re.S).group(1)
    def cells(r):
        r = re.sub(r'\\rowcolor\{[^}]*\}', '', r)
        return [inline(c) for c in r.split('&')]
    h = cells(head.strip().rstrip('\\').strip())
    out = [f'**Table {labels.get(lab, "?")}: {inline(cap)}**', '',
           '| ' + ' | '.join(h) + ' |', '|' + '---|' * len(h)]
    for r in rows.split('\\\\'):
        if r.strip():
            out.append('| ' + ' | '.join(cells(r.strip())) + ' |')
    return '\n'.join(out)

def figure(block):
    cap = re.search(r'\\caption\{(.*)\}\s*\\label', block, re.S).group(1)
    lab = re.search(r'\\label\{([^}]*)\}', block).group(1)
    return f'**Fig. {labels.get(lab, "?")}:** {inline(cap)} *(TikZ figure — rendered in main.pdf)*'

main = strip_comments(main)
out = []
# tokenise environments
pat = re.compile(r'\\begin\{(table\*?|figure\*?|equation|itemize|enumerate|mdframed)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}', re.S)
pos = 0
chunks = []
for m in pat.finditer(main):
    chunks.append(('text', main[pos:m.start()]))
    chunks.append((m.group(1), m.group(2)))
    pos = m.end()
chunks.append(('text', main[pos:]))

for kind, c in chunks:
    if kind == 'text':
        for para in re.split(r'\n\s*\n', c):
            p = para.strip()
            if not p:
                continue
            p = re.sub(r'\\label\{[^}]*\}', '', p)
            sm = re.match(r'\\section\*?\{(.*)\}\s*(.*)', p, re.S)
            ss = re.match(r'\\subsection\{(.*)\}\s*(.*)', p, re.S)
            if sm:
                t = inline(sm.group(1))
                n = re.search(r'\\section\{', p)
                out.append(f'## {t}')
                rest = sm.group(2)
            elif ss:
                out.append(f'### {inline(ss.group(1))}')
                rest = ss.group(2)
            else:
                rest = p
            rest = ' '.join(l.strip() for l in rest.splitlines())
            if rest.strip():
                out.append(inline(rest))
    elif kind.startswith('table'):
        out.append(table(c))
    elif kind.startswith('figure'):
        out.append(figure(c))
    elif kind == 'equation':
        eq = re.sub(r'\\label\{[^}]*\}', '', c).strip()
        out.append(f'$$ {eq} $$')
    elif kind in ('itemize', 'enumerate'):
        items = [i.strip() for i in re.split(r'\\item', c) if i.strip()]
        for i, it in enumerate(items, 1):
            b = f'{i}.' if kind == 'enumerate' else '-'
            out.append(b + ' ' + inline(' '.join(l.strip() for l in it.splitlines())))
        out[-len(items):] = ['\n'.join(out[-len(items):])]
    elif kind == 'mdframed':
        txt = ' '.join(l.strip() for l in c.splitlines())
        txt = re.sub(r'\\begin\{(itemize|enumerate)\}|\\end\{(itemize|enumerate)\}', '', txt)
        parts = [inline(x) for x in re.split(r'\\item', txt)]
        out.append('> ' + parts[0] + ''.join('\n> - ' + x for x in parts[1:] if x))

# number sections in markdown headings (roman) using aux order
sec_labels = re.findall(r'\\section\{.*?\}\s*\n\\label\{([^}]*)\}', strip_comments(main))
roman = [labels.get(l, '') for l in sec_labels]
k = 0
for i, o in enumerate(out):
    if o.startswith('## ') and not o.startswith('## Acknowledgments'):
        if k < len(roman):
            out[i] = f'## {roman[k]}. {o[3:]}'
        k += 1

# references from bbl
refs = []
for m in re.finditer(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})', bbl, re.S):
    r = ' '.join(m.group(2).split())
    r = re.sub(r'\\BIBentry\w+\{[^}]*\}', '', r)
    r = re.sub(r'\\url\{([^}]*)\}', r'\1', r)
    r = re.sub(r'\\(?:emph|textit)\{([^{}]*)\}', r'*\1*', r)
    r = re.sub(r'\\newblock\s*', '', r)
    r = r.replace('{', '').replace('}', '').replace('\\&', '&').replace('~', ' ').replace('--', '–')
    r = r.replace("``", '"').replace("''", '"').replace('\\%', '%').replace('\\_', '_')
    r = r.replace('\\textasciitilde', '≈')
    r = re.sub(r'\\em\s*', '', r)
    r = re.sub(r'\\BIB\w+', '', r).strip()
    refs.append(f'[{num[m.group(1)]}] {r}')

author = '**Author:** Muhammad Faisal Laiq — Email: shmlaiq@gmail.com — ORCID: 0009-0007-5779-9836'
md = [f'# {title}', '', author, '', '---', '', '## Abstract', '', inline(abstract), '',
      f'**Index Terms:** {inline(kw)}', '', '---', '']
md += [o + '\n' for o in out]
md += ['## References', ''] + [r + '\n' for r in refs]
open(f'{D}/paper.md', 'w', encoding='utf-8').write('\n'.join(md))
print('paper.md written:', len(out), 'blocks,', len(refs), 'refs')
