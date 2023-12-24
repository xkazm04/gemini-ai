# Short term memory
# Conversation summary memory
# Conversation memory

import os
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models.openai import ChatOpenAI
from langchain.chains import ConversationChain
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from langchain.memory.chat_message_histories.upstash_redis import (UpstashRedisChatMessageHistory)

URL = os.getenv("UPSTASH_REDIS_REST_URL")
TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")


history = UpstashRedisChatMessageHistory(
    url=URL, token=TOKEN, session_id="my-test-session"
)
# Basic conversation example

llm = ChatOpenAI(
    model="davinci",
    temperature=0.4,
)
    

memory = ConversationBufferMemory(
    chat_memory=history
)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=memory
)

conversation.run(input="I am Michal")