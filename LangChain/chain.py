from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda

from utility.print_tokens import print_tokens

from .llm import get_local_llm, get_openai_llm
from .prompt import CV_EXTRACT_PROMPT, JOB_EXTRACT_PROMPT, MATCH_PROMPT



llm = get_local_llm()
json_parser = JsonOutputParser()
str_parser = StrOutputParser()



cv_match_chain = MATCH_PROMPT | llm | RunnableLambda(print_tokens("CV Match")) | str_parser
job_extract_chain = JOB_EXTRACT_PROMPT | llm |RunnableLambda(print_tokens("Job Extract")) | json_parser
cv_extract_chain = CV_EXTRACT_PROMPT | llm | RunnableLambda(print_tokens("CV Extract")) | json_parser



