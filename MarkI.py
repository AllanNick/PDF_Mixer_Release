import os
from PyPDF2 import PdfMerger

cwd = os.getcwd()
print('\033c')
print('PDF Mixer.')
print('[C]Nick 2019-2023')
print('---------Version:Mk.I_rev1--')
print('current path:%s'%(cwd))
print('Step 1 of 3: paste your file that needs to connect in current path')
print('input E to open Explorer.exe[input any key to skip]')
if input() == 'E':
    os.system('explorer.exe %s'%(cwd))

input('ENTER to continue')

n_fname = input('Step 2 of 3: input filename for new .pdf file:')

files = os.listdir()
merger = PdfMerger()
print('Step 3 of 3: combining...')

for file in files:
    if file[-4:]  == '.pdf':
        merger.append(open(file, 'rb'))

with open('combined.pdf','wb') as fout:
    merger.write(fout)

print('Done!')
input()
