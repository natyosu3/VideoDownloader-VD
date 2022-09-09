import threading
import time
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip
import ffmpeg
import os
import sys

sg.theme('DarkTeal12')

def merge(value, title, filename, window):
  window['-CONDITION-'].update('merge')

  videopath = 'video.mp4'
  audiopath = 'audio.wav'
  output = title + '.mp4'

  print(output)

  while True:
    is_file = os.path.isfile(videopath)
    if is_file == True:
      break

  instream1 = ffmpeg.input(videopath)
  instream2 = ffmpeg.input(audiopath)
  stream = ffmpeg.output(instream1, instream2, output, vcodec="copy", acodec="copy")
  ffmpeg.run(stream, overwrite_output=True)

  time.sleep(2)

  os.remove(videopath)
  os.remove(audiopath)

  time.sleep(3)

  if value['-SAVE_NAME-'] == False:
      os.replace(output, 'downloads/' + title + '.mp4')
  else:
      os.replace(output, 'downloads/' + filename + '.mp4')
  
  window['-CONDITION-'].update('完了')
  time.sleep(3)
  window['-CONDITION-'].update('入力待ち...')

def start_merge(value, title, filename, window):
  th = threading.Thread(target=merge, args=(value, title, filename, window))
  th.start()

def start(ydl_opts, inp_url, window):
  th = threading.Thread(target=workDL, args=(ydl_opts, inp_url, window))
  th.start()

def workDL(ydl_opts, inp_url, window):
  with YoutubeDL(ydl_opts) as ydl:
    ydl.download([inp_url])
  
  window['-CONDITION-'].update('完了')
  time.sleep(3)
  window['-CONDITION-'].update('入力待ち...')

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
    aaa = sys.executable
    print(aaa)

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
                    'outtmpl':'video.mp4',
                    'format': 'bestvideo',
                }
                start(ydl_opts, inp_url, window)

                ydl_opts = {
                    'outtmpl':'audio.wav',
                    'format': 'bestaudio',
                }
                start(ydl_opts, inp_url, window)
                start_merge(value, title, filename, window)

    window.close()

if __name__ == '__main__':
    main()