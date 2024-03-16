import json
from http import HTTPStatus

import requests
from fastapi import APIRouter, Form
from starlette.responses import JSONResponse, Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from src.bot.bot import send_message
from src.core.config import settings

router = APIRouter()

@router.post("/chat")
async def chat(
        From: str = Form(...),
        Body: str = Form(...),
):

    send_message("+79320505025", "Boy")

    return "" # Response(content=str(response), media_type="application/xml")
