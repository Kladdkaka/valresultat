import requests
from pathlib import Path
import hashlib
import urllib.parse

BASE_URL = 'https://resultat.val.se/resultatfiler/'

r = requests.get(BASE_URL + 'index.md5')

Path('data').mkdir(exist_ok=True)

for line in r.text.splitlines():
    md5, filename = line.split()
    
    fpath = Path('data', filename)
    fpath.parent.mkdir(parents=True, exist_ok=True)

    if fpath.exists():
      b = fpath.read_bytes()
      hash = hashlib.md5(b).hexdigest()

      if hash == md5:
        print('Skipping', filename)
        continue
    
    print('Downloading', filename)
    print(urllib.parse.urljoin(BASE_URL, filename.replace('./', '')))
    r = requests.get(urllib.parse.urljoin(BASE_URL, filename))
    fpath.write_bytes(r.content)