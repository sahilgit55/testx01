from asyncio import sleep as asynciosleep
from pyrogram.errors import FloodWait
from helper_fns.helper import hrb, getbotuptime, Timer, timex, get_readable_time, get_stats, process_checker
from helper_fns.process import get_sub_process, get_master_process


def get_progress_bar_string(current,total):
    completed = int(current) / 8
    total = int(total) / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 6
    p_str = '■' * cFull
    p_str += '□' * (16 - cFull)
    p_str = f"[{p_str}]"
    return p_str

timer = Timer(7)


async def progress_bar(current,total,reply,start, client, datam, modes):
      if modes['files']>1:
          process_id = modes['process_id']
          subprocess_id = modes['subprocess_id']
          check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
      else:
          process_id = modes['process_id']
          check_data = [[process_id, get_master_process()]]
      checker = await process_checker(check_data)
      if not checker:
          client.stop_transmission()
      if timer.can_send():
        now = timex()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            sp=str(hrb(speed))+"ps"
            tot=hrb(total)
            cur=hrb(current)
            progress = get_progress_bar_string(current,total)
            try:
                if modes['files']>1:
                    name = datam[0]
                    opt = datam[1]
                    remaining = datam[2]
                    process_name = datam[3]
                    mode = datam[4]
                    sub_time = datam[5]
                    mas_time = datam[6]
                    failed = datam[7]
                    cancelled = datam[8]
                    wfailed = datam[9]
                    mfailed = datam[10]
                    fstats = f"❗Failed: {str(failed)}\n🚫Cancelled: {str(cancelled)}\n🤒FWatermark: {str(wfailed)}\n😬FMuxing: {str(mfailed)}"
                    subprocess_time = get_readable_time(timex() - sub_time)
                    masterprocess_time = get_readable_time(timex() - mas_time)
                    bot_uptime = getbotuptime()
                    ctext = f"⛔Skip Video: `/cancel sp {str(subprocess_id)}`"
                    ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                    process_head = f"{str(process_name)} ({opt})\n🎟️File: {name}\n🧶Remaining: {str(remaining)}"
                    process_mid = f"🔸SP Time: {str(subprocess_time)}\n🔹MP Time: {str(masterprocess_time)}"
                    process_foot = f"♥️Bot Uptime: {str(bot_uptime)}\n{str(fstats)}\n{str(ctext)}\n{str(ptext)}"
                else:
                    name = datam[0]
                    process_name = datam[1]
                    mode = datam[2]
                    mas_time = datam[3]
                    masterprocess_time = get_readable_time(timex() - mas_time)
                    bot_uptime = getbotuptime()
                    process_head = f"{str(process_name)}\n🎟️File: {name}"
                    process_mid = f"🔹MP Time: {str(masterprocess_time)}"
                    ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                    process_foot = f"♥️Bot Uptime: {str(bot_uptime)}\n{str(ptext)}"
                pro_bar = f"{str(process_head)}\n\n\n {str(progress)}\n\n ┌ 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜:【 {perc} 】\n ├ 𝚂𝚙𝚎𝚎𝚍:【 {sp} 】\n ├ {mode}:【 {cur} 】\n └ 𝚂𝚒𝚣𝚎:【 {tot} 】\n\n\n{str(process_mid)}\n{str(get_stats())}\n{str(process_foot)}"
                await reply.edit(pro_bar)
            except FloodWait as e:
                    await asynciosleep(int(e.value)+10)
            except Exception as e:
                    print(e)