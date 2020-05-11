import yaml
import networkx as nx


class CwlParser:

    def __init__(self, filelocation):
        self.filelocation = filelocation
        self.g = nx.DiGraph()
        self.tasks = []
        self.cwl_to_dag()

    def check_and_add_dependencies(self, steps):
        for task, value in steps.items():
            self.tasks.append(task)
            self.g.add_node(task)
            for k, v in value.items():
                if k == 'in':
                    if isinstance(v, list):
                        for i in v:
                            self.add_dependencies(i, task)

                    elif isinstance(v, dict):
                        for k2, v2 in v.items():
                            self.add_dependencies(v2, task)

                    else:
                        self.add_dependencies(v, task)

    def add_dependencies(self, index, task):
        if '/' in index:
            res = index.split('/')
            if res[0] in self.tasks:
                self.g.add_edge(res[0], task)

    def cwl_to_dag(self):
        with open(self.filelocation, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                if '$graph' in data:
                    graph = data['$graph']
                    for i in graph:
                        if i['id'] == 'main':
                            steps = i['steps']
                            self.check_and_add_dependencies(steps, self.g)

                else:
                    if 'steps' in data:
                        steps = data['steps']
                        self.check_and_add_dependencies(steps)

                    # raise ValueError('Invalid workflow, $graph is missing')

            except yaml.YAMLError as exc:
                print(exc)