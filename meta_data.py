import requests
import json

# ----- 元数据 ------ start
# appKey和域名，分别获取staging和线上的token
staging_appkey = "98d07885-eca5-4c03-8434-e2c697ba72e8"
prod_appkey = "d6c6da4c-8a06-4421-bb97-4f830eb88c85"
prod_domain = "https://is-gateway.corp.kuaishou.com"
staging_domain = 'https://is-gateway-test.corp.kuaishou.com'
# 密钥，只有线上环境需要
secret_key = '55d0532ec796df671f3bbab5d1d44d4d'

# 实际使用的域名和appKey
domain = staging_domain
appkey = staging_appkey

# 小组所有的biz，快意和可图不同
# kwaiyi_biz = 'hackthon_19746eaa57'
# ketu_biz = "hackathon_967644"

kwaiyi_biz = 'api_test'
ketu_biz = "vcg-test"

# 照片blobStore存储元数据
bucket_name = "mmu-aiplatform-temp"
db = "mmu"
table = "aiplatform-temp"
global_ip = ""
# ----- 元数据 ------ end

# 获取token
def get_token():
    url = domain + '/token/get?appKey=' + appkey
    if domain == prod_domain:
        url += '&secretKey=' + secret_key
    response = requests.get(url)
    json_response = json.loads(response.content)
    access_token = json_response['result']['accessToken']
    return access_token

# 每次调用接口都需要使用token，第一次获取后缓存下来
access_token = get_token()

