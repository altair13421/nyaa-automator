import os, shutil
import requests
from automator import DOWNLOAD_DIR, SAVED_TORRENTS_DIR, LIBRARY_DIR, MEDIA_DIR, USERS
from automator.utils import rprint_log, rprint_error, rprint_success, sleeper, rprint, console, get_state_strings
import libtorrent as lt
from rich.progress import Progress
session = lt.session()
session.listen_on(6881, 6891)

# Making Directories
os.makedirs(LIBRARY_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(SAVED_TORRENTS_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# Download Passer
def download_torrent(magnet=None, torrent_link=None, title = None, object=None, verbose = False):
    if magnet is not None:
        actual_downloading(magnet=magnet, verbose=verbose)
    elif torrent_link is not None and title is not None:
        requ = requests.get(torrent_link)
        requ.raise_for_status()
        if title.__contains__('.torrent'):
            torrent_loc = f'{SAVED_TORRENTS_DIR}{os.sep}{title}'
        else:
            torrent_loc = f'{SAVED_TORRENTS_DIR}{os.sep}{title}.torrent'
        with open(torrent_loc, 'wb') as torrent_file:
            for chunk in requ.iter_content(1000000):
                torrent_file.write(chunk)
        actual_downloading(torrent_location=f'{torrent_loc}', title=title, object=object, verbose=verbose)
    return f"Download Complete at {DOWNLOAD_DIR}"

# Actual Downloader..........
def actual_downloading(magnet=None, torrent_location=None, title=None, object=None, verbose = False):
    session = lt.session()
    session.listen_on(6881, 6891)
    if object is None and title is not None and title.split('.')[0].isnumeric():
        savepath = os.path.join(DOWNLOAD_DIR, 'other_downloads')
    elif object is not None:
        savepath = os.path.join(DOWNLOAD_DIR, object['title'])
    else:
        savepath = os.path.join(DOWNLOAD_DIR, 'other_downloads')
    os.makedirs(savepath, exist_ok=True)

    if magnet is not None:
        parameters = {
            'save_path': savepath,
            'storage_mode': lt.storage_mode_t(2),
        }
        handler = lt.add_magnet_uri(session, magnet, parameters)
        if verbose: rprint_log('Downloading Metadata')
        while not handler.has_metadata():
            sleeper(1)
        name_file = handler.name
        if verbose: 
            rprint_success('Metadata Download Successful')
            rprint_success(f'Downloading {name_file}')
    elif torrent_location is not None:
        parameters = {
            'save_path': savepath,
            'storage_mode': lt.storage_mode_t(2),
            'ti': lt.torrent_info(torrent_location),
        }
        handler = session.add_torrent(parameters)
        if verbose: rprint_log(f'Downloading {handler.status().name}')
        name_file = handler.status().name
    session.start_dht()

    with Progress() as progress:
        if verbose: download = progress.add_task('Downloading...')
        while handler.status().state != lt.torrent_status.seeding:
            stat = handler.status()
            if verbose:
                progress.update(
                    download,
                    description=f'[cyan]Peers: {stat.num_peers}[/cyan] [yellow]D/S: {stat.download_rate/1000}kbps[/yellow] [aquamarine1]U/S: {stat.upload_rate/1000}kbps[/aquamarine1] [sky_blue4]STATE: {stat.state}[/sky_blue4]',
                    completed=stat.progress*100,
                    total=100,
                )
            sleeper(1)
    if verbose: rprint_success('Download Successful')
    if verbose: rprint_success('Copying')
    try:
        move_downloaded(name=name_file, savepath=savepath)
    except Exception as e:
        rprint_error(f'Error {e} Occurred')
    if verbose: rprint_success('Copied')

# MAL List Getter or Something
def get_anime(object=None):
    pass

# Mover: Moves Downloads From DOWNLOAD_DIR to MEDIA_DIR
def move_downloaded(name=None, savepath=None):
    if os.path.isfile(os.path.join(savepath, name)):
        shutil.move(os.path.join(savepath, name), os.path.join(MEDIA_DIR, name))
    elif os.path.isdir(os.path.join(savepath, name)):
        if shutil.copytree(os.path.join(savepath,name), os.path.join(MEDIA_DIR, name), dirs_exist_ok=True, copy_function = shutil.copy2):
            shutil.rmtree(os.path.join(savepath,name))
        else:
            return False
    return True

# Renamer: Renames the Episode to {title} - S{season_number}E{episode_number}.{extension}
def rename_download(name=None, savepath=None):
    pass

# BULLSHIT
def pause_torrents():
    session.pause()
def resume_torrents():
    session.resume()
