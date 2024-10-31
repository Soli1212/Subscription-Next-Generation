# https://github.com/Soli1212
# Telegram: @Bigx4

from fastapi import FastAPI, Request, Query, Depends, status, HTTPException
from fastapi.responses import PlainTextResponse
from telethon import TelegramClient
from telethon.sessions import StringSession
from base64 import b64encode, b64decode
from json import loads, dumps
from re import findall
from dotenv import load_dotenv
from os import getenv
from io import BytesIO

# Load environment variables
load_dotenv()

# Environment variables
Session = getenv("Session")
ApiID = getenv("ApiID")
ApiHash = getenv("ApiHash")
AuthKey = getenv("AuthKey")

# Configuration settings
Conf = {
    "VlessRegEx": "(?:vless)://[^\s]+",
    "AllTypesRegEx": '''(?:vmess|vless|trojan|ss)://[^\s]+''',
    "Channels": """
        @ForExample
        @Example2
        @example3"""
}

# Initialize FastAPI app
app = FastAPI()

class ConfigWorker:

    @staticmethod
    def CheckBase64(encoded_str):
        try:
            decoded_bytes = b64decode(encoded_str, validate=True)
            return decoded_bytes.decode('utf-8')
        except:
            return False

    @staticmethod
    def DetectConfig(Txt: str):
        return findall(Conf["VlessRegEx"], Txt)

    @staticmethod
    def NameEditor(Config: str, NewName: str = "@Bigx4"):
        EditableConfig = Config
        SplitConfig = Config.split("://", -1)
        ConfigType = SplitConfig[0]
        ConfigData = SplitConfig[1]
        if X := ConfigWorker.CheckBase64(ConfigData):
            try:
                Data = loads(X)
                Data['ps'] = NewName
                Data = b64encode(dumps(Data).encode('utf-8')).decode('utf-8')
                EditableConfig = (ConfigType + "://" + Data).replace("\n", "")
            except:
                pass
        else:
            try:
                O = ConfigData.split("#", -1)
                O[1] = NewName
                EditableConfig = (ConfigType + "://" + "#".join(O)).replace("\n", "")
            except:
                pass
        return EditableConfig

# Authentication middleware
async def Auth(request: Request):
    key = request.query_params.get("key", None)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Auth key not available"
        )
    if (key == AuthKey):
        return True
    else:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid auth key"
        )

# Retrieve and process configurations
async def GetConfigs(LimitMsg: int = 15):
    DetectedConfigs = []
    for i in Conf["Channels"].split("\n"):
        try:
            Messages = client.iter_messages(
                entity = i,
                limit = LimitMsg,
            )
            Messages = "\n".join(
                [i.text async for i in Messages if i.text is not None]
            )
            for i in ConfigWorker.DetectConfig(Txt = Messages):
                DetectedConfigs.append(i)
        except:
            pass

    DetectedConfigs = list(dict.fromkeys(DetectedConfigs))
    DetectedConfigs.sort()
    return "\n\n".join(
        [ConfigWorker.NameEditor(Config=i) for i in DetectedConfigs]
    )

# Save configurations to a file and send it via Telegram
async def save_configs(Configs: str, user_id: str = "me"):
    file = BytesIO(Configs.encode('utf-8'))
    file.name = "Configs.txt"
    await client.send_file(
        entity = user_id,
        file = file,
        caption = '''https://github.com/Soli1212'''
    )

# Event handler for application startup
@app.on_event("startup")
async def on_startup():
    global client
    client = TelegramClient(
        StringSession(Session),
        api_id = ApiID,
        api_hash = ApiHash
    )
    await client.start()

# Main route to send configurations via Telegram
@app.get("/")
async def send_msg(
    auth: Auth = Depends(),
    limit: int = Query(default=15, ge=15, le=200),
):
    ReadyConfigs: GetConfigs = await GetConfigs(LimitMsg=limit)
    return PlainTextResponse(
        content=ReadyConfigs,
        status_code=200
    )

@app.get("/send")
async def send_config(
    auth: Auth = Depends(),
    limit: int = Query(default=15, ge=15, le=200),
    User: str = Query()
):
    ReadyConfigs: GetConfigs = await GetConfigs(LimitMsg=limit)
    try:
        await save_configs(Configs = ReadyConfigs, user_id = User)
        return True
    except:
        return False