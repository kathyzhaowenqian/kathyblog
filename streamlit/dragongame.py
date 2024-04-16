import streamlit as st
from openai import OpenAI
 # import numpy as np
import json
import anthropic
import random
import os
from datetime import timedelta
from minio import Minio
import json


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kathyblog.local_settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kathyblog.publish_settings')

# from img_compare import img_compare_dict
from django.conf import settings

# from config.LLM_API import *
# def main():

minio_url = settings.MINIO_URL
# st.image(image='{minio_url}/defeatant/3.png')

#--------------------------------------------
APIKEY=settings.APIKEY_OPENAI
ORGANIZATION = settings.ORGANIZATION_OPENAI
client1=OpenAI(organization=ORGANIZATION,api_key=APIKEY)

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=settings.APIKEY_CLAUDE,
)
#----------------------
MINIO_STORAGEENDPOINT =settings.MINIO_STORAGE_ENDPOINT
MINIO_STORAGE_ACCESSKEY = settings.MINIO_STORAGE_ACCESS_KEY
MINIO_STORAGE_SECRETKEY=settings.MINIO_STORAGE_SECRET_KEY
MinioClient = Minio(MINIO_STORAGEENDPOINT,
    access_key=MINIO_STORAGE_ACCESSKEY,
    secret_key=MINIO_STORAGE_SECRETKEY,
    secure=False
)
bucket='dragongame'
SCENE_ORDER='''按顺序：
        1. 绿油油的田野;
        2. 森林;
        3. 森林深处的城堡;'''

eg='{"场景":"森林"}'
eg2='{"场景":""}'


SYSTEM_PROMPT_TEMPLATE = f'''
你是只返回json格式的机器人
    
'''  

SCENE='''依次按如下场景:
1. 绿油油的田野: 该场景中没有任何宝藏。一次只遇到一只小怪, 可能遇到小蚂蚁怪或者坏老鼠怪。
2. 森林:该场景中可能遇到小怪或者宝藏，可能遇到的小怪有：有黄鼠狼、毒蛇机、老鹰；可能捡到的宝藏有：苹果干、大门牙、笼子。
3. 森林深处的城堡: 该场景中遇到恶龙王或者捡到宝藏, 概率各50%。若捡到宝藏,其中:捡到苹果干机率80%,捡到大门牙机率70%,捡到笼子机率70%'''

SCENE_CHOICE='''
依次按如下场景:
1,绿油油的田野; 2,森林; 3,森林深处的城堡;
'''

ENDINGS='''
1. 完美结局:阿呆进入了森林深处的城堡,打败了恶龙王,拯救阿瓜,开心的生活再一起。游戏结束。
2. 失败结局:阿呆属性值不足以打败小怪或者恶龙王,阿呆战败被吃掉,阿瓜被恶龙王吃掉。游戏结束。
3. 普通结局: 阿呆一直在田野或者森林中,说明阿呆没有找到正确的路线前往城堡, 阿呆永远迷失在田野或者森林中。阿瓜被恶龙王吃掉了。游戏结束。
'''





