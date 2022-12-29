const decodeSelect = (target) => {
    let opt1=document.getElementById("optSelect");
    console.log(target.value);
    if (target.value==="opt_1_greedy"){
        opt1.innerHTML='<span class="opt_n">do_sample</span><span><input style="width: 5em;" class="opt_v" type="text" value="" placeholder="False" disabled></span>&nbsp;';
    }
    else if (target.value==="opt_2_beam"){
        opt1.innerHTML= '<span class="opt_n">do_sample</span><span><input type="text" placeholder="False" value="" class="opt_v" style="width: 5em;" disabled></span>&nbsp;\
<span class="opt_n">num_beams</span><span><input type="number" class="opt_v"  style="width: 5em;" value="3"></span>&nbsp;';
    }
    else{
        opt1.innerHTML= '<span class="opt_n">do_sample</span><span><input class="opt_v" type="text" value="True" style="width: 5em;" disabled></span>&nbsp;\
<span class="opt_n">top_k</span><span><input class="opt_v" type="number" style="width: 5em;" value="25"></span>&nbsp;\
<span class="opt_n">top_p</span><span><input class="opt_v" type="number" style="width: 5em;" value="0.9"></span>&nbsp;';
    }
}

const getOptionVal = () => {
    let optionList={};
    let opt_name=document.getElementsByClassName("opt_n");
    let opt_val=document.getElementsByClassName("opt_v");
    for (let i=0; i<opt_name.length ; i++){
        console.log((opt_name[i].innerText)+opt_val[i].value);
        optionList[opt_name[i].innerText]=opt_val[i].value;
    }
    return optionList;
}

model_loaded=0;
async function loadModel() {
    let model=document.getElementById("type_model");
    let path=''
    if (model.value==="model_1") {
        path='./models/kobart_model_1.bin'
    }
    else if (model.value=="model_2"){
        path='./models/kobart_model_2_positive.bin'
    }
    const btn=document.getElementById('btn_loadModel');
    data={};
    data['path']=path;
    const responce = await fetch('/load_model', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    btn.innerText='로딩중...';
    btn.disabled=true;
    const result=await responce.text();
    btn.disabled=false;
    btn.innerText='로딩 됨'
    model_loaded=1;
}

const getTypeVal = () => {
    const quest_type=document.getElementById('type_quest');
    const style_type=document.getElementById('type_style');
    const place=document.getElementById('k_place').value;
    const obj=document.getElementById('k_object').value;
    const act=document.getElementById('k_action').value;
    
    let c1="";
    let c2="";
    let c3="";

    let o1="";
    let o2="";
    let o3="";
    console.log(place);
    if (place!=""){
        c1=`${place}[PLACE] `;
        o1='[ADNOM] ';
    }
    console.log(place);
    
    if (obj!=""){
        c2=`${obj}[OBJECT] `;
        o2='[ADNOM] ';
    }
    if (act!=""){
        c3=`${act}[VERB] `;
        o3='[ADVERB] ';
    }

    let input="";
    if (quest_type.value=="quest_2_free"){
        o1='[MASK][MASK] ';
        o2='[MASK][MASK] ';
        o3='[MASK][MASK] ';
    }
    else if (quest_type.value=="quest_2_long"){
        o1='[MASK][MASK][MASK][MASK] ';
        o2='[MASK][MASK][MASK][MASK] ';
        o3='[MASK][MASK][MASK][MASK] ';
    }
    input=o1+c1+o3+o2+c2+c3;

    sentence=input;
    if (style_type.value==="style_2_enfp")
        sentence='[STYLE1] '+input+' [/STYLE]';
    else if (style_type.value==="style_3_oldKing")
        sentence='[STYLE2] '+input+' [/STYLE]';        
    else if (style_type.value==="style_4_robot")
        sentence='[STYLE3] '+input+' [/STYLE]';
    else if (style_type.value==="style_5_old")
        sentence='[STYLE4] '+input+' [/STYLE]';
    console.log(sentence);
    return sentence;
}

async function makeSentence(){
    if (model_loaded===0){
        await loadModel();
    }
    let optionList=getOptionVal();
    let input=getTypeVal();
    console.log(input);
    optionList['input_sentence']=input;
    const newSent=document.getElementById('result').insertRow(0);
    newSent.innerText='생성중...';
    const responce = await fetch('/quest_gen_web', {
        method: 'POST',
        body: JSON.stringify(optionList),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
        }
    });
    const result=await responce.text();
    newSent.innerText=result;
}