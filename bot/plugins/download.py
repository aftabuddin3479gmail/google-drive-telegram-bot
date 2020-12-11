import os
from time import sleep
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError

def get_torrent(site):
    results = site
    url = "https://nyaa.si/download/958359.torrent"
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'CERN-LineMode/2.15 libwww/2.17b3')]
    urllib.request.install_opener(opener)  # NOTE: global for the process
    for line in results:
        name = "[HorribleSubs] " + line + " [720p].torrent"
        urllib.request.urlretrieve(url, name)

@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
  user_id = message.from_user.id
  if not message.media:
    sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
    if message.command:
      link = message.command[1]
    else:
      link = message.text
    if 'drive.google.com' in link:
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)
    ifelse:
       'magnet:\?xt=urn:btih:[a-zA-Z0-9]*'
def make_reply(msg):
    result=re.match(pattern,msg)
    if result:
        print(msg)
        handle = lt.add_magnet_uri(ses, msg, params)
        ses.start_dht()

        begin = time.time()
        print(datetime.datetime.now())

        print ('Downloading Metadata...')
        while (not handle.has_metadata()):
            time.sleep(1)
        print ('Got Metadata, Starting Torrent Download...')

        print("Starting", handle.name())
        startreply=('Download started for',handle.name())
        bot.send_message(startreply,from_)
        while (handle.status().state != lt.torrent_status.seeding):
            s = handle.status()
            state_str = ['queued', 'checking', 'downloading metadata', \
                    'downloading', 'finished', 'seeding', 'allocating']
            print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                    (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                    s.num_peers, state_str[s.state]))
            time.sleep(5)

        end = time.time()
        print(handle.name(), "COMPLETE")

        print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")

        print(datetime.datetime.now())
        reply='Download Finished You can find downloaded file @ https://drive.google.com/folderview?id=1Lt3_3mY_Jjdgt9llNGAz8yZHl-QccBJO'
       
      else:
      if '|' in link:
        link, filename = link.split('|')
        link = link.strip()
        filename.strip()
        dl_path = os.path.join(f'{DOWNLOAD_DIRECTORY}/{filename}')
      else:
        link = link.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))


@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = message.reply_text('🕵️**Checking File...**', quote=True)
  if message.document:
    file = message.document
  elif message.video:
    file = message.video
  elif message.audio:
    file = message.audio
  elif message.photo:
  	file = message.photo
  	file.mime_type = "images/png"
  	file.file_name = f"IMG-{user_id}-{message.message_id}.png"
  sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
  LOGGER.info(f'Download:{user_id}: {file.file_id}')
  try:
    file_path = message.download(file_name=DOWNLOAD_DIRECTORY)
    sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
    msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
    sent_message.edit(msg)
  except RPCError:
    sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)

@Client.on_message(filters.incoming & filters.private & filters.command(BotCommands.Ytdl) & CustomFilters.auth_users)
def _ytdl(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    sent_message = message.reply_text('🕵️**Checking Link...**', quote=True)
    link = message.command[1]
    LOGGER.info(f'YTDL:{user_id}: {link}')
    sent_message.edit(Messages.DOWNLOADING.format(link))
    result, file_path = utube_dl(link)
    if result:
      sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
      msg = GoogleDrive(user_id).upload_file(file_path)
      sent_message.edit(msg)
      LOGGER.info(f'Deleteing: {file_path}')
      os.remove(file_path)
    else:
      sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
  else:
    message.reply_text(Messages.PROVIDE_YTDL_LINK, quote=True)
