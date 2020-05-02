# _*_ coding:utf-8 _*_
from app.libs.enums import PendingStatus

class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data=[]
        self.__prase(drifts, current_user_id)

    def __prase(self,drifts, current_user_id):
        for drift in drifts:
            temp=DriftViewModel(drift,current_user_id)
            self.data.append(temp.data)

class DriftViewModel:
    def __init__(self,drift,current_user_id):
        self.data={}
        self.drift=drift
        self.current_user_id=current_user_id
        self.__prase()


    def requester_or_gifter(self):
        if self.drift.requester_id==self.current_user_id:
            you_are='requester'
        else:
            you_are='gifter'
        return you_are


    def __prase(self):
        you_are=self.requester_or_gifter()
        pending_status=PendingStatus.pending_str(self.drift.pending,you_are)
        r = {
            'you_are':you_are,
            'drift_id': self.drift.id,
            'book_title': self.drift.book_title,
            'book_author': self.drift.book_author,
            'book_img': self.drift.book_img,
            'operator': self.drift.requester_nickname if you_are != 'requester' \
                else self.drift.gifter_nickname,
            'date': self.drift.create_datetime.strftime('%Y-%m-%d'),
            'message': self.drift.message,
            'address': self.drift.address,
            'status_str': pending_status,
            'recipient_name': self.drift.recipient_name,
            'mobile': self.drift.mobile,
            'status': self.drift.pending
        }
        self.data=r