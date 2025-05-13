import zipfile
import string
import itertools
import time

def unlock_zip():
    charset = string.ascii_letters + string.digits  # 대소문자 + 숫자
    max_len = 6
    zip_file = 'emergency_storage_key.zip'
    found = False
    attempt_count = 0
    start_time = time.time()

    with zipfile.ZipFile(zip_file) as zf:
        for pw_tuple in itertools.product(charset, repeat=max_len):
            password = ''.join(pw_tuple)
            attempt_count += 1
            try:
                zf.extractall(pwd=password.encode('utf-8'))
                print(f'[✓] Password found: {password}')
                with open('password.txt', 'w') as f:
                    f.write(password)
                found = True
                break
            except:
                continue

    end_time = time.time()
    print(f'>> Total attempts: {attempt_count}')
    print(f'>> Total time: {end_time - start_time:.2f} seconds')

    if not found:
        print('[!] Password not found.')
