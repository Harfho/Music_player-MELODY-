import tkinter.messagebox
import os
import time
import threading
import webbrowser

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from ttkthemes import themed_tk as tk

mixer.init()

root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.title('MusicP')
root.iconbitmap(os.path.join(file=os.path.join('images/icon.ico')))#r'F:\ALONE\PYTHON\APP CREATED BY ME\MUSICPLAYER\images/icon.ico'))
# root.geometry('300x300')

mBar = Frame(root, relief=SUNKEN, borderwidth=1, bg='blue')
mBar.pack(fill=X)

statusbar = Label(root, text='Welcome To Melody', relief=SUNKEN, anchor=W, fg='blue')
statusbar.pack(side=BOTTOM, fill=X)


def openlinkedin():
    webbrowser.open_new_tab('www.linkedin.com/harfho')


def openfacebook():
    webbrowser.open_new_tab('www.facebook.com/harfho')


def openinstagram():
    webbrowser.open_new_tab('www.instgram.com/harfho')


def opengravater():
    webbrowser.open_new('www.gravater.com/harfho')


def about_me():
    msg = '''
            Music player built by python
            Facebook group=ALPHA GROUP
            Follow me on instagram- @harfho
            Email-harfho77@gmail.com
            '''
    ttk.tkinter.messagebox.showinfo('ABOUT', msg)


def helpdoc():
    msg = '''
            This app was built with python using tkinter.
            -----------------
                -USAGE:
                    ADD the music to play to the playlist(At the rightside).
                    SELECT the music to play.
                    Click on the play button.                        
            -----------------
                -NOTE:
                    This app was built when am still learning programming.
                    That's the reason why it requires you to manaully
                    add your music To the playlist.
                    In the future am sure the automated one will be ready.
                            Thanks for your understanding.
                                                              -HARFHO
                                                                2018   
          '''
    tkinter.messagebox.showinfo('HELP', msg)


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    # filename_path=filedialog.askdirectory()
    # print(filename_path)
    if filename_path == '':
        tkinter.messagebox.showerror('Error','No music selected')
    else:
        add_to_playlist(filename_path)


def add_to_playlist(filename):
    index = 0
    playlistbox.insert(index, os.path.basename(filename))
    playlist.insert(index, filename)
    index += 1
    print(playlist)


# playlist-contains the full path for filename to play
# playlistbox-

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


playlist = []


def file():
    File = Menubutton(mBar, text='File')
    File.pack(side=LEFT, ipadx='1m')

    File.file = Menu(File, tearoff=0)
    File.file.add_command(label='Open', command=browse_file)
    File.file.add_command(label='Exit', command=root.destroy)
    File['menu'] = File.file

    File = Menubutton(mBar, text='Help')
    File.pack(side=LEFT)

    File.file = Menu(File, tearoff=0)
    File.file.add_command(label='About us', command=about_me)
    File.file.add_command(label='About Harfho', command=opengravater)
    File.file.add_command(label='Help', command=helpdoc)
    File['menu'] = File.file


def topmenu():
    menubar = Menu(root, tearoff=0)
    root.config(menu=menubar)

    submenu = Menu(menubar, tearoff=0)

    menubar.add_cascade(label='HARFHO', menu=submenu)
    submenu.add_command(label='instagram-@harfho', command=openinstagram)
    submenu.add_command(label='Linkin-Harfho', command=openlinkedin)
    submenu.add_command(label='Facebook-Eon Harfho', command=openfacebook)
    # submenu.add_command(label='------------------')


Filemenu = file()

topmenu()

leftframe = Frame(root)
leftframe.pack(side=RIGHT, padx=30, pady=30)

addbtn = ttk.Button(leftframe, text='+Add', command=browse_file)
addbtn.pack()

delbtn = ttk.Button(leftframe, text='-Del', command=del_song)
delbtn.pack(side=BOTTOM)

playlistbox = Listbox(leftframe, height=20, width=50)
# playlistbox.pack()
scroll = ttk.Scrollbar(leftframe, command=playlistbox.yview)
playlistbox.pack(side=LEFT)
playlistbox.configure(yscrollcommand=scroll.set)
scroll.pack(side=LEFT, fill=Y)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

# file_name = Label(root, text='Let make a noise')
# file_name.pack()

time_label = Label(topframe, text='Time_length- --:--')
time_label.pack(pady=5)

current_label = Label(topframe, text='Current_time   - --:--', relief=GROOVE)
current_label.pack()

