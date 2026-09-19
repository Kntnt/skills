"""Run the eight predeclared baseline invocations; preserve every result."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/Users/thomas/Projects/skills')
FOLLOW = ROOT / 'docs/evaluation/editorial-329/followup'
RUNNER = ROOT / 'docs/evaluation/editorial-329/harness/run.py'
CLEANUP = '/Users/thomas/.agents/skills/kntnt/features/session-cleanup/scripts/session_cleanup.py'
subprocess.run(['uv', 'run', CLEANUP, 'add', 'pid', str(os.getpid()), 'Editorial #349 eight native baseline invocations'], check=True, capture_output=True)
rows = [
 ('opinion-sv-r1', 'opinion', 'sv', 'docs/evaluation/corpus/editorial-quality/sources/opinion.md', '6e531f5'),
 ('opinion-sv-r2', 'opinion', 'sv', 'docs/evaluation/corpus/editorial-quality/sources/opinion.md', '6e531f5'),
 ('case-study-en_US-r1', 'case-study', 'en_US', 'docs/evaluation/corpus/editorial-quality/sources/case-study.md', '6e531f5'),
 ('case-study-en_US-r2', 'case-study', 'en_US', 'docs/evaluation/corpus/editorial-quality/sources/case-study.md', '6e531f5'),
 ('opinion-unknown-sv-r1', 'opinion', 'sv', 'docs/evaluation/editorial-329/followup/fixtures/opinion-unknown-sv.md', 'bf14dc2'),
 ('opinion-absence-en_GB-r1', 'opinion', 'en_GB', 'docs/evaluation/editorial-329/followup/fixtures/opinion-absence-en_GB.md', 'bf14dc2'),
 ('case-unprompted-en_US-r1', 'case-study', 'en_US', 'docs/evaluation/editorial-329/followup/fixtures/case-unprompted-en_US.md', 'bf14dc2'),
 ('case-question-en_GB-r1', 'case-study', 'en_GB', 'docs/evaluation/editorial-329/followup/fixtures/case-question-en_GB.md', 'bf14dc2'),
]
results=[]
for case, genre, locale, source, source_revision in rows:
    source_path=ROOT/source
    frozen=subprocess.check_output(['git','show',f'{source_revision}:{source}'],cwd=ROOT)
    assert frozen==source_path.read_bytes(), source
    case_dir=FOLLOW/'runs/baseline'/case
    case_dir.mkdir(parents=True,exist_ok=False)
    prompt=case_dir/'prompt.txt'
    prompt.write_text(f'/write --genre={genre} --language={locale} --output=response source.md\n')
    result=subprocess.run(['python3',str(RUNNER),'--revision','7ff6ec0','--corpus-revision','bf14dc2','--prompt',str(prompt),'--input',str(source_path),'--input-name','source.md','--output',str(case_dir/'write')],cwd=ROOT,capture_output=True,text=True)
    (case_dir/'runner-stdout.txt').write_text(result.stdout)
    (case_dir/'runner-stderr.txt').write_text(result.stderr)
    results.append({'case':case,'returncode':result.returncode,'source_revision':source_revision})
    (FOLLOW/'harness/baseline-batch-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(case,result.returncode,flush=True)
