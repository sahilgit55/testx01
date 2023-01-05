from requests import get
from bot.helper.code128 import code128_image
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from config import Config
from pyrogram import filters
from os import remove

khokha = Config.khokha
khokha_voterids = Config.voterids


def make_epic(text):
    width=2800
    height=500
    opacity=1
    black = (0,0,0)
    white = (255,255,255)
    transparent = (0,0,0,0)

    font = ImageFont.truetype('NotoSans-Bold.ttf',250)
    wm = Image.new('RGBA',(width,height),transparent)
    im = Image.new('RGBA',(width,height),transparent) # Change this line too.

    draw = ImageDraw.Draw(wm)
    w,h = draw.textsize(text, font)
    draw.text(((width-w)/2,(height-h)/2),text,black,font)

    en = ImageEnhance.Brightness(wm)
    #en.putalpha(mask)
    mask = en.enhance(1-opacity)
    im.paste(wm,(25,25),mask)
    return im


def epic_paste(background, frontImage):
    frontImage = frontImage.convert("RGBA")
    background = background.convert("RGBA")
    background.paste(frontImage, (850, 425), frontImage)
    return background


def text(draw, data, fnt, size, x, y):
    font = ImageFont.truetype(fnt, size=size)
    draw.text((x, y), data, font=font, fill =(0, 0, 0))
    return draw



def front_voter(epic_no, name1, name2, name3, name4, photo):
    im = code128_image(epic_no)
    size = 809, 150
    im_resized = im.resize(size, Image.ANTIALIAS)
    im1 = Image.open('1.png')
    image = im1.copy()
    image.paste(im_resized, (68, 474))
    size = 870, 1085
    im = Image.open(photo)
    im_resized = im.resize(size, Image.ANTIALIAS)
    curr_sharp = ImageEnhance.Sharpness(im_resized)
    new_sharp = 8.3
    img_sharped = curr_sharp.enhance(new_sharp)
    image.paste(img_sharped, (405, 664))
    epic_img = make_epic(epic_no)
    if len(epic_no)>10:
                size = 770, 170
                epic_img = epic_img.resize(size, Image.ANTIALIAS)
                image = epic_paste(image, epic_img)
    else:
                size = 850, 170
                epic_img = epic_img.resize(size, Image.ANTIALIAS)
                image = epic_paste(image, epic_img)
    draw = ImageDraw.Draw(image)
    draw = text(draw, name1, "NotoSans-Medium.ttf", 75, 20, 1800)
    draw = text(draw, name2, "Roboto-Bold.ttf", 65, 20, 2000)
    draw = text(draw, name3, "NotoSans-Medium.ttf", 75, 20, 2200)
    draw = text(draw, name4, "Roboto-Bold.ttf", 65, 20, 2400)
    return image


def sign_paste(background, filename):
    frontImage = Image.open(filename)
    frontImage = frontImage.convert("RGBA")
    background = background.convert("RGBA")
    background.paste(frontImage, (900, 550), frontImage)
    return background


def back_voter(S1, gender, gender2, S6, S5, S4, S16, S3, S2, S13, S12, S11, S10, S8, S9, S7):
    image = Image.open('2.png')
    image = sign_paste(image, 'sign.png')
    draw = ImageDraw.Draw(image)
    draw = text(draw, S1, "NotoSans-SemiBold.ttf", 65, 40, 20)
    draw = text(draw, gender, "NotoSans-SemiBold.ttf", 65, 610, 20)
    if gender2 == "Female":
            draw = text(draw, gender2, "Roboto-Bold.ttf", 58, 988, 33)
    else:
          draw = text(draw, gender2, "Roboto-Bold.ttf", 58, 943, 33)
    draw = text(draw, S2, "Roboto-Bold.ttf", 58, 170, 33)
    draw =text(draw, S3, "NotoSans-SemiBold.ttf", 65, 40, 120)
    draw = text(draw, S16, "Roboto-Bold.ttf", 58, 610, 120)
    draw = text(draw, S4, "Roboto-Bold.ttf", 58, 40, 200)
    draw = text(draw, S5, "NotoSans-SemiBold.ttf", 65, 40, 320)
    draw = text(draw, S6, "Roboto-Bold.ttf", 55, 40, 420)
    draw = text(draw, S7, "NotoSans-SemiBold.ttf", 65, 710, 710)
    draw = text(draw, S9, "Roboto-Bold.ttf", 58, 730, 810)
    draw = text(draw, S8, "Roboto-Bold.ttf", 58, 40, 720)
    draw = text(draw, S10, "NotoSans-SemiBold.ttf", 65, 40, 930)
    draw = text(draw, S11, "Roboto-Bold.ttf", 58, 40, 1030)
    draw =  text(draw, S12, "NotoSans-SemiBold.ttf", 65, 40, 1160)
    draw = text(draw, S13, "Roboto-Bold.ttf", 58, 40, 1260)
    return image


