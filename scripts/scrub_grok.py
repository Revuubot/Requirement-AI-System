import re
from pathlib import Path

pattern_line = re.compile(r"^\s*os\.environ\[\s*['\"]GROK_API_KEY['\"]\s*\]\s*=\s*.*$", re.MULTILINE)
pattern_token = re.compile(r'gsk_[A-Za-z0-9_-]{10,}')

for p in Path('.').rglob('*.py'):
    try:
        s = p.read_text(encoding='utf-8')
    except Exception:
        continue
    new = pattern_line.sub('', s)
    new = pattern_token.sub('[REDACTED_GROK_KEY]', new)
    if new != s:
        p.write_text(new, encoding='utf-8')
