#import time
class StateMachine(object):

    def __init__(self, name):
        self.name = name
        self.current_state = 'idle'
        self.prev_state = None
        self.new_state = None
    
    def _process(self):
        if self.current_state != self.new_state:
            self.update_state()
        self.process_state()

    def update_state(self):
        if self.new_state != None:
            if self.current_state != self.new_state:
                
                init_method = "_init_" + self.new_state
                end_method = "_end_" + self.current_state
                
                if hasattr(self, end_method):
                    getattr(self,end_method)()

                self.prev_state = self.current_state
                self.current_state = self.new_state
                self.new_state = None

                if hasattr(self,init_method):
                    getattr(self,init_method)()

    def process_state(self):
        if hasattr(self, '_' + self.current_state):
            eval('self.' + '_' + self.current_state + '()')

    def _idle(self):
        print('im stoped!')

    def _init_idle(self):
        print('im going to rest!')

    def _end_idle(self):
        print('im going to move!')
        
    def _run(self):
        print('im running!')

    def _init_run(self):
        print('im start to move!')

    def _end_run(self):
        print('im going to stop move!')
        
'''
a = StateMachine('a')
cont = 1

while True:
    a._process()
    if cont == 5:
        a.new_state = "run"
        time.sleep(1)
        
        cont=0
    else:
        a.new_state = "idle"
        time.sleep(1)
        cont+=1
'''