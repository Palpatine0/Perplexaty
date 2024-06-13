from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_exa import ExaSearchRetriever

from dotenv import load_dotenv
from langchain.callbacks.tracers.langchain import wait_for_all_tracers

load_dotenv()
wait_for_all_tracers()

retriever = ExaSearchRetriever(k = 3, highlights = True)
documents = retriever.invoke("Best time to visit Japan")


print(documents[0].page_content)

print(documents[0].metadata["highlights"])

print(documents[0].metadata["highlights"])
