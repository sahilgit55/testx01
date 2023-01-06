from pyrogram import Client,  filters
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, USER_DATA, get_media, timex, delete_all, delete_trash, new_user, create_process_file, make_direc, durationx, clear_trash_list, check_filex, save_restart, process_checker
from config import botStartTime
from helper_fns.watermark import vidmarkx, hardmux_vidx, softmux_vidx, softremove_vidx
from string import ascii_lowercase, digits
from random import choices
from asyncio import sleep as asynciosleep
from pyrogram.errors import FloodWait
from helper_fns.process import append_master_process, remove_master_process, get_master_process, append_sub_process, remove_sub_process, get_sub_process
from os.path import getsize
from os import execl
from sys import argv, executable
from helper_fns.engine import ffmpeg_engine
from helper_fns.progress_bar import progress_bar
from helper_fns.helper import execute
from json import loads
from math import ceil
from os.path import getsize, splitext, join




############Variables##############
sudo_users = eval(Config.SUDO_USERS)
USER = Config.USER
wpositions = {'5:5': 'Top Left', 'main_w-overlay_w-5:5': 'Top Right', '5:main_h-overlay_h': 'Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Bottom Right'}


###########Send Video##############
async def send_tg_video(bot, user_id, final_video_list, cc_options, duration, final_thumb, reply, start_time, datam, modes):
                        success = []
                        failed = []
                        z = 1
                        total = len(final_video_list)
                        for final_video in final_video_list:
                                        vname = str(final_video.split('/')[-1])
                                        datam[0] = vname + f" [{str(z)}/{str(total)}]"
                                        cc = f"{str(vname)}\n\n{str(cc_options)}"
                                        print("🔶Starting Video Upload", vname)
                                        try:
                                                the_media = await bot.send_video(
                                                                chat_id=user_id,
                                                                video=final_video,
                                                                caption=cc,
                                                                supports_streaming=True,
                                                                duration=duration,
                                                                thumb=final_thumb,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time, bot, datam, modes)
                                                )
                                                print("✅Video Uploaded Successfully", vname)
                                                success.append(final_video)
                                        except FloodWait as e:
                                                await asynciosleep(int(e.value)+10)
                                                the_media =await bot.send_video(
                                                                chat_id=user_id,
                                                                video=final_video,
                                                                caption=cc,
                                                                supports_streaming=True,
                                                                duration=duration,
                                                                thumb=final_thumb,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time, bot, datam, modes)
                                                )
                                                print("✅Video Uploaded Successfully", vname)
                                                success.append(final_video)
                                        except Exception as e:
                                                print("❌Error While Sending Video\n", e, vname)
                                                failed.append(final_video)
                                                await bot.send_message(user_id, f"❌Error While Uploading Video\n`{str(vname)}`\n\n{str(e)}")
                        return [True, success, failed]


#########Download Tg File##############
async def download_tg_file(bot, m, dl_loc, reply, start_time, datam, modes):
                                print("🔶Starting Download", datam[0])
                                try:
                                        the_media = await bot.download_media(
                                                        message=m,
                                                        file_name=dl_loc,
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, bot, datam, modes)
                                                )
                                        print("✅Successfully Downloaded", datam[0])
                                        return [True, the_media]
                                except FloodWait as e:
                                                await asynciosleep(int(e.value)+10)
                                                the_media = await bot.download_media(
                                                        message=m,
                                                        file_name=dl_loc,
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, bot, datam, modes)
                                                )
                                                print("✅Successfully Downloaded", datam[0])
                                                return [True, the_media]
                                except Exception as e:
                                                print("❌Downloading Error\n", e, datam[0])
                                                return [False, e]

###########Split File##############
async def split_video_file(bot, user_id, reply, split_size, dirpath, file, file_name, progress, duration, datam, modes):
        success = []
        trash_list = []
        try:
                        size = getsize(file)
                        parts = ceil(size/split_size)
                        base_name, extension = splitext(file)
                        i=1
                        start_time = 0
                        while i <= parts:
                                parted_name = f"{str(file_name)}.part{str(i).zfill(3)}{str(extension)}"
                                out_path = join(dirpath, parted_name)
                                trash_list.append(out_path)
                                command = ["ffmpeg", "-hide_banner", "-progress", "progress", "-ss", str(start_time),
                                         "-i", str(file), "-fs", str(split_size), "-map", "0", "-map_chapters", "-1",
                                         "-c", "copy", out_path]
                                sresult = await ffmpeg_engine(bot, user_id, reply, command, file, out_path, 'None', progress, duration, datam, modes)
                                if sresult[0]:
                                        if sresult[1]:
                                                await clear_trash_list(trash_list)
                                                return [True, True]
                                else:
                                        await delete_trash(out_path)
                                        command = ["ffmpeg", "-hide_banner", "-progress", "progress", "-ss", str(start_time),
                                         "-i", str(file), "-fs", str(split_size), "-map_chapters", "-1",
                                         "-c", "copy", out_path]
                                        sresult = await ffmpeg_engine(bot, user_id, reply, command, file, out_path, 'None', progress, duration, datam, modes)
                                        if sresult[0]:
                                                if sresult[1]:
                                                        await clear_trash_list(trash_list)
                                                        return [True, True]
                                        else:
                                                await clear_trash_list(trash_list)
                                                return [False]
                                cut_duration = durationx(out_path)
                                if cut_duration <= 4:
                                        break
                                success.append(out_path)
                                start_time += cut_duration - 3
                                i = i + 1
                        return [True, False, success]
        except Exception as e:
                print(e)
                await bot.send_message(user_id, f"❌Error While Splitting Video\n\n{str(e)}")
                await clear_trash_list(trash_list)
                return [False]


