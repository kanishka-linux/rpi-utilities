#! /usr/bin/python3

import os
import re
import getpass
import hashlib
import base64
import subprocess

HOME = os.path.expanduser('~')

KAWAII_HOME = os.path.join(HOME, ".config/kawaii-player")

AUTOSTART_PATH = os.path.join(HOME, ".config/autostart")

MPV_CONFIG_PATH = os.path.join(HOME, ".config/mpv")

def get_lan_ip():
    a = subprocess.check_output(['ip', 'addr', 'show'])
    b = str(a, 'utf-8')
    c = re.findall('inet [^ ]*', b)
    final = ''
    for i in c:
        if '127.0.0.1' not in i:
            final = i.replace('inet ', '')
            final = re.sub('/[^"]*', '', final)
    print(final)
    return final

def create_deb_and_install():
    cwd = os.getcwd()
    git_dir_path = os.path.join(cwd, "kawaii-player")
    if not os.path.exists(git_dir_path): 
        subprocess.call(["git", "clone", "https://github.com/kanishka-linux/kawaii-player"])
    deb_dir = os.path.join(cwd, "kawaii-player/ubuntu") 
    os.chdir(deb_dir)
    subprocess.call(["python3", "create_deb.py"])
    for file_name in os.listdir(deb_dir):
        if file_name.endswith(".deb"):
            deb_file = file_name
            break
    subprocess.call(["sudo", "apt", "clean"])
    subprocess.call(["sudo", "apt", "install", "-y", "./{}".format(deb_file)])
    subprocess.call(["sudo", "apt", "remove", "-y", "youtube-dl"])
    subprocess.call(["sudo", "apt", "autoremove", "-y"])
    subprocess.call(["sudo", "pip3", "install", "youtube-dl", "--upgrade"])
    subprocess.call(["sudo", "pip3", "install", "pympv", "--upgrade"])
    
def create_config_files():
    if not os.path.exists(KAWAII_HOME):
        os.makedirs(KAWAII_HOME)
    options_file = os.path.join(KAWAII_HOME, "other_options.txt")
    config_file = os.path.join(KAWAII_HOME, "config.txt")
    tmpdir = os.path.join(KAWAII_HOME, "tmp")
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    if not os.path.exists(AUTOSTART_PATH):
        os.makedirs(AUTOSTART_PATH)
    if not os.path.exists(MPV_CONFIG_PATH):
        os.makedirs(MPV_CONFIG_PATH)
    mpv_config_file = os.path.join(MPV_CONFIG_PATH, "config")
    autostart_desktop_file = os.path.join(AUTOSTART_PATH, "kawaii.desktop")
    user = input("Setup user name for server:")
    if user:
        pass_val = getpass.getpass("Enter password for the server:")
        auth = set_user_password(user, pass_val)
    else:
        auth = "none"
    if auth == "none":
        print("You have not setup username and password for media server")
    create_options_file(options_file, tmpdir, auth)
    create_config_file(config_file)
    create_mpv_config(mpv_config_file)
    create_autostart_file(autostart_desktop_file)

def create_autostart_file(autostart_desktop_file):
    if not os.path.exists(autostart_desktop_file):
        with open(autostart_desktop_file, "w") as f:
            f.write("[Desktop Entry]")
            f.write("\nName=Kawaii-Player")
            f.write("\nType=Application")
            f.write("\nComment=Media-Player")
            f.write('\nExec=bash -c "kawaii-player"')
            f.write("\nTerminal=false")
            f.write("\nNoDisplay=false")
            f.write("\nCategories=Audio,Video")
            f.write("\nHidden=false")
            f.write("\nX-GNOME-Autostart-Delay=0")
            f.write("\nX-LXDE-Autostart-Delay=0")
            f.write("\nX-LXDE-Need-Tray=true")
            f.write("\nX-LXQt-Need-Tray=true")

def create_mpv_config(mpv_config_file):
    if not os.path.exists(mpv_config_file):
        with open(mpv_config_file, "w") as f:
            f.write("vo=libmpv")
            f.write("\nao=alsa")
            f.write("\nytdl=yes")
            f.write("\nytdl-format=bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]")
            f.write("\nfullscreen")
            f.write("\nframedrop=decoder")
            f.write("\ncache=auto")
            f.write("\ncache-secs=120")
            f.write("\ncache-default=10000")
            f.write("\ncache-initial=0")
            f.write("\ncache-seek-min=100")
            f.write("\ncache-pause")
            f.write("\ncache-pause-wait=4")
            f.write("\nvideo-aspect=-1")
            f.write("\nprefetch-playlist=yes")
        
