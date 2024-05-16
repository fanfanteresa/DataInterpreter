# -*- encoding: utf-8 -*-
import asyncio

from logs import logger
from data_interpreter import DataInterpreter
from utils.recovery_util import save_history


async def main(requirement: str = ""):
    configs = {
        "tools": ["report interpreting"]
    }
    di = DataInterpreter(**configs)
    rsp = await di.run(requirement)
    logger.info(rsp)
    save_history(role=di)


if __name__ == "__main__":
    # requirement = """
    #     Load the Banking Business Completion Rate Indicator Report in pandas dataframe format.
    #     The report is in excel format, and located in '/Users/chenliu/Desktop/cmb/yuanfang.xlsx'.
    #     Now please read this report, and output important statics, no need to do exploratory data analysis.
    # """
    requirement = """
        Read this report and output important statics.
    """
    asyncio.run(main(requirement))