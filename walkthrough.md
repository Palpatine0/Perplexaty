## Perplexaty

### Project Introduction

This project involves building a web-based Retrieval-Augmented Generation (RAG) chatbot using several tools: LangChain,
Exa (a search engine), LangSmith, and Hosted Langserve. The chatbot leverages LangChain for developing LLM-powered
applications, Exa for retrieving relevant web-based context, LangSmith for debugging and observability, and Hosted
Langserve for deployment.

### Prerequisites

- Python 3.11
- pip (Python package installer)
- Git (optional)

### Step 1: Initial Setup

#### 1. Initialize the Environment

First, let's set up the environment and install necessary dependencies.

1. **Create a `.env` file:**

2. This file will store your API keys and other configuration settings. Ensure it is included in your `.gitignore` file
   to prevent it from being committed to your repository.

   Example `.env` file:
   ```plaintext
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
   LANGCHAIN_API_KEY="your_langchain_api_key"
   LANGCHAIN_PROJECT="Perplexaty"
   OPENAI_API_KEY="your_open_api_key"
   ```

2. **Install required packages:**
   ```bash
   pip install langchain langchain_community openai streamlit python-dotenv
   ```
   ```bash
   pip install -U langchain-cli
   ```
   ```bash
   pip install langchain-exa
   ```

#### Key Concepts

##### 1. LangChain-Exa Integration

- **Definition**:`langchain-exa` is a package that facilitates the integration of LangChain with Exa, a search engine.
  This integration allows for seamless communication between LangChain applications and Exa, enabling the retrieval of
  relevant web-based context to enhance the capabilities of LLM-powered applications.
- **Usage**:By using the `langchain-exa` package, developers can leverage Exa's search capabilities within their
  LangChain workflows. This integration supports the Retrieval-Augmented Generation (RAG) framework, which enhances
  language models with external data sources for more accurate and contextually relevant responses.

### Step 2: Setup LangServe and LangSmith

#### 1. LangServe Setup

Set up LangServe to manage our application deployment.
Use the LangServe CLI to create a new application called `pinecone-serverless`.

```bash
langchain app new perplexaty
```   

#### 2. LangSmith Setup

Make sure u have created a LangSmith project for this lab.

**Project Name:** PineconeServerless

### Step 3: Setup Exa

#### 1: Create a Account

