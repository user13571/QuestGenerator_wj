from flask import Flask, request, render_template
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import BartConfig
from konlpy.tag import Komoran
from soylemma import Lemmatizer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
from place2key import return_keys_random, return_adds
from key2sent_base import quest_generate_strict
from key2sent_add import description_gen
import torch
app = Flask(__name__)



tok = AutoTokenizer.from_pretrained("./models/tok")
from transformers import BartConfig
config=BartConfig.from_pretrained("./models/tok")
model = BartForConditionalGeneration(config=config)

model.load_state_dict(torch.load('./models/bart_final_withoutStyle.bin',map_location=torch.device('cpu')))
model.eval()

style_model = BartForConditionalGeneration(config=config)
style_model.load_state_dict(torch.load('./models/enfp_final_1.bin',map_location=torch.device('cpu')))
style_model.eval()


@app.route('/quest_gen',methods=['GET','POST'])
def quest_gen():
    if request.method=='POST':
        content=request.get_json(silent=True)
        place=content['keywords']
        k_place, k_space, k_object, k_action, k_location, k_time, k_place_modify, k_add =return_keys_random(place)
        sent=f'[BOS] [MASK][ADNOM] {k_place}[PLACE] [MASK][ADVERB] [MASK][ADNOM] {k_object}[OBJECT] {k_action}[VERB] [/STYLE] [EOS]'
        print(sent)
        
        input_ids=tok([sent],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(style_model.generate(input_ids,num_beams=5, do_sample=True, top_p=0.6, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]
        print(sent)
        data={
            'sentence':sent,
            'keys': f'{k_place}*{k_space}*{k_object}*{k_action}*{k_location}*{k_time}*{k_place_modify}*{k_add}'
        }
        send=json.dumps(data)
        send=f'{sent}@{k_place}*{k_space}*{k_object}*{k_action}*{k_location}*{k_time}*{k_place_modify}*{k_add}'
        return send

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/quest_gen_web',methods=['GET','POST'])
def quest_gen_web():
    if request.method=='POST':
        content=request.get_json(silent=True)
        sent=q_gen_final(content['k_place'],content['k_object'],content['k_action'],1)
        input_ids=tok([sent],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(model.generate(input_ids,num_beams=2,no_repeat_ngram_size=3, do_sample=True,temperature=1.5, top_p=0.9, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]
        return sent

def q_gen_final(place,obj,action,choice):
    sent=sent=f'[BOS] [MASK][ADNOM] {place}[PLACE] [MASK][ADVERB] [MASK][ADNOM] {obj}[OBJECT] {action}[VERB]'
    if (choice==1):
        sent+=' [EOS]'
    else:
        sent+=' [/STYLE] [EOS]'
    return sent

@app.route('/quest_gen_web_2',methods=['GET','POST'])
def quest_gen_web_2():
    if request.method=='POST':
        content=request.get_json(silent=True)
        sent=q_gen_final(content['k_place'],content['k_object'],content['k_action'],0)
        input_ids=tok([sent],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(style_model.generate(input_ids,num_beams=2,temperature=1.1, no_repeat_ngram_size=3, do_sample=True, top_p=0.8, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]
        return sent

@app.route('/style', methods=['GET','POST'])
def change_style():
    if request.method=='POST':
        content=request.get_json(silent=True)
        input_ids=tok(['[BOS] '+content['sent']+' [EOS]'],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(style_model.generate(input_ids,no_repeat_ngram_size=3, num_beams=2, do_sample=True, top_p=0.6, max_length=1024, num_return_sequences=1),skip_special_tokens=False)[0]
        print(sent)
        return sent[5:-5].replace('[BOS]','')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)
'''
    test('교실')
    test('갤러리')
    test('쥐라기 파크')
    test('복도')
    test('옥상')
    test('태양계')
'''
