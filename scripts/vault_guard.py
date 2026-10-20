#!/usr/bin/env python3
"""Read-only safety preflight; does not authorize or perform writes."""
import argparse, json, subprocess
from pathlib import Path

def git(root,*args):
    p=subprocess.run(['git','-C',str(root),*args],capture_output=True,text=True,encoding='utf-8',errors='replace')
    return p.returncode,p.stdout.strip(),p.stderr.strip()

def main():
    ap=argparse.ArgumentParser(description='Read-only path and Git preflight (not write permission)')
    ap.add_argument('vault'); ap.add_argument('target'); ap.add_argument('--expected-head')
    a=ap.parse_args()
    errors=[]
    try:
        root=Path(a.vault).expanduser().resolve(strict=True)
        target=Path(a.target).expanduser()
        if not target.is_absolute(): errors.append('target must be absolute')
        # reject existing or parent symlinks/junctions conservatively; Windows junctions require additional OS checks
        if root.is_symlink(): errors.append('vault root is a symlink')
        if target.is_symlink(): errors.append('target is a symlink')
        final=target.resolve(strict=False)
        if root not in final.parents: errors.append('target is outside Vault')
        if any(x in {'.git','.obsidian'} for x in target.parts): errors.append('protected path')
        if final.suffix.lower()!='.md': errors.append('target must end in .md')
        code,repo,_=git(root,'rev-parse','--show-toplevel')
        if code or Path(repo).resolve()!=root: errors.append('Vault root must equal Git root')
        code,head,_=git(root,'rev-parse','HEAD')
        if code: errors.append('Git HEAD unavailable')
        code,status,_=git(root,'status','--porcelain=v1','--untracked-files=all')
        if code or status: errors.append('Git workspace is not clean or Git status unavailable')
        if a.expected_head and head!=a.expected_head: errors.append('Git HEAD changed')
        print(json.dumps({'ok':not errors,'vault':str(root),'target':str(final),'head':head,'errors':errors,'note':'Read-only preflight; never implies permission to write. Re-run immediately before authorized write.'},ensure_ascii=False,indent=2))
    except Exception as e:
        print(json.dumps({'ok':False,'errors':[str(e)]},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
