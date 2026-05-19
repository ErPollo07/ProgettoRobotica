from dotenv import load_dotenv
import os

from src.shared.server_log import _log

# __file__ = src/shared/util.py
# dirname(__file__) = src/shared/
# dirname(dirname(__file__)) = src/
# poi scendi in flask_server/.env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # → src/
ENV_PATH = os.path.join(BASE_DIR, "flask_server", ".env")

load_dotenv(dotenv_path=ENV_PATH)


access_token_dict: dict[str, str] = {
    "1": str(os.getenv("ACCESS_TOKEN_1")),
    "2": str(os.getenv("ACCESS_TOKEN_2")),
    "3": str(os.getenv("ACCESS_TOKEN_3")),
}

server_ips: dict[str, str] = {
    "1": str(os.getenv("ROBOT_1_SERVER")),
    "2": str(os.getenv("ROBOT_2_SERVER")),
    "3": str(os.getenv("ROBOT_3_SERVER")),
}

port = str(os.getenv("PORT"))

server_number = str(os.getenv("SERVER_NUMBER"))

def retriveTelemetryLink(robotId: str):
    baseLink = str(os.getenv("TELEMETRY_LINK"))
    accessTok: str = str(access_token_dict.get(str(robotId)))
    link = baseLink + accessTok + "/telemetry"
    _log(f"[retriveTelemetryLink] {link=}")
    return link