- **Access Exa:**

  Navigate to [Exa](https://dashboard.exa.ai/login?redirect=/).

  <img src="https://i.imghippo.com/files/sjw3a1718256877.jpg" alt="" border="0">

#### 2: Get Your Own API Key

1. **Navigate to API Keys:**

   Navigate to [Exa API Key](https://dashboard.exa.ai/api-keys).

   <img src="https://i.imghippo.com/files/RAsfi1718257187.jpg" alt="" border="0">


3. **Update your `.env` file:**

   Copy the generated API key and store it securely.
   Add it to your `.env` file:

    ```plaintext
    EXA_API_KEY="your_exa_api_key"
    ```

#### Key Concepts

#### Key Concepts

##### 1. Exa Account Setup

- **Definition**: etting up an Exa account is the initial step required to utilize Exa's capabilities for your projects.
  It involves creating an account, obtaining an API key, and configuring your environment to interact with Exa's
  services.
- **Usage**: An account is necessary to manage and access Exa's features, including data retrieval, processing, and
  other API services.

### Step 4: Integrate ExaSearchRetriever

In this step, we will integrate the ExaSearchRetriever to retrieve documents based on user queries.

#### 1. Create `chain.py` to Integrate ExaSearchRetriever

**File**: `perplexaty/app/chain.py`

**Updated Code for `chain.py`:**

```python
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

```

#### 2. Test the Chain

Run the `chain.py` file and inspect the results

<img src="https://i.imghippo.com/files/fFd8h1718259524.jpg" alt="" border="0">

### Key Concepts

#### ExaSearchRetriever

- **Definition**: The `ExaSearchRetriever` is a component from the `langchain-exa` package that allows for retrieving
  documents from the Exa search engine. It is designed to work seamlessly with LangChain applications to fetch relevant
  web-based content.
- **Usage**: The `ExaSearchRetriever` is used to perform document retrieval based on user queries, enabling the
  integration of external data sources into LangChain workflows. This enhances the chatbot's ability to provide accurate
  and contextually relevant responses.

### Step 5: Add Document Processing Chain with ExaSearchRetriever and Highlights

In this step, we will create a document processing chain that uses the `ExaSearchRetriever` to retrieve documents with
highlights and format their details.

#### 1. Create `chain.py` to Integrate ExaSearchRetriever and Document Processing Chain

Here, we extend the functionality of the `chain.py` file to include a document processing chain. This chain retrieves
documents using `ExaSearchRetriever` and formats the details, including highlights and URLs, using a template.

**File**: `perplexaty/app/chain.py`

**Updated Code for `chain.py`:**

```python
...

from langchain_exa import ExaSearchRetriever
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda

...

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

print(retrieval_chain.invoke("Best time to visit Japan"))
```

<img src="https://i.imghippo.com/files/1qtr01718262864.jpg" alt="" border="0">

In this updated `chain.py`, the code initializes the `ExaSearchRetriever` with parameters to retrieve documents with
highlights. A `document_template` is defined to format the document details, and a `document_chain` processes the
retrieved document metadata. Finally, the `retrieval_chain` combines these components to format and display the
retrieved document details.

#### 2. Test the Chain

Run the `chain.py` file and inspect the results:

<img src="https://i.imghippo.com/files/VAToB1718263535.jpg" alt="" border="0">

### Step 6: Add Context-Based Query Answering Chain with ExaSearchRetriever

In this step, we will create a context-based query answering chain using the `ExaSearchRetriever`. This chain will
process queries and contexts, generate responses, and cite sources.

#### 1. Create `chain.py` to Integrate Context-Based Query Answering Chain

Here, we extend the functionality of the `chain.py` file to include a context-based query answering chain. This chain
combines query and context processing, generates responses, and cites sources.

**File**: `perplexaty/app/chain.py`

**Updated Code for `chain.py`:**

```python
...

from langchain_exa import ExaSearchRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

...

# Define templates for the research assistant response
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

# Combine the retriever and document chain to process retrieved documents and display highlights and URLs
retrieval_chain = retriever | document_chain.map() | (lambda docs: "\n".join([i.text for i in docs]))

# Define the full context-based query answering chain
chain = RunnableParallel({
    "query": RunnablePassthrough(),
    "context": retrieval_chain,
}) | prompt | ChatOpenAI()

# Main execution to test the query answering chain
if __name__ == "__main__":
    print(chain.invoke("Best time to visit Japan"))
```

<img src="https://i.imghippo.com/files/QJ7j41718264524.jpg" alt="" border="0">

In this updated `chain.py`, the code initializes the `ExaSearchRetriever` with parameters to retrieve documents with
highlights. A `document_template` is defined to format the document details, and a `document_chain` processes the
retrieved document metadata. The `retrieval_chain` combines these components to format and display the retrieved
document details. Additionally, the code defines templates for the research assistant response and integrates these
templates into a context-based query answering chain.

Now this chain can query answering chain combines multiple components to process queries and contexts, generate
responses, and cite sources. It integrates the ExaSearchRetriever with a formatting template to display document
details, including highlights and URLs, and uses a prompt template to generate responses based on the provided context.

#### 2. Test the Chain

Run the `chain.py` file and inspect the results:

<img src="https://i.imghippo.com/files/7pMTI1718264649.jpg" alt="" border="0">

#### Key Concepts

##### 1. ArxivRetriever

- **Definition**: ArxivRetriever is a tool that allows developers to fetch academic papers from the Arxiv repository
  programmatically. It provides an easy way to access and summarize research papers.
- **Usage**: It is used in this project to perform document-based research and retrieve summaries of academic papers
  based on a user's query.
- **Example**:
  ```python
  from langchain.retrievers import ArxivRetriever

  retriever = ArxivRetriever()
  docs = retriever.get_summaries_as_docs("What papers did Emil Khalisi write?")
  print(docs)
  ```

#### 2. Test the Document-Based Research Chain

Run the `doc_chain.py` file and inspect the results to ensure that the document-based research chain is functioning
correctly and generating summaries of academic papers.

<img src="https://i.imghippo.com/files/6trR21718152471.jpg" alt="" border="0">

### Step 7: Serve the Application Using LangServe

#### 1. Update `server.py`:

<img src="https://i.imghippo.com/files/cHqn91718266965.jpg" alt="" border="0">

#### 2. Update `chain.py`:

<img src="https://i.imghippo.com/files/kdW6s1718267004.jpg" alt="" border="0">

#### 3. Serving the Application by LangServe

Run the following commands to set up and serve the application using LangServe.

   ```bash
   cd perplexaty
   langchain serve
   ```

You can now access the application through the following links:

Access [Playground](http://127.0.0.1:8000/perplexaty/playground/)

<img src="https://i.imghippo.com/files/rh07Z1718267175.jpg" alt="" border="0">
