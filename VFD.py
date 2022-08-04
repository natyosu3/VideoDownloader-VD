from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing.spawn import import_main_path
from sqlalchemy import true
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip
import threading
import time

sg.theme('DarkTeal7')

def btn(inp_url):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    thread1 = threading.Thread(args=(inp_url,), target=workDL, daemon=true)
    thread1.start()
    #window['condition'].update('完了')
    #window.Refresh()
    
def workDL(inp_url):
    ydl_opts = {
        'outtmpl':path,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([inp_url])

layout = [
[sg.Text('URL'), sg.Input(key='inp_url'), sg.Button('paste', key='-PASTE_BTN-')],
[sg.Text('保存するファイル名'), sg.InputText(key='filename')],
[sg.Text(size=(45, 2)), sg.Button('Download', key='-DL-')],
[sg.Text('', key='condition')]
]

window = sg.Window('YouTube FastDownlorder', layout)

while True:
    event, value = window.read(timeout=100, timeout_key='-TIMEOUT-')
    if event == '-PASTE_BTN-':
        next = pyperclip.paste()
        window['inp_url'].update(next)
    

    if event == sg.WIN_CLOSED:
        break

    filename = value['filename']
    inp_url = value['inp_url']
    filename = filename + '.mp4'
    path = 'downloads/' + filename

    if event == '-DL-':
        window['condition'].update('処理中')

    if event == '-DL-':

        window['condition'].update('処理中')
        window.Refresh()

        ydl_opts = {
            'outtmpl':path,
        }
        btn(inp_url)
        
        #window['condition'].update('完了')
        #window.read(100)
        #window['condition'].update('入力待ち...')

    if event == '-TIMEOUT-':
        print('timeoutの中です')
        st = 'timeout'
        window['condition'].update(st)


window.close()
    #with ProcessPoolExecutor(max_workers=2) as executor:
        #executor.submit(workDL, ydl_opts, inp_url)


