import json,re,zipfile
from pathlib import Path
from PIL import Image,ImageStat
p=Path(__file__).resolve().parents[1]
out=['# Verdant Meadow Theme color specification','', '| VS Code region | Light | Dark |','|---|---|---|']
themes=[json.loads((p/'themes'/f'verdant-meadow-{v}-color-theme.json').read_text()) for v in ['light','dark']]
for k in themes[0]['colors']:
    out.append(f"| `{k}` | `{themes[0]['colors'][k]}` | `{themes[1]['colors'][k]}` |")
(p/'COLOR-SPEC.md').write_text('\n'.join(out)+'\n',encoding='utf-8')
for v,t in zip(['light','dark'],themes):
    assert all(re.fullmatch(r'#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?',c) for c in t['colors'].values())
    im=Image.open(p/'store-assets/screenshots/en'/f'screenshot-{v}.png').convert('RGB')
    row=ImageStat.Stat(im.crop((0,0,im.width,1))).mean
    col=ImageStat.Stat(im.crop((0,0,1,im.height))).mean
    expected=tuple(int(t['colors']['titleBar.activeBackground'][i:i+2],16) for i in [1,3,5])
    assert max(abs(a-b) for a,b in zip(row,expected))<1,(v,row,expected)
    print(v,len(t['colors']),'UI colors; screenshot',im.size,'first row',row,'first column',col)
    # Below the title bar the left column is the activity bar, which has its own
    # background; the status bar sits under it.
    act=ImageStat.Stat(im.crop((10,60,11,im.height-40))).mean
    act_expected=tuple(int(t['colors']['activityBar.background'][i:i+2],16) for i in [1,3,5])
    assert max(abs(a-b) for a,b in zip(act,act_expected))<2,(v,act,act_expected)
archive=p/'verdant-meadow-theme-1.0.0.vsix'
if archive.exists():
    with zipfile.ZipFile(archive) as z:
        m=json.loads(z.read('extension/package.json'))
        assert m['publisher']=='lilinhuang' and m['version']=='1.0.0'
        for t in m['contributes']['themes']: assert 'extension/'+t['path'].removeprefix('./') in z.namelist()
        assert 'Version="1.0.0"' in z.read('extension.vsixmanifest').decode()
    print('VSIX manifest, publisher, version and theme entries verified')
