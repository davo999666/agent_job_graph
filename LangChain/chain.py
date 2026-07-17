from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

from utility.print_tokens import print_tokens

from .llm import get_llm
from .prompt import CV_EXTRACT_PROMPT, JOB_EXTRACT_PROMPT, MATCH_PROMPT



llm = get_llm()
parser = JsonOutputParser()



cv_match_chain = MATCH_PROMPT | llm | RunnableLambda(print_tokens("CV Match")) | parser
job_extract_chain = JOB_EXTRACT_PROMPT | llm |RunnableLambda(print_tokens("Job Extract")) | parser
cv_extract_chain = CV_EXTRACT_PROMPT | llm | RunnableLambda(print_tokens("CV Extract")) | parser



