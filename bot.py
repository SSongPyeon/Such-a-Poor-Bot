from random import randint
import discord # Imported from https://github.com/Rapptz/discord.py
import asyncio
import random
from discord.ext import commands



bot = discord.Client()
bot = commands.Bot(command_prefix='송편아 ', description="디스코드 송편 봇 made by 송편도사") #, pm_help = True)



@bot.event
@asyncio.coroutine
def on_ready():
    print('로그인 완료')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    bot.loop.create_task(status_task())
    bot.loop.create_task(send_message())

# help 지우기
bot.remove_command("help")    


# 플레이 중 바꾸기

async def status_task():
    while True:
        await bot.change_presence(game=discord.Game(name='송편봇 1.2 온라인!'))
        await asyncio.sleep(2)
        await bot.change_presence(game=discord.Game(name='송편아 도움 해봐'))
        await asyncio.sleep(4)

    


# 송편봇 고객센터 sp-bot

async def send_message():
    await bot.send_message(bot.get_channel('377830864140238848'), '***송편봇 온라인!***')






def is_me(m):
    return m.author == bot.user



def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



def roll_basic(a, b, modifier, threshold):
    results = ""
    base = randint(int(a), int(b))
    if (base + modifier) >= threshold:
        if modifier != 0:
            if modifier > 0:
                results += "**성공**: {}+{} [{}] meets or beats the {} threshold.".format(base, modifier, (base + modifier), threshold)
            else:
                results += "**성공**: {}{} [{}] does not meet the {} threshold.".format(base, modifier, (base + modifier), threshold)
        else:
            results += "**성공**: {}".format(base)
    else:
        if modifier != 0:
            if modifier > 0:
                results += "**실패**: {}+{} [{}]".format(base, modifier, (base + modifier))
            else:
                results += "**실패**: {}{} [{}]".format(base, modifier, (base + modifier))
        else:
            results += "**실패**: {}".format(base)
    return results



def roll_hit(num_of_dice, dice_type, hit, modifier, threshold):
    results = ""
    total = 0
    for x in range(0, int(num_of_dice)):
        y = randint(1, int(dice_type))
        if (int(hit) > 0):
            if (y >= int(hit)):
                results += "**{}** ".format(y)
                total += 1
            else:
                results += "{} ".format(y)
        else:
            results += "{} ".format(y)
            total += y
    total += int(modifier)
    if modifier != 0:
        if modifier > 0:
            results += "+{} = {}".format(modifier, total)
        else:
            results += "{} = {}".format(modifier, total)
    else:
        results += "= {}".format(total)
    if threshold != 0:
        if total >= threshold:
            results += " meets or beats the {} threshold. **성공**".format(threshold)
        else:
            results += " does not meet the {} threshold. **성공**".format(threshold)
    return results



    

