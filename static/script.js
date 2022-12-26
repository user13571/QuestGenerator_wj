$(document).ready(function(){
    let genNum=0;
    $('.send').click(function(e){
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

        let id=e.target.getAttribute('id')

        if (id==='send1'){
            keyInfo['option']=1;
        }
        else if (id==='send2'){
            keyInfo['option']=2;
        }
        else if (id==='send3'){
            keyInfo['option']=3;
        }
        else if (id==='send4'){
            keyInfo['option']=4;
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
                let newRow2=document.getElementById('result').insertRow(0);
                newRow2.classList.add('sent');
                newRow2.innerHTML=`<td class="s_" id="sent_${genNum}"></td>`;
                console.log(data);
			},
            error : function(){
				console.log("getSentence_fail");
			}
		});
    })
});
