# VNNews
Crawlers for Vietnamese news sites

## Quickstart
```bash
git clone https://github.com/lanPN85/VNNews
cd VNNews
pip3 install -r requirements.txt

# List all available crawlers
scrapy list

# Start all available crawlers
# Files will be available in the text/ directory
./crawl_all.sh
```

## Configurations
### Crawl Limit
Each crawler has a page limit specified in `VNNews/crawl_limit.py`.

### Proxy Setting
To turn on proxies (which may help avoid IP blocks on certain sites), uncomment line 56 in `VNNews/settings.py`

When proxy is on, the proxy list can be edited in `VNNews/proxy.py`