play_time =''
def show_title(play_song):
    global play_time
    # file_name['text'] = ('Playing-' + os.path.basename(filename_path))

    file_dat = os.path.splitext(play_song)
    if file_dat[-1] == '.mp3':
        # mp3 file
        audio = MP3(play_song)
        total_length = audio.info.length


    else:
        sound = mixer.Sound(play_song)
        total_length = sound.get_length()
        # print(total_length)
    m, s = divmod(total_length, 60)
    mins = round(m)
    secs = round(s)

    total_time = f'%02d:%02d' % (mins, secs)  # '{02d}:{:02d}'.format(mins,secs)
    # print(total_time)
    time_label['text'] = ('Time_length- ' + total_time)
    play_time += total_time
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    # start_count(total_length)


def start_count(total):
    global paused
    currenttime = 0
    while currenttime <= total and mixer.music.get_busy():
        if paused:
            continue
        else:
            m, s = divmod(currenttime, 60)
            mins = round(m)
            secs = round(s)
            total_time = f'%02d:%02d' % (mins, secs)
            current_label['text'] = ('current time- ' + total_time)
            time.sleep(1)
            currenttime += 1


paused = FALSE
init = TRUE


def Play_music():
    global paused
    global init
    global play_time
    time_label['text'] = 'Time_length- --:--'

    if paused:
        playBtn.configure(image=Photoplay)
        statusbar['text'] = 'Music Resume'
        statusbar['text']='Playing Music-'+os.path.basename(filename_path)
        mixer.music.unpause()
        paused = FALSE
        time_label['text'] = ('Time_length- ' + play_time)
    else:
        try:
            Stop_music()
            playBtn.configure(image=Photoplay)
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = 'Playing Music-' + os.path.basename(play_it)
            show_title(play_it)
        except:
            if playlist != []:
                msg = '''
                    Select music to play from the playlist     
                    '''
                tkinter.messagebox.showerror('Fail to Play', msg)
            else:
                msg = '''No file to play
                                    Add music to the playlist
                                '''
                tkinter.messagebox._show('Empty Playlist', msg)
                browse_file()
            # Button(root,text='Open',command=browse_file).pack(side=TOP)
    current_label['text'] = 'Current_time  - --:--'

def Stop_music():
    global paused
    mixer.music.stop()
    statusbar['text'] = 'Music Stop'
    current_label['text'] = 'current time- 00:00'
    # init=True
    playBtn.configure(image=Photplaypause)
    try:
        paused = FALSE
    except:
        pass


def Pause_music():
    global paused
    paused = TRUE
    # mixer.music.pause()
    mixer.music.pause()
    statusbar['text'] = 'Music Pause'
    playBtn.configure(image=Photplaypause)


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.50)
        volBtn.configure(image=volphoto)
        scale.set(50)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volBtn.configure(image=Mutephoto)
        scale.set(0)
        muted = TRUE


middle_frame = Frame(rightframe, borderwidth=3, relief=GROOVE)
middle_frame.pack(padx=30, pady=30)

Photplaypause = PhotoImage(file=os.path.join('images/playpause.png'))
Photoplay = PhotoImage(file=os.path.join('images/play.png'))
playBtn = ttk.Button(middle_frame, image=Photoplay, command=Play_music)
playBtn.grid(row=0, column=0)  # pack(side=LEFT,padx=10)

Photostop = PhotoImage(file=os.path.join(('images/stop.png')))
stopBtn = ttk.Button(middle_frame, image=Photostop, command=Stop_music)
stopBtn.grid(row=0, column=1)  # pack(side=LEFT,padx=10)

Photopause = PhotoImage(file=os.path.join('images/pause.png'))
pauseBtn = ttk.Button(middle_frame, image=Photopause, command=Pause_music)
pauseBtn.grid(row=0, column=2)  # pack(side=LEFT,padx=10)

bottom_frame = Frame(rightframe)
bottom_frame.pack(pady=10, padx=10, anchor=E)

Mutephoto = PhotoImage(file=os.path.join('images/mute.png'))
volphoto = PhotoImage(file=os.path.join('images/vol.png'))

volBtn = ttk.Button(bottom_frame, image=volphoto, command=mute_music)
volBtn.grid(row=0, column=1)  # pack(side=LEFT,padx=10)

scale = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, command_=set_vol)
scale.set(50)
mixer.music.set_volume(0.50)
scale.pack(padx=10)


def closed():
    # tkinter.messagebox.show(title='close',message="Are you sure you what to close this window",)
    Stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", closed)
root.mainloop()
