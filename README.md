# Upbit API / ChatGPT를 이용한 비트코인 자동거래 레포지토리
- ChatGPT가 분석해주는 전략을 이용하여 암호화폐 거래소 Upbit에서 제공하는 계정 / 거래 / 조회 api를 사용해서 자동거래 시스템을 구축해보고자 한다.
- Python을 기반으로 구현한다.

## 진행 과정
### 25.01.05.
#### [Upbit Open API Key](https://upbit.com/service_center/open_api_guide) 발급
- <img width="713" alt="image" src="https://github.com/user-attachments/assets/9b4ae4ab-6c33-4ce1-9346-d4819f62d060" />
- Open API Key를 발급받을 때 IP 주소를 등록해야 하는데, 이 때 공유기를 통한 사설 IP (192.128.~ 같은?)로는 발급받을 수 없으므로 각자의 상황에 따라 공인 IP를 확인해야 한다.
  - 작성자 케이스의 경우 ipTime 공유기를 쓰고 있어서 어드민페이지에서 확인했다.
- 또한 upbit API를 사용하기 위해서는 [pyupbit](https://github.com/sharebook-kr/pyupbit)이라는 라이브러리를 사용해야 한다.
  - 사용법이 한국어로 친절하게 나와있고, 초당/분당 제한까지 상세하게 나와있으므로 설명은 생략한다.

#### OpenAi API Key 발급 및 결제카드 등록
- OpenAi의 Api를 사용하기 위해서는 결제카드를 미리 [등록](https://platform.openai.com/settings/organization/billing/overview)해두어야 한다.
- 무려 10달러, 피같은 돈이지만.. 수익을 내준다면 이정도는 지불할 수 있지.. (최초 5달러지만, 부족시 자동충전 옵션때문에 5달러가 추가결제되어 10달러가 충전되었다.)
- <img width="535" alt="image" src="https://github.com/user-attachments/assets/50e1e39b-f94a-4180-af9e-7be7e8377fd8" />
- 그리고 [API Key](https://platform.openai.com/settings/organization/api-keys)를 발급받았다.
- 사용시 가격과 관련해서는 [Billing Overview](https://openai.com/api/pricing/) 페이지에 자세히 나와있다.
  - 현재 시점에서는 제대로 사용해보지 않아서, 사용 후에 얼마가 소모되는지에 대해서도 확인하고 정리할 생각이다.
- 우선 gpt 3.5turbo를 먼저 사용해보고, api 사용에 익숙해졌다 싶으면 그때 4o로 올릴 예정.

#### 개인정보 보호
- API Key들은 모두 개인정보이므로 Git에 올렸다가는 정말로 큰 일이 발생할 수 있다. (이걸 누가 탈취해서 임의로 마구 사용해버리면 생각만해도 끔찍하다)
- 그렇기에 라이브러리를 통해서 Git에 올리지 않고 비밀 장소에 상수 형태로 값을 저장해두고 사용할 수 있도록 구성했다.
- [python-dotenv](https://pypi.org/project/python-dotenv/) 라이브러리를 사용한다.

#### 진행
- requirements.txt 파일에서 라이브러리를 관리할 수 있다.
- 여기에 작성해놓은 라이브러리들을 설치하고 싶다면 `pip3 install -r requirements.txt`을 하면 작성한 라이브러리들이 동시에 설치된다.
  - `-r` 옵션의 경우 requirements의 약자이다.

#### 기본 Script 작성
- 조코딩님이 작성해놓은 기본 코드를 불러와서 코드 정리 후 테스트 완료
- 추가해야 할 부분, 보완해야 할 부분에 대해서 주석 추가
