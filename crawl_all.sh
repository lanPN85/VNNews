#!/usr/bin/env bash
set -e

scrapy list | \
    while read SPIDER; do
        CMD="scrapy crawl $SPIDER"
        echo ${CMD}
        eval ${CMD}
    done
