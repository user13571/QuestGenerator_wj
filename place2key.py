'''
key={
    'place': None,
    'object': None,
    'location': None,
    'action': None,
    'time/duration': None,
    'etc1': None,
    'etc2': None,
    'add': None
}
'''
import os
import pandas as pd
import random
def get_place(data, place): # 갤러리
    idx=0
    while len(data)>idx and data.iloc[idx]['장소']!=place:
        idx+=1
    start_i=idx
    while len(data)>idx and  data.iloc[idx]['장소']==place:
        idx+=1
    end_i=idx  # [start,end)
    i=random.randint(start_i,end_i-1)
    print(i)
    print(data.iloc[i])
    raw=data.iloc[i]
    return raw

def return_keys_random(place):
    data=pd.read_csv('./keywordsFolder/KeyList_Fordemo.csv')
    raw=get_place(data,place)
    k=[]
    k.append(raw['장소'])
    k.append(raw['공간'])
    k.append(raw['대상'])
    k.append(raw['행동'])
    k.append(raw['위치'])
    k.append(raw['횟수/시간'])
    k.append('0')
    k.append('0')
    return k

def return_adds(place):
    add_base=['재미있는게 많#','즐거#','놀기 좋#','좋#','멋지#', '같이 #']
    add_more=[]
    if place=='교실':
        add_more=['즐거운']
    elif place=='쥐라기 파크':
        add_more=['멋진 공룡이 있#']
    elif place=='도서관':
        add_more=['# 책이 많#','# 이야기가 가득#', '흥미진진#', '# 책을 읽#']
    elif place=='갤러리':
        add_more=['# 그림이 있#','# 이야기가 #', '흥미진진#','멋진 그림을 보#']

    add_base.extend(add_more)
    return add_base

## (raw + add) & action_original 돌려줌