def battle(bucket,current_scene,current_monster,adai, monster):
    while adai["HP"] > 0 and monster["HP"] > 0:
        deltaHP_MONSTER = max(0, adai["ATTACK"] - monster["DEFENCE"])
        monster["HP"] -= deltaHP_MONSTER
        if monster["HP"]<=0:
            break
        deltaHP_ADAI = max(0, monster["ATTACK"] - adai["DEFENCE"])
        adai["HP"] -= deltaHP_ADAI
        if adai["HP"]<=0:
            break
    if adai["HP"] <= 0:
        if current_scene=="绿油油的田野" and current_monster=="坏老鼠怪":
            # img_path="streamlit/dragongame_images/lose_rat"
            folder_name='lose-rat'
        # elif current_scene=="绿油油的田野" and current_monster=="小蚂蚁怪":
        #     img_path="streamlit/dragongame_images/lose_ant"
        elif current_scene=="森林" and current_monster=="黄鼠狼":
            # img_path="streamlit/dragongame_images/lose_weasel"
            folder_name='lose-weasel'
        elif current_scene=="森林" and current_monster=="老鹰":
            # img_path="streamlit/dragongame_images/lose_eagle"
            folder_name='lose-eagle'
        elif current_scene=="森林" and current_monster=="毒蛇":
            # img_path="streamlit/dragongame_images/lose_snake"
            folder_name='lose-snake'
        elif current_scene=="森林深处的城堡" and current_monster=="恶龙王":
            # img_path="streamlit/dragongame_images/lose_dragon"
            folder_name='lose-dragon'
        else:
            # img_path="streamlit/dragongame_images/get_lost"
            folder_name='get-lost'
        full_img_path=image(bucket,folder_name)
 
        if current_monster=="恶龙王":
            st.session_state['is_end']=True
        else:
            #被其他小怪打败
            st.session_state['is_end_small']=True
        return full_img_path,adai,f"阿呆战败, 游戏结束。阿呆被{current_monster}吃掉了, 阿瓜最终也被恶龙王吃掉了。游戏结束。需要刷新浏览器重启游戏。"
    else:
        addexp=monster["exp"]
        adai["exp"]+=addexp
        if adai["exp"]>=10 and adai["exp"]<20:
            lv=1
        elif adai["exp"]>=20 and adai["exp"]<40:
            lv=2
        elif adai["exp"]>=40 and adai["exp"]<60:
            lv=3
        elif adai["exp"]>=60 and adai["exp"]<80:
            lv=4
        elif adai["exp"]>=80:
            lv=5
        else:
            lv=0
        deltalv= lv-adai["lv"]
        print('deltalv',deltalv)
        if current_scene=="绿油油的田野" and current_monster=="小蚂蚁怪":
            # img_path="streamlit/dragongame_images/defeat_ant"
            folder_name='defeat-ant'
        elif current_scene=="绿油油的田野" and current_monster=="坏老鼠怪":
            # img_path="streamlit/dragongame_images/defeat_rat"
            folder_name='defeat-rat'
        elif current_scene=="森林" and current_monster=="黄鼠狼":
            # img_path="streamlit/dragongame_images/defeat_weasel"
            folder_name='defeat-weasel'
        elif current_scene=="森林" and current_monster=="老鹰":
            # img_path="streamlit/dragongame_images/defeat_eagle"
            folder_name='defeat-eagle'
        elif current_scene=="森林" and current_monster=="毒蛇":
            # img_path="streamlit/dragongame_images/defeat_snake"
            folder_name='defeat-snake'
        elif current_scene=="森林深处的城堡" and current_monster=="恶龙王":
            # img_path="streamlit/dragongame_images/defeat_dragon"
            folder_name='defeat-dragon'
        else:
            # img_path="streamlit/dragongame_images/get_lost"
            folder_name='get-lost'
        full_img_path=image(bucket,folder_name)
        if deltalv > 0:
            adai["lv"]=lv
            adai["HP"]=adai["HP"]*2**deltalv
            adai["ATTACK"]=adai["ATTACK"]*2**deltalv
            adai["DEFENCE"]=adai["DEFENCE"]*2**deltalv
            if current_monster=="恶龙王":
                st.session_state['is_win']=True
                return full_img_path,adai,f"阿呆成功打败了{current_monster},阿呆经验值加{addexp},升级为{lv},属性值乘以{deltalv},阿呆最新的属性为:{adai},阿呆获得了胜利，解救了阿瓜，完美结局。"
            else:
                return full_img_path,adai,f"阿呆成功打败了{current_monster},阿呆经验值加{addexp},升级为{lv},属性值乘以{deltalv},阿呆最新的属性为:{adai}"

        else:  
            if current_monster=="恶龙王":  
                st.session_state['is_win']=True
                return full_img_path,adai,f"阿呆成功打败了{current_monster},阿呆经验值加{addexp},阿呆最新的属性为:{adai}，阿呆获得了胜利，解救了阿瓜，完美结局。"
            else:
                return full_img_path,adai,f"阿呆成功打败了{current_monster},阿呆经验值加{addexp},阿呆最新的属性为:{adai}"

    
