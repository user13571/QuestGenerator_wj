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

@app.route('/load_model',methods=['POST','GET'])
def load_model():
    if request.method=='POST':
        content=request.get_json(silent=True)
        path=content['path']
        global model
        model.load_state_dict(torch.load(path,map_location=torch.device('cpu')))
        model.eval()
        return "success"

@app.route('/quest_gen',methods=['GET','POST'])
def quest_gen():
    global tok, model
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
        sent=tok.batch_decode(model.generate(input_ids, do_sample=True, top_p=0.6, max_length=1024),skip_special_tokens=True)[0]
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
        input_sentence=content['input_sentence']
        print(input_sentence)
        sent=sentence_generate(input_sentence, content)
        return sent

def sentence_generate(sent, content):
    global tok, model
    input_ids=tok(['[BOS] '+sent+' [EOS]'],return_tensors='pt')['input_ids']
    opt_int=['num_return_sequences','num_beams','no_repeat_ngam_size','top_k','min_length']
    opt_float=['temperature','repetition_penalty','top_p']
    opt_bool=['do_sample']
    opt_str=[]
    optionList={'max_length':1024}
    for k,v in content.items():
        print(k)
        if k in opt_int:
            optionList[k]=int(v)
        elif k in opt_bool:
            print(k+v)
            if v=="True":
                optionList[k]=True
            else:
                optionList[k]=False
        elif k in opt_str:
            optionList[k]=str(v)
        elif k in opt_float:
            optionList[k]=float(v)
    gen=model.generate(input_ids, **optionList)
    sent=tok.batch_decode(gen,skip_special_tokens=True)
    print(sent)
    return sent[0]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000)