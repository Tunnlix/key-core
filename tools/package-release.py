#!/usr/bin/env python3
"""Package an existing reviewed core tag; never publish or change Git refs."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', args.tag):
        parser.error('Expected a vMAJOR.MINOR.PATCH tag')
    if git('status', '--porcelain', '--untracked-files=no').strip():
        parser.error('Tracked working tree must be clean')
    revision = git('rev-parse', args.tag + '^{commit}').decode().strip()
    if revision != git('rev-parse', 'HEAD').decode().strip():
        parser.error('Check out the tagged commit before packaging')
    version = args.tag[1:]
    cmake = git('show', args.tag + ':CMakeLists.txt').decode()
    match = re.search(r'project\(key_core VERSION ([0-9.]+) LANGUAGES C\)', cmake)
    if not match or match[1] != version:
        parser.error('Tag must match the CMake project version')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / ('key-core-' + version + '.tar.gz')
    if archive.exists():
        parser.error('Output archive already exists; do not replace release assets')
    source = git('archive', '--format=tar', '--prefix=key-core-' + version + '/', args.tag)
    compressed = io.BytesIO()
    # GzipFile fixes the header filename/time/OS across Python 3.12+ platforms.
    with gzip.GzipFile(filename="", fileobj=compressed, mode="wb", compresslevel=9, mtime=0) as stream:
        stream.write(source)
    data = compressed.getvalue()
    archive.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    (output / 'SHA256SUMS').write_text(digest + '  ' + archive.name + '\n')
    provenance = {'version': version, 'tag': args.tag, 'source_commit': revision,
                  'source_archive': archive.name, 'sha256': digest}
    (output / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(json.dumps(provenance, indent=2))

if __name__ == '__main__':
    main()
