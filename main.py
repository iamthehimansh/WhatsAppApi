from flask import Flask , render_template,request,redirect,send_from_directory,make_response,render_template_string
from selenium import webdriver
import json
import pickle
from time import sleep,time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
chromedriver = r"chromedriver.exe"
continuetomessagexpath=r'//*[@id="action-button"]'
messagexpath=r'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
sendbtnxpath=r'//*[@id="main"]/footer/div[1]/div[3]'
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=./User_Data')
driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=options)
driver.get("https://web.whatsapp.com/")

# with open(r"time.json","r")as time_file:
#     time_json=json.load(time_file)
# try:
#     s_time=int(time_json["time"])
# except:
#     s_time=20


print(f"Waiting  while we load the Whatsapp")
WebDriverWait(driver,600).until(ec.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]")))
app=Flask(__name__)

@app.route("/")
def login():
    driver.get("https://web.whatsapp.com/")
    return "sucess"
@app.route("/api/<id_>/<api_key>/<no>/msg",methods=["GET","POST"])
def api(id_,api_key,no):
    t1=time()
    with open(r"api_json.json","r") as read:
        my_json=json.load(read)
    if id_ in my_json.keys():
        if my_json[id_]==api_key:
            try:
                
                mymsg=request.args.get('q')
                msg=mymsg
                print(mymsg)
                if driver.current_url=="https://web.whatsapp.com/":
                    try:
                        search_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')#_2zCfw
                        search_box.clear()
                        search_box.send_keys(no)
                        
                        driver.find_element_by_class_name("_3Pwfx").click()
                        sleep(.1)
                    except Exception as e :
                        print(e,"find")
                        url=f"https://web.whatsapp.com/send?phone={no}&amp;text&amp;source&amp;data&amp;app_absent"
                        print("Message sending to",no,"With msg :-",msg)
                        driver.get(url)
                        with open(r"time.json","r")as time_file:
                            time_json=json.load(time_file)
                        try:
                            sleep(int(time_json["time"]))
                        except:
                            sleep(25)
                else:
                    url=f"https://web.whatsapp.com/send?phone={no}&amp;text&amp;source&amp;data&amp;app_absent"
                    
                    driver.get(url)
                    try:
                        driver.find_element_by_class_name("_2xUEC _2XHG4").click()
                        with open('chat_history.pkl', 'rb') as fr:
                            chatlist = pickle.load(fr)
                        chatlist.append({"Sent_By":id_,"msg":msg,"no":no,"datetime":str(datetime.datetime.now()),"Failed":True})
                        with open('chat_history.pkl', 'wb') as fw:
                            pickle.dump(chatlist, fw)
                        t2=time()
                        return {"return":False,"request_id":f"{len(chatlist)-1}","message":["Message not sent",{"time elacped":int(t2-t1)}],"error":"Mobile no not find"}
                    except:
                        pass
                    # with open(r"time.json","r")as time_file:
                    #     time_json=json.load(time_file)
                    # try:
                    #     sleep(int(time_json["time"]))
                    # except:
                    #     sleep(25)
                print("Message sending to",no,"With msg :-",msg)
                inp_xpath = r'//div[@class="_2S1VP copyable-text selectable-text"][@contenteditable="true"][@data-tab="1"]'
                inp_xpath=r'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
                # input_box = driver.find_element_by_xpath(inp_xpath)
                input_box=WebDriverWait(driver,600).until(ec.visibility_of_element_located((By.XPATH,inp_xpath)))
                # print("finded input box")
                sleep(2)
                # print("Sending key")
                input_box.send_keys(mymsg + Keys.ENTER)
                t2=time()
                with open('chat_history.pkl', 'rb') as fr:
                    chatlist = pickle.load(fr)
                chatlist.append({"Sent_By":id_,"msg":msg,"no":no,"datetime":str(datetime.datetime.now()),"Failed":False,"other":{"time elacped":int(t2-t1)}})
                with open('chat_history.pkl', 'wb') as fw:
                    pickle.dump(chatlist, fw)
                
                return {"return":True,"request_id":f"{len(chatlist)-1}","message":["Message sent successfully",{"time elacped":int(t2-t1)}]}
            #{"status":"success","data":"sent"}
            except Exception as e:
                return {"status":"error","data":"Failed " + str(e)}
        else:
            return {"status":"error","data":"ID and KEY not Mached"}
    else:
        return {"status":"error","data":"ID and KEY not Mached"}
@app.route("/msghistory/<id_>/<api_key>/")
def ChatHistory(id_,api_key):
    with open(r"api_json.json","r") as read:
        my_json=json.load(read)
    if id_ in my_json.keys():
        if my_json[id_]==api_key:
            with open(r'chat_history.pkl', 'rb') as f:
                chatlist = pickle.load(f)
            return {"ChatHistory":chatlist}
    return "Some Error Occurs Cheak Your Id and API KEY"
@app.route("/msghistory/<id_>/<api_key>/<msg_id>")
def ChatHistory_by_id(id_,api_key,msg_id):
    with open(r"api_json.json","r") as read:
        my_json=json.load(read)
    if id_ in my_json.keys():
        if my_json[id_]==api_key:
            with open(r'chat_history.pkl', 'rb') as f:
                chatlist = pickle.load(f)
            try:
                return {f"ChatHistory for Message id {msg_id}":chatlist[int(msg_id)]}
            except:
                return f"ChatHistory for Message id {msg_id} is not avilable Cheack your id"
    return "Some Error Occurs Cheak Your Id and API KEY"
app.run()