monster_group={
            "小蚂蚁怪": {"HP":1, "ATTACK":1, "DEFENCE":0, "exp":10},
                "坏老鼠怪":{ "HP":2, "ATTACK":2, "DEFENCE":0, "exp": 12}, 
                "黄鼠狼":{"HP":5, "ATTACK":5, "DEFENCE":1, "exp":15}, 
                "毒蛇": {"HP":10, "ATTACK":8, "DEFENCE":5, "exp":20}, 
                "老鹰":{"HP":20, "ATTACK":10, "DEFENCE":10, "exp":30},
                "恶龙王":{"HP":100, "ATTACK":20, "DEFENCE":20,"exp":100}
            }

def treasure(bucket,current_treasure,adai_current_profile):
    if current_treasure=='苹果干':
        adai_current_profile['HP']+=20
        adai=adai_current_profile
        # img_path="streamlit/dragongame_images/pick_apple"
        folder_name='pick-apple'
        full_img_path=image(bucket,folder_name)
        return full_img_path,adai,f'{current_treasure}可以补充阿呆能量, 让阿呆的HP增加20点, 阿呆更新属性为:{adai_current_profile}，阿呆变得更加强壮。'

    elif current_treasure=='大门牙':
        adai_current_profile['ATTACK']+=10
        adai=adai_current_profile
        # img_path="streamlit/dragongame_images/pick_teeth"
        folder_name='pick-teeth'
        full_img_path=image(bucket,folder_name)
        return full_img_path,adai,f'{current_treasure}可以增加阿呆的攻击力, 让阿呆的ATTACK增加10点, 阿呆更新属性为::{adai_current_profile}。'

    elif current_treasure=='笼子':
        adai_current_profile['DEFENCE']+=5
        adai=adai_current_profile
        # img_path="streamlit/dragongame_images/pick_cage"
        folder_name='pick-cage'
        full_img_path=image(bucket,folder_name)
        return full_img_path,adai,f'{current_treasure}可以保护阿呆被小怪攻击, 让阿呆的DEFENCE增加5点, 阿呆更新属性为::{adai_current_profile}。'

    else:
        adai=adai_current_profile
        # img_path="streamlit/dragongame_images/get_lost"
        folder_name='get-lost'
        full_img_path=image(bucket,folder_name)
        return adai,f'该宝藏没有用,阿呆的属性依然是::{adai_current_profile}'       

def GET_MONSTER_OR_TREASURE(next_scene):
    if next_scene=='绿油油的田野':
        monster_field = [{"场景":"绿油油的田野","小怪":"小蚂蚁怪","宝藏":""},{"场景":"绿油油的田野","小怪":"坏老鼠怪","宝藏":""}]
        monster_field_weights = [0.5,0.5]
        selected_data = random.choices(monster_field, monster_field_weights, k=1)
        return selected_data[0]
    
    elif next_scene=='森林':
        example1={"场景":"森林","小怪":"黄鼠狼","宝藏":""}
        example2={"场景":"森林","小怪":"毒蛇","宝藏":""}
        example3={"场景":"森林","小怪":"老鹰","宝藏":""}
        example4={"场景":"森林","小怪":"","宝藏":"苹果干"}
        example5={"场景":"森林","小怪":"","宝藏":"笼子"}
        example6={"场景":"森林","小怪":"","宝藏":"大门牙"}
        monster_forest = [example1,example2,example3,example4,example5,example6]
        monster_forest_weights = [0.3,0.2,0.2,0.1,0.1,0.1]
        selected_data = random.choices(monster_forest, monster_forest_weights, k=1)
        return selected_data[0]
    elif next_scene=='森林深处的城堡':
        example1={"场景":"森林深处的城堡","小怪":"恶龙王","宝藏":""}
        example2={"场景":"森林深处的城堡","小怪":"","宝藏":"苹果干"}
        example3={"场景":"森林深处的城堡","小怪":"","宝藏":"笼子"}
        example4={"场景":"森林深处的城堡","小怪":"","宝藏":"大门牙"}
        monster_castle = [example1,example2,example3,example4]
        monster_castle_weights = [0.7,0.1,0.1,0.1]
        selected_data = random.choices(monster_castle, monster_castle_weights, k=1)
        return selected_data[0]
    else:
        return {"场景":next_scene,"小怪":"","宝藏":""}
    
