from flask import Flask
from flask import jsonify
from aaaelasticmanager import ElasticIndex
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask import render_template
from flask import abort, redirect, url_for, send_from_directory

app = Flask(__name__)
    
index = ElasticIndex(
    'uosuits', 
    'https://search-suits-vbaatnpkzo5wgizkdelx64a2w4.us-west-2.es.amazonaws.com',
    port=443
)

@app.route('/')
def home():
    return send_from_directory('static', 'views/index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', 'js/' + path) 

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'img/favicon.ico') 

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static', 'css/' + path) 

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('static', 'vendor/' + path) 

@app.route('/modules/<path:path>')
def send_module(path):
    return send_from_directory('node_modules', path) 

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static', 'img/' + path) 

@app.route('/views/<path:path>')
def send_views(path):
    return send_from_directory('static', 'views/' + path) 

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static', 'fonts/' + path) 


@app.route("/user/<userId>")
def user_detail(userId):
    search_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "has_child": {
                            "type": "suits",
                             "query": {
                                "match_all": {}
                             },
                             "inner_hits": {
                                  "sort": [
                                      {
                                          "suits.found_date": {
                                              "order": "desc"   
                                          }
                                      }
                                  ],
                                  "size": 15
                            }
                        }
                    },
                    {
                        "ids": {
                            "values": [userId] 
                        }
                    }
                ]
            }
        }
    } 
    print "searching"
    result = index.search(search_query, ['user'])
    print "finished searching"
    return jsonify(**result)


@app.route("/search/<query>")
def search(query):
    fromNum = request.args.get('from')
    search_query = {
       "query": {
          "filtered": {
             "filter": {
                "or": [
                   {
                      "and": [
                         {
                            "has_child": {
                               "type": "suits",
                               "query": {
                                  "match_all": {}
                               },
                               "inner_hits": {
                                  "sort": [
                                     {
                                        "suits.found_date": {
                                           "order": "desc"
                                        }
                                     }
                                  ],
                                  "size": 1
                               }
                            }
                         },
                         {
                            "query": {
                               "multi_match": {
                                  "query": query,
                                  "fields": ["name", "names"]
                               }
                            }
                         }
                      ]
                   },
                   {
                      "has_child": {
                         "type": "suits",
                         "query": {
                            "nested": {
                               "path": "gear",
                               "query": {
                                  "match": {
                                     "gear.name": query
                                  }
                               },
                               "inner_hits": {
                                  "sort": [
                                     {
                                        "suits.found_date": {
                                           "order": "desc"
                                        }
                                     }
                                  ],
                                  "size": 1
                               }
                            }
                         }
                      }
                   }
                ]
             }
          }
       },
      "size":10,
      "from":fromNum
    } 
    
    print "searching"
    result = index.search(search_query, ['user'])
    print "finished searching"
    return jsonify(**result)

if __name__ == "__main__":
    app.run()
