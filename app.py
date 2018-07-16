# coding:utf-8
from flask import Flask, request, jsonify
import MeCab
import argparse


app = Flask(__name__)
# 返すJSONの中で日本語が文字化けしないための対策
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/")
def hello():
    return "hello"


@app.route("/parse")
def parse():
    response = None
    sentence = request.args.get("sentence", "")
    # dic指定は実装予定
    # dic = request.args,get("dic", "")
    if sentence is None:
        response = jsonify({"error": {
                                "message": "You must fill sentence parameter",
                                "code": "400",
                                "url": "/parse"}})
        response.status_code = 400
        return response
    m = MeCab.Tagger(" -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    mrphs = m.parse(sentence).split("\n")
    mrph_list = []
    for i, mrph in enumerate(mrphs):
        if mrph == "EOS" or mrph == "":
            continue
        morph = {}
        surface, feature = mrph.split("\t")[0], mrph.split("\t")[1]
        morph["index"] = i
        morph["surface"] = surface
        morph["feature"] = feature
        mrph_list.append(morph)

    response_dict = {
                        "total_count": len(mrph_list),
                        "word_list": mrph_list
                    }
    response = jsonify(response_dict)
    response.status_code = 200
    return response


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-host",
        help="host name",
        default="0.0.0.0",
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