##########Processor################
async def processor(bot, message, muxing_type):
                user_id = message.chat.id
                userx = message.from_user.id
                Ddir = f'./{str(userx)}_RAW'
                Wdir = f'./{str(userx)}_WORKING'
                Sdir = f'./{str(userx)}_Split'
                await make_direc(Ddir)
                await make_direc(Wdir)
                try:
                                file_type = message.reply_to_message.video or message.reply_to_message.document
                                if file_type.mime_type.startswith("video/"):
                                        file_id = int(message.reply_to_message.id)
                                else:
                                        await bot.send_message(user_id, "❌Invalid Media")
                                        return
                except:
                        try:
                                ask = await bot.ask(user_id, '*️⃣ Send Me Video\n\n⌛Request TimeOut In 120 Seconds', timeout=120, filters=(filters.document | filters.video))
                                file_type = ask.video or ask.document
                                if file_type.mime_type.startswith("video/"):
                                        file_id = ask.id
                                else:
                                        await ask.request.delete()
                                        await bot.send_message(user_id, "❌Invalid Media")
                                        return
                        except:
                                await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                                return
                        await ask.request.delete()
                custom_thumb = False
                try:
                        ask = await bot.ask(user_id, f'*️⃣ Send Me Thumbnail For This Video\n\n🔷Send `pass` for default Thumbnail\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.photo | filters.text))
                        thumb = ask.id
                        if ask.photo or (ask.document and ask.document.mime_type.startswith("image/")):
                                thumbm = await bot.get_messages(user_id, thumb, replies=0)
                                thumb_name = get_media(thumbm).file_name.replace(' ', '')
                                thumb_loc = f'{Ddir}/{str(userx)}_{str(thumb_name)}'
                                thumb_download = await bot.download_media(thumbm, thumb_loc)
                                if thumb_download is None:
                                        await delete_trash(thumb_loc)
                                        await  bot.send_message(chat_id=user_id,
                                                        text=f"❌Failed To Download Thumbnail, Default Thumbnail Will Be Used Now")
                                else:
                                        custom_thumb = True
                except Exception as e:
                                print(e)
                                await bot.send_message(user_id, "🔃Timed Out Or Some Error Occured! Tasked Has Been Cancelled.\nDefault Thumbnail Will Be Used Now")
                print("🎨Process Type", muxing_type)
                if muxing_type not in ('Watermark' 'Compressing'):
                        try:
                                ask = await bot.ask(user_id, f'*️⃣Send Subtitle File To Mux\n\n⏳Request Time Out In 60 Seconds', timeout=60, filters=filters.document)
                                if ask.document:
                                        file_type = ask.document
                                        if not file_type.mime_type.startswith("video/"):
                                                        sub_id = ask.id
                                        else:
                                                        await ask.request.delete()
                                                        await bot.send_message(user_id, "❌Invalid Media")
                                                        return
                                else:
                                        await ask.request.delete()
                                        await bot.send_message(user_id, "❌Invalid Media")
                                        return
                        except:
                                        await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                                        return
                        await ask.request.delete()
                process_id = str(''.join(choices(ascii_lowercase + digits, k=10)))
                append_master_process(process_id)
                mptime = timex()
                trash_list = []
                map = '0:a'
                if muxing_type not in ('Watermark', 'Compressing'):
                                subm = await bot.get_messages(user_id, sub_id, replies=0)
                                sub_name = get_media(subm).file_name.replace(' ', '')
                                sub_loc = f'{Ddir}/{str(userx)}_{str(sub_name)}'
                                sub_download = await bot.download_media(subm, sub_loc)
                                if sub_download is None:
                                        await delete_trash(sub_loc)
                                        remove_master_process(process_id)
                                        await  bot.send_message(chat_id=user_id,
                                                        text=f"❌Failed To Download Subtitles")
                                        return
                m = await bot.get_messages(user_id, file_id, replies=0)
                media = get_media(m)
                file_name = media.file_name.replace(' ', '').replace('/', '_').replace('[', '_').replace(']', '_')
                dl_loc = f'{Ddir}/{str(userx)}_{str(file_name)}'
                start_time = timex()
                modes = {'files': 1, 'process_id': process_id}
                datam = (file_name, '🔽Downloading Video', '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍', mptime)
                reply = await bot.send_message(chat_id=user_id,
                                        text=f"🔽Starting Download\n🎟️File: {file_name}")
                try:
                        download = await download_tg_file(bot, m, dl_loc, reply, start_time, datam, modes)
                        check_data = [[process_id, get_master_process()]]
                        checker = await process_checker(check_data)
                        if not checker:
                                await delete_trash(dl_loc)
                                await reply.edit("🔒Task Cancelled By User")
                                return
                        if download[0]:
                                the_media = download[1]
                                trash_list.append(the_media)
                                select_stream = USER_DATA()[userx]['select_stream']
                                language = 'ENG'
                                if select_stream:
                                        get_streams = await execute(
                                                                                                f"ffprobe -hide_banner -show_streams -print_format json '{the_media}'"
                                                                                        )
                                        if not get_streams:
                                                        await bot.send_message(user_id, "❌Failed To Get Audio Streams From Video")
                                                        select_stream = False
                                        else:
                                                details = loads(get_streams[0])
                                                stream_data = {}
                                                smsg = ''
                                                try:
                                                        for stream in details["streams"]:
                                                                stream_name = stream["codec_name"]
                                                                stream_type = stream["codec_type"]
                                                                codec_long_name = stream['codec_long_name']
                                                                if stream_type in ("audio"):
                                                                        mapping = stream["index"]
                                                                        try:
                                                                                lang = stream["tags"]["language"]
                                                                        except:
                                                                                lang = mapping
                                                                        sname = f"{stream_type.upper()} - {str(lang).upper()} [{codec_long_name}]"
                                                                        stream_data[sname] = {}
                                                                        stream_data[sname]['index'] =mapping
                                                                        stream_data[sname]['language'] = str(lang).upper()
                                                                        smsg+= f'`{sname}`\n\n'
                                                        if len(stream_data)==0:
                                                                await bot.send_message(user_id, "❗No Stream Found In Video")
                                                                select_stream = False
                                                        elif len(stream_data)==1:
                                                                await bot.send_message(user_id, "🔶Only One Audio Present In The Video So Skipping Stream Select.")
                                                                select_stream = False
                                                        else:
                                                                skeys = list(stream_data.keys())
                                                                LFound= False
                                                                for k in skeys:
                                                                        if stream_data[k]['language']==language:
                                                                                LFound = True
                                                                                cstream = k
                                                                                stream_no = stream_data[cstream]['index']
                                                                                map = f'0:a:{str(int(stream_no)-1)}'
                                                                                print(f'🔶Stream Selected For {str(file_name)}\n{str(cstream)}\nStream No: {str(stream_no)}')
                                                                if not LFound:
                                                                        try:
                                                                                        ask = await bot.ask(user_id, f'*️⃣{str(len(stream_data))} Streams Found, Send Stream From Below Streams\n\n\n{str(smsg)}\n⌛Request Timeout In 5 Minutes.', timeout=300, filters=filters.text)
                                                                                        cstream  = ask.text
                                                                                        if cstream not in stream_data:
                                                                                                await ask.request.delete()
                                                                                                await bot.send_message(user_id, "❗Invalid Stream")
                                                                                                select_stream = False
                                                                                        else:
                                                                                                await ask.request.delete()
                                                                                                stream_no = stream_data[cstream]['index']
                                                                                                map = f'0:a:{str(int(stream_no)-1)}'
                                                                                                print(f'🔶Stream Selected For {str(file_name)}\n{str(cstream)}\nStream No: {str(stream_no)}')
                                                                        except:
                                                                                await bot.send_message(user_id, "🔃Timed Out Or Invalid Values! Tasked Has Been Cancelled.")
                                                                                select_stream = False
                                                except Exception as e:
                                                        await bot.send_message(user_id, "❌Failed To Get Audio Streams From Video")
                                                        select_stream = False
                                duration = 0
                                try:
                                        duration = int(durationx(the_media))
                                except:
                                        pass
                                progress = f"{Wdir}/{str(userx)}_{str(file_name)}_progress.txt"
                                await create_process_file(progress)
                                if muxing_type=='Watermark':
                                        output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}"
                                        preset = USER_DATA()[userx]['watermark']['preset']
                                        watermark_position = USER_DATA()[userx]['watermark']['position']
                                        watermark_size = USER_DATA()[userx]['watermark']['size']
                                        watermark_crf = USER_DATA()[userx]['watermark']['crf']
                                        modes['watermark_position'] = watermark_position
                                        modes['watermark_size'] = watermark_size
                                        modes['crf'] = watermark_crf
                                        watermark_path = f'./{str(userx)}_watermark.jpg'
                                        process_name = '🛺Adding Watermark'
                                        command = [
                                                                "ffmpeg", "-hide_banner", "-progress", progress, "-i", the_media, "-i", watermark_path, "-map", f"0:v", "-map", f"{str(map)}", "-map", f"0:s",
                                                                "-filter_complex", f"[1][0]scale2ref=w='iw*{watermark_size}/100':h='ow/mdar'[wm][vid];[vid][wm]overlay={watermark_position}", "-preset", preset,'-vcodec','libx265',
                                                                '-vtag', 'hvc1', '-crf',f'{str(watermark_crf)}', "-c:a", "copy", "-y", output_vid
                                                        ]
                                elif muxing_type == 'HardMux':
                                        output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(muxing_type)}).mp4"
                                        preset =  USER_DATA()[userx]['muxer']['preset']
                                        process_name = '🎮HardMuxing Subtitles'
                                        command = [
                                                                'ffmpeg','-hide_banner',
                                                                '-progress', progress, '-i', the_media,
                                                                '-vf', f"subtitles='{sub_loc}'",
                                                                '-map','0:v',
                                                                '-map',f'{str(map)}',
                                                                '-preset', preset,
                                                                '-c:a','copy',
                                                                '-y',output_vid
                                                                ]
                                elif muxing_type == 'SoftMux':
                                        output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(muxing_type)}).mkv"
                                        preset =  USER_DATA()[userx]['muxer']['preset']
                                        process_name = '🎮SoftMuxing Subtitles'
                                        command = [
                                                                'ffmpeg','-hide_banner',
                                                                '-progress', progress, '-i', the_media,
                                                                '-i',sub_loc,
                                                                '-map','1:0',
                                                                '-map','0:v',
                                                                '-map',f'{str(map)}',
                                                                '-map','0:s',
                                                                '-disposition:s:0','default',
                                                                '-c:v','copy',
                                                                '-c:a','copy',
                                                                '-c:s','copy',
                                                                '-y',output_vid
                                                                ]
                                elif muxing_type == 'SoftReMux':
                                        output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(muxing_type)}).mkv"
                                        preset =  USER_DATA()[userx]['muxer']['preset']
                                        process_name = '🎮SoftReMuxing Subtitles'
                                        command = [
                                                                'ffmpeg','-hide_banner',
                                                                '-progress', progress, '-i', the_media,
                                                                '-i',sub_loc,
                                                                '-map','0:v',
                                                                '-map',f'{str(map)}',
                                                                '-map','1:0',
                                                                '-disposition:s:0','default',
                                                                '-c:v','copy',
                                                                '-c:a','copy',
                                                                '-c:s','copy',
                                                                '-y',output_vid
                                                                ]
                                elif muxing_type=='Compressing':
                                        output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}.mkv"
                                        preset =  USER_DATA()[userx]['compress']['preset']
                                        compress_crf = USER_DATA()[userx]['compress']['crf']
                                        process_name = '🏮Compressing Video'
                                        modes['crf'] = compress_crf
                                        command = [
                                                                'ffmpeg','-hide_banner',
                                                                '-progress', progress, '-i', the_media,
                                                                '-map','0:v',
                                                                '-map',f'{str(map)}',
                                                                "-map", "0:s",
                                                                '-vcodec','libx265',
                                                                '-vtag', 'hvc1',
                                                                '-preset', preset,
                                                                '-crf',f'{str(compress_crf)}',
                                                                '-y',output_vid
                                                                ]
                                trash_list.append(output_vid)
                                await delete_trash(output_vid)
                                datam = (file_name, process_name, mptime)
                                modes['process_type'] = muxing_type
                                wresult = await ffmpeg_engine(bot, user_id, reply, command, the_media, output_vid, preset, progress, duration, datam, modes)
                                if wresult[0]:
                                        if wresult[1]:
                                                await clear_trash_list(trash_list)
                                                await reply.edit("🔒Task Cancelled By User")
                                        else:
                                                compression = False
                                                if compression:
                                                        base_name, extension = splitext(output_vid)
                                                        compressed_vid = f"{Wdir}/{str(userx)}_{str(file_name)}_compressed{str(extension)}"
                                                        preset =  USER_DATA()[userx]['compress']['preset']
                                                        compress_crf = USER_DATA()[userx]['compress']['crf']
                                                        process_name = '🏮Compressing Video'
                                                        modes['crf'] = compress_crf
                                                        command = [
                                                                                'ffmpeg','-hide_banner',
                                                                                '-progress', progress, '-i', output_vid,
                                                                                '-map','0:v',
                                                                                '-map','0:a',
                                                                                "-map", "0:s",
                                                                                '-vcodec','libx265',
                                                                                '-vtag', 'hvc1',
                                                                                '-preset', preset,
                                                                                '-crf',f'{str(compress_crf)}',
                                                                                '-y',compressed_vid
                                                                                ]
                                                        trash_list.append(compressed_vid)
                                                        await delete_trash(compressed_vid)
                                                        await create_process_file(progress)
                                                        datam = (file_name, process_name, mptime)
                                                        modes['process_type'] = 'Compressing'
                                                        cresult = await ffmpeg_engine(bot, user_id, reply, command, output_vid, compressed_vid, preset, progress, duration, datam, modes)
                                                        if cresult[0]:
                                                                if cresult[1]:
                                                                        await clear_trash_list(trash_list)
                                                                        await reply.edit("🔒Task Cancelled By User")
                                                                else:
                                                                        output_vid = compressed_vid
                                                split_video = False
                                                premium = False
                                                if getsize(output_vid)>209715200:
                                                        if split_video:
                                                                await reply.edit("🪓Splitting Video")
                                                                if not premium:
                                                                        # split_size = 104857600 - 5000000
                                                                        split_size = 209715200
                                                                        await make_direc(Sdir)
                                                                        await create_process_file(progress)
                                                                        modes['process_type'] = 'Splitting'
                                                                        datam = (file_name, '🪓Splitting Video', mptime)
                                                                        sresult = await  split_video_file(bot, user_id, reply, split_size, Sdir, output_vid, file_name, progress, duration, datam, modes)
                                                                        if sresult[0]:
                                                                                if sresult[1]:
                                                                                        await clear_trash_list(trash_list)
                                                                                        await reply.edit("🔒Task Cancelled By User")
                                                                                        return
                                                                                else:
                                                                                        trash_list = trash_list + sresult[2]
                                                                                        final_video = sresult[2]
                                                                        else:
                                                                                final_video = [output_vid]
                                                else:
                                                        final_video = [output_vid]
                                                if not custom_thumb:
                                                        final_thumb = './thumb.jpg'
                                                else:
                                                        final_thumb = thumb_loc
                                                if not select_stream:
                                                        cc = ''
                                                else:
                                                        cc = f"✅Stream: {str(cstream)}"
                                                datam = [file_name, '🔼Uploading Video', '𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍', mptime]
                                                start_time = timex()
                                                upload = await send_tg_video(bot, user_id, final_video, cc, duration, final_thumb, reply, start_time, datam, modes)
                                                check_data = [[process_id, get_master_process()]]
                                                checker = await process_checker(check_data)
                                                if not checker:
                                                        await clear_trash_list(trash_list)
                                                        await reply.edit("🔒Task Cancelled By User")
                                                        return
                                                await clear_trash_list(trash_list)
                                                await reply.delete()
                                                await bot.send_message(user_id, "✅Task Completed Successfully")
                                else:
                                        await clear_trash_list(trash_list)
                                        await reply.edit(f"❌{muxing_type} Process Failed")
                        else:
                                await delete_trash(dl_loc)
                                await reply.edit(f"❌Downloading Failed\n\nError: {str(download[1])}")
                except Exception as e:
                        await reply.edit(f"❌Some Error Occured, While Processing.\n\nError: {str(e)}")
                await clear_trash_list(trash_list)
                remove_master_process(process_id)
                return

