import threading
import time
from yt_dlp import YoutubeDL
import PySimpleGUI as sg
import pyperclip
import ffmpeg
import os
import sys

sg.theme('LightGrey4')

base_path = sys._MEIPASS
print(base_path)
os.environ['Path'] = base_path

videopath = 'video.webm'
audiopath = 'audio.webm'

def merge(value, title, filename, window):
  print('merge')
  try:
    title = title.replace('/', '')
    output = title + '.webm'

    print(output)

    while True:
      is_file = os.path.isfile(audiopath)
      window['-DOWNLOAD-'].update(disabled=True)
      window['-CONDITION-'].update('downloading...')
      if is_file == True:
        break

    while True:
      is_file = os.path.isfile(videopath)
      window['-DOWNLOAD-'].update(disabled=True)
      window['-CONDITION-'].update('downloading...')
      if is_file == True:
        break

    window['-CONDITION-'].update('merge')
    window['-DOWNLOAD-'].update(disabled=True)
    


    instream1 = ffmpeg.input(videopath)
    instream2 = ffmpeg.input(audiopath)
    stream = ffmpeg.output(instream1, instream2, output, vcodec="copy", acodec="copy")
    ffmpeg.run(stream)

    time.sleep(1)
    while True:
      is_file = os.path.isfile(output)
      window['-DOWNLOAD-'].update(disabled=True)
      window['-CONDITION-'].update('marge...')
      if is_file == True:
        break
    
    os.remove(videopath)
    os.remove(audiopath)

    if value['-SAVE_NAME-'] == False:
        os.replace(output, 'downloads/' + output)
    else:
        os.replace(output, 'downloads/' + filename + '.webm')

    window['-DOWNLOAD-'].update(disabled=True)
    window['-CONDITION-'].update('完了')
    window['-DOWNLOAD-'].update(disabled=False)
    time.sleep(1)
    window['-CONDITION-'].update('入力待ち...')
  except:
    print('error3')
    window['-CONDITION-'].update('入力待ち...')

def start_merge(value, title, filename, window):
  print('start_marge')
  th = threading.Thread(target=merge, args=(value, title, filename, window))
  th.start()

def start(ydl_opts, inp_url, window):
  print('start')
  th = threading.Thread(target=workDL, args=(ydl_opts, inp_url, window))
  th.start()

def workDL(ydl_opts, inp_url, window):
  print('workDL')
  try:
    with YoutubeDL(ydl_opts) as ydl:
      ydl.download([inp_url])
    
    window['-CONDITION-'].update('入力待ち...')
    window['-DOWNLOAD-'].update(disabled=False)
  except:
    print('error2')
    window['-CONDITION-'].update('入力待ち...')

def get_title(inp_url):
  print('get_title')
  try:
    with YoutubeDL() as ydl:
      res = ydl.extract_info(inp_url, download=False)
      title = res['title']
    return title
  except:
    print('error1')

def create_dir():
  print('create_dir')
  bool = os.path.exists('./downloads')
  if bool == False:
    os.mkdir('./downloads')

def remove():
  if (os.path.isfile(videopath)):
    os.remove(videopath)
  if (os.path.isfile(audiopath)):
    os.remove(audiopath)
  if (os.path.isfile('video.webm.part')):
    os.remove('video.webm.part')
  if (os.path.isfile('audio.webm.part')):
    os.remove('audio.webm.part')


def url_check(inp_url):
  print('url_check')
  try:
    with YoutubeDL() as ydl:
      ydl.extract_info(inp_url, download=False)
      re = 'correct'
  except:
    re = 'error'
    return re
    
def main():
  layout = [
      [sg.Text('URL'), sg.Input(key='-INP_URL-'), sg.Button('paste', key='-PASTE_BTN-')],
      [sg.Checkbox('保存するファイル名', key='-SAVE_NAME-'), sg.InputText(key='-FILENAME-', size=(28, 2))],
      [sg.Combo(['webm最高品質', 'mp3最高品質', 'mp4標準品質'], key='-COMBO-', size=(15, 1), readonly=True, default_value="選択して下さい")],
      [sg.Text(size=(45, 2)), sg.Button('Download', key='-DOWNLOAD-', disabled=False)],
      [sg.Text('入力待ち...', key='-CONDITION-')]
  ]

  window = sg.Window('Video Downloader', layout, icon=base_path + '\main.ico')
  create_dir()

  while True:
    event, value = window.read()

    if event == sg.WIN_CLOSED:
      remove()
      break
    
    if event == '-PASTE_BTN-':
      next = pyperclip.paste()
      window['-INP_URL-'].update(next)

    filename = value['-FILENAME-']
    inp_url = value['-INP_URL-']

    if event == '-DOWNLOAD-':
      window['-DOWNLOAD-'].update(disabled=True)
      window['-CONDITION-'].update('処理中')
      if url_check(inp_url) == 'error':
        sg.popup_error('正しいURLを入力して下さい', title='error')
        window['-DOWNLOAD-'].update(disabled=False)
      if value['-COMBO-'] == '選択して下さい':
        sg.popup_error('出力形式を選択して下さい', title='error')
        window['-DOWNLOAD-'].update(disabled=False)

      title = get_title(inp_url)

      if value['-COMBO-'] == 'mp4標準品質':
        try:
          if value['-SAVE_NAME-'] == False:
            path = 'downloads/' + title + '.mp4'
          else:
            path = 'downloads/' + filename + '.mp4'

          ydl_opts = {
            'outtmpl':path,
            'format':'best'
          }
          start(ydl_opts, inp_url, window)
        except:
          print('error4')
          window['-CONDITION-'].update('入力待ち...')

      if value['-COMBO-'] == 'webm最高品質':
        ydl_opts = {
          'outtmpl':videopath,
          'format': 'bestvideo',
        }
        start(ydl_opts, inp_url, window)

        ydl_opts = {
          'outtmpl':audiopath,
          'format': 'bestaudio',
        }
        start(ydl_opts, inp_url, window)
        time.sleep(1)
        start_merge(value, title, filename, window)

      if value['-COMBO-'] == 'mp3最高品質':
        try:
          if value['-SAVE_NAME-'] == False:
            path = 'downloads/' + title + '.mp3'
          else:
            path = 'downloads/' + filename + '.mp3'

          ydl_opts = {
            'outtmpl':path,
            'format':'bestaudio',
          }
          start(ydl_opts, inp_url, window)
        except:
          print('error5')
          window['-CONDITION-'].update('入力待ち...')

  window.close()

if __name__ == '__main__':
  main()