import os
import glob
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option

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
    )
    
    def handle(self, *args, **options):
        
        staging_dir = getattr(settings, 'SASSILY_SRC_DIR', None)
        use_compass = getattr(settings, 'SASSILY_USE_COMPASS', False)
        reqs = getattr(settings, 'SASSILY_REQS', None)
        
        if not staging_dir:
            raise CommandError('Make sure to set SASSILY_SRC_DIR in your project settings to point to your scss files.')
            
        dest_dir = getattr(settings, 'SASSILY_DEST_DIR', None)
        
        if not dest_dir:
            raise CommandError('Make sure to set SASSILY_DEST_DIR in your settings to point to the destination for scss->css conversions.')
            
        if options['compress']:
            style = 'compressed'
        else:
            style = 'nested'
            
        watch = options['watch_dir']
        quiet = options['quiet']
        
        path = ("{0}" + os.path.sep + "*.scss").format(staging_dir)
        
        if use_compass:
            cmd_name = "sass --compass"
        else:
            cmd_name = "sass"
        
        if reqs:
            for req in reqs:
                cmd_name += ' --require ' + req
                
        if not watch:
            cmd_fmt = cmd_name + " --style {0} {1} {2}" + os.path.sep + "{3}.css"
                        
            for f in glob.glob(path):
                base = os.path.basename(f)
                filename = os.path.splitext(base)
                if not quiet:
                    self.stdout.write('Converting {0}...'.format(base))
                filename = filename[0]
                cmd = cmd_fmt.format(style, f, dest_dir, filename)                
                
                os.system(cmd)
        else:
            cmd_fmt = cmd_name + " --style {0} --watch {1}:{2}"
            cmd = cmd_fmt.format(style, staging_dir, dest_dir)
            os.system(cmd)

