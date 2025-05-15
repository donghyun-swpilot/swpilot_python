import zipfile
import string
import itertools
import time

def unlock_zip():
    charset = string.ascii_lowercase + string.digits
    max_len = 6
    zip_file = 'emergency_storage_key.zip'
    found = False
    attempt_count = 0
    start_time = time.time()

    print("[*] Brute-force 시작합니다...")

    try:
        with zipfile.ZipFile(zip_file) as zf:
            for pw_tuple in itertools.product(charset, repeat=max_len):
                password = ''.join(pw_tuple)
                attempt_count += 1

                if attempt_count % 500000 == 0:
                    print(f"시도 중: {password} (#{attempt_count})")

                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    print(f"[✓] 비밀번호 찾음: {password}")
                    with open("password.txt", "w") as f:
                        f.write(password)
                    found = True
                    break
                except:
                    continue
    except FileNotFoundError:
        print("[!] zip 파일을 찾을 수 없습니다. 이름 확인 필요!")

    end_time = time.time()
    print(f">> 시도 횟수: {attempt_count}")
    print(f">> 소요 시간: {end_time - start_time:.2f}초")

    if not found:
        print("[X] 실패: 비밀번호를 찾지 못했습니다.")