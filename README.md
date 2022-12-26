# QuestGenerator
> 키워드를 인풋으로 주면, 아웃풋으로 퀘스트 문장을 생성하는 모델입니다. <br>
> 데모 사이트를 통해 생성할 수도 있고, 모델 파일을 직접 이용하여 문장을 생성할 수도 있습니다.

#### 1. git clone 및 패키지 설치
사용 파이썬 버전: 3.8 <br>
``` git clone https://github.com/user13571/QuestGenerator_wj.git ``` <br>
``` pip install -r requirements.txt ```
<br>
#### 2. 모델 다운로드
모델 용량이 커서 깃허브에 직접 올리기 힘들어 구글 드라이브 링크로 공유합니다. <br>
다운로드 받은 .bin 파일을 models 폴더에 넣으면 됩니다. 각 모델에 대한 설명은 하단에 있습니다. <br>
(링크)
<br>
#### 3. 데모 사이트를 통한 생성
``` python main.py ``` : 퀘스트를 생성할 수 있는 데모 사이트가 열립니다. 유니티에서 서버 주소로 request를 받을 시 output을 돌려주는 기능도 동시에 실행됩니다. <br>
> 데모 사이트 접속 뒤, UI 표시대로 장소, 대상, 행동('-다'(가다, 하다...) 형태의 기본형)을 입력하고 원하는 생성 방식을 선택하면 됩니다. <br>
> 이용되는 모델은 "~.bin"이 기본으로 설정되어 있습니다. ```python main.py --model-name (모델명.bin) ``` 을 통해 변경할 수도 있습니다. (각 모델 설명: 하단에 있음) <br>
#### 4. gen.py를 통한 생성
``` python gen.py --model-name (모델명.bin) --place (장소) --object (대상) --action (행동) --gen-num (생성개수) (... 기타 옵션 ...) ``` 을 통해 디코딩 옵션을 바꿔 생성할 수도 있습니다. output 폴더에 csv 파일로 저장이 됩니다.
#### 5. 파이썬 코드 내에서 직접 생성
```python
from transformers import AutoTokenizer, BartConfig, BartForConditionalGeneration
import torch

tokenizer = AutoTokenizer.from_pretrained("./models/tok")
config=BartConfig.from_pretrained("./models/tok")
model = BartForConditionalGeneration(config=config)
model.load_state_dict(torch.load('./models/모델명.bin',map_location=torch.device('cpu')))
model.eval()

```
이를 통해 파이썬 내에서 직접 문장 생성을 테스트 할 수도 있습니다.
```python
input_sentence="장소[PLACE] 대상[OBJECT] 행동[VERB]" #예시: 도서관[PLACE] 책[OBJECT] 읽다[VERB] / 도서관[PLACE] 가다[VERB]
```
input_ids=tokenizer(['[BOS] '+input_sentence+' [EOS]'],return_tensors='pt')['input_ids']
result=tokenizer.batch_decode(model.generate(input_ids,num_beams=2,no_repeat_ngram_size=3, do_sample=True,temperature=1.5, top_p=0.9, max_length=1024, num_return_sequences=1),skip_special_tokens=True)[0]

```
