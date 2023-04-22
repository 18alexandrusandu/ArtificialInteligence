from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import time

hostName = "localhost"
serverPort = 8080
from FOL import *
import re
import json
import os
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("path of request is:" ,self.path)
        result= re.search("/messages",self.path)
        if(not result==None):
            map1={"fol":build_dict_from_messages(),
                  "texts": build_dict_from_texts()}
            reset_page()
            json_string =json.dumps(map1)
            # print json_string
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
            self.send_header('Access-Control-Allow-Headers',"Content-Type")
            self.end_headers()
            self.wfile.write(json_string.encode(encoding='utf_8'))
            return

        else:
            result = re.search("/bombs", self.path)
            if (not result == None):
                map1 = {"obstacol":build_dict_from_obst()}
                json_string=json.dumps(map1)
                # print json_string
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header('Access-Control-Allow-Origin', "*")
                self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                self.end_headers()
                self.wfile.write(json_string.encode(encoding='utf_8'))

                return
            else:
             result= re.search("/safe/i=(\d+),j=(\d+)", self.path)
             if not result==None:
               i=int(result.group(1))
               j=int(result.group(2))
               print("search safe at:",i,j)
               ok=False
               safe=check_safe(i,j)

               if not safe:
                 mine=check_prop(i,j)
                 if mine==False:
                     ok=True
               else:
                ok= True
               if ok:
                   map1 = {"safe":"true"}
                   set_safe(i,j)
                   json_string = json.dumps(map1)
                   print json_string
                   self.send_response(200)
                   self.send_header("Content-Type", "application/json")
                   self.send_header('Access-Control-Allow-Origin', '*')
                   self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                   self.send_header('Access-Control-Allow-Headers', "Content-Type")
                   self.end_headers()
                   self.wfile.write(json_string.encode(encoding='utf_8'))
                   return
               else :
                   map1 = {"safe": "false"}
                   json_string = json.dumps(map1)
                   print json_string
                   self.send_response(200)
                   self.send_header("Content-Type", "application/json")
                   self.send_header('Access-Control-Allow-Origin', '*')
                   self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                   self.send_header('Access-Control-Allow-Headers', "Content-Type")
                   self.end_headers()
                   self.wfile.write(json_string.encode(encoding='utf_8'))
                   return

             else:
                result = re.search("/message/i=(\d+),j=(\d+)", self.path)
                if not result == None:
                    i = result.group(1)
                    j = result.group(2)
                    print("add message at:",i,j)
                    grab_message(int(i),int(j),msgs,text)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                    self.send_header('Access-Control-Allow-Headers', "Content-Type")
                    self.end_headers()
                    map1 = {"message_position": "(" + str(i) + "," + str(j) + ")"}
                    json_string = json.dumps(map1)
                    self.wfile.write(json_string.encode(encoding='utf_8'))
                    return

                else:
                    result = re.search("/visited/i=(\d+),j=(\d+)", self.path)
                    if not result == None:
                        i = int(result.group(1))
                        j = int(result.group(2))
                        print("visited position:", i, j)
                        visited.set_state(i,j,1)
                        set_visited_fol(i,j,assunptions_ruler)
                        # print("visited:",visited.locations)
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                        self.send_header('Access-Control-Allow-Headers', "Content-Type")
                        self.end_headers()
                        map1 = {"visited_position": "(" +str(i)+","+str(j)+")"}
                        json_string = json.dumps(map1)
                        self.wfile.write(json_string.encode(encoding='utf_8'))
                        return

                    else:
                        result = re.search("/won", self.path)
                        if not result == None:
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json")
                            self.send_header('Access-Control-Allow-Origin', '*')
                            self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                            self.send_header('Access-Control-Allow-Headers', "Content-Type")
                            self.end_headers()

                            if check_win(assunptions_ruler):

                                map1 = {"win": "true"}
                                json_string = json.dumps(map1)
                                self.wfile.write(json_string.encode(encoding='utf_8'))
                                return
                            else:
                                map1 = {"win": "false"}
                                json_string = json.dumps(map1)
                                self.wfile.write(json_string.encode(encoding='utf_8'))
                                return
                        else:
                            result = re.search("/lose", self.path)
                            if not result == None:
                                self.send_response(200)
                                self.send_header("Content-Type", "application/json")
                                self.send_header('Access-Control-Allow-Origin', '*')
                                self.send_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PUT, PATCH, DELETE')
                                self.send_header('Access-Control-Allow-Headers', "Content-Type")
                                self.end_headers()
                                if check_lose(assunptions_ruler):
                                  map1 = {"lost": "true"}
                                  json_string = json.dumps(map1)
                                  self.wfile.write(json_string.encode(encoding='utf_8'))
                                  return
                                else:
                                  map1 = {"lost": "false"}
                                  json_string = json.dumps(map1)
                                  self.wfile.write(json_string.encode(encoding='utf_8'))
                                  return
                            else:
                                result = re.search("/set_mine/i=(\d+),j=(\d+)", self.path)
                                if not result == None:
                                    i = int(result.group(1))
                                    j = int(result.group(2))
                                    print("mine position:", i, j)
                                    visited.set_state(i, j, 1)
                                    set_obst(i, j)
                                    self.send_response(200)
                                    self.send_header("Content-Type", "application/json")
                                    self.send_header('Access-Control-Allow-Origin', '*')
                                    self.send_header('Access-Control-Allow-Methods',
                                                     'HEAD, GET, POST, PUT, PATCH, DELETE')
                                    self.send_header('Access-Control-Allow-Headers', "Content-Type")
                                    self.end_headers()
                                    map1 = {"mine_position": "(" + str(i) + "," + str(j) + ")"}
                                    json_string = json.dumps(map1)
                                    self.wfile.write(json_string.encode(encoding='utf_8'))
                                    return
                                else:
                                   result = re.search("/reset", self.path)
                                   if not result == None:
                                    reset_game_new_game()                            
                                    self.send_response(200)
                                    self.send_header("Content-Type", "application/json")
                                    self.send_header('Access-Control-Allow-Origin', '*')
                                    self.send_header('Access-Control-Allow-Methods',
                                                     'HEAD, GET, POST, PUT, PATCH, DELETE')
                                    self.send_header('Access-Control-Allow-Headers', "Content-Type")
                                    self.end_headers()
                                    map1 = {"reseted":"ok"}
                                    json_string = json.dumps(map1)
                                    self.wfile.write(json_string.encode(encoding='utf_8'))
                                    return



        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path))
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path))
        self.wfile.write(bytes("<body>"))
        self.wfile.write(bytes("<p>This is an example web server.</p>"))
        self.wfile.write(bytes("</body></html>"))