################Start####################
@Client.on_message(filters.command('start'))
async def startmsg(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
    text = f"Hi {message.from_user.mention(style='md')}, I Am Alive."
    await client.send_message(chat_id=user_id,
                                text=text,reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        f'⭐ Bot By 𝚂𝚊𝚑𝚒𝚕 ⭐',
                                        url='https://t.me/nik66')
                                ], [
                                    InlineKeyboardButton(
                                        f'❤ Join Channel ❤',
                                        url='https://t.me/nik66x')
                                ]]
                        ))
    return


################Time####################
@Client.on_message(filters.command(["time"]))
async def timecmd(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
    if userx in sudo_users:
        currentTime = get_readable_time(timex() - botStartTime)
        await client.send_message(chat_id=message.chat.id,
                                text=f'♻Bot Is Alive For {currentTime}')
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


##############Req######################
@Client.on_message(filters.command(["add"]))
async def add(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
    if userx not in sudo_users:
                await client.send_message(user_id, "❌Not Authorized")
                return
    vdata = {}
    q = 1
    while True:
            data = {}
            try:
                        ask = await client.ask(user_id, f'*️⃣ Send Me Video No. {str(q)}\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.video | filters.text))
                        video = ask.id
                        try:
                            if not ask.video or ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                        except:
                            pass
                        if ask.video or ask.document:
                            file_type = ask.video or ask.document
                            if file_type.mime_type.startswith("video/"):
                                data['chat'] = user_id
                                data['vid'] =  video
                        else:
                            continue
                        ask = await client.ask(user_id, f'*️⃣ Send Me Thumbnail For Video No. {str(q)}\n\n🔷Send `pass` for default Thumbnail\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.photo | filters.text))
                        thumb = ask.id
                        try:
                            if not ask.photo or ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                    else:
                                        data['thumb'] = False
                        except:
                            pass
                        if ask.photo or (ask.document and ask.document.mime_type.startswith("image/")):
                                data['thumb'] = True
                                data['tid'] =  thumb
                        else:
                            data['thumb'] = False
                        ask = await client.ask(user_id, f'*️⃣ If You Want To Remux Subitle To This Video, Send Subtitle File or If  You Dont Want To Remux Send `pass`\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.text))
                        sub = ask.id
                        try:
                            if not ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                    else:
                                            data['sub'] = False
                                            vdata[q] = data
                                            q+=1
                                            continue
                        except:
                            pass
                        if ask.document:
                            file_type = ask.document
                            if not file_type.mime_type.startswith("video/"):
                                ask = await client.ask(user_id, f'*️⃣ Send Remux Type\n\n`softremove`  ,   `softmux`    ,   `hardmux`\n\nIf  You Dont Want To Remux Send `pass`\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=filters.text)
                                valid = ['softremove', 'softmux', 'hardmux']
                                if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                if ask.text == "pass":
                                            data['sub'] = False
                                if ask.text in valid:
                                        data['sub'] = True
                                        data['sid'] = sub
                                        data['smode'] = ask.text
                                else:
                                    data['sub'] = False
                        else:
                            data['sub'] = False
                        vdata[q] = data
                        q+=1
            except Exception as e:
                    print(e)
                    await client.send_message(user_id, "🔃Tasked Has Been Cancelled.")
                    break
            await ask.request.delete()
    caption=f"🧩Total Files: {str(q-1)}"
    zxx = open('Nik66Bots.txt', "w", encoding="utf-8")
    zxx.write(str(vdata))
    zxx.close()
    await client.send_document(chat_id=user_id, document='Nik66Bots.txt', caption=caption)
    return


##########WaterMark Adder############
@Client.on_message(filters.command('addwatermark'))
async def addwatermark(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        watermark_path = f'./{str(userx)}_watermark.jpg'
        watermark_check = await check_filex(watermark_path)
        if not watermark_check:
                await bot.send_message(user_id, "❗No Watermark Found, Save Watermark First With /watermark Command.")
                return
        if userx in sudo_users:
                muxing_type = 'Watermark'
                await processor(bot, message,muxing_type)
                return
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return
        

###########Hard Muxing#################
@Client.on_message(filters.command('hardmux'))
async def hardmuxvideo(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        if userx in sudo_users:
                muxing_type = 'HardMux'
                await processor(bot, message,muxing_type)
                return
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return

###########Soft Muxing#################
@Client.on_message(filters.command('softmux'))
async def softmuxvideo(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        if userx in sudo_users:
                muxing_type = 'SoftMux'
                await processor(bot, message,muxing_type)
                return
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return

###########SoftRe Muxing#################
@Client.on_message(filters.command('softremux'))
async def softremuxvideo(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        if userx in sudo_users:
                muxing_type = 'SoftReMux'
                await processor(bot, message,muxing_type)
                return
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return

###########Compress Video#################
@Client.on_message(filters.command('compress'))
async def compressvideo(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        if userx in sudo_users:
                muxing_type = 'Compressing'
                await processor(bot, message,muxing_type)
                return
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return


############Split###############
@Client.on_message(filters.command('split'))
async def split(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        if userx in sudo_users:
                reply = await bot.send_message(user_id, "splitting video")
                out_files = await split('o.mkv')
                mptime = timex()
                modes = {'files': 1, 'process_id': '123'}
                for file in out_files:
                        cc = f"{str(file)}"
                        duration = durationx(file)
                        final_thumb = "./thumb.jpg"
                        start_time = timex()
                        datam = (file, '🔼Uploading Video', '𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍', mptime)
                        upload = await send_tg_video(bot, user_id, file, cc, duration, final_thumb, reply, start_time, datam, modes)
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return

###############start remux##############

@Client.on_message(filters.command('process'))
async def process(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
        watermark_path = f'./{str(userx)}_watermark.jpg'
        watermark_check = await check_filex(watermark_path)
        if not watermark_check:
                await bot.send_message(user_id, "❗No Watermark Found, Save Watermark First With /watermark Command.")
                return
        if userx in sudo_users:
                try:
                                file_id = int(message.reply_to_message.id)
                                filetype = message.reply_to_message.document
                except:
                        try:
                                ask = await bot.ask(user_id, '*️⃣ Send Bot Dict File', timeout=60, filters=filters.document)
                                filetype = ask.document
                        except:
                                await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                                return
                        file_id = ask.id
        else:
                await bot.send_message(user_id, "❌Not Authorized")
                return
        try:
                file_size = filetype.file_size
                if int(file_size)>512000:
                        await bot.send_message(chat_id=user_id, text="❌Invalid File")
                        return
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=user_id,
                text=f"❗Error: {str(e)}")
            return
        m = await bot.get_messages(user_id, file_id, replies=0)
        DEFAULT_DOWNLOAD_DIR = f"./{str(user_id)}_ongoing_dict.txt"
        await bot.download_media(m, DEFAULT_DOWNLOAD_DIR)
        users_open1 = open(DEFAULT_DOWNLOAD_DIR, 'r', encoding="utf-8")
        dic = eval(str(users_open1.read()))
        users_open1.close()
        dvalue = 'File'
        dvaluex = 'Files'
        try:
                m0 = await bot.ask(user_id, f'*️⃣ {str(len(dic))} {dvaluex} Found. Where You Want To Start Process Out Of These {str(len(dic))} {dvaluex}❔\n\n🔘Quick Notes:\n\n🔸Send 3-8 If You Want To Process From {dvalue} No. 3 To {dvalue} No. 8\n🔸Send 3- If You Want To Process Only {dvalue} No. 3\n🔸Send 3 If You Want To Process From {dvalue} No. 3 To Last {dvalue}', timeout=90, filters=filters.text)
                m0_text = m0.text
                if '-' in m0_text:
                        limiter = m0_text.split("-")
                        if len(limiter)>2:
                                await bot.send_message(user_id, "❗Invalied Values.")
                                return
                        try:
                                limit = int(limiter[0]) - 1
                                if len(limiter[1])==0:
                                        limit_to = int(limiter[0])
                                else:
                                        limit_to = int(limiter[1])
                        except:
                                await bot.send_message(user_id, "❗Invalied Values.")
                                return
                else:        
                        try:
                                limit = int(m0_text) - 1
                                if limit<0:
                                        limit = 0
                                limit_to = len(dic)
                        except ValueError:
                                await m.reply('❗Error: Value Must Be Numerical.')
                                return
        except:
                await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                return
        if limit_to>len(dic):
                await bot.send_message(user_id, "❗Invalied Values.")
                return
        
        countx = 1
        failed = {}
        wfailed = {}
        mfailed = {}
        cancelled = {}
        process_id = str(''.join(choices(ascii_lowercase + digits, k=10)))
        append_master_process(process_id)
        mtime = timex()
        Ddir = f'./{str(userx)}_RAW'
        Wdir = f'./{str(userx)}_WORKING'
        await make_direc(Ddir)
        await make_direc(Wdir)
        MCancel = False
        SCancel = False
        for i in range(limit, limit_to):
                trash_list = []
                if process_id in get_master_process():
                                stime = timex()
                                send_file = False
                                subprocess_id = str(''.join(choices(ascii_lowercase + digits, k=10)))
                                append_sub_process(subprocess_id)
                                remnx = str((limit_to-limit)-countx)
                                value = i+1
                                data = dic[value]
                                vid = data['vid']
                                chat_id = data['chat']
                                m = await bot.get_messages(chat_id, vid, replies=0)
                                media = get_media(m)
                                file_name = media.file_name.replace(' ', '')
                                dl_loc = f'{Ddir}/{str(userx)}_{str(file_name)}'
                                start_time = timex()
                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading Video', '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                reply = await bot.send_message(chat_id=user_id,
                                                        text=f"🔽Starting Download ({str(countx)}/{str(limit_to-limit)})\n🎟️File: {file_name}\n🧶Remaining: {str(remnx)}")
                                the_media = None
                                try:
                                        the_media = await bot.download_media(
                                                        message=m,
                                                        file_name=dl_loc,
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                )
                                except FloodWait as e:
                                                await asynciosleep(int(e.value)+10)
                                                the_media = await bot.download_media(
                                                        message=m,
                                                        file_name=dl_loc,
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                )
                                except Exception as e:
                                                await bot.send_message(chat_id=user_id,
                                                        text=f"❗Unable to Download Media!\n\n{str(e)}\n\n{str(data)}")
                                                await delete_trash(the_media)
                                                failed[value] = data
                                                try:
                                                        await reply.delete()
                                                except:
                                                        pass
                                                continue
                                trash_list.append(the_media)
                                if subprocess_id not in get_sub_process():
                                                                                SCancel = True
                                                                                cancelled[value] = data
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                await bot.send_message(chat_id=user_id, text=f"🔒Video Skipped By User\n\n{str(file_name)}")
                                                                                continue
                                if process_id not in get_master_process():
                                                                                MCancel = True
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                break
                                if the_media is None:
                                        await delete_trash(the_media)
                                        await bot.send_message(chat_id=user_id,
                                                        text=f"❗Unable to Download Media!")
                                        failed[value] = data
                                        try:
                                                        await reply.delete()
                                        except:
                                                        pass
                                        continue
                                duration = 0
                                try:
                                        duration = int(durationx(the_media))
                                except:
                                        pass
                                output_vid = f"{Wdir}/{str(userx)}_{str(file_name)}"
                                progress = f"{Wdir}/{str(userx)}_{str(file_name)}_progress.txt"
                                await create_process_file(progress)
                                await delete_trash(output_vid)
                                preset = USER_DATA()[userx]['watermark']['preset']
                                watermark_position = USER_DATA()[userx]['watermark']['position']
                                watermark_size = USER_DATA()[userx]['watermark']['size']
                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🛺Adding Watermark', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                output_vid_res = await vidmarkx(the_media, reply, progress, watermark_path, output_vid, duration, preset, watermark_position, watermark_size, datam,subprocess_id, process_id)
                                trash_list.append(output_vid)
                                await delete_trash(progress)
                                if output_vid_res[0]:
                                        if output_vid_res[1]:
                                                if subprocess_id not in get_sub_process():
                                                                SCancel = True
                                                                cancelled[value] = data
                                                                await clear_trash_list(trash_list)
                                                                try:
                                                                                        await reply.delete()
                                                                except:
                                                                                        pass
                                                                await bot.send_message(chat_id=user_id, text=f"🔒Video Skipped By User\n\n{str(file_name)}")
                                                                continue
                                                if process_id not in get_master_process():
                                                                MCancel = True
                                                                await clear_trash_list(trash_list)
                                                                try:
                                                                        await reply.delete()
                                                                except:
                                                                        pass
                                                                break
                                        send_file = True
                                        final_video = output_vid
                                        WP = True
                                        cc = f"{str(file_name)}\n\n✅watermark"
                                else:
                                        captionx=f"{str(file_name)}\n\n❌Failed To Add Watermark"
                                        wfail_file = f'{str(file_name)}_wlog.txt'
                                        zxx = open(wfail_file, "w", encoding="utf-8")
                                        zxx.write(str(output_vid_res[1]))
                                        zxx.close()
                                        await bot.send_document(chat_id=user_id, document=wfail_file, caption=captionx)
                                        print("⛔Watermark Adding Failed")
                                        await delete_trash(wfail_file)
                                        wfailed[value] = data
                                        output_vid = the_media
                                        WP = False
                                        cc = f"{str(file_name)}\n\n❌watermark"
                                if data['sub']:
                                        print("🔶Muxing Found")
                                        sid = data['sid']
                                        subm = await bot.get_messages(chat_id, sid, replies=0)
                                        media = get_media(subm)
                                        sub_name = media.file_name.replace(' ', '')
                                        sub_loc = f'{Ddir}/{str(userx)}_{str(sub_name)}'
                                        start_time = timex()
                                        datam = (sub_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading Subtitle',  '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                        subtitle = await bot.download_media(
                                                        message=subm,
                                                        file_name=sub_loc,
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                )
                                        if subtitle is None:
                                                await delete_trash(subtitle)
                                                await bot.send_message(chat_id=user_id,
                                                        text=f"❗Unable to Download Subtitle!\n\n{str(data)}")
                                                mfailed[value] = data
                                                if WP:
                                                                cc = f"{str(file_name)}\n\n✅watermark\n❌{str(sub_mode)}"
                                                else:
                                                                cc = f"{str(file_name)}\n\n❌watermark\n❌{str(sub_mode)}"
                                        else:
                                                trash_list.append(subtitle)
                                                sub_mode = data['smode']
                                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🎮Remuxing Subtitles', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                                remux_preset =  USER_DATA()[userx]['muxer']['preset']
                                                await create_process_file(progress)
                                                if sub_mode=="softremove":
                                                        mux_output = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(sub_mode)}).mkv"
                                                        mux_res = await softremove_vidx(output_vid, sub_loc, mux_output, reply, subprocess_id, remux_preset, duration, progress, process_id, datam)
                                                elif sub_mode=="softmux":
                                                        mux_output = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(sub_mode)}).mkv"
                                                        mux_res = await softmux_vidx(output_vid, sub_loc, mux_output, reply, subprocess_id, remux_preset, duration, progress, process_id, datam)
                                                elif sub_mode=="hardmux":
                                                        mux_output = f"{Wdir}/{str(userx)}_{str(file_name)}_({str(sub_mode)}).mp4"
                                                        mux_res = await hardmux_vidx(output_vid, sub_loc, mux_output, reply, subprocess_id, remux_preset, duration, progress, process_id, datam)
                                                if mux_res[0]:
                                                        if mux_res[1]:
                                                                if subprocess_id not in get_sub_process():
                                                                                SCancel = True
                                                                                cancelled[value] = data
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                await bot.send_message(chat_id=user_id, text=f"🔒Video Skipped By User\n\n{str(file_name)}")
                                                                                continue
                                                                if process_id not in get_master_process():
                                                                                MCancel = True
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                break
                                                        final_video = mux_output
                                                        trash_list.append(mux_output)
                                                        send_file = True
                                                        if WP:
                                                                cc = f"{str(file_name)}\n\n✅watermark\n✅{str(sub_mode)}"
                                                        else:
                                                                cc = f"{str(file_name)}\n\n❌watermark\n✅{str(sub_mode)}"
                                                else:
                                                        captionx=f"{str(file_name)}\n\n❌Failed To {str(sub_mode)}"
                                                        sfail_file = f'{str(file_name)}_slog.txt'
                                                        zxx = open(sfail_file, "w", encoding="utf-8")
                                                        zxx.write(str(mux_res[1]))
                                                        zxx.close()
                                                        await bot.send_document(chat_id=user_id, document=sfail_file, caption=captionx)
                                                        print("⛔Muxing Failed")
                                                        await delete_trash(sfail_file)
                                                        await delete_trash(subtitle)
                                                        await delete_trash(mux_output)
                                                        final_video = output_vid
                                                        mfailed[value] = data
                                                        if WP:
                                                                cc = f"{str(file_name)}\n\n✅watermark\n❌{str(sub_mode)}"
                                                        else:
                                                                cc = f"{str(file_name)}\n\n❌watermark\n❌{str(sub_mode)}"
                                if send_file:
                                        print("🔶Sending Video")
                                        if data['thumb']:
                                                thumb_id = data['tid']
                                                thumbm = await bot.get_messages(chat_id, thumb_id, replies=0)
                                                media = get_media(thumbm)
                                                thumb_name = media.file_name.replace(' ', '')
                                                thumb_loc = f'{Ddir}/{str(userx)}_{thumb_name}'
                                                start_time = timex()
                                                datam = (thumb_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading Thumbnail',  '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                                thumbnail = await bot.download_media(
                                                                message=thumbm ,
                                                                file_name=thumb_loc,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                        )
                                                if thumbnail is None:
                                                        final_thumb = './thumb.jpg'
                                                else:
                                                        final_thumb = thumb_loc
                                                        trash_list.append(thumb_loc)
                                        else:
                                                        final_thumb = './thumb.jpg'
                                        datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔼Uploadinig Video', '𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍', stime, mtime, len(failed), len(cancelled), len(wfailed), len(mfailed))
                                        print(final_thumb)
                                        print(final_video)
                                        if getsize(final_video)<2094000000:
                                                sendx = await send_tg_video(bot, user_id, final_video, cc, duration, final_thumb, reply, start_time, subprocess_id, process_id, datam)
                                        else:
                                                user_reply = await USER.send_message(chat_id=user_id,
                                                        text=f"🔶File Size Greater Than 2GB, Using User Account To Upload.")
                                                sendx = await send_tg_video(USER, user_id, final_video, cc, duration, final_thumb, user_reply, start_time, subprocess_id, process_id, datam)
                                                await user_reply.delete()
                                        if not sendx[0]:
                                                await bot.send_message(chat_id=user_id,
                                                        text=f"❗Unable to Upload Media!\n\n{str(sendx[1])}\n\n{str(data)}")
                                                failed[value] = data
                                        if subprocess_id not in get_sub_process():
                                                                                SCancel = True
                                                                                cancelled[value] = data
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                await bot.send_message(chat_id=user_id, text=f"🔒Video Skipped By User\n\n{str(file_name)}")
                                                                                continue
                                        if process_id not in get_master_process():
                                                                                MCancel = True
                                                                                await clear_trash_list(trash_list)
                                                                                try:
                                                                                        await reply.delete()
                                                                                except:
                                                                                        pass
                                                                                break
                                await clear_trash_list(trash_list)
                                try:
                                        await reply.delete()
                                except:
                                        pass
                else:
                        MCancel = True
                        try:
                                await reply.delete()
                        except:
                                pass
                        break
        try:
                await reply.delete()
        except:
                pass
        await delete_all(Ddir)
        await delete_all(Wdir)
        fstats = f"❗Failed: {str(len(failed))}\n🚫Cancelled: {str(len(cancelled))}\n🤒FWatermark: {str(len(wfailed))}\n😬FMuxing: {str(len(mfailed))}"
        if MCancel:
                await bot.send_message(chat_id=user_id,
                                                text=f"🔒Task Cancelled By User\n\n{str(fstats)}")
        else:
                await bot.send_message(chat_id=user_id,
                                                text=f"✅Task Completed\n\n{str(fstats)}")
        return



################Cancel Process###########
@Client.on_message(filters.command(["cancel"]))
async def cancell(client, message):
  user_id = message.chat.id
  userx = message.from_user.id
  if userx not in USER_DATA():
            await new_user(userx)
  if userx in sudo_users:
        if len(message.command)==3:
                processx = message.command[1]
                process_id = message.command[2]
                try:
                        if processx=='sp':
                                        remove_sub_process(process_id)
                                        await client.send_message(chat_id=user_id,
                                                        text=f'✅Successfully Cancelled.')
                        elif processx=='mp':
                                        remove_master_process(process_id)
                                        await client.send_message(chat_id=user_id,
                                                        text=f'✅Successfully Cancelled.')
                except Exception as e:
                        await client.send_message(chat_id=user_id,
                                        text=f'❗No Running Processs With This ID')
                return
        else:
                await client.send_message(chat_id=user_id,
                                        text=f'❗Give Me Process ID To Cancel.')
  else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


##############Setting################
@Client.on_message(filters.command(["settings"]))
async def settings(client, message):
                user_id = message.chat.id
                userx = message.from_user.id
                if userx not in USER_DATA():
                        await new_user(userx)
                if userx not in sudo_users:
                                await client.send_message(user_id, "❌Not Authorized")
                                return
                watermark_position = USER_DATA()[userx]['watermark']['position']
                watermark_size = USER_DATA()[userx]['watermark']['size']
                watermark_preset = USER_DATA()[userx]['watermark']['preset']
                muxer_preset = USER_DATA()[userx]['muxer']['preset']
                compress_preset = USER_DATA()[userx]['compress']['preset']
                select_stream = USER_DATA()[userx]['select_stream']
                stream = USER_DATA()[userx]['stream']
                split_video = USER_DATA()[userx]['split_video']
                split = USER_DATA()[userx]['split']
                positions = {'Set Top Left':"position_5:5", "Set Top Right": "position_main_w-overlay_w-5:5", "Set Bottom Left": "position_5:main_h-overlay_h", "Set Bottom Right": "position_main_w-overlay_w-5:main_h-overlay_h-5"}
                sizes = [5,7,10,13,15,17,20,25,30,35,40,45]
                pkeys = list(positions.keys())
                KeyBoard = []
                watermark_path = f'./{str(userx)}_watermark.jpg'
                watermark_check = await check_filex(watermark_path)
                if watermark_check:
                        key = [InlineKeyboardButton(f"🔶Watermark - Found✅🔶", callback_data="lol-water")]
                else:
                        key = [InlineKeyboardButton(f"🔶Watermark - Not Found❌🔶", callback_data="lol-water")]
                KeyBoard.append(key)
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Position - {wpositions[watermark_position]}🔶", callback_data="lol-wposition")])
                WP1 = []
                WP2 = []
                zx = 1
                for z in pkeys:
                    s_position = positions[z].replace('position_', '')
                    if s_position !=watermark_position:
                            datam = z
                    else:
                        datam = f"{str(z)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=str(positions[z]))
                    if zx<3:
                        WP1.append(keyboard)
                    else:
                        WP2.append(keyboard)
                    zx+=1
                KeyBoard.append(WP1)
                KeyBoard.append(WP2)
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Size - {str(watermark_size)}%🔶", callback_data="lol-wsize")])
                WS1 = []
                WS2 = []
                WS3 = []
                zz = 1
                for x in sizes:
                    vlue = f"size_{str(x)}"
                    if int(watermark_size)!=int(x):
                        datam = f"{str(x)}%"
                    else:
                        datam = f"{str(x)}% 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    if zz<5:
                            WS1.append(keyboard)
                    elif zz<9:
                            WS2.append(keyboard)
                    else:
                            WS3.append(keyboard)
                    zz+=1
                KeyBoard.append(WS1)
                KeyBoard.append(WS2)
                KeyBoard.append(WS3)
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Preset - {watermark_preset}🔶", callback_data="lol-wpset")])
                presets = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
                WX1 = []
                WX2 = []
                WX3 = []
                zz = 1
                for pp in presets:
                    if watermark_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'wpreset_{str(pp)}')
                    if zz<4:
                            WX1.append(keyboard)
                    elif zz<7:
                            WX2.append(keyboard)
                    else:
                            WX3.append(keyboard)
                    zz+=1
                KeyBoard.append(WX1)
                KeyBoard.append(WX2)
                KeyBoard.append(WX3)
                KeyBoard.append([InlineKeyboardButton(f"🔶Muxer Preset - {muxer_preset}🔶", callback_data="lol-mpset")])
                MP1 = []
                MP2 = []
                MP3 = []
                zz = 1
                for pp in presets:
                    if muxer_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'mpreset_{str(pp)}')
                    if zz<4:
                            MP1.append(keyboard)
                    elif zz<7:
                            MP2.append(keyboard)
                    else:
                            MP3.append(keyboard)
                    zz+=1
                KeyBoard.append(MP1)
                KeyBoard.append(MP2)
                KeyBoard.append(MP3)
                KeyBoard.append([InlineKeyboardButton(f"🔶Compress Preset - {compress_preset}🔶", callback_data="lol-cpset")])
                cp1 = []
                cp2 = []
                cp3 = []
                zz = 1
                for pp in presets:
                    if compress_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'cpreset_{str(pp)}')
                    if zz<4:
                            cp1.append(keyboard)
                    elif zz<7:
                            cp2.append(keyboard)
                    else:
                            cp3.append(keyboard)
                    zz+=1
                KeyBoard.append(cp1)
                KeyBoard.append(cp2)
                KeyBoard.append(cp3)
                streams = [True, False]
                KeyBoard.append([InlineKeyboardButton(f"🔶Select Stream - {str(select_stream)}🔶", callback_data="lol-sstream")])
                st = []
                for x in streams:
                    vlue = f"sstream_{str(x)}"
                    if select_stream!=x:
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    st.append(keyboard)
                KeyBoard.append(st)
                streams = ['ENG', 'HIN']
                KeyBoard.append([InlineKeyboardButton(f"🔶Auto Select Stream - {str(stream)}🔶", callback_data="lol-sstream")])
                st = []
                for x in streams:
                    vlue = f"autostream_{str(x)}"
                    if stream!=x:
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    st.append(keyboard)
                KeyBoard.append(st)
                streams = [True, False]
                KeyBoard.append([InlineKeyboardButton(f"🔶Split Video - {str(split_video)}🔶", callback_data="lol-splitv")])
                st = []
                for x in streams:
                    vlue = f"splitvideo_{str(x)}"
                    if split_video!=x:
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    st.append(keyboard)
                KeyBoard.append(st)
                streams = ['2GB', '4GB']
                KeyBoard.append([InlineKeyboardButton(f"🔶Split Size - {str(split)}🔶", callback_data="lol-splits")])
                st = []
                for x in streams:
                    vlue = f"splitsize_{str(x)}"
                    if split!=x:
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    st.append(keyboard)
                KeyBoard.append(st)
                await message.reply_text(
                        text="Settings",
                        disable_web_page_preview=True,
                        reply_markup= InlineKeyboardMarkup(KeyBoard)
                        )
                return

##############CRFS################
@Client.on_message(filters.command(["crf"]))
async def crf(client, message):
                user_id = message.chat.id
                userx = message.from_user.id
                if userx not in USER_DATA():
                        await new_user(userx)
                if userx not in sudo_users:
                                await client.send_message(user_id, "❌Not Authorized")
                                return
                compress_crf = USER_DATA()[userx]['compress']['crf']
                watermark_crf = USER_DATA()[userx]['watermark']['crf']
                muxer_crf = USER_DATA()[userx]['muxer']['crf']
                crfs = [0, 3, 6, 9, 12, 15, 18, 21, 23, 24, 27, 28, 30, 33, 36, 39, 42, 45, 48, 51]
                KeyBoard = []
                KeyBoard.append([InlineKeyboardButton(f"🔶WaterMark CRF - {watermark_crf}🔶", callback_data="lol-wcrf")])
                CCRP1 = []
                CCRP2 = []
                CCRP3 = []
                CCRP4 = []
                CCRP5 = []
                zz = 1
                for x in crfs:
                    vlue = f"wcrf_{str(x)}"
                    if int(watermark_crf)!=int(x):
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    if zz<5:
                            CCRP1.append(keyboard)
                    elif zz<9:
                            CCRP2.append(keyboard)
                    elif zz<13:
                            CCRP3.append(keyboard)
                    elif zz<17:
                        CCRP4.append(keyboard)
                    else:
                        CCRP5.append(keyboard)
                    zz+=1
                KeyBoard.append(CCRP1)
                KeyBoard.append(CCRP2)
                KeyBoard.append(CCRP3)
                KeyBoard.append(CCRP4)
                KeyBoard.append(CCRP5)
                KeyBoard.append([InlineKeyboardButton(f"🔶Muxer CRF - {muxer_crf}🔶", callback_data="lol-mcrf")])
                CCRP1 = []
                CCRP2 = []
                CCRP3 = []
                CCRP4 = []
                CCRP5 = []
                zz = 1
                for x in crfs:
                    vlue = f"mcrf_{str(x)}"
                    if int(muxer_crf)!=int(x):
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    if zz<5:
                            CCRP1.append(keyboard)
                    elif zz<9:
                            CCRP2.append(keyboard)
                    elif zz<13:
                            CCRP3.append(keyboard)
                    elif zz<17:
                        CCRP4.append(keyboard)
                    else:
                        CCRP5.append(keyboard)
                    zz+=1
                KeyBoard.append(CCRP1)
                KeyBoard.append(CCRP2)
                KeyBoard.append(CCRP3)
                KeyBoard.append(CCRP4)
                KeyBoard.append(CCRP5)
                KeyBoard.append([InlineKeyboardButton(f"🔶Compress CRF - {compress_crf}🔶", callback_data="lol-ccrp")])
                CCRP1 = []
                CCRP2 = []
                CCRP3 = []
                CCRP4 = []
                CCRP5 = []
                zz = 1
                for x in crfs:
                    vlue = f"ccrf_{str(x)}"
                    if int(compress_crf)!=int(x):
                        datam = f"{str(x)}"
                    else:
                        datam = f"{str(x)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    if zz<5:
                            CCRP1.append(keyboard)
                    elif zz<9:
                            CCRP2.append(keyboard)
                    elif zz<13:
                            CCRP3.append(keyboard)
                    elif zz<17:
                        CCRP4.append(keyboard)
                    else:
                        CCRP5.append(keyboard)
                    zz+=1
                KeyBoard.append(CCRP1)
                KeyBoard.append(CCRP2)
                KeyBoard.append(CCRP3)
                KeyBoard.append(CCRP4)
                KeyBoard.append(CCRP5)
                await message.reply_text(
                        text="Settings",
                        disable_web_page_preview=True,
                        reply_markup= InlineKeyboardMarkup(KeyBoard)
                        )
                return
        

########Save Watermark#######
@Client.on_message(filters.command('watermark'))
async def watermark(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
    if userx not in sudo_users:
                await client.send_message(user_id, "❌Not Authorized")
                return
    watermark_path = f'./{str(userx)}_watermark.jpg'
    watermark_check = await check_filex(watermark_path)
    if watermark_check:
                text = f"🔶Watermark Already Present\n\nSend Me New Watermark To Replace.\n\n⌛Request TimeOut In 30 Secs"
    else:
            text = f"🔷Watermark Not Present\n\nSend Me Watermark To Save.\n\n⌛Request TimeOut In 30 Secs"
    try:
        ask = await client.ask(user_id, text, timeout=30, filters=(filters.document | filters.photo))
        wt = ask.id
        if ask.photo or (ask.document and ask.document.mime_type.startswith("image/")):
                m = await client.get_messages(user_id, wt, replies=0)
                await client.download_media(m, watermark_path)
                await client.send_message(chat_id=user_id,
                                text=f"✅Watermark Saved Successfully")
        else:
                await client.send_message(chat_id=user_id,
                                        text=f"❗Invalid Media")
    except Exception as e:
                    print(e)
                    await client.send_message(user_id, "🔃Tasked Has Been Cancelled.")
    return


#########Renew _Bot#############
@Client.on_message(filters.command(["renew"]))
async def renew(_, message):
    userx = message.from_user.id
    if userx in sudo_users:
                inline_keyboard = []
                ikeyboard = []
                ikeyboard.append(
                    InlineKeyboardButton("Yes 🚫", callback_data=("renewme").encode("UTF-8"))
                )
                ikeyboard.append(
                    InlineKeyboardButton("No 😓", callback_data=("notdelete").encode("UTF-8"))
                )
                inline_keyboard.append(ikeyboard)
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                await message.reply_text(
                    "Are you sure?\n\n🚫 This will delete all your downloads and saved watermark locally 🚫",
                    reply_markup=reply_markup,
                    quote=True,
                )
                return
    else:
           await message.reply_text("❌Not Authorized", True)
           return
        
#########Restart Bot###########
@Client.on_message(filters.command("restart"))
async def restart(_, message):
    userx = message.from_user.id
    if userx in sudo_users:
        reply = await message.reply_text("♻Restarting...", True)
        await save_restart(message.chat.id, reply.id)
        execl(executable, executable, *argv)
