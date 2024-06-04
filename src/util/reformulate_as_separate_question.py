import json
from openai.types.chat import ChatCompletionMessageParam
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.adapters.openai import convert_openai_messages

from service.openai import llm

reformulate_as_separate_question_template = open(
    "prompt/reformulate_as_separate_question.md", "r"
).read()


# 根据上下文将问题重新表述为独立问题
def reformulate_as_separate_question(
    # question: str, history: list[ChatCompletionMessageParam]
    messages: list[ChatCompletionMessageParam],
):
    """
    question = reformulate_as_separate_question(question="这个多少钱", history=[{ "role": "user", "content": "这个苹果看起来真好吃" }])
    question <= "这个苹果多少钱？"
    """
    # contextualize_q_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", reformulate_as_separate_question_template),
    #         MessagesPlaceholder(variable_name="chat_history"),
    #         ("human", "{question}"),
    #     ]
    # )

    # contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()
    # return contextualize_q_chain.invoke(
    #     {
    #         "chat_history": convert_openai_messages(
    #             [
    #                 {"role": x.get("role", ""), "content": x.get("content", "")}
    #                 for x in history
    #             ]
    #         ),
    #         "question": question,
    #     }
    # )

    prompt = ChatPromptTemplate.from_template(reformulate_as_separate_question_template)

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"messages": json.dumps(messages)})
