$(document).ready(function(){
    let genNum=0;
    let savedString="";
    $('#send').click(function(){
        let keyInfo={};
        let key_n=document.getElementsByClassName('k');
        let key_name=document.getElementsByClassName('kn');

        keyInfo={
            'k_place_modify': '0',
            'k_location': '0',
            'k_time': '0',
            'k_add': '0',
        }

        for (let i=0; i<key_n.length ; i++) {
            let tmp='k_'+((key_name[i].innerText.split('/')[0]).toLowerCase());
            keyInfo[tmp]=key_n[i].value;
        }
        info=keyInfo
        keyInfo=JSON.stringify(keyInfo);
        console.log(keyInfo);
        $.ajax({
			type:'post',   //post 방식으로 전송
			url: '/quest_gen_web',
			data: keyInfo,
            contentType:'application/json',
            dataType: 'text',
			success : function(data){                
                let newRow2=document.getElementById('result').insertRow();
                newRow2.classList.add('sent');
                newRow2.innerHTML=`<td class="s_" id="sent_${genNum}"></td>`;
                console.log(data);

                n=(info['k_action'].split(' ')).length; // action 길이 (이거만큼 뒤에)
                dataList=data.split(' ');
                dataLen=dataList.length;

                if(dataList[dataLen-1]=='싶어요.' ){
                    endi=dataLen; // 싶어요 </span>
                    starti=dataLen-n-1; // <span> 게임을 하고
                }
                else{
                    endi=dataLen;
                    starti=dataLen-n;
                }
//                dataList.splice(endi,0,`%</span>`);
//                dataList.splice(starti,0,`%<span class='blue'>`);

                console.log(dataList[0])
                sent='';
                for (let d of dataList){
                    console.log(d)
                    if (d[0]=='%'){
                        sent+=d.slice(1)
                    }
                    else
                        sent+=(' '+d)
                }

                for (let k in info){
                    let regex = new RegExp(`${info[k]}`);
                    if (info[k]!=''){
                        sent=sent.replace(regex,`<span class='blue'>${info[k]}</span>`);
                    }
                    console.log(sent);
                }

                document.getElementById(`sent_${genNum}`).innerHTML=sent;
                genNum+=1;
                savedString=data;
			},
            error : function(){
				console.log("getSentence_fail");
			}
		});
    })
    $('#send2').click(function(){
        let keyInfo={};
        let key_n=document.getElementsByClassName('k');
        let key_name=document.getElementsByClassName('kn');

        keyInfo={
            'k_place_modify': '0',
            'k_location': '0',
            'k_time': '0',
            'k_add': '0',
        }

        for (let i=0; i<key_n.length ; i++) {
            let tmp='k_'+((key_name[i].innerText.split('/')[0]).toLowerCase());
            keyInfo[tmp]=key_n[i].value;
        }
        info=keyInfo
        keyInfo=JSON.stringify(keyInfo)
        console.log(keyInfo)
        $.ajax({
			type:'post',   //post 방식으로 전송
			url: '/quest_gen_web_2',
			data: keyInfo,
            contentType:'application/json',
            dataType: 'text',
			success : function(data){
                let newRow2=document.getElementById('result').insertRow();
                newRow2.classList.add('sent');
                newRow2.innerHTML=`<td class="s_" id="sent_${genNum}"></td>`;
                console.log(data);

                n=(info['k_action'].split(' ')).length; // action 길이 (이거만큼 뒤에)
                dataList=data.split(' ');
                dataLen=dataList.length;

                console.log(dataList[0])
                sent='';
                for (let d of dataList){
                    console.log(d)
                    if (d[0]=='%'){
                        sent+=d.slice(1)
                    }
                    else
                        sent+=(' '+d)
                }

                for (let k in info){
                    let regex = new RegExp(`${info[k]}`);
                    if (info[k]!=''){
                        sent=sent.replace(regex,`<span class='blue'>${info[k]}</span>`);
                    }
                    console.log(sent);
                }

                document.getElementById(`sent_${genNum}`).innerHTML=sent;
                genNum+=1;
                savedString=data;
			},
            error : function(){
				console.log("getSentence_fail");
			}
		});
    })
});
