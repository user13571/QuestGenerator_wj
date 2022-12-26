from flask import Flask, request, render_template
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import BartConfig
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
from place2key import return_keys_random
import torch
app = Flask(__name__)



tok = AutoTokenizer.from_pretrained("./models/kobart-myTokenizer")
from transformers import BartConfig
config=BartConfig.from_pretrained("./models/kobart-myTokenizer")
model = BartForConditionalGeneration(config=config)

model.load_state_dict(torch.load('./models/kobart-myModel-positive.bin',map_location=torch.device('cpu')))
model.eval()


@app.route('/quest_gen',methods=['GET','POST'])
def quest_gen():
    if request.method=='POST':
        content=request.get_json(silent=True)
        place=content['keywords']
        k_place, k_space, k_object, k_action, k_location, k_time, k_place_modify, k_add =return_keys_random(place)
        if k_object!='0':
            sent=f'[BOS] [STYLE1] [MASK][ADNOM] {k_place}[PLACE] [MASK][ADVERB] [MASK][ADNOM] {k_object}[OBJECT] {k_action}[VERB] [/STYLE] [EOS]'
        else:
            sent=f'[BOS] [STYLE1] [MASK][ADNOM] {k_place}[PLACE] [MASK][ADVERB] {k_action}[VERB] [/STYLE] [EOS]'
        print(sent)
        
        input_ids=tok([sent],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(style_model.generate(input_ids, do_sample=True, top_p=0.6, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]
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
        sent=input_gen(content['k_place'],content['k_object'],content['k_action'],content['option'])
        input_ids=tok([sent],return_tensors='pt')['input_ids']
        sent=tok.batch_decode(model.generate(input_ids,num_beams=2,no_repeat_ngram_size=3, do_sample=True,temperature=1.2, top_p=0.9, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]
        return sent

def input_gen(place, obj, action, opt):
    sent=""
    if opt==1:
        if obj!='':
            sent=f'[BOS] [ADNOM] {place}[PLACE] [ADVERB] [ADNOM] {obj}[OBJECT] {action}[VERB] [EOS]'
        else:
            sent=f'[BOS] [ADNOM] {place}[PLACE] [ADVERB] {action}[VERB] [EOS]'
    elif opt==2:
        if obj!='':
            sent=f'[BOS] [STYLE1] [ADNOM] {place}[PLACE] [ADVERB] [ADNOM] {obj}[OBJECT] {action}[VERB] [/STYLE] [EOS]'
        else:
            sent=f'[BOS] [STYLE1] [ADNOM] {place}[PLACE] [ADVERB] {action}[VERB] [/STYLE] [EOS]'
    elif opt==3:
        if obj!='':
            sent=f'[BOS] [STYLE1] [MASK][MASK][MASK] {place}[PLACE] [MASK][MASK][MASK] {obj}[OBJECT] {action}[VERB] [/STYLE] [EOS]'
        else:
            sent=f'[BOS] [STYLE1] [MASK][MASK][MASK] {place}[PLACE] [MASK][MASK][MASK] {action}[VERB] [/STYLE] [EOS]'
    else:
        if obj!='':
            sent=f'[BOS] [STYLE2] [MASK][MASK][MASK] {place}[PLACE] [MASK][MASK][MASK] {obj}[OBJECT] {action}[VERB] [/STYLE] [EOS]'
        else:
            sent=f'[BOS] [STYLE2] [MASK][MASK][MASK] {place}[PLACE] [MASK][MASK][MASK] {action}[VERB] [/STYLE] [EOS]'
    return sent

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)