import discord
from discord.ext import tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다.
load_dotenv()

# 디스코드 클라이언트 설정
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# 봇 토큰
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 스케줄러 설정
scheduler = AsyncIOScheduler()

# 타겟 유저 ID와 메시지
target_user_id = int(os.getenv('TARGET_USER_ID'))
message_content = "테스트"

# 메시지를 보내는 작업을 정의합니다
async def send_scheduled_message():
    user = await client.fetch_user(target_user_id)
    await user.send(message_content)
    print(f"메시지를 {user.name}에게 보냈습니다: {message_content}")

# 봇이 준비되었을 때 실행될 작업을 정의합니다
@client.event
async def on_ready():
    print(f'봇이 로그인했습니다: {client.user}')
    # 매일 특정 시간에 메시지를 보내도록 스케줄링합니다. 여기서는 예시로 11:00 PM로 설정합니다.
    send_time = datetime.time(hour=23, minute=37, second=0)
    scheduler.add_job(send_scheduled_message, 'cron', hour=send_time.hour, minute=send_time.minute, second=send_time.second)
    scheduler.start()

# 봇 실행
client.run(TOKEN)
