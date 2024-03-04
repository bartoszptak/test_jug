import subprocess
from glob import glob
import shutil

with open('repositories_list.txt', 'r') as file:
    repositories = file.readlines()
    repositories = [repo.strip() for repo in repositories]
    

for repo in repositories:
  if len(repo) == 0:
    continue
  
  repo_name = repo.split('/')[-1].split('.')[0]
  
  print(f'Cloning {repo_name}...')
  subprocess.run(['git', 'clone', repo, repo_name])
  
  print(f'Buiding {repo_name}...')
  subprocess.run(['python', 'repo_name/compile.py', f'--working-directory {repo_name}'])
  
  print(f'Create index.html for {repo_name}...')
  files_to_index = glob(f'{repo_name}/*.html', recursive=True)
  
  txt = '<html><body>'
  for file in files_to_index:
    txt += f'<a href="{file}">{file}</a><br>'
  txt += '</body></html>'
  
  with open(f'{repo_name}/index.html', 'w') as file:
    file.write(txt)
  
  shutil.move(f'{repo_name}', f'./_site/{repo_name}')
  
  
# Generate index.html for the root

print('Create index.html for the root...')
txt = '<html><body>'
for repo in repositories:
  if len(repo) == 0:
    continue
  repo_name = repo.split('/')[-1].split('.')[0]
  txt += f'<a href="{repo_name}">{repo_name}</a><br>'
  
txt += '</body></html>'

with open(f'./_site/index.html', 'w') as file:
  file.write(txt)
