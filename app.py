# coding:utf-8
from flask import Flask, request, jsonify
import MeCab
import argparse


app = Flask(__name__)


@app.route("/")
def hello():
    return "hello"

@app.route("/parse")
def parse():
    response = None
    sentence = request.args.get("sentence", "").encode("utf-8")
    # dic指定は実装予定
    # dic = request.args,get("dic", "")
    if sentence is None:
        response = jsonify({"error": {
                                "message": "You must fill sentence parameter",
                                "code": "400",
                                "url": "/parse"}})
        response.status_code = 400
        return response
    print sentence
    tg = MeCab.Tagger("-Ochasen")
    tg.parse("")
    words = tg.parseToNode(str(sentence))
    word_list = []
    index = 0
    while words:
        if words.feature.split(",")[0] == "BOS/EOS":
            words = words.next
            continue
        word = {}
        word["index"] = index
        word["surface"] = words.surface
        word["feature"] = words.feature
        word_list.append(word)
        words = words.next
        index += 1
    response_dict = {"header": {
                        "status": "ok",
                        "code": 200
                    },
                    "response": {
                        "total_count": len(word_list),
                        "word_list": word_list
                    }}
    response = jsonify(response_dict)
    response.status_code = 200
    return response


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-host",
        help="host name",
        default="localhost",
        dest="host"
        )
    parser.add_argument(
        "-port",
        help="server port",
        default=80,
        dest="port"
        )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_options()
    app.run(host=args.host, port=args.port)
    # app.run()
