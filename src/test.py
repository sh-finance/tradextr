from service.ec import ECService
from service.eia import EIAService

# 拉取sitemap中的所有网页并存储html到本地 正文到mongo
# ECService.fetch_and_store_sitemap_page_content()

# 拉取所有路由下的所有数据 存储到mongo
# EIAService.recursive_fetch_and_store_data()
# 拉取total-energy下的所有数据 存储到mongo
# EIAService.recursive_fetch_and_store_data("total-energy")
# 拉取所有路由的meta信息 存储到本地
# EIAService.recursive_fetch_and_store_meta()
