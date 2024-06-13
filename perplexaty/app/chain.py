from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_exa import ExaSearchRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
from langchain.callbacks.tracers.langchain import wait_for_all_tracers

load_dotenv()
wait_for_all_tracers()

retriever = ExaSearchRetriever(k = 3, highlights = True)

document_template = """
<source>
    <url>{url}</url>
    <highlights>{highlights}</highlights>
</source>
"""

document_prompt = PromptTemplate.from_template(document_template)

document_chain = RunnableLambda(
    lambda document: {
        "highlights": document.metadata["highlights"],
        "url": document.metadata["url"]
    }
) | document_prompt

retrieval_chain = retriever | document_chain.map() | (lambda docs: "\n".join([i.text for i in docs]))

system_template = "You are an expert research assistant. You use xml-formatted context to research people's questions."

human_template = """
Please answer the following query based on the provided context. Please cite your sources at the end of your response.

Query: 
{query}
---
<context>
{context}
</context>
"""

# Combine the system and human templates into a prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template)
])

chain = RunnableParallel({
    "query": RunnablePassthrough(),
    "context": retrieval_chain,
}) | prompt | ChatOpenAI()

if __name__ == "__main__":
    print(chain.invoke("Best time to visit Japan"))
