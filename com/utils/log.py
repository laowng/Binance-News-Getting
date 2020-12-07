import time
import os
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


if __name__ == '__main__':
    log=Log("./")
    log.write("aaa","bbb","ccc")
    log.write("aadddddda","bddddbb","ccc")