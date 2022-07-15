# crawl_enterprise_info
crawl enterprise Information

# 抓取顺企网工商数据

## 抓取流程

- 获得第一层city分类链接共421
    - https://b2b.11467.com/ 为例
- 第二层，通过所有city分类获取里面所有主分类链接
    - https://www.11467.com/shenzhen/  为例
- 第三层,通过主分类解析详细分类链接
    - https://www.11467.com/shenzhen/dir/a01.htm  为例
- 第四层，解析上述网页中所有公司链接
    - https://www.11467.com/shenzhen/dir/a011.htm  为例
- 最后解析每个公司详情页中企业信息
    - 解析过程中只要不是200状态就将该企业链接存入rollback_company等待下次回滚

## redis

- city_category
    - 存放所有城市分类链接
- main_category_urls

- detailed_category

- company_link

- rollback_company
    - 第一次解析不成功的链接

## mongo DB

- company_info
    ```
    { 
        "_id" : ObjectId("62a2adf4386e6abea522c134"), 
        "company_name" : "湖南臻有趣咨询管理有限公司", 
        "product" : "商务代理代办、创业指导、文化活动、职业中介的服务；场地准备活动；家政服务；其他企业管理咨询服务(限于组织管理服务）；财务咨询服务（不含金融、证券、期货）；体系认证咨询服务；产品认证咨询服务；电脑图文设计；知识产权代理；食品、日用百货、服装、鞋帽、工艺品、纸制品、家具用品、花卉、苗木、文化用品、体育用品、电子产品、化妆品、玩具、建材、化工原料及产品（不含危化品和监控化学品）、针纺织品及纺织原料、初级农副产品的销售及网上销售；电子商务平台的开发建设（不得从事增值电信、金融业务、支付业务）。（依法须经批准的项目，经相关部门批准后方可开展经营活动）", 
        "business_scope" : "", 
        "license_num" : "", 
        "business_status" : "开业", 
        "business_model" : "", 
        "capital" : "2000 (万元)", 
        "category" : "代理公司", 
        "city" : "益阳企业网", 
        "company_code" : "97334371", 
        "shop_link" : ""
    }
    
    ```
