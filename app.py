# -*- encoding: utf-8 -*-
import chainlit as cl

from logs import logger
from data_interpreter import DataInterpreter
from utils.recovery_util import save_history


@cl.on_chat_start
async def on_chat_start():
    configs = {
        "tools": ["report interpreting"]
    }
    di = DataInterpreter(**configs)
    cl.user_session.set("di", di)


@cl.on_message
async def on_message(message: cl.Message):
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="请上传数据文件，支持csv, excel", accept=[
                "text/csv"
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ]
        ).send()

    data_file = files[0].path

    files = None
    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="请上传prompt，支持yaml格式", accept=[
                "text/x-yaml",
                "text/yaml",
                "text/yml",
                "application/x-yaml",
                "application/yaml",
                "application/yml",
            ]
        ).send()

    structure_file = files[0].path

    bot = cl.user_session.get("di")

    msg = cl.Message(author="Assistant", content="")
    await msg.send()

    # step 1: user request and first response from the bot
    rsp = await bot.run(message.content, data_file, structure_file)
    logger.info(rsp)
    save_history(role=bot)
    # response_message = rsp
    # msg.content = response_message.content or ""
    msg.content = bot.planner.plan.tasks[-1].result or ""

    # pending message to be sent
    if len(msg.content) > 0:
        await msg.update()