def image(bucket,folder_name):
    # jpg_files = [f for f in os.listdir(img_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    # random_file = random.choice(jpg_files)
    # full_file_path = os.path.normpath(os.path.join(img_path, random_file))
    # return full_file_path
    objects = MinioClient.list_objects(bucket,prefix=folder_name, recursive=True)
    random_obj = random.choice(list(objects))
    random_file=random_obj.object_name
    print(random_file)
    full_file_path = f'{minio_url}/{bucket}/{random_file}'
    return full_file_path


if 'rows' not in st.session_state:
    st.session_state['rows'] = 0
    # st.session_state['tmp_messages']=[{"role": "system", "content":SYSTEM_PROMPT_TEMPLATE}]
    st.session_state['tmp_messages']=[{"role": "system", "content":SYSTEM_PROMPT_TEMPLATE}]
    st.session_state["adai_current_profile"]= {"HP":10, "ATTACK":1, "DEFENCE": 1, "exp":0, "lv":0}
    st.session_state["scene_monster_treasure"]={"场景":"绿油油的田野","小怪":"","宝藏":""}
    st.session_state['image_list']=[]
    st.markdown(''' **龙猫阿呆斗恶龙**
                
你是小龙猫阿呆🐹，你的好友阿瓜公主👸被邪恶的龙王🐲抓走关进了森林深处的城堡🏰！
                
为了拯救她，你需要穿越田野🌾和森林🌲，与小怪👾战斗，不断提升自己的力量⚔️，最终前往城堡🏰挑战恶龙王🐲，解救被困的阿瓜公主👸！
            ''')

    st.markdown('对话框在 :red[最下方哦~] 👇👇👇')
    # st.image('streamlit/dragongame_images/gamehead.jpg') 
    st.image(f'{minio_url}/dragongame/gamehead.jpg')
    st.session_state['messages']=[{"role": "assistant", "content":'阿呆，你现在正在一片广阔的田野中，如果想在田野里历练自己，请输入:"留在田野"；如果你想进入森林探索，请输入："前往森林"。'}]
    st.session_state['is_end']=False
    st.session_state['is_end_small']=False
    st.session_state['is_win']=False



def GPT_RESPONSE(messages):
    completion = client1.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return completion.choices[0].message.content
    


# session_state_messages = st.session_state['messages']
for i in range(0,len(st.session_state['messages'])):
    j=st.session_state['messages'][i]
    if (isinstance(j, dict) and j.get('role') in ['assistant', 'user']):
        # print('j:::::',j)
        if j.get('role')=='user':
            with st.chat_message(j['role'],avatar=f'{minio_url}/dragongame/adaihead.png'):
                st.write(j['content'])
        if j.get('role')=='assistant':      
            with st.chat_message("assistant",avatar=f'{minio_url}/dragongame/aguahead.png'):#,avatar='龙猫.png'
                st.write(j['content'])
                selected_image=[d for d in st.session_state['image_list'] if i in d]
                # print('selected_image',selected_image)
                if selected_image:
                    imagename=selected_image[0][i]
                    st.image(imagename)

user_prompt = st.chat_input(placeholder="请输入问题",key="user_prompt")#,on_submit=submit_action)

