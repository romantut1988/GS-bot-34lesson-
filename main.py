import discord
import sqlite3

token = 'MTE2MjI1MTg0NDIyNDA0MTAzMA.G955H6.w4VDGjMuf3anDh3oMC7_muurCFCufFiUssu85w'

intents = discord.Intents.all()
client = discord.Client(intents=intents)


def checkCaps(text):
    count = 0
    for i in text:
        if i.isupper():
            count += 1
    if count > len(text) // 2:
        return True
    else:
        return False


def checkBadWords(text):
    bad_words = ['идиот', 'козел', 'дурак']
    words = text.split()
    for i in words:
        if i.lower() in bad_words:
            return True
    return False


def makeBanEmbed(author, reason):
    emb = discord.Embed(title='Нарушение правил', colour=discord.Color.dark_red())
    emb.set_author(name=author.name, icon_url=author.avatar_url)
    emb.add_field(name='Бан пользователя', value=f'Пользователь забанен за нарушение правил чата')
    emb.set_footer(text=f'Причина бана: {reason}')
    return emb


def makeLevelEmbed(author, lvl, exp, exp_to):
    emb = discord.Embed(title=f'Ваш уровень: {lvl}')
    emb.set_author(name=author.name, icon_url=author.avatar_url)
    emb.add_field(name=f'Ваш опыт: {exp} / {exp_to}', value=f'До следующего уровня осталось {exp_to - exp}')
    return emb


def executeScript(script):
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute(script)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    if result:
        return result[0]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'Привет' or message.content == 'Hello':
        await message.channel.send('Привет!')
    if message.content.startswith('$'):
        await message.channel.send('$$$')
    if message.content.isdigit():
        await message.channel.send(int(message.content) ** 2)
    # if message.content.isupper():
    #    await message.channel.send('Хватит писать капсом')
    words = message.content.split()
    for i in words:
        if i == 'деньги':
            await message.channel.send('Хватит писать про деньги')
        if i == 'море':
            await message.channel.send('Я тоже хочу на море')
    if message.author.id == 722366477516144740:
        if message.content == 'я':
            await message.channel.send('о это ты')
    if message.content.count('#') > len(message.content) // 3:
        await message.channel.send(f'{message.author.mention} слишком много решеток')
        await message.delete()
    if checkCaps(message.content):
        await message.channel.send(f'{message.author.mention} не злоупотребляй CAPS LOCK')
        await message.author.send('Ты злоупотреблял CAPS LOCK - поэтому тебя забанили')
        await message.author.ban(reason='Злоупотреблял CAPS LOCK')
    if checkBadWords(message.content):
        emb = makeBanEmbed(message.author, 'Использование запрещенных слов')
        try:
            await message.author.kick(reason='Использование запрещенных слов')
        except:
            print('не получилось забанить', message.author.name)
        await message.channel.send(embed=emb)


@client.event
async def on_ready():
    print(f'Зашел под именем {client.user}')
    channel = client.get_channel(1162251507727601699)
    # await channel.send(f'Hello! My name is {client.user}')
    executeScript(''' create table if not exists users
                      (id integer primary key autoincrement,
                      level integer, exp integer);''')
    # executeScript('insert into users values (722366477516144740, 0,0);')
    # print( executeScript('select * from users') )
    executeScript(''' create table if not exists expirience
                      (id integer primary key autoincrement, exp_to_level integer);''')


@client.event
async def on_member_join(member):
    print(f'Пользователь {member.name} присоединился к серверу')
    executeScript(f'insert into users values({member.id}, 0, 0)')


@client.event
async def on_member_remove(member):
    print(f'Пользователь {member.name} покинул сервер')
    executeScript(f'delete from users where id = {member.id}')


client.run(token)
