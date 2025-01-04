import os
import pyupbit
from openai import OpenAI
from dotenv import load_dotenv
import json
import time

# dotenv 환경 구축
load_dotenv()

def ai_trading():
    # 1. 업비트 30일 일봉 차트 데이터 가져오기 
    df = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")


    # 2. AI에게 데이터 제공하고 답변 확인하기
    client = OpenAI()

    # TODO : 안정화되면 추후 gpt-4o로 바꾸기
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": "You are an expert in Bitcoin investing. Tell me whether to buy, sell, or hold at the moment based on the chart data provided. response in json format.\n\nResponse Example:\n{\"decision\": \"buy\", \"reason\": \"some technical reason\"}\n{\"decision\": \"sell\", \"reason\": \"some technical reason\"}\n{\"decision\": \"hold\", \"reason\": \"some technical reason\"}"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": df.to_json()
                    }
                ]
            }
        ],
        response_format={
            "type": "json_object"
        }
    )
    # 메시지만 뽑아내기
    # TODO : 영어로 돌아오는 메시지를 한국어로 번역을 할 수 있으면 보기 편하지 않을까?
    result = response.choices[0].message.content


    # 3. AI의 판단에 따라 실제로 자동매매 진행하기
    result = json.loads(result)
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)

    # 확인을 위한 출력부
    print("### AI Decision: ", result["decision"].upper(), "###")
    print(f"### Reason: {result['reason']} ###")

    # 조건에 따라 api 요청이 갈 수 있도록 조건문 작성하기
    if result["decision"] == "buy":
        my_krw = upbit.get_balance("KRW")
        # 구매시 최소 5000원 이상 조건이 충족해야 정상적으로 api를 사용할 수 있음
        if my_krw * 0.9995 > 5000:
            print("### Buy Order Executed ###")
            print(upbit.buy_market_order("KRW-BTC", my_krw * 0.9995))
        # 그렇지 않으면 오류메시지 출력
        else:
            print("### Buy Order Failed: Insufficient KRW (less than 5000 KRW) ###")
    elif result["decision"] == "sell":
        my_btc = upbit.get_balance("KRW-BTC")
        current_price = pyupbit.get_orderbook(ticker="KRW-BTC")['orderbook_units'][0]["ask_price"]
        # 판매시 최소 5000원 이상 조건이 충족해야 정상적으로 api를 사용할 수 있음
        if my_btc * current_price > 5000:
            print("### Sell Order Executed ###")
            print(upbit.sell_market_order("KRW-BTC", my_btc))
        # 그렇지 않으면 오류메시지 출력
        else:
            print("### Sell Order Failed: Insufficient BTC (less than 5000 KRW worth) ###")
    elif result["decision"] == "hold":
        print("### Hold Position ###")
        
while True:
    # 10초마다 ai_trading() 함수 반복
    time.sleep(10)
    ai_trading()