# -*- encoding: utf-8 -*-

USER_PERSONALIZED_REQUIREMENT_PROMPT = """
    {user_requirement}
    
    The data file locates in {data_file}
    
    Follow this Guidelines
    - In the final response message do not provide technical details like code, table or column details, the response will be read by business user not technical person.
    - provide rich markdown response - if it is table data show it in markdown table format
    - At the last step, translate information generated into Chinese
    - Pay careful attention to the schema and table details I have provided below. Only use columns and tables mentioned in the schema details
    
    """

