from flask import Flask, request, json
from github import Github
import subprocess
import requests

g=Github("f1a51c65e60ec352849963361f34c59030d9873b")
app = Flask(__name__)

@app.route('/abc/exam1/api/v1/packages', methods=['POST'])
def set_packages():
    content=request.get_data()
    string=str(content, 'utf-8')
    jsonFile=json.loads(string)
    r=requests.get('https://api.github.com/repos/abc1196/sd2018b-exam1/pulls/2/files', auth=('token', 'f1a51c65e60ec352849963361f34c59030d9873b'))
    print("HOLA")
    print(r.text)
    file=open("/vagrant/pull.txt", "w")
    file.write(r.text)
    file.close()
    print(r)
    print(g.get_user().get_repo("sd2018b-exam1").get_pull(jsonFile["number"]))
    print(jsonFile["number"])
    print("ADIOS")
    return "danke"


if __name__ == '__main__':
   app.run(debug=True)
