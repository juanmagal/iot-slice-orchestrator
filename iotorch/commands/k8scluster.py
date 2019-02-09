"""The k8s cluster command."""

from json import dumps

from .base import Base


class K8scluster(Base):
    """The k8s cluster command."""

    def create(self):
        print('Creating k8s cluster!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))        

    def run(self):
        if self.options['create']:
            self.create()
        else:
            print("Option not implemented")    
            raise NotImplementedError('Option not implemented')