from sys import argv
import os
import random









def process_argv():

  for option in argv:
     if option=="-b":
         path= argv[argv.index(option)+1]
         load_obstacles(path,obst)
     if option=="-m":
         path= argv[argv.index(option)+1]
         load_messages(path,msgs, text) 
     if option=="-v":
         version= argv[argv.index(option)+1]
         ver_result=choce_random_game_version(version)
         load_messages(ver_result[1],msgs, text)  
         load_obstacles(ver_result[0],obst)  
         
         
         
def choce_random_game_version(ver=None):

 file_dir_path=os.path.dirname(os.path.realpath("__file__"))
 g_dir="/games_configurations"
 files1=os.listdir("."+g_dir)
 #bomb
 r = re.compile("bombs(.*)")
 files=filter(r.match,files1)
 print(files)
 #versions of games
 versions=map(r.search,files)
 versions2=[]
 for v in versions:
  versions2.append(v.group(1))
 print(versions2)

  #choose a random version
 paths=[]
 if ver==None:
   version=versions2[int(random.random()*(len(versions2)-1))]
   print("Your chosen version is:",version)
   paths=[file_dir_path+g_dir+"/bombs"+version,file_dir_path+g_dir+"/messages"+version]
 else:
   paths=[file_dir_path+g_dir+"/bombs"+ver,file_dir_path+g_dir+"/messages"+ver]
   print("Your chosen version is:",ver)
 
 print(paths)
 return paths


def reset_game_new_game():
    version=choce_random_game_version()
    load_messages(version[1], msgs, text)
    load_obstacles(version[0], obst)
    
    process_argv()
    setup_assumptions_mine_fol()
    setup_assumptions_rule_maker()


         

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    #random setup for game
    reset_game_new_game()
 
   
    #run_game(8, visited, obst, msgs, text)




    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
