from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy import false, true
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip

sg.theme('DarkTeal7')

def workDL(ydl_opts, inp_url):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([inp_url])

def main():
    layout = [
    [sg.Text('URL'), sg.Input(key='inp_url'), sg.Button('paste', key='-PASTE_BTN-')],
    [sg.Text('保存するファイル名'), sg.InputText(key='filename')],
    [sg.Text(size=(45, 2)), sg.Button('Download', key='download')],
    [sg.Text('', key='condition')]
    ]

    window = sg.Window('YouTube FastDownlorder', layout)

    while True:
        event, value = window.read()
        if event == '-PASTE_BTN-':
            next = pyperclip.paste()
            window['inp_url'].update(next)
        

        if event == sg.WIN_CLOSED:
            break

        filename = value['filename']
        inp_url = value['inp_url']
        filename = filename + '.mp4'
        path = 'downloads/' + filename

        if event == 'download':
            window['condition'].update('処理中')
            window.read(360)

            ydl_opts = {
                'outtmpl':path,
                'prefer_ffmpeg':false
            }
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(workDL, ydl_opts, inp_url)
         
            window['condition'].update('完了')
            window.read(100)
            window['condition'].update('入力待ち...')

    window.close()

if __name__ == '__main__':
    main()
    #with ProcessPoolExecutor(max_workers=2) as executor:
        #executor.submit(workDL, ydl_opts, inp_url)