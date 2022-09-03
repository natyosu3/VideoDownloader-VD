from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import false
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip
from moviepy.editor import *
import os

sg.theme('DarkTeal12')

def remove():
    os.remove('video')
    os.remove('audio')

def workDL(ydl_opts, inp_url):
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([inp_url])

def main():
    layout = [
    [sg.Text('URL'), sg.Input(key='-INP_URL-'), sg.Button('paste', key='-PASTE_BTN-')],
    [sg.Text('保存するファイル名'), sg.InputText(key='-FILENAME-')],
    [sg.Text(size=(45, 2)), sg.Button('Download', key='-DOWNLOAD-')],
    [sg.Checkbox('mp3出力', key='-CHECK1-')],
    [sg.Text('入力待ち...', key='-CONDITION-')]
    ]

    window = sg.Window('Video Fast Downlorder', layout)

    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if event == '-PASTE_BTN-':
            next = pyperclip.paste()
            window['-INP_URL-'].update(next)

        filename = value['-FILENAME-']
        inp_url = value['-INP_URL-']
        filename = filename + '.mp4'
        path = 'downloads/' + filename

        if event == '-DOWNLOAD-':
            window['-CONDITION-'].update('処理中')
            window.read(360)

            if value['-CHECK1-'] == True:

                ydl_opts = {
                    'outtmpl':'video',
                    'format': 'bestvideo',
                }
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(workDL, ydl_opts, inp_url)

                ydl_opts = {
                    'outtmpl':'audio',
                    'format': 'bestaudio',
                }
                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(workDL, ydl_opts, inp_url)

                clip = VideoFileClip("video")
                audioclip = AudioFileClip("audio")
                new_videoclip = clip.set_audio(audioclip)
                new_videoclip.write_videofile(path)
                remove()

            window['-CONDITION-'].update('完了')
            window.read(1200)
            window['-CONDITION-'].update('入力待ち...')

    window.close()

if __name__ == '__main__':
    main()
    #with ProcessPoolExecutor(max_workers=2) as executor:
        #executor.submit(workDL, ydl_opts, inp_url)