import uuid
from enum import Enum, auto
class ExecList:
    def __init__(self):
        self.exec_list:TargetScan = []


class TargetScan:
    def __init__(self):
        self.ip_fqdn = ''
        # 実行するサービス
        self.service:dict = {
            'Nmap': True
        }
        self.uuid = uuid.uuid4()
        self.status:Status = Status.NONE
        self.progress = 0

    def find_uuid(self, uuid):
        if self.uuid == uuid:
            return self
        else:
            return None


class Status(Enum):
    NONE = "未実行"
    WAITING = "実行待ち"
    RUNNING = "実行中"
    DONE = "完了"
    ERROR = "エラー"
    CANCELED = "キャンセル"
