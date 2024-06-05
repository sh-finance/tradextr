from logger import logger

from langchain_core.output_parsers import StrOutputParser

from service.ec import ECService
from service.eia.api import EiaAPIService
from service.eia.page import eia_page_service

# from service.eia._page import EiaPageService
from service.iata import IATAService
from service.biofuels_news import BiofuelsNewsService
from service.openai import llm
from service.redis import redis
from service.es import es, es_vector_store
from service.mongo import mongo
from service.tavily import search as tavily_search

from util.reformulate_as_separate_question import reformulate_as_separate_question
from util.extractor import keywords_extractor

chain = llm | StrOutputParser()

eia_page_service.recursive_fetch_and_store_page()

# 拉取所有路由下的所有数据 存储到mongo
# EiaAPIService.recursive_fetch_and_store_data()
# 拉取total-energy下的所有数据 存储到mongo
# EiaAPIService.recursive_fetch_and_store_data("total-energy")
# 拉取所有路由的meta信息 存储到本地
# EiaAPIService.recursive_fetch_and_store_meta()
# 拉取EIA所有网页 向量化并入库es
# EiaPageService.start_crawl()


# 拉取EC sitemap中的所有网页并存储html到本地 正文到mongo
# ECService.fetch_and_store_sitemap_page_content()

# 拉取IATA sitemap中的所有网页并存储html到本地 正文到mongo
# IATAService.fetch_and_store_sitemap_page_content()

# 拉取BiofuelsNewsService中的所有网页并存储html到本地 正文到mongo
# print(BiofuelsNewsService.fetch_sitemap_urls())

# logger.info(redis.info())

# logger.info(es.info())

# logger.info(mongo.server_info())

############################################################################################


# docs: list[str] = [
#     """
# title: 什么是检索增强生成？
# content: 检索增强生成（RAG）是指对大型语言模型输出进行优化，使其能够在生成响应之前引用训练数据来源之外的权威知识库。大型语言模型（LLM）用海量数据进行训练，使用数十亿个参数为回答问题、翻译语言和完成句子等任务生成原始输出。在 LLM 本就强大的功能基础上，RAG 将其扩展为能访问特定领域或组织的内部知识库，所有这些都无需重新训练模型。这是一种经济高效地改进 LLM 输出的方法，让它在各种情境下都能保持相关性、准确性和实用性。
# """,
#     """
# title: 为什么检索增强生成很重要？

# content: LLM 是一项关键的人工智能（AI）技术，为智能聊天机器人和其他自然语言处理（NLP）应用程序提供支持。目标是通过交叉引用权威知识来源，创建能够在各种环境中回答用户问题的机器人。不幸的是，LLM 技术的本质在 LLM 响应中引入了不可预测性。此外，LLM 训练数据是静态的，并引入了其所掌握知识的截止日期。

# LLM 面临的已知挑战包括：

# 在没有答案的情况下提供虚假信息。
# 当用户需要特定的当前响应时，提供过时或通用的信息。
# 从非权威来源创建响应。
# 由于术语混淆，不同的培训来源使用相同的术语来谈论不同的事情，因此会产生不准确的响应。
# 您可以将大型语言模型看作是一个过于热情的新员工，他拒绝随时了解时事，但总是会绝对自信地回答每一个问题。不幸的是，这种态度会对用户的信任产生负面影响，这是您不希望聊天机器人效仿的！

# RAG 是解决其中一些挑战的一种方法。它会重定向 LLM，从权威的、预先确定的知识来源中检索相关信息。组织可以更好地控制生成的文本输出，并且用户可以深入了解 LLM 如何生成响应。
# """,
#     """
# title: 检索增强生成有哪些好处？

# content: RAG 技术为组织的生成式人工智能工作带来了多项好处。

# 经济高效的实施
# 聊天机器人开发通常从基础模型开始。基础模型（FM）是在广泛的广义和未标记数据上训练的 API 可访问 LLM。针对组织或领域特定信息重新训练 FM 的计算和财务成本很高。RAG 是一种将新数据引入 LLM 的更加经济高效的方法。它使生成式人工智能技术更广泛地获得和使用。

# 当前信息
# 即使 LLM 的原始训练数据来源适合您的需求，但保持相关性也具有挑战性。RAG 允许开发人员为生成模型提供最新的研究、统计数据或新闻。他们可以使用 RAG 将 LLM 直接连接到实时社交媒体提要、新闻网站或其他经常更新的信息来源。然后，LLM 可以向用户提供最新信息。

# 增强用户信任度
# RAG 允许 LLM 通过来源归属来呈现准确的信息。输出可以包括对来源的引文或引用。如果需要进一步说明或更详细的信息，用户也可以自己查找源文档。这可以增加对您的生成式人工智能解决方案的信任和信心。

# 更多开发人员控制权
# 借助 RAG，开发人员可以更高效地测试和改进他们的聊天应用程序。他们可以控制和更改 LLM 的信息来源，以适应不断变化的需求或跨职能使用。开发人员还可以将敏感信息的检索限制在不同的授权级别内，并确保 LLM 生成适当的响应。此外，如果 LLM 针对特定问题引用了错误的信息来源，他们还可以进行故障排除并进行修复。组织可以更自信地为更广泛的应用程序实施生成式人工智能技术。
# """,
#     """
# title: 检索增强生成的工作原理是什么？

# content: 如果没有 RAG，LLM 会接受用户输入，并根据它所接受训练的信息或它已经知道的信息创建响应。RAG 引入了一个信息检索组件，该组件利用用户输入首先从新数据源提取信息。用户查询和相关信息都提供给 LLM。LLM 使用新知识及其训练数据来创建更好的响应。以下各部分概述了该过程。

