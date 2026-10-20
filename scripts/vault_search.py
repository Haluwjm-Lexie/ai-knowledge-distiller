#!/usr/bin/env python3
"""Read-only candidate search in Markdown files (no semantic deduplication)."""
import argparse, json, re
from pathlib import Path

SKIP = {'.git', '.obsidian', 'node_modules', '.venv', '__pycache__'}

def main():
    ap=argparse.ArgumentParser(description='Read-only Markdown keyword candidate search')
    ap.add_argument('vault', help='Explicit Vault directory')
    ap.add_argument('terms', nargs='+', help='Search terms; any match')
    ap.add_argument('--limit', type=int, default=10)
    ap.add_argument('--context', type=int, default=1)
    a=ap.parse_args()
    root=Path(a.vault).expanduser().resolve(strict=True)
    if not root.is_dir() or a.limit < 1 or a.context < 0: ap.error('Invalid root/limit/context')
    hits=[]; scanned=0; unreadable=0
    for f in root.rglob('*.md'):
        rel=f.relative_to(root)
        if any(part in SKIP or part.startswith('.') for part in rel.parts): continue
        # Do not follow symlink files outside the authorized Vault.
        if f.is_symlink() or root not in f.resolve().parents: continue
        scanned+=1
        try: lines=f.read_text(encoding='utf-8-sig').splitlines()
        except (OSError,UnicodeError): unreadable+=1; continue
        matches=[i for i,line in enumerate(lines) if any(t.casefold() in line.casefold() for t in a.terms)]
        if matches:
            excerpt=[]
            for i in matches[:8]:
                start=max(0,i-a.context); end=min(len(lines),i+a.context+1)
                excerpt.append({'line':i+1,'context': [{'line':j+1,'text':lines[j][:500]} for j in range(start,end)]})
            hits.append({'path':str(f),'match_count':len(matches),'excerpts':excerpt})
    hits.sort(key=lambda x:(-x['match_count'],x['path']))
    print(json.dumps({'root':str(root),'scanned_markdown':scanned,'unreadable':unreadable,'matched_files':len(hits),'returned_files':len(hits[:a.limit]),'truncated':len(hits)>a.limit,'candidates':hits[:a.limit]},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
