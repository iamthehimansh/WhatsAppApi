from flask import Flask , render_template,request,redirect,send_from_directory,make_response,render_template_string
from selenium import webdriver
import json
import pickle
from time import sleep
import datetime
from selenium.webdriver.common.keys import Keys
chromedriver = "chromedriver.exe"
continuetomessagexpath=r'//*[@id="action-button"]'
messagexpath=r'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
sendbtnxpath=r'//*[@id="main"]/footer/div[1]/div[3]'
options = webdriver.ChromeOptions();
options.add_argument('--user-data-dir=./User_Data')
driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=options)

app=Flask(__name__)

@app.route("/")
def login():
    driver.get("https://web.whatsapp.com/")
    return "sucess"
@app.route("/api/<id_>/<api_key>/<no>/msg",methods=["GET","POST"])
def api(id_,api_key,no):
    with open("api_json.json","r") as read:
        my_json=json.load(read)
    if id_ in my_json.keys():
        if my_json[id_]==api_key:
            try:
                
                mymsg=request.args.get('q')
                msg=mymsg
                print(mymsg)
                url=f"https://web.whatsapp.com/send?phone={no}&amp;text&amp;source&amp;data&amp;app_absent"
                print("Message sending to",no,"With msg :-",msg)
                driver.get(url)
                inp_xpath = '//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
                inp_xpath=r'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
                with open("time.json","r")as time_file:
                    time_json=json.load(time_file)
                try:
                    sleep(int(time_json["time"]))
                except:
                    sleep(25)
                input_box = driver.find_element_by_xpath(inp_xpath)
                # print("finded input box")
                sleep(2)
                # print("Sending key")
                input_box.send_keys(mymsg + Keys.ENTER)
                with open('chat_history.pkl', 'rb') as fr:
                    chatlist = pickle.load(fr)
                chatlist.append({"Sent_By":id_,"msg":msg,"no":no,"datetime":str(datetime.datetime.now())})
                with open('chat_history.pkl', 'wb') as fw:
                    pickle.dump(chatlist, fw)
                return {"return":True,"request_id":"sk8vrucxl3hip5t","message":["Message sent successfully to NonDND numbers"]}
            #{"status":"success","data":"sent"}
            except Exception as e:
                return {"status":"error","data":"Failed " + str(e)}
        else:
            return {"status":"error","data":"ID and KEY not Mached"}
    else:
        return {"status":"error","data":"ID and KEY not Mached"}
@app.route("/msghistory/<id_>/<api_key>/")
def ChatHistory(id_,api_key):
    with open("api_json.json","r") as read:
        my_json=json.load(read)
    if id_ in my_json.keys():
        if my_json[id_]==api_key:
            with open('chat_history.pkl', 'rb') as f:
                chatlist = pickle.load(f)
            return {"ChatHistory":chatlist}
    return "Some Error Occurs Cheak Your Id and API KEY"
app.run()