def create_config_file(config_file):
    with open(config_file, 'w') as f:
        f.write("DefaultPlayer=libmpv")

def create_options_file(options_file, tmpdir, auth):
    if not os.path.exists(options_file):
        with open(options_file, 'w') as f:
            f.write("\nBROWSER_BACKEND=QTWEBKIT")
            local_ip = get_lan_ip()
            f.write("\nLOCAL_STREAM_IP={}:9001".format(local_ip))
            print("Servie is available at http://{}:9001".format(local_ip))
            f.write("\nDEFAULT_DOWNLOAD_LOCATION="+tmpdir)
            f.write("\nKEEP_BACKGROUND_CONSTANT=no")
            f.write("\nTMP_REMOVE=no")
            f.write("\n#GET_LIBRARY=pycurl,curl,wget")
            f.write("\nGET_LIBRARY=pycurl")
            f.write("\nTHUMBNAIL_ENGINE=mpv")
            f.write("\n#IMAGE_FIT_OPTION=0-9")
            f.write("\nIMAGE_FIT_OPTION=3")
            f.write("\nAUTH={}".format(auth))
            f.write("\nACCESS_FROM_OUTSIDE_NETWORK=False")
            f.write("\nCLOUD_IP_FILE=none")
            f.write("\nHTTPS_ON=False")
            f.write("\nMEDIA_SERVER_COOKIE=False")
            f.write("\nCOOKIE_EXPIRY_LIMIT=24")
            f.write("\nCOOKIE_PLAYLIST_EXPIRY_LIMIT=24")
            f.write("\nLOGGING=Off")
            f.write("\n#YTDL_PATH=default,automatic")
            f.write("\nYTDL_PATH=DEFAULT")
            f.write("\nANIME_REVIEW_SITE=False")
            f.write("\nGET_MUSIC_METADATA=False")
            f.write("\nREMOTE_CONTROL=True")
            f.write("\nMPV_INPUT_CONF=False")
            f.write("\nBROADCAST_MESSAGE=False")
            f.write("\nMEDIA_SERVER_AUTOSTART=True")
            f.write("\n#THEME=default,system,dark")
            f.write("\nTHEME=DARK")
            f.write("\n#EXTRA_PLAYERS=vlc,kodi etc..")
            f.write("\nEXTRA_PLAYERS=NONE")
            f.write("\n#GLOBAL_FONT=Name of Font")
            f.write("\nGLOBAL_FONT=Default")
            f.write("\nGLOBAL_FONT_SIZE=18")
            f.write("\nFONT_BOLD=False")
            msg = ("\n#THUMBNAIL_TEXT_COLOR/LIST_TEXT_COLOR=red,green,blue,yellow,\
                   gray,white,black,cyan,magenta,darkgray,lightgray,darkred,\
                   darkblue,darkyellow,transparent")
            msg = re.sub('[ ]+', ' ', msg)
            f.write(msg)
            f.write("\n#For Dark Theme, use lightgray, if white color looks bright")
            f.write("\nTHUMBNAIL_TEXT_COLOR=white")
            f.write("\nTHUMBNAIL_TEXT_COLOR_FOCUS=green")
            f.write("\nLIST_TEXT_COLOR=white")
            f.write("\nLIST_TEXT_COLOR_FOCUS=violet")
            f.write("\nREMEMBER_VOLUME_PER_VIDEO=False")
            f.write("\nREMEMBER_ASPECT_PER_VIDEO=True")
            f.write("\nVARIABLE_WIDTH_LIST=False")
            f.write("\nOSX_NATIVE_FULLSCREEN=False")
            f.write("\nLIBMPV_API=OPENGL-CB")
            f.write("\nDEVICE_PIXEL_RATIO=0.0")
            f.write("\nPLAYLIST_CONTINUE=True")
            f.write("\nDISPLAY_DEVICE=rpitv")
            f.write("\nGAPLESS_PLAYBACK=True")
            f.write("\nGAPLESS_NETWORK_STREAM=True")
            f.write("\nPC_TO_PC_CASTING=Slave")
            
def set_user_password(text_val, pass_val):
    if not text_val:
        text_val = ''
    if not pass_val:
        pass_val = ''
    new_combine = bytes(text_val+':'+pass_val, 'utf-8')
    new_txt = base64.b64encode(new_combine)
    new_txt_str = 'Basic '+str(new_txt, 'utf-8')
    new_txt_bytes = bytes(str(new_txt_str), 'utf-8')
    h = hashlib.sha256(new_txt_bytes)
    h_digest = h.hexdigest()
    return h_digest
    
def main():
    create_deb_and_install()
    create_config_files()

if __name__ == "__main__":
    main()


