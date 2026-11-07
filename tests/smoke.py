import importlib.machinery, tempfile, pathlib, unittest.mock as mock, subprocess, os
p=pathlib.Path(__file__).resolve().parents[1]
m=importlib.machinery.SourceFileLoader('themes',str(p/'my-themes')).load_module()
with tempfile.TemporaryDirectory() as td:
 h=pathlib.Path(td); m.HOME=h; m.USER_THEMES=h/'.config/omarchy/themes'; m.INCLUDE_FILE=h/'include'; m.EXCLUDE_FILE=h/'exclude'; m.STOCK_LOCATIONS=[h/'stock']
 for n in ['custom-theme','stock-theme','hidden']:
  d=m.USER_THEMES/n;d.mkdir(parents=True);(d/'colors.toml').touch()
 (h/'stock/stock-theme').mkdir(parents=True);m.EXCLUDE_FILE.write_text('hidden\n')
 assert m.themes()==['custom-theme']
 m.INCLUDE_FILE.write_text('stock-theme\n');assert m.themes()==['custom-theme','stock-theme']
 with mock.patch.object(m.shutil,'which',return_value='/bin/mock'), mock.patch.object(m.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'Custom Theme\n','')):
  assert m.current()=='custom-theme'
 with mock.patch.object(m,'themes',return_value=['custom-theme']),mock.patch.object(m,'current',return_value='custom-theme'),mock.patch.object(m,'picker',return_value='[active] custom-theme') as pick,mock.patch.object(m.shutil,'which',return_value='/bin/mock'),mock.patch.object(m.subprocess,'call',return_value=0) as call,mock.patch.object(m.sys,'argv',['my-themes']):
  assert m.main()==0;pick.assert_called_once_with(['[active] custom-theme']);call.assert_called_once_with(['omarchy','theme','set','custom-theme'])
 for choice in [None,'malicious']:
  with mock.patch.object(m,'themes',return_value=['custom-theme']),mock.patch.object(m,'current',return_value=''),mock.patch.object(m,'picker',return_value=choice),mock.patch.object(m.subprocess,'call') as call,mock.patch.object(m.sys,'argv',['my-themes']):
   assert m.main()==(0 if choice is None else 1);call.assert_not_called()
 for n in ['custom-theme','stock-theme']:(m.USER_THEMES/n/'preview.png').touch()
 def image_pick(argv,**kwargs):
  links=list(pathlib.Path(argv[-1]).iterdir());assert len(links)==2
  return subprocess.CompletedProcess(argv,0,str(next(x for x in links if x.name.startswith('[active]')))+'\n','')
 with mock.patch.object(m.shutil,'which',return_value='/bin/mock'),mock.patch.object(m.subprocess,'run',side_effect=image_pick):
  assert m.previews(['custom-theme','stock-theme'],'custom-theme')=='[active] custom-theme'
 env=dict(os.environ,HOME=str(h))
 subprocess.run(['bash',str(p/'install.sh')],env=env,check=True,capture_output=True)
 assert (h/'.local/bin/my-themes').is_file()
 subprocess.run(['bash',str(p/'uninstall.sh')],env=env,check=True,capture_output=True)
 assert not (h/'.local/bin/my-themes').exists();assert m.USER_THEMES.is_dir()
print('PASS: discovery, filtering, active labels, switching, cancellation, preview mapping, install/uninstall')