def get_value(data, string):
                        try:
                            value = data['response']['docs'][0][string]
                            return value
                        except:
                            value = ''
                            return value


async def get_voter_card(client, user_id, url, village):
                    proc = await client.send_message(chat_id=user_id,
                                    text="⌛Making Request, Please Wait........")
                    try:
                        data = get(url).json()
                    except Exception as e:
                        await client.send_message(chat_id=user_id, text=f'❗Failed To Get Data From URL.\n\nError: {str(e)}')
                        await proc.delete()
                        return
                    epic_no = get_value(data, 'epic_no')
                    namex1 = get_value(data, 'name_v1')
                    namex2 = get_value(data, 'name')
                    namex3 = get_value(data, 'rln_name_v1')
                    namex4 = get_value(data, 'rln_name')
                    genderx = get_value(data, 'gender')
                    age = get_value(data, 'age')
                    relationtype = get_value(data, 'rln_type')
                    ac_no = get_value(data, 'ac_no')
                    ac_name_v1 = get_value(data, 'ac_name_v1')
                    ac_name = get_value(data, 'ac_name')
                    part_no = get_value(data, 'part_no')
                    part_name_v1 = get_value(data, 'part_name_v1')
                    part_name =  get_value(data, 'part_name')
                    
                    epic_data = False
                    if village=="khokha":
                            for key in khokha_voterids:
                                if epic_no in key:
                                    photo = f"./photo/{str(khokha[key][0])}"
                                    epic_data = str(khokha[key][1])
                                else:
                                    pass
                    if not epic_data:
                        await client.send_message(chat_id=user_id, text=f'❗No Saved Voter Data Found.')
                        await proc.delete()
                        return
                    hn = epic_data.split()
                    final_hn = False
                    for u in range(len(hn)):
                        try:
                            nox = hn[u]
                            hnox = int(nox)
                            if 'नं०' in hn[u-1]:
                                final_hn = hnox
                                break
                        except:
                            pass
                    DELETE = False
                    if not final_hn:
                        e_data = ''
                        for g in hn:
                            e_data = e_data + g + "\n"
                        try:
                                    ask = await client.ask(user_id, f'*️⃣Unable To Get The House Number, Send Me The House Number\n\n{str(e_data)}', timeout=60, filters=filters.text)
                                    result  = ask.text
                                    await proc.delete()
                                    DELETE = True
                                    try:
                                        await ask.request.delete()
                                        final_hn = int(result)
                                    except:
                                        await client.send_message(chat_id=user_id, text=f'❗Wrong House Number.')
                                        return
                        except:
                                    await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled. Start Deploying Again With /deploy.")
                                    await proc.delete()
                                    return
                        await ask.request.delete()
                    if not DELETE:
                        try:
                            await proc.delete()
                        except:
                            pass
                    name1 = f"नाम               :  {namex1}"
                    name2 = f"Name               :  {namex2}"
                    if relationtype=="H":
                                name3 = f"पति का नाम    :  {namex3}"
                                cname = f"पति का नाम : {namex3}"
                                name4 = f"Husband's Name  :   {namex4}"
                                cname2 = f"Husband's Name : {namex4}"
                    else:
                                name3 = f"पिता का नाम    :  {namex3}"
                                cname = f"पिता का नाम : {namex3}"
                                name4 = f"Father's Name  :   {namex4}"
                                cname2 = f"Father's Name : {namex4}"


                    if genderx=="M":
                        gender = ":          पुरुष/"
                        gender2 = "Male"
                    else:
                        gender = ":          महिला/"
                        gender2 = "Female"
                        
                    assembly_hindi = f"{str(ac_no)}-{ac_name_v1}"
                    assembly_english = f'{str(ac_no)}-{str(ac_name)}'

                    part_hindi = f"{str(part_no)}-{part_name_v1}"
                    part_eng = f"{str(part_no)}-{part_name}"


                    S1 = f"लिंग/"
                    S2 = f"SEX"

                    S3 = "जन्म तिथि/उम्र"
                    S4 = "Data of Birth/ Age"

                    if village=="khokha":
                                S5 = f'पता: म.नं. {str(final_hn)}, गांव-खोखा , तह-हिसार, जिला-हिसार'
                                S6 = f"Address : H.No. {str(final_hn)},VILL-KHOKHA ,TEH-HISAR,DIST-HISAR"
                    S7 = "निर्वाचक रजिस्ट्रीकरण अधिकारी"
                    S9 = "Electoral Registration Officer"
                    S10 = f"विधानसभा निर्वाचन क्षेत्र संख्या और नाम : {assembly_hindi}"
                    S11 = f"Assembly Constituency No. and Name : {assembly_english}"
                    S12 = f"भाग संख्या और नाम : {part_hindi}"
                    S13 = f"Part No. and Name : {part_eng}"
                    S16 = f":            {str(age)}"
                    proc = await client.send_message(chat_id=user_id,
                                    text="⌛Generating Voter Front, Please Wait........")
                    datetime_ist = datetime.now()
                    DATE = datetime_ist.strftime("%d-%m-%Y")
                    S8 = f"Date : {str(DATE)}"
                    front = front_voter(epic_no, name1, name2, name3, name4, photo).convert('RGB')
                    await proc.edit_text(text="⌛Generating Voter Back, Please Wait........")
                    back = back_voter(S1, gender, gender2, S6, S5, S4, S16, S3, S2, S13, S12, S11, S10, S8, S9, S7).convert('RGB')
                    await proc.edit_text(text="⌛Making PDF, Please Wait........")
                    image_list = [back]
                    voter_card_file = f'{str(namex2)}_Voter_Card.pdf'
                    front.save(voter_card_file, save_all=True, append_images=image_list)
                    caption = f"{str(epic_no)}\nनाम : {namex1}\nName : {namex2}\n{str(cname)}\n{str(cname2)}\nGender: {str(gender2)}\nAge: {str(age)}\nVillage: {str(part_name)}\nH.No. : {str(final_hn)}\nPart No. {str(part_no)}"
                    await client.send_document(chat_id=user_id, document=voter_card_file, caption=caption)
                    await proc.delete()
                    remove(voter_card_file)
                    return
                
                
