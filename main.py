print("hello mars")
try:
    with open("C:/Users/MASTER/Downloads/1-1-mission_computer_main (2).log", "r", encoding="utf-8") as 폭팔로그:
        print(폭팔로그.read())


except Exception as 에러코드:
    print(f"알 수 없는 오류 발생: {에러코드}")