# Data DataStructure

## EIA

> <https://www.eia.gov/totalenergy/data/browser/?tbl=T10.01#/?f=A&start=1949&end=2022&charted=6-7-8-9-14-2-3>

### total-energy

```json
{
  "period": "2013", // 时间周期: 只有一个年份代表这个数据是按年统计的, 有月份代表是按月统计, Q1~4代表按季度统计
  "msn": "WDPRBUS", // 用于区分资源类型的code, 其他接口下可能不是`msn`这个字段
  "seriesDescription": "Wood Energy Production in Trillion Btu",
  "value": "2338.256",
  "unit": "Trillion Btu"
}
```

### EC

> <https://commission.europa.eu/sitemap.xml>

```json
{
  "url": "https://commission.europa.eu/index_en", // 静态网页地址
  "content": "Managing migration responsibly\n.......Share this page", // 提取出正文内容 不包含页眉页脚的不相关的信息
  "html": "<!DOCTYPE html>\n<html lang=\"en\" dir=\"ltr\" prefix=\"og: https://ogp.me/ns#\">.....</html>\n" // 网页原文
}
```

### IATA

> <https://www.iata.org/sitemap.xml>

```json
{
  "_id": {
    "$oid": "65f15d84250126e8d82de08c"
  },
  "url": "https://www.iata.org/en/programs/safety/safety-risk/sirm/sirm-insights/airwothiness/", // 静态网页地址
  "content": "SIRM Insights\nTopics from the Safety Issue Review Meetings..... especially as we approach the summer months.", // 提取出正文内容 不包含页眉页脚的不相关的信息
  "html": "\n\n\n\n<!DOCTYPE html>\n<html lang=\"en\" class=\"on-page-editor\">\n<head>\n.....\n</html>\n\n\n\n" // 网页原文
}
```