# Parse !roll verbiage
@bot.command(pass_context=True,description='Rolls dice.\nExamples:\n100  Rolls 1-100.\n50-100  Rolls 50-100.\n3d6  Rolls 3 d6 dice and returns total.\nModifiers:\n! Hit success. 3d6!5 Counts number of rolls that are greater than 5.\nmod: Modifier. 3d6mod3 or 3d6mod-3. Adds 3 to the result.\n> Threshold. 100>30 returns success if roll is greater than or equal to 30.\n\nFormatting:\nMust be done in order.\nSingle die roll: 1-100mod2>30\nMultiple: 5d6!4mod-2>2')
@asyncio.coroutine
def 주사위(ctx, roll : str):
    a, b, modifier, hit, num_of_dice, threshold, dice_type = 0, 0, 0, 0, 0, 0, 0
    # author: Writer of discord message
    author = ctx.message.author
    if (roll.find('>') != -1):
        roll, threshold = roll.split('>')
    if (roll.find('mod') != -1):
        roll, modifier = roll.split('mod')
    if (roll.find('!') != -1):
        roll, hit = roll.split('!')
    if (roll.find('d') != -1):
        num_of_dice, dice_type = roll.split('d')
    elif (roll.find('-') != -1):
        a, b = roll.split('-')
    else:
        a = 1
        b = roll
    #Validate data
    try:
        if (modifier != 0):
            if (is_num(modifier) is False):
                raise ValueError("Modifier value format error. 올바른 사용법: 1d4+1")
                return
            else:
                modifier = int(modifier)
        if (hit != 0):
            if (is_num(hit) is False):
                raise ValueError("Hit value format error. 올바른 사용법: 3d6!5")
                return
            else:
                hit = int(hit)
        if (num_of_dice != 0):
            if (is_num(num_of_dice) is False):
                raise ValueError("주사위 포맷의 숫자 오류. 올바른 사용법: 3d6")
                return
            else:
                num_of_dice = int(num_of_dice)
        if (num_of_dice > 200):
            raise ValueError("주사위가 너무 많습니다. 200 이하로 해주세요.")
            return
        if (dice_type != 0):
            if (is_num(dice_type) is False):
                raise ValueError("주사위 종류 포맷 오류. 올바른 사용법: 3d6")
                return
            else:
                dice_type = int(dice_type)
        if (a != 0):
            if (is_num(a) is False):
                raise ValueError("오류: 최솟값은 숫자여야 합니다. 올바른 사용법: 1-50.")
                return
            else:
                a = int(a)
        if (b != 0):
            if (is_num(b) is False):
                raise ValueError("오류: 최댓값은 숫자여야 합니다. 올바른 사용법: 1-50 또는 50.")
                return
            else:
                b = int(b)
        if (threshold != 0):
            if (is_num(threshold) is False):
                raise ValueError("Error: Threshold must be a number. Proper usage 1-100>30")
                return
            else:
                threshold = int(threshold)
        if (dice_type != 0 and hit != 0):
            if (hit > dice_type):
                raise ValueError("오류: Hit value cannot be greater than dice type")
                return
            elif (dice_type < 0):
                raise ValueError("주사위 종류는 음수가 될 수 없습니다.")
                return
            elif (num_of_dice < 0):
                raise ValueError("주사위의 숫자는 음수가 될 수 없습니다.")
                return
        if a != 0 and b != 0:
            yield from bot.say("{} 가 {}부터 {}까지의 주사위를 굴렸습니다. 결과는? {}".format(author, a, b, roll_basic(a, b, modifier, threshold)))
        else:
            yield from bot.say("{} 가 {}부터 {}까지의 주사위를 굴렸습니다. 결과는? {}".format(author, num_of_dice, dice_type, roll_hit(num_of_dice, dice_type, hit, modifier, threshold)))
    except ValueError as err:
        #에러메시지 띄우기
        yield from bot.say(err)


        
# 입장 시각 확인

