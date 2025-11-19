from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
resp = llm.invoke("Say hi in one word.")
print(resp)