if user_prompt:
    
    st.session_state['messages'].append({"role": "user", "content": user_prompt})
    st.session_state["rows"] += 1

    with st.chat_message('user',avatar=f'{minio_url}/dragongame/adaihead.png'):
        st.write(user_prompt)

    with st.chat_message('assistant',avatar=f'{minio_url}/dragongame/aguahead.png'):
        container1=st.container()
        # container2=st.container()
        with container1:
            placeholder = st.empty()
            response_message = ''

            with st.spinner('正在努力思考'):
                #调用选择小怪或者宝藏的prompt {"场景":"绿油油的田野","小怪":"小蚂蚁怪","宝藏":""}
                current_scene=st.session_state["scene_monster_treasure"]["场景"]
                print('current_scene',current_scene,type(current_scene))
   
                #st.session_state['tmp_messages'] 仅仅作记录
                st.session_state['tmp_messages'].append({"role": "user", "content":f" 场景选择:{SCENE_ORDER},当前场景是:{current_scene},用户的选择是:{user_prompt}。\
                    你需要根据上述场景顺序, 当前的场景以及用户的选择,判断用户的选择是否是针对场景的选择(针对场景选择的文字例如:继续,下一步,田野,留在田野,留在田野打小怪,前往森林,前往森林打怪,留在森林,前往城堡,前往森林深处的城堡,留在城堡,去城堡.etc)。\
                    如果用户做出了针对场景的选择,则以json格式返回用户表达的场景,比如:{eg}。value值限定为:绿油油的田野或者森林或者森林深处的城堡\
                    如果用户的选择与场景无关,或者不符合场景信息,则返回:{eg2}。"})
                #一次性的tmp_session_state_messages仅供单次调用
                tmp_session_state_messages=[{"role": "system", "content":SYSTEM_PROMPT_TEMPLATE},{"role": "user", "content":f" 场景选择:{SCENE_ORDER},当前场景是:{current_scene},用户的选择是:{user_prompt}。\
                    你需要根据上述场景顺序, 当前的场景以及用户的选择,判断用户的选择是否是针对场景的选择(针对场景选择的文字例如:继续,下一步,田野,留在田野,留在田野打小怪,前往森林,前往森林打怪,留在森林,前往城堡,前往森林深处的城堡,留在城堡,去城堡.etc)。\
                    如果用户做出了针对场景的选择,则以json格式返回用户表达的场景,比如:{eg}。value值限定为:绿油油的田野或者森林或者森林深处的城堡\
                    如果用户的选择与场景无关,或者不符合场景信息,则返回:{eg2}。"}]
                
              
                response_choice = GPT_RESPONSE(tmp_session_state_messages)
                # '{"场景":"森林"}'
                print('response_choice',response_choice)
                json_response_choice_scene=json.loads(response_choice)
                next_scene=json_response_choice_scene.get('场景')               
                print('next_scene',next_scene,type(next_scene))
                if next_scene:
                    json_response_choice=GET_MONSTER_OR_TREASURE(next_scene)
                else:
                    json_response_choice={"场景":current_scene,"小怪":"","宝藏":""}
                print('json_response_choice',json_response_choice,type(json_response_choice))

                st.session_state["scene_monster_treasure"]=json_response_choice
                current_scene=json_response_choice['场景']
                current_monster=json_response_choice.get('小怪')
                current_treasure=json_response_choice.get('宝藏')
                adai_current_profile= st.session_state["adai_current_profile"]

                print('上一轮的is_end',st.session_state['is_end'])
                print('上一轮的is_end_small',st.session_state['is_end_small'])
                print('上一轮的is_win',st.session_state['is_win'])

                if st.session_state['is_end'] or st.session_state['is_end_small'] or st.session_state['is_win'] :
                    current_monster=''
                    st.session_state["scene_monster_treasure"]['小怪']=current_monster
                    current_treasure=''
                    st.session_state["scene_monster_treasure"]['宝藏']=current_treasure
                
                print('调整后的怪物',current_monster,'调整后的宝藏',current_treasure)

                if current_monster:
                    full_img_path,adai_update_profile,battle_result = battle(bucket,current_scene,current_monster,adai_current_profile, monster_group[current_monster])
                    print('这一轮的is_end',st.session_state['is_end'])
                    print('这一轮的is_end_small',st.session_state['is_end_small'])
                    st.session_state["adai_current_profile"]=adai_update_profile
                    print(battle_result)
                    if st.session_state['is_end']:
                        prompt_template= f'''
                            你是龙猫版本的勇者斗恶龙的文字游戏中的一个环节,你需要直接描述该环节。
                            游戏故事背景:游戏的主人公是一只叫做阿呆的龙猫(由用户扮演),阿呆的好朋友龙猫阿瓜公主被恶龙王抓住,阿呆需要通过打怪、升级,最终打败恶龙王,拯救阿瓜公主,但是阿呆也有可能失败。

                            描述步骤:
                            1,根据目前场景、遇到的小怪、阿呆决斗的结果,整合成该步骤的游戏描述,添加生动的描述语句，直接描述。
                            2,如果阿呆战败，被打败了，那就是失败的结局，游戏结束, 告知用户：如果要重新开始游戏则需要刷新浏览器。
                            描述举例：
                            ```勇敢的阿呆遇到了一只凶猛的小蚂蚁怪。经过激烈的战斗,阿呆最终成功击败了这只小怪物,获得了2点宝贵的经验值。\
                            这次战斗使得阿呆的属性得到了提升,当前属性为:'HP': 10, 'ATTACK': 1, 'DEFENCE': 1, 'exp': 2, 'lv': 0。只有不断通过打怪获取经验、不断升级,阿呆才能最终打败恶龙王。\
                            现在,阿呆需要做出选择 - 是继续留在这片田野探索,还是前往神秘的森林寻找新的挑战? 请输入："留在田野"/"前往森林"
                            ```。
                            全部场景设定:{SCENE_CHOICE};
                            目前场景:{current_scene};
                            遇到的小怪:{current_monster};
                            阿呆决斗的结果:{battle_result};
                            
                            '''
                    elif st.session_state['is_end_small']:
                        prompt_template= f'''
                            你是龙猫版本的勇者斗恶龙的文字游戏中的一个环节,你需要直接描述该环节。
                            游戏故事背景:游戏的主人公是一只叫做阿呆的龙猫(由用户扮演),阿呆的好朋友龙猫阿瓜公主被恶龙王抓住,阿呆需要通过打怪、升级,最终打败恶龙王,拯救阿瓜公主,但是阿呆也有可能失败。
                            全部场景设定:{SCENE_CHOICE};
                            目前场景:{current_scene};
                            遇到的小怪:{current_monster};
                            阿呆决斗的结果:{battle_result};
                            描述步骤:
                            1,根据目前场景、遇到的小怪、阿呆决斗小怪的结果, 整合成该步骤的游戏描述,添加生动的描述语句，直接描述。
                            2,如果阿呆战败，是失败结局，游戏结束, 告知用户：如果要重新开始游戏则需要刷新浏览器。
                            描述举例：
                            ```勇敢的阿呆遇到了一只凶猛的小蚂蚁怪。经过激烈的战斗,阿呆最终成功击败了这只小怪物,获得了2点宝贵的经验值。\
                            这次战斗使得阿呆的属性得到了提升,当前属性为:'HP': 10, 'ATTACK': 1, 'DEFENCE': 1, 'exp': 2, 'lv': 0。只有不断通过打怪获取经验、不断升级,阿呆才能最终打败恶龙王。\
                            现在,阿呆需要做出选择 - 是继续留在这片田野探索,还是前往神秘的森林寻找新的挑战? 请输入："留在田野"/"前往森林"
                            ```。

                            '''                       
                    else:
                        prompt_template= f'''
                            你是龙猫版本的勇者斗恶龙的文字游戏中的一个环节,你需要直接描述该环节。
                            游戏故事背景:游戏的主人公是一只叫做阿呆的龙猫(由用户扮演),阿呆的好朋友龙猫阿瓜公主被恶龙王抓住,阿呆需要通过打怪、升级,最终打败恶龙王,拯救阿瓜公主,但是阿呆也有可能失败。
                            全部场景设定:{SCENE_CHOICE};
                            目前场景:{current_scene};
                            遇到的小怪:{current_monster};
                            阿呆决斗的结果:{battle_result};
                            最终结局设定(选则其一):{ENDINGS};
                            描述步骤:
                            1,根据目前场景、遇到的小怪、阿呆决斗小怪的结果、最终结局设定,整合成该步骤的游戏描述,添加生动的描述语句，直接描述。
                            2,如果阿呆战败，是失败结局，游戏结束, 告知用户：如果要重新开始游戏则需要刷新浏览器。
                            3,如果阿呆打败了小怪,则根据全部场景设定, 询问user是否继续留在该场景中？还是进入下一个场景？规范提问,比如：```请输入："留在田野"/"前往森林"```。 必须让user做二选一的选择(按场景顺序依次为：田野、森林、森林深处的城堡)。如果现在已经在森林深处的城堡里了,那么规范提问：```请输入："留在城堡"/"返回森林"```。
                            描述举例：
                            ```勇敢的阿呆遇到了一只凶猛的小蚂蚁怪。经过激烈的战斗,阿呆最终成功击败了这只小怪物,获得了2点宝贵的经验值。\
                            这次战斗使得阿呆的属性得到了提升,当前属性为:'HP': 10, 'ATTACK': 1, 'DEFENCE': 1, 'exp': 2, 'lv': 0。只有不断通过打怪获取经验、不断升级,阿呆才能最终打败恶龙王。\
                            现在,阿呆需要做出选择 - 是继续留在这片田野探索,还是前往神秘的森林寻找新的挑战? 请输入："留在田野"/"前往森林"
                            ```。

                            '''
                    print('if::::')

                elif current_treasure:
                    full_img_path,adai_update_profile,treasure_result=treasure(bucket,current_treasure,adai_current_profile)
                    st.session_state["adai_current_profile"]=adai_update_profile
                    print(treasure_result)
                    prompt_template= f'''
                            你需要直接描述龙猫版本的勇者斗恶龙的文字游戏中的一个环节, 你需要直接描述这个环节。
                            游戏故事背景:游戏的主人公是一只叫做阿呆的龙猫(由用户扮演),阿呆的好朋友龙猫阿瓜公主被恶龙王抓住,阿呆需要通过打怪、升级,最终打败恶龙王,拯救阿瓜公主,但是阿呆也有可能失败。
                            全部场景设定:{SCENE_CHOICE};
                            目前场景:{current_scene};
                            遇到的宝藏:{current_treasure};
                            阿呆捡到宝藏的结果:{treasure_result};
                            没有遇到小怪。
                            描述步骤:
                            1,你需要根据目前场景、遇到的宝藏、阿呆最新的属性值及结果、整合成该步骤的游戏文字描述,适当添加生动简洁的描述语句。
                            2,根据全部场景设定的及场景顺序,询问user是继续留在该场景中？还是进入下一个场景？, 规范提问,比如：```请输入："留在田野"/"前往森林"```。必须让user做二选一的选择(按场景顺序依次为：田野、森林、森林深处的城堡)。如果现在已经在森林深处的城堡里了,那么规范提问：```请输入："留在城堡"/"返回森林"```
                            描述举例：
                            ```阿呆在森林中前进，突然在树叶下发现了一片苹果干，阿呆开心地捡起苹果干吃了起来。\
                            令阿呆惊喜的是,这片苹果干竟然能够补充阿呆的体力,让阿呆的HP增加了20点,现在阿呆的属性变为:'HP': 52, 'ATTACK': 44, 'DEFENCE': 24, 'exp': 20, 'lv': 2。\
                            阿呆变得能量满满，现在阿呆需要做出选择 - 是继续留在这片森林中探索,还是前往森林深处的城堡寻找新的挑战? 请输入："留在森林"/"前往城堡"
                            ```
                            '''
                    print('elif::::')

                else:  
                    if st.session_state['is_end']:
                        prompt_template= f'''你只可以返回一句话：```本轮游戏已结束，请刷新浏览器重新进入游戏```'''
                        # img_path="streamlit/dragongame_images/lose_dragon"
                        folder_name="lose-dragon"
                    elif st.session_state['is_end_small']:
                        prompt_template= f'''你只可以返回一句话：```本轮游戏已结束，请刷新浏览器重新进入游戏```'''
                        # img_path="streamlit/dragongame_images/lose_general"
                        folder_name="lose-general"
                    elif st.session_state['is_win']:
                        prompt_template= f'''你只可以返回一句话：```本轮游戏已结束，请刷新浏览器重新进入游戏```'''
                        # img_path="streamlit/dragongame_images/defeat_dragon"
                        folder_name="defeat-dragon"
                    else:
                        prompt_template= f'''
                                你是龙猫版本的勇者斗恶龙的文字游戏中的一个场景环节。用户扮演游戏的主人翁龙猫阿呆。需要根据下方需求直接输出答案。
                                1, 结合游戏故事背景,生动地回答用户的问题。你必须直接输出答案，不需要重复问题是什么。 如果问题偏离主题,则不回答，强调游戏主题。
                                2, 询问用户是继续留在该场景中？还是进入下一个场景？用这个规范提问,比如：```请输入："留在田野"/"前往森林"```。 必须让用户做二选一的选择。(按场景顺序依次为：田野、森林、森林深处的城堡)。如果现在已经在最后一个场景了,那么此步骤可省略
                                游戏故事背景:
                                游戏的主人公是一只叫做阿呆的龙猫(由用户扮演),森林深处的城堡中的住着一只恶龙王，阿呆的好朋友龙猫阿瓜公主被恶龙王抓住,阿瓜被囚禁在城堡中。阿呆需要通过打怪、升级,最终打败恶龙王,拯救阿瓜公主,但是阿呆也有可能失败。
                                目前场景:{current_scene};
                                阿呆目前的属性：{adai_current_profile}；                            
                                用户的问题:{user_prompt};
                                example:
                                ```用户的问题:宝藏在哪里？```
                                你需要直接输出：
                                ```宝藏隐藏在森林中，阿呆需要不断战斗、升级才能有力量一步步闯关、才有机会获取宝藏，最终挑战恶龙王。
                                    现在,阿呆需要做出选择 - 是继续留在这片田野探索,还是前往神秘的森林寻找新的挑战? 请输入："留在田野"/"前往森林"。
                                ```
                                '''
                    
                        if current_scene=='绿油油的田野':
                            # img_path="streamlit/dragongame_images/scene_field"
                            folder_name="scene-field"
                        elif current_scene=='森林':
                            # img_path="streamlit/dragongame_images/scene_forest"
                            folder_name="scene-forest"
                        elif current_scene=='森林深处的城堡':
                            # img_path="streamlit/dragongame_images/scene_castle"
                            folder_name="scene-castle"
                        else:
                            # img_path="streamlit/dragongame_images/get_lost"
                            folder_name="get-lost"
                    full_img_path=image(bucket,folder_name)
                    print('else::::')
                        


            with client.messages.stream(
                max_tokens=1024,
                messages=[
                        {"role": "user", "content":prompt_template},
                        ],
                    model="claude-3-haiku-20240307",

                ) as stream:
                for text in stream.text_stream:    
                    response_message += text
                    placeholder.write(response_message) 

        st.session_state['rows'] += 1

        # if os.path.exists(full_img_path):       
        with container1:
            print(full_img_path,type(full_img_path))
            st.image(full_img_path)
            st.session_state['image_list'].append({st.session_state['rows']:full_img_path})
        
    st.session_state['messages'].append({"role": "assistant", "content": response_message})#完整答案录入正规message
    st.session_state['tmp_messages'].append({"role": "assistant", "content": response_choice})

