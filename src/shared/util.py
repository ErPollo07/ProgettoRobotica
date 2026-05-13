from dotenv import load_dotenv
import os

from src.shared.server_log import _log

load_dotenv()

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


def retriveTelemetryLink(robotId: str):
    baseLink = str(os.getenv("TELEMETRY_LINK"))
    accessTok: str = str(access_token_dict.get(str(robotId)))
    link = baseLink + accessTok + "/telemetry"
    _log(f"[retriveTelemetryLink] {link=}")
    return link
