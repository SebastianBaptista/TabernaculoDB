
class Event():
    def __init__(self,id_event,name_event,kind_event,leader,matirials,start_time,end_time,info):
        super().__init__()
        self.id_event=id_event
        self.name_event=name_event
        self.kind_event=kind_event
        self.leader=leader
        self.matirials=matirials
        self.start_time=start_time
        self.end_time=end_time
        self.info=info