# -*- encoding: utf-8 -*-
from functools import partial
from pathlib import Path

from const import METAGPT_ROOT
from utils.yaml_model import YamlModel

USER_PERSONALIZED_REQUIREMENT_PROMPT = """
    {user_requirement}
    
    The data file locates in {data_file}
    This table is {table_desc}
    
    Follow this Guidelines
    - In the final response message do not provide technical details like code, table or column details, the response will be read by business user not technical person.
    - provide rich markdown response - if it is table data show it in markdown table format
    - At the last step, translate information generated into Chinese
    - Pay careful attention to the schema and table details I have provided below. Only use columns and tables mentioned in the schema details
    
    Here are column details:
{column_info}
    
    """

# table_info = YamlModel.read_yaml(Path(METAGPT_ROOT / "config/table_structure/bank_assessment_structure.yaml"))
# s = partial("{foo} {bar}".format, foo="FOO")
# user_personalized_prompt = partial(USER_PERSONALIZED_REQUIREMENT_PROMPT.format, table_desc=table_info["description"],
#                                    column_info="\n".join([f"    - {cc['column_name']}: {cc['description']}" for cc in
#                                                           table_info["columns"]]))
