import threading
import time
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip
from moviepy.editor import *
import os

sg.theme('DarkTeal12')

def remove():
  os.remove('video')
  os.remove('audio')

def marge(value, title, filename):
  clip = VideoFileClip("video")
  audioclip = AudioFileClip("audio")
  new_videoclip = clip.set_audio(audioclip)
  new_videoclip.write_videofile('fin.mp4')

  os.remove('video')
  os.remove('audio')

  if value['-SAVE_NAME-'] == False:
      os.replace('fin.mp4', 'downloads/' + title + '.mp4')
  else:
      os.replace('fin.mp4', 'downloads/' + filename + '.mp4')

def start_marge(value, title, filename):
  th = threading.Thread(target=marge, args=(value, title, filename))
  th.start()

def start(ydl_opts, inp_url, window):
  th = threading.Thread(target=workDL, args=(ydl_opts, inp_url, window))
  th.start()

def workDL(ydl_opts, inp_url, window):
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([inp_url])
  window['-CONDITION-'].update('完了')

def get_title(inp_url):
  with YoutubeDL() as ydl:
    res = ydl.extract_info(inp_url, download=False)
    title = res['title']
  return title

def main():
    layout = [
        [sg.Text('URL'), sg.Input(key='-INP_URL-'), sg.Button('paste', key='-PASTE_BTN-')],
        [sg.Checkbox('保存するファイル名', key='-SAVE_NAME-'), sg.InputText(key='-FILENAME-', size=(28, 2))],
        [sg.Combo(['mp4標準品質', 'mp4最高品質'], key='-COMBO-', size=(15, 1), readonly=True, default_value="選択して下さい")],
        [sg.Text(size=(45, 2)), sg.Button('Download', key='-DOWNLOAD-')],
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

        if event == '-DOWNLOAD-':
            window['-CONDITION-'].update('処理中')
            window.read(360)

            title = get_title(inp_url)

            if value['-COMBO-'] == 'mp4標準品質':
                if value['-SAVE_NAME-'] == False:
                    path = 'downloads/' + title + '.mp4'
                else:
                    path = 'downloads/' + filename + '.mp4'

                ydl_opts = {
                    'outtmpl':path,
                    'format':'best'
                }
                start(ydl_opts, inp_url, window)

            if value['-COMBO-'] == 'mp4最高品質':

                ydl_opts = {
                    'outtmpl':'video',
                    'format': 'bestvideo',
                }
                start(ydl_opts, inp_url, window)

                ydl_opts = {
                    'outtmpl':'audio',
                    'format': 'bestaudio',
                }
                start(ydl_opts, inp_url, window)

                #clip = VideoFileClip("video")
                #audioclip = AudioFileClip("audio")
                #new_videoclip = clip.set_audio(audioclip)
                #new_videoclip.write_videofile('fin.mp4')
                start_marge(value, title, filename)
                #remove()
                #if value['-SAVE_NAME-'] == False:
                    #os.replace('fin.mp4', 'downloads/' + title + '.mp4')
                #else:
                    #os.replace('fin.mp4', 'downloads/' + filename + '.mp4')

            #window['-CONDITION-'].update('完了')
            #window.read(1200)
            #window['-CONDITION-'].update('入力待ち...')

    window.close()

if __name__ == '__main__':
    main()