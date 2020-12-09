import time
import os
import logging
class Log():
    def __init__(self,log_dir):
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        self.log_path=os.path.join(log_dir,"log.txt")
    def write(self,*args):
        with open(self.log_path, "a",encoding='utf-8') as log:
            log.writelines(self.get_date()+":")
            for i,info in enumerate(args):
                log.writelines("\t"+str(i)+": "+info)
            log.writelines("\n")
    def get_date(self):
        return time.strftime("%m-%d %H:%M:%S", time.localtime())
    def get(self,i:int):
        with open(self.log_path, "r",encoding='utf-8') as log:
            lines=log.readlines()
            message=lines[-i]
            for line in lines[-i+1:]:
                message+="\n"+line
            return message
def get_log():
    curPath = os.path.abspath(os.path.dirname(__file__))
    root_path = os.path.split(os.path.split(curPath)[0])[0]
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)  # Log�ȼ��ܿ���
    # ����һ��handler������д����־�ļ�
    rq = time.strftime('%Y%m%d', time.localtime(time.time()))
    log_path = root_path + '/Logs/'
    os.makedirs(log_path,exist_ok=True)
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='a',encoding="utf-8")
    fh.setLevel(logging.INFO)  # �����file��log�ȼ��Ŀ���
    # ����handler�������ʽ
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    rf_handler = logging.StreamHandler(sys.stderr)
    rf_handler.setLevel(logging.ERROR)
    rf_handler.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(rf_handler)
    # ʹ��logger.XX����¼����,�����"error"���Ը�������Ҫ�ļ�������޸�
    return logger


if __name__ == '__main__':
    log=Log("./")
    log.write("aaa","bbb","ccc")
    log.write("aadddddda","bddddbb","ccc")