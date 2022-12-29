const decodeSelect = (target) => {
    let opt1=document.getElementById("optSelect");
    if (target.value==="opt_greedy"){
        opt1.innerHTML='<td class="opt_n">do_sample</td><td><input style="width: 5em;" class="opt_v" type="text" value="" placeholder="False" disabled></td>';
    }
    else if (target.value==="opt_beam"){
        opt1.innerHTML= '<td class="opt_n">do_sample</td><td><input type="text" placeholder="False" value="" class="opt_v" style="width: 5em;" disabled></td>\
<td class="opt_n">num_beams</td><td><input type="number" class="opt_v"  style="width: 5em;" value="3"></td>';
    }
    else{
        opt1.innerHTML= '<td class="opt_n">do_sample</td><td><input class="opt_v" type="text" value="True" style="width: 5em;" disabled></td>\
<td class="opt_n">top_k</td><td><input class="opt_v" type="number" style="width: 5em;" value="10"></td>\
<td class="opt_n">top_p</td><td><input class="opt_v" type="number" style="width: 5em;" value="0.9"></td>';
    }
}

const getOptionVal = () => {
    let optionList={};
    let opt_name=document.getElementsByClassName("opt_n");
    let opt_val=document.getElementsByClassName("opt_v");
    for (let i=0; i<opt_name.length ; i++){
        optionList[opt_name[i]]=opt_val[i];
    }
    return optionList;
}

model_loaded=0;
async function loadModel() {
    let model=documents.getElementById("type_model");
    if (model.value==="model_1") {

    }
    else if (model.value=="model_2"){

    }
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

    if (place!=""){
        c1=`${place}[PLACE] `;
        o1='[ADNOM] ';
    }
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
        o1=o2=o3='[MASK][MASK] ';
    }
    else if (quest_type.value=="quest_2_long"){
        o1=o2=o3='[MASK][MASK][MASK][MASK] ';
    }
    input=o1+c1+o3+o2+c2+c3;

    sentence=""
    if (style_type.value==="style_2_enfp")
        sentence='[STYLE1] '+input+' [/STYLE]';
    else if (style_type.value==="style_3_oldKing")
        sentence='[STYLE2] '+input+' [/STYLE]';        
    else if (style_type.value==="style_4_robot")
        sentence='[STYLE3] '+input+' [/STYLE]';
    else if (style_type.value==="style_5_old")
        sentence='[STYLE4] '+input+' [/STYLE]';
    return sentence;
}

async function makeSentence(){
    if (model_loaded===0){
        await loadModel();
    }
    let optionList=getOptionVal();
    let input=getTypeVal();
    optionList['input_sentence']=input;
    const responce = await fetch('/quest_gen_web', {
        method: 'POST',
        body: JSON.stringify(optionList),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const result=await responce.json();
    const newSent=document.getElementById('result').insertRow(0);
    newSent.innerHTML=result;
}