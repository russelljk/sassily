from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
import time
from ...manager import Manager

def mulitple_args_cb(option, opt_str, value, parser):
    args=[]
    for arg in parser.rargs:
        if arg[0] != "-":
            args.append(arg)
        else:
            del parser.rargs[:len(args)]
            break
    if getattr(parser.values, option.dest):
        args.extend(getattr(parser.values, option.dest))
    setattr(parser.values, option.dest, args)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-w", 
            "--watch", 
            dest="watch_dir",
            action="store_true",
            default=False,
            help="Watch for css changes."),
        make_option(
            "-q", 
            "--quiet", 
            dest="quiet",
            action="store_true",
            default=False,
            help="Run quietly."
        ),
        make_option(
            "-c", 
            "--compress", 
            dest="compress",
            action="store_true",
            default=False,
            help="Compress css files."
        ),
        make_option(
            "-l", 
            "--location", 
            dest="locations",
            action='callback',
            callback=mulitple_args_cb,
            help="Which location(s) of scss files to process."
        ),
    )
    
    def handle(self, *args, **options):
        sassily_config = getattr(settings, 'SASSILY_CONFIG', None)
        
        if sassily_config is None:
            raise CommandError('Make sure to set SASSILY_CONFIG in your project settings to point to your scss files.')
        
        compress = options['compress']
        watch = options['watch_dir']
        quiet = options['quiet']
        locations = options['locations']
        
        managers = []
        
        for location in sassily_config:
            # Skip this location depending on what the user wants.
            if locations and (location not in locations):
                continue
            
            if not quiet:
                self.stdout.write('\nProcessing location {0}\n'.format(location))
            
            config = sassily_config[location]
            sass_args = config.copy()
            sass_args['command'] = self
            sass_args['compress'] = compress
            
            manager = Manager(**sass_args)
            managers.append(manager)
            
            if watch:
                manager.watch()
            else:
                manager.run()
        
        '''
        We need to keep running as long as the subprocess's are running. So every 1s 
        we poll the process and print out and input it has waiting.
        
        The processes are running in the background, they are not put to sleep when we
        are.
        '''
        if watch:
            processes_running = True
            while processes_running:
                time.sleep(1)
                processes_running = False
                for manager in managers:
                    if manager.is_running():
                        lines = manager.readlines()
                        if lines:
                            self.stdout.write('\n'.join(lines))
                        processes_running = True
    


