import os
import logging

path_croud = 'c:\\CRoud'
path_croud_sample = 'C:\\CRoud\\마케팅\\디자인ㅣ자여니'
INFECTED_PROOF = '.ublgmmk'
logging.basicConfig(filename='result.log', level=logging.INFO)
README_FIRSTLINE = 'ALL YOUR DOCUMENTS PHOTOS DATABASES AND OTHER IMPORTANT FILES HAVE BEEN ENCRYPTED!'

def huntdown_infected(rootdir, files):
    """
    1. 감염된 파일의 증거인 .ublgmmk 확장자인 파일을 찾는다.
    2. 감염된 파일인데 중복된 파일이 있는 지 찾는다.
        1.1. 알파벳 순서 상으로 앞뒤 파일이름이 같은게 있으면 삭제한다.
        1.2. 없으면 복구에 실패한 것이므로 유지한다.
    3. 협박문구가 들어간 readme.txt를 삭제한다.
    """
    # 혹시 모르니까 정렬
    files.sort()

    # 감염된 파일들만 인덱스와 함께 정리
    files_infected = [[i, n] for i, n in enumerate(files) if INFECTED_PROOF in n]

    # 감염된 파일 앞뒤로 동일한 파일이 있다면 인덱스 대신에 원래 파일명으로 변경.
    for i, n in files_infected:
        # 이름이 같은 파일의 확장자가 INFECTED_PROOF 보다 알파벳 상 빠른 경우
        n_clean  = os.path.splitext(n)[0] #n.rstrip(INFECTED_PROOF)
        if files[i-1] == n_clean:
            # files_infected[i_origin][0] = files[i-1]
            fullpath = os.path.join(rootdir, n)
            os.remove(fullpath)
            logging.info("[복구성공]"+fullpath)
        # 이름이 같은 파일의 확장자가 INFECTED_PROOF 보다 알파벳 상 느린 경우
        else:
            try:
                if files[i+1] == n_clean:
                    # files_infected[i_origin][0] = files[i+1]
                    fullpath = os.path.join(rootdir, n)
                    os.remove(fullpath)
                    logging.info("[복구성공]"+fullpath)
                    break
            except IndexError: 
                continue
            finally:
                logging.info("[복구실패]"+os.path.join(rootdir, n))

            #  하구 try 때려야 함니다
        # 복구 실패해서 이름이 같은 파일, 즉 원본을 소실한 경우

    # 마지막으로 readme.txt를 삭제해야 합니다. 이건 파일을 열어서 첫 줄을 확인한 후 삭제합니다.
    if 'readme.txt' in files:
        fullpath_readme = os.path.join(rootdir, 'readme.txt')
        memo = False
        with open(fullpath_readme, 'r') as readme:
            if README_FIRSTLINE in readme.readline():
                memo = True
        if memo:
            os.remove(fullpath_readme)
            logging.info("[삭제조치]"+README_FIRSTLINE)


def search_folder_recursively(path):
    """
    It can get abspath by concatnating 'rootdir' and file name in var 'files'
    It can get what directory this function walk so it go to subdirectory recursively.
    """
    for rootdir, dirs, files in os.walk(path):
        huntdown_infected(rootdir, files)

    # If there is subfolders, run ifself recursively.
    if len(dirs) > 0:
        for subdir in dirs:
            logging.debug("enter to " + subdir)
            search_folder_recursively(os.path.join(rootdir, subdir))

if __name__ == '__main__':
    # huntdown_infected(path_croud_sample)
    search_folder_recursively(path_croud)
    # for path_root in os.walk(path_croud):
    #     print(path_root)
    #     break