async def get_custom_voter_card_all(client, user_id, genderx, namex4 , namex3, relationtype, namex2, namex1, epic_no, final_hn, part_no, age, photo,ac_no, ac_name_v1, ac_name,part_name_v1, part_name,villagename1, villagename, district_name1, district_name, tehshilname1, tehshil_name):
                    name1 = f"नाम               :  {namex1}"
                    name2 = f"Name               :  {namex2}"
                    if relationtype=="H":
                                name3 = f"पति का नाम    :  {namex3}"
                                cname = f"पति का नाम : {namex3}"
                                name4 = f"Husband's Name  :   {namex4}"
                                cname2 = f"Husband's Name : {namex4}"
                    else:
                                name3 = f"पिता का नाम    :  {namex3}"
                                cname = f"पिता का नाम : {namex3}"
                                name4 = f"Father's Name  :   {namex4}"
                                cname2 = f"Father's Name : {namex4}"


                    if genderx=="M":
                        gender = ":          पुरुष/"
                        gender2 = "Male"
                    else:
                        gender = ":          महिला/"
                        gender2 = "Female"
                        
                    assembly_hindi = f"{str(ac_no)}-{ac_name_v1}"
                    assembly_english = f'{str(ac_no)}-{str(ac_name)}'

                    part_hindi = f"{str(part_no)}-{part_name_v1}"
                    part_eng = f"{str(part_no)}-{part_name}"


                    S1 = f"लिंग/"
                    S2 = f"SEX"

                    S3 = "जन्म तिथि/उम्र"
                    S4 = "Data of Birth/ Age"

                    S5 = f'पता: म.नं. {str(final_hn)}, गांव-{villagename1} , तह-{tehshilname1}, जिला-{district_name1}'
                    S6 = f"Address : H.No. {str(final_hn)},VILL-{villagename} ,TEH-{tehshil_name},DIST-{district_name}"
                    S7 = "निर्वाचक रजिस्ट्रीकरण अधिकारी"
                    S9 = "Electoral Registration Officer"
                    S10 = f"विधानसभा निर्वाचन क्षेत्र संख्या और नाम : {assembly_hindi}"
                    S11 = f"Assembly Constituency No. and Name : {assembly_english}"
                    S12 = f"भाग संख्या और नाम : {part_hindi}"
                    S13 = f"Part No. and Name : {part_eng}"
                    S16 = f":            {str(age)}"
                    proc = await client.send_message(chat_id=user_id,
                                    text="⌛Generating Voter Front, Please Wait........")
                    datetime_ist = datetime.now()
                    DATE = datetime_ist.strftime("%d-%m-%Y")
                    S8 = f"Date : {str(DATE)}"
                    front = front_voter(epic_no, name1, name2, name3, name4, photo).convert('RGB')
                    await proc.edit_text(text="⌛Generating Voter Back, Please Wait........")
                    back = back_voter(S1, gender, gender2, S6, S5, S4, S16, S3, S2, S13, S12, S11, S10, S8, S9, S7).convert('RGB')
                    await proc.edit_text(text="⌛Making PDF, Please Wait........")
                    image_list = [back]
                    voter_card_file = f'{str(namex2)}_Voter_Card.pdf'
                    front.save(voter_card_file, save_all=True, append_images=image_list)
                    caption = f"{str(epic_no)}\nनाम : {namex1}\nName : {namex2}\n{str(cname)}\n{str(cname2)}\nGender: {str(gender2)}\nAge: {str(age)}\nVillage: {str(part_name)}\nH.No. : {str(final_hn)}\nPart No. {str(part_no)}"
                    await client.send_document(chat_id=user_id, document=voter_card_file, caption=caption)
                    await proc.delete()
                    remove(voter_card_file)
                    remove(photo)
                    return

