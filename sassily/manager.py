import subprocess
import os
import sys
import glob
import six
from nbstreamreader import NonBlockingStreamReader
__all__ = ['Manager']

def genlines(proc):
    '''
    Generator that will read any lines already outputted by our process.
    '''
    if not proc:
        return
    
    while True:
        line = proc.readline(0.1)
        if line:
            yield line
        else:
            return

class Manager(object):
    def __init__(self, source, destination, command, requirements=None, compass=False, compress=False, stdout=sys.stdout, quiet=False):
        self.source = source
        self.destination = destination
        
        self.requirements = requirements
        if isinstance(self.requirements, six.string_types):
            self.requirements = [ self.requirements ]
        
        self.command = command
        self.compress = compress
        self.process = None
        self.compass = bool(compass)
        self.quiet = quiet
        self.output = None
        
    @property
    def stdout(self):
        return self.command.stdout
    
    def get_arguments(self):
        args = []
                
        # Compass support
        if self.compass:
            args.append('--compass')
        
        # CSS Style
        args.append('--style')
        
        if self.compress:
            args.append('compressed')
        else:
            args.append('nested')
        
        # Optional Requirements
        if self.requirements:
            args.append('--require')
            if not isinstance(self.requirements, list):
                self.requirements = list(self.requirements)
            args += self.requirements
        
        return args
    
    def is_running(self):
        if self.process:
            return (self.process.poll() is None)
        return False
    
    def readlines(self):
        if self.output:
            return list(genlines(self.output))
    
    def run(self):
        path = ("{0}" + os.path.sep + "*.scss").format(self.source)
        print self.source
        for f in glob.glob(path):
            args = ['sass'] + self.get_arguments()
            # Add the source scss file
            args.append(f) 
            
            '''
            
            Now construct the destination filename based on the source file name.
            For instance if the file is /dest/folder/mystyle.scss the destination
            will be /dest/folder/mystyle.css
            
            '''
            base = os.path.basename(f)
            filename = os.path.splitext(base)
            if not self.quiet:
                self.stdout.write('Converting {0}...'.format(base))
            filename = filename[0]                
            dest = ("{0}" + os.path.sep + "{1}.css").format(self.destination, filename)
            args.append(dest) # Now add the destination.
                        
            process = self.popen(args)
            process.wait()
    
    def popen(self, args):
        '''
        shell=False should allow us to have unescaped paths. Needs to be tested. If it
        doesn't work then we should properly espaced paths with spaces.
        '''
        return subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
    
    def watch(self):
        args = ['sass'] + self.get_arguments()
        args.append('--watch')
        args.append('{0}:{1}'.format(self.source, self.destination))
        self.process = self.popen(args)
        self.output = NonBlockingStreamReader(self.process.stdout)
                