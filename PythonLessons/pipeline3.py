# Credit: Bob Gailer

import sqlite3 as sq
db = sq.connect('pipeline_db')

def main(pipelineset_spec): # We pass in a specification below

    def add(cls=None, d={}):
        if cls: d.update({cls.__name__.lower(): cls}); return cls
        return d
    
    class Stream():
        pass

    class InStream(Stream):
        def run(self,record): pass 

    class OutStream(Stream):
        def output(self, record): pass

    class Stage():
        driver = False # overridden on IODriver class

        def __init__(self, pipeline):
            self.pipeline = pipeline
            self.position = len(pipeline)

            # stages may add more streams as needed
            self.instreams = [InStream()]
            self.instreams[0].run = self.run

            self.outstreams = [OutStream()]
            self.output = self.outstreams[0].output 
        
        def run(self, *args): raise NotImplementedError
        def output(self, *args): raise NotImplementedError
        def setup(self, args): pass

    class IODriver(Stage):
        driver = True

    @add
    class Console(IODriver):
        names = 'CONSole TERMinal'
    
    @add
    class Console0(Console): # will eventually have its own module
        "For if Console appears first in the pipeline"
        def run(self):
            while True:
                record = input(">")
                if record: self.output(record)
                else: break 
    
    @add
    class Console1(Console): # will eventually have its own module
        def run(self, record):
            print(record); self.output(record)
    
    @add
    class Locate(Stage): # will eventually have its own module
        # This class can accommodate a second output stream, to which unmatched records are printed
        def __init__(self, pipeline):
            super().__init__(pipeline)  
            self.outstreams.append(OutStream())
            self.output1 = self.outstreams[1].output 
        
        def setup(self, args):
            print("We're here")
            delstr = args[0].strip()
            print(delstr)
            delim = delstr[0]
            if delstr[-1] == delim: self.search = delstr[1:-1]
            else: return 'Locate missing final delimiter'

        def run(self, record):
            if self.search in record: self.output(record)
            else: self.output1(record)

    @add
    class Literal(Stage): # will eventually have its own module
        def setup(self, args):
            self.lit = args[0]
        
        def run(self):
            self.output(self.lit)

    @add
    class Change(Stage): # will eventually have its own module
        def setup(self, args):
            search = args[0].strip()
            delim = search[0]
            if search[-1] == delim:
                if search.count(delim) != 3: return 'extra delimeters in Change'
                self.search, self.replace = search[1:-1].split(delim)
            else: return 'Change missing final delimeter'
        
        def run(self, record):
            if self.search in record: self.output(record)

    stage_dict = add()

    class PipelineSet:
        def __init__(self):
            labels = dict()
    pipelineset = PipelineSet()
    class Pipeline:
        def __init__(self, spec):
            prev = None
            stages = spec.split('|')
            for stage_no, stage_spec in enumerate(stages):
                args = stage_spec.split(maxsplit=1)
                if args[0][:-1] == ':':
                    label = args[0][:-2]
                    if label not in labels:
                        if len(args) == 1:
                            raise NameError
                        labels.update({label: [pipeline, stage_no]})
                    x,y = labels[label]
                    stage_spec = args[1]   
                else:
                    stage_spec = args[0]

                is_space = stage_spec.find(' ')
                if is_space == -1:
                    stage_name = stage_spec
                else:
                    stage_name = stage_spec[:is_space]

                sql = f"SELECT stagename FROM stage WHERE stagename LIKE ? AND  min_length <= ?;"
                tup = (stage_name + '%', len(stage_name))
                curs = db.execute(sql, tup)
                stage_name = curs.fetchone()[0]
                cls = stage_dict.get(stage_name, None)
                if cls.driver:
                    pos = '0' if stage_no == 0 else '1'
                    cls = stage_dict.get(stage_name+pos, None)
                stage = cls(pipeline)
                set_call = stage.setup(args)
                if set_call:
                    print(set_call)


                # stage.setup(args)
                pipeline.append(stage)
                if prev: prev.output = stage.run
                prev = stage 


    pipelinespecs = [pipe for pipe in spec.split('?')]
    for spec in pipelinespecs:
        pipeline = Pipeline(spec)
        pipelineset.append(pipeline)
    for pipe in pipelineset:
        pipe[0].run()

if __name__ == '__main__':
    input = __builtins__.input; print = __builtins__.print
    main('console|locate /apple/|console ? literal bob|console') # modified to take two pipelines

data = ['banana', 'apple', ' fig']
expected = ['apple', 'bob']
result = []

def input(prompt):
    if data: return data.pop(0)
def print(item): result.append(item)

main('console|locate /apple/|console ? literal bob|console')
input = __builtins__.input; print = __builtins__.print

try: assert expected == result
except AssertionError: print('test failed', result)
else: print('test succeeded!')
