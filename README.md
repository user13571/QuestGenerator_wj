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
#### 3. (옵션) 데모 사이트를 통한 생성
``` python main.py ``` : 퀘스트를 생성할 수 있는 데모 사이트가 열립니다. 유니티에서 서버 주소로 request를 받을 시 output을 돌려주는 기능도 동시에 실행됩니다. <br>
> 데모 사이트 접속 뒤, UI 표시대로 장소, 대상, 행동('-다'(가다, 하다...) 형태의 기본형)을 입력하고 원하는 생성 방식을 선택하면 됩니다. <br>
> 이용되는 모델은 "~.bin"이 기본으로 설정되어 있습니다. ```python main.py --model-name (모델명.bin) ``` 을 통해 변경할 수도 있습니다. (각 모델 설명: 하단에 있음) <br>
#### 4. (옵션) 파이썬 코드 내에서 직접 생성
```python
from transformers import AutoTokenizer, BartConfig, BartForConditionalGeneration
import torch

tokenizer = AutoTokenizer.from_pretrained("./models/tok")
config=BartConfig.from_pretrained("./models/tok")
model = BartForConditionalGeneration(config=config)
model.load_state_dict(torch.load('./models/모델명.bin',map_location=torch.device('cpu')))
model.eval()

```
폴더 안에 .py 파일을 만들고, 이를 통해 파이썬 내에서 직접 문장 생성을 테스트 할 수도 있습니다.
```python
input_sentence="(~~~)" #예시: "도서관[PLACE] 책[OBJECT] 읽다[VERB]" / "도서관[PLACE] 가다[VERB]"
input_ids=tokenizer(['[BOS] '+input_sentence+' [EOS]'],return_tensors='pt')['input_ids']
```
input_sentence의 형식은 모델마다 약간의 차이가 있지만, 기본 문장 구조를 만드는 구조는 공통적으로 "장소[PLACE] 대상[OBJECT] 행동[VERB]" 입니다. <br>
더 길고 다양한 문장을 만들기 위해 다음과 같은 입력을 넣어줄 수 있습니다. <br>
- (모델 공통)
  -  "[ADNOM] 도서관[PLACE] [ADVERB] 책[OBJECT] 읽다[VERB]" : 명사 앞에는 [ADNOM], 동사 앞에는 [ADVERB]을 넣어주어 모델이 원하는 문장의 의도를 크게 벗어나지 않게, 수식어(관형어/부사어) 위주로 생성하게 합니다.
  -  "[MASK] 도서관[PLACE] [MASK] 책[OBJECT] [MASK] 읽다[VERB]" : 수식어 위주라는 제한을 주지 않고, 모델이 자유롭게 추가적인 단어들을 생성하도록 합니다.
- (.bin 모델)
  -  말투를 변환시키기 위해, 앞선 입력 앞/뒤에 [STYLE(숫자)] [/STYLE] 토큰을 넣어줍니다. (ex. "[STYLE1] [MASK] 도서관[PLACE] [MASK] 책[OBJECT] 읽다[VERB] [/STYLE]" )
      - [STYLE1] : 외향형 말투
      - [STYLE2] : 조선시대 왕 말투 
      - [STYLE3] : 로봇 말투
      - [STYLE4] : 사극 선비 말투

```python
result=model.generate(input_ids,num_beams=2, do_sample=True,temperature=1.2, top_p=0.8, max_length=1024, num_return_sequences=1)
result_sentence=tokenizer.batch_decode(result,skip_special_tokens=True)
print(result_sentence)
```
model.generate 시 괄호 안 옵션을 다양하게 변경하여 문장 생성을 다양화 할 수 있습니다.
- 주요 parameter
  -  do_sample : False면 greedy, True면 sampling을 해서(top-p 혹은 top-k 설정) decoding 합니다. sampling을 하면 더 자연스러운 문장이 생깁니다.
  -  num_beams : 클수록 문장이 자연스럽고 무난해(?)집니다.
  -  temperature : 1이 기본값, 1보다 클 수록 창의적이고 다양한 (혹은 말이 안될 수도 있는) 문장을 생성합니다.
  -  num_return_sequences : 생성되는 문장 개수입니다.
  -  no_repeat_ngram_size : 이 단위로 반복되는 어구를 만들지 않습니다.

#### 5. (옵션) gen.py를 통한 생성
``` python gen.py --model-name (모델명.bin) --place (장소) --object (대상) --action (행동) --gen-num (생성개수) (... 기타 옵션 ...(ex. --do-sample / --top-p / --top-k : 앞서 설명한 것과 동일) ) ``` 을 통해 생성할 수도 있습니다. output 폴더에 키워드, 옵션, 문장 쌍이 csv 파일로 저장이 됩니다.

## 모델 설명
> 총 ~개의 모델이 있습니다.
- ~.bin : 
- ~.bin :
- ~.bin :
