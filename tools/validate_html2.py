from html.parser import HTMLParser
from pathlib import Path

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.voids = set(['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'])
        self.ignored = False
        self.issues = []
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ('script','style'):
            self.ignored = True
            # push to stack to ensure closing
            self.stack.append(tag)
            return
        if tag in self.voids:
            return
        self.stack.append(tag)
    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.ignored and tag in ('script','style'):
            # pop the script/style
            if not self.stack:
                self.issues.append(f'Unexpected closing tag </{tag}>')
                self.ignored = False
                return
            last = self.stack.pop()
            if last != tag:
                self.issues.append(f'Expected closing </{last}> but found </{tag}>')
            self.ignored = False
            return
        if self.ignored:
            return
        if not self.stack:
            self.issues.append(f'Unmatched closing tag </{tag}>')
            return
        last = self.stack.pop()
        if last != tag:
            self.issues.append(f'Mismatched tag: opened <{last}> but closed </{tag}>')

p = Path('index.html')
text = p.read_text(encoding='utf-8')
parser = TagChecker()
parser.feed(text)
if parser.stack:
    parser.issues.append('Unclosed tags at end: ' + ', '.join(parser.stack[-10:]))

print('TagChecker report')
print('------------------')
if parser.issues:
    for it in parser.issues:
        print('-', it)
    raise SystemExit(1)
else:
    print('No tag mismatch issues detected')
    raise SystemExit(0)
