import json
import argparse
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeImagesRequest import DescribeImagesRequest

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--alicloud_access_key', help='Alicloud Key', required=True)
parser.add_argument('-s', '--alicloud_secret_key', help='Alicloud Secret', required=True)
parser.add_argument('-r', '--alicloud_region', help='Alicloud Region', required=True)
args = parser.parse_args()

access_key = args.alicloud_access_key
secret_key = args.alicloud_secret_key
region = args.alicloud_region

client = AcsClient(access_key, secret_key, region)

request = DescribeRegionsRequest()
request.set_accept_format('json')

response = client.do_action_with_exception(request)

parsed = json.loads(str(response, encoding='utf-8'))

image_count = 0

for x in range(len(parsed['Regions']['Region'])):
  client = AcsClient(access_key, secret_key, parsed['Regions']['Region'][x]["RegionId"])
  request = DescribeImagesRequest()
  request.set_accept_format('json')
  request.set_ImageOwnerAlias("self")
  response = client.do_action_with_exception(request)
  data = json.loads(str(response, encoding='utf-8'))
  if data['TotalCount'] > 0:
    print(parsed['Regions']['Region'][x]["RegionId"])
    images = data['Images']['Image']
    for x in range(len(images)):
      print('\t' + images[x]["ImageName"] + '\t' + images[x]["ImageId"])
    image_count += data['TotalCount']
    print('\n') 

print("Total number of images %d" % (image_count))
