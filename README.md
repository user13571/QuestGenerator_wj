# QuestGenerator
> 키워드를 인풋으로 주면, 아웃풋으로 퀘스트 문장을 생성하는 모델입니다. <br>
> 데모 사이트를 통해 생성할 수도 있고, 모델 파일을 직접 이용하여 문장을 생성할 수도 있습니다.

## 문장 생성 - 웹 데모
http://52.78.11.226:5000
하단의 별도의 설치 과정 없이, 위 링크로 접속하여 실행할 수 있습니다.<br>
장소, 대상, 행동을 입력하고 디코딩 옵션을 선택한 뒤, 모델과 퀘스트 종류를 선택한 뒤 생성 버튼을 누릅니다.
##### 옵션 설명
- Greedy나 num_beams로 설정 시, 늘 가장 확률이 높다고 생각되는 똑같은 문장만 생깁니다.
- Sampling을 하면 매번 다른 문장이 생성됩니다. top_k는 정수, top_p는 0~1 사이 실수로 설정합니다.
- temperature가 1보다 작아지면 비슷한 문장들이, 커지면 더 다양한 문장들이 나옵니다.

##### 모델 종류
- 기본: huggingFace의 cosmoquester/base-ko-base 모델을 base 모델로 하여(https://huggingface.co/cosmoquester/bart-ko-base), 국립국어원 모두의 말뭉치 구어 데이터셋(https://corpus.korean.go.kr), smile gate 말투 데이터셋(https://smilegate.ai/2022/06/24/smilestyle/), 깃허브 한국어 발화의도 데이터셋(https://github.com/warnikchow/3i4k)을 이용하여 일반적인 문장들에 대하여 조사 생성, 말투 변환, 단어 생성 등을 학습시킨 모델입니다.
- 긍정:  어린이용 퀘스트에 적합하도록, 위 말뭉치 데이터에 임의로 긍정적인 단어를 추가하고 긍정적인 수식어 위주로 모델을 학습시킨 것으로, 말투 변환 기능은 없습니다.
### 링크가 잘 작동하지 않을 때 - 직접 설치 및 실행
#### 1. git clone 및 패키지 설치
``` git clone https://github.com/user13571/QuestGenerator_wj.git ```
```
pip install transformers==4.24
pip install flask
pip install torch
```
#### 2. 모델 다운로드
모델 용량이 커서 깃허브에 직접 올리기 힘들어 구글 드라이브 링크로 공유합니다. <br>
다운로드 받은 .bin 파일을 models 폴더에 넣으면 됩니다.<br>
https://drive.google.com/drive/folders/1Cf7Fa7CUcEL4BbtH2hTf-Iojyd3kEvst?usp=share_link

#### 3. 폴더 경로에서 ```python main.py``` 실행

## 개발과정
### 4~5월: 선행 학습
- 딥러닝 관련 공부
- 주제 선정, 개발 환경 세팅
### 6~8월: 하계집중학습
- Quest Generator 개발 시작
    - 장소, 대상, 행동 등 특정 키워드를 제시하면 그에 맞는 퀘스트 문장을 생성해주는 모델
- CBART(Xingwei He, Parallel Refinements for Lexically Constrained Text Generation with BART, 2021 / https://github.com/NLPCode/CBART) 논문 조사 및 영어 모델 fine-tuning
    - BART: BERT와 GPT2를 합친 딥러닝 모델 (Mike Lewis et al., BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension)
    - 영어 퀘스트 데이터, 영미권 어린이 및 청소년 권장 도서 추출 데이터 이용
    - 뉴스 데이터, 식당 리뷰 데이터 이용한 원 모델보다 더 나은 생성 결과 확인
- 한국어 모델 훈련
    - koBART 이용
    - 단어 사이사이에 모델이 반복적으로 새 단어를 추가하도록 하여 문장 생성
        - 키워드에 붙는 조사, 어미 등은 룰베이스로 바꿔줌
        - 의도와 벗어난 문장을 막기 위해 특정 단어(즐거운, 재밌는 등) 임의로 추가해줌
    - 어느정도 다양하고 의도에 맞는 퀘스트 문장 생성됨
### 9~12월: 
- 문장 말투 변환 모델 학습
    - smile gate 말투 데이터셋 이용, 문장의 말투를 외향형/반말/사극체 등으로 변환해주는 모델 훈련
- 어미/조사 변환 딥러닝 모델 등 학습
    - 기존에 룰베이스로 바꿔주던 부분을 Masking 등을 통해 학습시켜 딥러닝으로 대체
- 다양한 변환 모델을 하나의 모델로 합침
    - 모델에 새로운 토큰을 학습시켜 원하는 의도에 맞게 새로운 단어가 생성되도록 함
- 웹에서 장소 관련된 문장 데이터 크롤링
    - 네이버 블로그 글들을 크롤링하여 도서관, 쥐라기 파크 등 장소 관련 특수한 문장들 추출
    - 모델 훈련에 따로 이 데이터를 사용하지는 않음

## 파일 구성
```bash
├── keywordsFolder/
│   └── KeyList_Fordemo.csv
├── models/
│   └── kobart-myTokenizer/
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── main.py
├── place2key.py
└── README.md
```
