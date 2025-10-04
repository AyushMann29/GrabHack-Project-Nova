import re
from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')

issues = []

# 1) Conflict markers
if re.search(r'^<{7}|^={7}|^>{7}', text, re.M):
    issues.append('Found git merge conflict markers (<<<<<<<, =======, >>>>>>>)')

# 2) Count DOMContentLoaded occurrences
dom_count = len(re.findall(r"document\.addEventListener\(['\"]DOMContentLoaded['\"]", text))

# 3) Count csvResultsContainer hide calls
csv_hide_count = len(re.findall(r"csvResultsContainer\.classList\.add\(['\"]hidden['\"]\)", text))

# 4) Simple tag balance check (ignore script contents)
# Remove script contents
text_no_script = re.sub(r'<script[\\s\\S]*?<\\/script>', '<script></script>', text, flags=re.I)
# Find tags
tags = re.findall(r'<\s*(/?)([a-zA-Z0-9:-]+)[^>]*?>', text_no_script)
stack = []
self_closing = set(['br','img','hr','input','meta','link'])
for closing, tag in tags:
    tag = tag.lower()
    if closing == '':
        if tag in self_closing:
            continue
        stack.append(tag)
    else:
        if not stack:
            issues.append(f'Unmatched closing tag </{tag}>')
        else:
            last = stack.pop()
            if last != tag:
                issues.append(f'Mismatched tag: opened <{last}> but closed </{tag}>')

if stack:
    issues.append('Unclosed tags at end: ' + ', '.join(stack[-10:]))

# 5) Basic checks for obvious JS typos from earlier edits
if 'guidlinesModal' in text:
    issues.append("Found typo 'guidlinesModal' (should be 'guidelinesModal')")

# Build report
print('Validation report for index.html')
print('--------------------------------')
print(f'DOMContentLoaded listener count: {dom_count}')
print(f"csvResultsContainer.classList.add('hidden') occurrences: {csv_hide_count}")
print('')
if issues:
    print('Issues found:')
    for it in issues:
        print('-', it)
    raise SystemExit(2)
else:
    print('No issues found. HTML looks structurally OK (basic checks).')
    raise SystemExit(0)