@bot.command(pass_context=True)
async def 입장(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    await bot.say('{0} 는 {0.joined_at} 에 입장했습니다.'.format(member))



# 봇 메시지 지우기

@bot.command(pass_context=True,description='.')
@asyncio.coroutine
def 너지워(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=100, check=is_me)
    yield from bot.send_message(channel, '{}개 지워써'.format(len(deleted)))


@bot.command(pass_context=True,description='.')
@asyncio.coroutine
def 지워(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=20)
    yield from bot.send_message(channel, '{}개 지워써'.format(len(deleted)))


@bot.command(pass_context=True,description='.')
@asyncio.coroutine
def 더지워(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=100)
    yield from bot.send_message(channel, '{}개 지워써'.format(len(deleted)))


@bot.command(pass_context=True,description='.')
@asyncio.coroutine
def 더욱더지워(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=200)
    yield from bot.send_message(channel, '{}개 지워써'.format(len(deleted)))


@bot.command(pass_context=True,description='.')
@asyncio.coroutine
def 조금만지워(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=10)
    yield from bot.send_message(channel, '지웠쪙'.format(len(deleted)))



# 봇으로 메시지 보내기

#async def send_message():
    #await client.send_message(client.get_channel('12324234183172'), 'ㅂㅇㄹ')


# 계산기

@bot.command()
async def 덧셈(left : int, right : int):
    await bot.say(left + right)

@bot.command()
async def 뺄셈(left : int, right : int):
    await bot.say(left - right)

@bot.command()
async def 곱셈(left : int, right : int):
    await bot.say(left * right)

@bot.command()
async def 나눗셈(left : int, right : int):
    await bot.say(left / right)




# 여기부터 커스텀 커맨드

@bot.command(aliases=['명령어', '커맨드', '헬프'])
async def 도움():
    embed=discord.Embed(title="[ 송편봇 명령어 모음 ]", decsription="모든 명령어는 송편아 로 시작합니다.", color=0xffff00)
    embed.add_field(name=고객센터, value="송편봇 고객센터 링크를 보여줌", inline=False)
    embed.add_field(name=지워, value="최대 20개의 메시지를 지움", inline=True)
    embed.add_field(name=너지워, value="송편봇의 메시지만 지움 (최대 100개)", inline=True)
    embed.add_field(name=더지워, value="최대 100개의 메시지를 지움", inline=True)
    embed.add_field(name=더욱더지워, value="최대 200개의 메시지를 지움", inline=True)
    embed.add_field(name=조금만지워, value="최대 10개의 메시지를 지움", inline=True)
    embed.add_field(name=입장, value="유저의 서버 입장 시각을 알려줌", inline=False)
    embed.add_field(name=주사위, value="주사위 게임을 할 수 있음. (사용 예시: 송편아 주사위 6)", inline=True)
    embed.set_footer(text="그 외 여러가지 재미있는 명령어들이 있습니다. 직접 찾아보세요!")
    await bot.say(embed=embed)



@bot.command(pass_context=True, aliases=['지원', '지원센터', '고객'])
async def 고객센터(ctx):
    await bot.say("https://discord.gg/6Ea3tta")

@bot.command(pass_context=True)
async def 버전(ctx):
    await bot.say("*송편봇 1.1*")

@bot.command(pass_context=True, aliases=['놀아줘', '놀자'])
async def 심심해(ctx):
    await bot.say("송편아 help 해봐! 모든 명령어를 볼 수 있어. 남용은 안 돼!")

@bot.command(pass_context=True)
async def 앙(ctx):
    await bot.say("기모띠")

@bot.command(pass_context=True, aliases=['ㅂㅇㄹ'])
async def 보이루(ctx):
    msg = ['ㅂㅇㄹ', '보이루']
    await bot.say("{}".format(random.choice(msg)))

@bot.command(pass_context=True, aliases=['송편', '송도'])
async def 송편도사(ctx):
    msg = ['**갓**', '나를 만든 사람', '유튜버 (http://ytsp.tk)', '마이 대디']
    await bot.say("{}".format(random.choice(msg)))

@bot.command(pass_context=True)
async def 너는(ctx):
    await bot.say("**갓**")

@bot.command(pass_context=True, aliases=['하이', '안뇽', 'ㅎㅇ', '반가워'])
async def 안녕(ctx):
    msg = ['ㅎㅇ', 'ㅎㅇㅎㅇ', '안뇽', 'ㅇㅇ ㅎㅇ', '어 안녕', '(꾸벅)']
    await bot.say("{}".format(random.choice(msg)))

@bot.command(pass_context=True, aliases=['유튭', 'youtube', '유투브', '유툽'])
async def 유튜브(ctx):
    await bot.say("http://ytsp.tk")
    
@bot.command(pass_context=True)
async def 잘가(ctx):
    msg = ['안 갈 건데', '안 갈 거야']
    await bot.say("{}".format(random.choice(msg)))

@bot.command(pass_context=True, aliases=['오늘어때', '기분어때'])
async def 어때(ctx):
    await bot.say("기분 좋아")

@bot.command(pass_context=True)
async def 사랑해(ctx):
    await bot.say("나두 :heart:")

@bot.command(pass_context=True)
async def 고마워(ctx):
    await bot.say("뭐가")

@bot.command(pass_context=True)
async def 좋아해(ctx):
    await bot.say("...... :heart:")

@bot.command(pass_context=True, aliases=['굿밤', '굿나잇', '잘자요'])
async def 잘자(ctx):
    msg = ['잘 자', '잘 자!', '굿나잇', '굿나잇!', '굿밤', '굿밤!']
    await bot.say("{}".format(random.choice(msg)))

@bot.command(pass_context=True, aliases=['명언은', '명언은?'])
async def 명언(ctx):
    await bot.say("송편이는 잘생겼다")

@bot.command(pass_context=True, aliases=['인정?', '인정하시나요?', '인죵?', 'ㅇㅈ', 'ㅇㅈ?'])
async def 인정(ctx):
    msg = ['와... 인정사정없이 인정해버리는 부분', '인지용 권지용', '인G용 권G용', '어 인정', '어 인죵']
    await bot.say("{}".format(random.choice(msg)))



@bot.command(pass_context=True)
async def 어른(ctx):
    await bot.say("어~린이~")

@bot.command(pass_context=True)
async def 오징(ctx):
    await bot.say("어~볶음~")

@bot.command(pass_context=True)
async def 고등(ctx):
    await bot.say("어~조림~")
    
@bot.command(pass_context=True)
async def 양파(ctx):
    await bot.say("어~니언~")

@bot.command(pass_context=True)
async def 용비(ctx):
    await bot.say("어~천가~")

@bot.command(pass_context=True)
async def 동의(ctx):
    await bot.say("어~보감~")

@bot.command(pass_context=True)
async def 아빠(ctx):
    await bot.say("어~디가~")







bot.run('Mzc3MDgwMjMzOTYwMTQ0ODk3.DOHu4Q.AN0mNwnP224vStB0k1c6Ny0VLq8')