# 创建外部数据
# LLM 原始训练数据集之外的新数据称为外部数据。它可以来自多个数据来源，例如 API、数据库或文档存储库。数据可能以各种格式存在，例如文件、数据库记录或长篇文本。另一种称为嵌入语言模型的 AI 技术将数据转换为数字表示形式并将其存储在向量数据库中。这个过程会创建一个生成式人工智能模型可以理解的知识库。

# 检索相关信息
# 下一步是执行相关性搜索。用户查询将转换为向量表示形式，并与向量数据库匹配。例如，考虑一个可以回答组织的人力资源问题的智能聊天机器人。如果员工搜索：“我有多少年假？”，系统将检索年假政策文件以及员工个人过去的休假记录。这些特定文件将被退回，因为它们与员工输入的内容高度相关。相关性是使用数学向量计算和表示法计算和建立的。

# 增强 LLM 提示
# 接下来，RAG 模型通过在上下文中添加检索到的相关数据来增强用户输入（或提示）。此步骤使用提示工程技术与 LLM 进行有效沟通。增强提示允许大型语言模型为用户查询生成准确的答案。

# 更新外部数据
# 下一个问题可能是——如果外部数据过时了怎么办？ 要维护当前信息以供检索，请异步更新文档并更新文档的嵌入表示形式。您可以通过自动化实时流程或定期批处理来执行此操作。这是数据分析中常见的挑战——可以使用不同的数据科学方法进行变更管理。
# """,
#     """
# title: 检索增强生成和语义搜索有什么区别？
# content: 语义搜索可以提高 RAG 结果，适用于想要在其 LLM 应用程序中添加大量外部知识源的组织。现代企业在各种系统中存储大量信息，例如手册、常见问题、研究报告、客户服务指南和人力资源文档存储库等。上下文检索在规模上具有挑战性，因此会降低生成输出质量。

# 语义搜索技术可以扫描包含不同信息的大型数据库，并更准确地检索数据。例如，他们可以回答诸如 “去年在机械维修上花了多少钱？”之类的问题，方法是将问题映射到相关文档并返回特定文本而不是搜索结果。然后，开发人员可以使用该答案为 LLM 提供更多上下文。

# RAG 中的传统或关键字搜索解决方案对知识密集型任务产生的结果有限。开发人员在手动准备数据时还必须处理单词嵌入、文档分块和其他复杂问题。相比之下，语义搜索技术可以完成知识库准备的所有工作，因此开发人员不必这样做。它们还生成语义相关的段落和按相关性排序的标记词，以最大限度地提高 RAG 有效载荷的质量。
# """,
#     """
# title: AWS 如何支持您的 Retrieval-Augmented Generation 需求？
# content: Amazon Bedrock 是一项完全托管的服务，提供多种高性能基础模型以及多种功能，用于构建生成式人工智能应用程序，同时简化开发并维护隐私和安全。借助 Amazon Bedrock 的知识库，您只需点击几下即可将 FM 连接到您的 RAG 数据来源。矢量转换、检索和改进的输出生成均自动处理。

# 对于管理自己的 RAG 的组织来说，Amazon Kendra 是一项由机器学习提供支持的高精度企业搜索服务。它提供了经过优化的 Kendra 检索 API，您可以将其与 Amazon Kendra 的高精度语义排名器一起使用，作为 RAG 工作流程的企业检索器。例如，使用检索 API，您可以：

# 检索多达 100 个语义相关的段落，每个段落最多包含 200 个标记词，按相关性排序。
# 使用预构建的连接器连接到常用数据技术，例如 Amazon Simple Storage Service、SharePoint、Confluence 和其他网站。
# 支持多种文档格式，例如 HTML、Word、PowerPoint、PDF、Excel 和文本文件。
# 根据最终用户权限允许的文档筛选响应。
# 亚马逊还为想要构建更多自定义生成式人工智能解决方案的组织提供了选项。Amazon SageMaker JumpStart 是一个机器学习中心，包含基础模型、内置算法和预构建的机器学习解决方案，只需单击几下即可轻松部署。您可以通过参考现有的 SageMaker 笔记本和代码示例来加快 RAG 的实施。

# 立即创建免费账户，开始在 AWS 上使用 Retrieval-Augmented Generation
# """,
# ]


# def summarize(doc: str) -> str:
#     prompt = f"""Summarize the following text, requiring concise language and covering the core content

#     {doc}
#     """
#     return chain.invoke(prompt)


# def combine(docs: list[str], conclusions: list[str]) -> str:
#     context = ""

#     for i in range(len(docs)):
#         doc = docs[i]
#         summary = conclusions[i]
#         context += f"""
# origin: {doc}
# summary: {summary}
# """

#     prompt = f"""Below is some text content and its summary, based on which the user's questions are answered
# question: 检索增强生成有哪些现成的服务?

# context: {context}
# """
#     return chain.invoke(prompt)


# conclusions = [summarize(doc) for doc in docs]

# # logger.info(conclusions)

# res = combine(docs, conclusions)

# logger.info(res)

############################################################################################

# question = "where EIA's open source code available on?"

# res = keywords_extractor.invoke({ "text": question })

# keywords = res.keywords

# logger.info("keywords: %s", keywords)

# query = ""

# for k in keywords:
#   query += k + ' '

# logger.info("query: %s", query)

# query = question

# res = es_vector_store.similarity_search(query)
# logger.info(res)

# results = tavily_search(query)

# logger.info(results)

# context = ""

# for doc in res:
#   context += doc.page_content + '\n\n\n'

# res = chain.invoke(
#     f"""base on the context, answer the question: {question}
#            <context>{context}</context>
#            """
# )

# logger.info(res)
