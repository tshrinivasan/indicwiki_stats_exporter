# example - https://www.robustperception.io/writing-a-jenkins-exporter-in-python
# To make grafana public read only - https://stackoverflow.com/a/45643278/1301753


import json
from prometheus_client import start_http_server, MetricsHandler
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from xmlrpc.client import ServerProxy
import os
import sys
import threading
from http.server import HTTPServer
import requests
import subprocess
import glob
import datetime
import yaml
import traceback

PORT_NUMBER = 11810

wiki_info = yaml.load(open('/home/shrini/dev/indicwiki_stats_exporter/indic_wiki.yaml'))


indic_wikipedia  = wiki_info['indic_wikipedia'].split(",")


with open('/home/shrini/dev/indicwiki_stats_exporter/languages.json') as f:
      all_lang = json.load(f)

      
class WikiStatsCollector(object):


    def collect(self):
        try:
            

            
            wiki_pages = GaugeMetricFamily(
            'wiki_pages',
            'wiki_pages',
            labels=[ "lang_code","language"])



            wiki_articles = GaugeMetricFamily(
            'wiki_articles',
            'wiki_articles',
            labels=[ "lang_code","language"])


            wiki_edits = GaugeMetricFamily(
            'wiki_edits',
            'wiki_edits',
             labels=[ "lang_code","language"])


            wiki_images = GaugeMetricFamily(
            'wiki_images',
            'wiki_images',
             labels=[ "lang_code","language"])


            wiki_users = GaugeMetricFamily(
            'wiki_users',
            'wiki_users',
             labels=[ "lang_code","language"])


            wiki_activeusers = GaugeMetricFamily(
            'wiki_activeusers',
            'wiki_activeusers',
             labels=[ "lang_code","language"])


            wiki_admins = GaugeMetricFamily(
            'wiki_admins',
            'wiki_admins',
             labels=[ "lang_code","language"])

            

            for lang in indic_wikipedia:
                print(lang)


                url = "https://" + lang + ".wikipedia.org/w/api.php"

                PARAMS = {
                "action": "query",
                "meta": "siteinfo",
                "formatversion": "2",
                "format": "json",
                "siprop":"statistics"
                }


                r = requests.get(url = url, params = PARAMS) 

                data = r.json() 

                wiki_pages.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["pages"])
                wiki_articles.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["articles"])
                wiki_edits.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["edits"])
                wiki_images.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["images"])
                wiki_users.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["users"])
                wiki_activeusers.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["activeusers"])
                wiki_admins.add_metric([lang, all_lang[lang]["name"]],data["query"]["statistics"]["admins"])


                                
            yield wiki_pages
            yield wiki_articles
            yield wiki_edits
            yield wiki_images
            yield wiki_users
            yield wiki_activeusers
            yield wiki_admins


        except Exception:
            
            print(traceback.format_exc())


            
if __name__ == "__main__":
    REGISTRY.register(WikiStatsCollector())
    thread = threading.Thread(target=WikiStatsCollector())
    thread.start()

    server = HTTPServer(('',PORT_NUMBER),MetricsHandler)
    server.serve_forever()

    while True:
        pass

