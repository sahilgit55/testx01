from pyrogram import Client,  filters
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, USER_DATA, get_media, timex, delete_all, delete_trash, new_user, create_process_file, make_direc, durationx, clear_trash_list, check_filex, save_restart
from helper_fns.pbar import progress_bar
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


############Variables##############
sudo_users = eval(Config.SUDO_USERS)
USER = Config.USER
wpositions = {'5:5': 'Top Left', 'main_w-overlay_w-5:5': 'Top Right', '5:main_h-overlay_h': 'Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Bottom Right'}


###########Send Video##############
async def send_tg_video(bot, user_id, final_video, cc, duration, final_thumb, reply, start_time, subprocess_id, process_id, datam):
                                        try:
                                                await bot.send_video(
                                                                chat_id=user_id,
                                                                video=final_video,
                                                                caption=cc,
                                                                supports_streaming=True,
                                                                duration=duration,
                                                                thumb=final_thumb,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                )
                                                return [True]
                                        except FloodWait as e:
                                                await asynciosleep(int(e.value)+10)
                                                await bot.send_video(
                                                                chat_id=user_id,
                                                                video=final_video,
                                                                caption=cc,
                                                                supports_streaming=True,
                                                                duration=duration,
                                                                thumb=final_thumb,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time, bot, subprocess_id, process_id, *datam)
                                                )
                                                return [True]
                                        except Exception as e:
                                                return [False, e]




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
                                        if getsize(final_video)<2093796556:
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
                positions = {'Set Top Left':"position_5:5", "Set Top Right": "position_main_w-overlay_w-5:5", "Set Bottom Left": "position_5:main_h-overlay_h", "Set Bottom Right": "position_main_w-overlay_w-5:main_h-overlay_h-5"}
                sizes = [5,7,10,13,15,17,20,25,30,35,40,45]
                pkeys = list(positions.keys())
                KeyBoard = []
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
                presets = ['ultrafast', 'veryfast']
                WP = []
                for pp in presets:
                    if watermark_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'wpreset_{str(pp)}')
                    WP.append(keyboard)
                KeyBoard.append(WP)
                KeyBoard.append([InlineKeyboardButton(f"🔶Muxer Preset - {muxer_preset}🔶", callback_data="lol-mpset")])
                MP = []
                for pp in presets:
                    if muxer_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'mpreset_{str(pp)}')
                    MP.append(keyboard)
                KeyBoard.append(MP)
                watermark_path = f'./{str(userx)}_watermark.jpg'
                watermark_check = await check_filex(watermark_path)
                if watermark_check:
                        key = [InlineKeyboardButton(f"🔶Watermark - Found✅🔶", callback_data="lol-water")]
                else:
                        key = [InlineKeyboardButton(f"🔶Watermark - Not Found❌🔶", callback_data="lol-water")]
                KeyBoard.append(key)
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