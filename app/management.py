# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------

"""
Creates the default Objects, after created tables (syncdb) 
"""

from django.db.models import signals
from django.db import connections
from django.db import router
import models as site_app
from django.core.management.color import no_style

from app import models


import os, sys
from django.db.models import signals
from django.db import connection, transaction
from django.conf import settings

def load_customized_sql(app, created_models, verbosity=2, **kwargs):
    app_dir = os.path.normpath(os.path.join(os.path.dirname(app.__file__),'sql'))
    custom_files = [os.path.join(app_dir, "custom.%s.sql" % settings.DATABASES['default']['ENGINE']),
                    os.path.join(app_dir, "custom.sql")]

    for custom_file in custom_files: 
        if os.path.exists(custom_file):
            print "Loading customized SQL for %s" % app.__name__
            fp = open(custom_file, 'U')
            cursor = connection.cursor()
            try:
                cursor.execute(fp.read().decode(settings.FILE_CHARSET))
            except Exception, e:
                sys.stderr.write("Couldn't execute custom SQL for %s" % app.__name__)
                import traceback
                traceback.print_exc()
                transaction.rollback_unless_managed()
            else:
                transaction.commit_unless_managed()

        
signals.post_syncdb.connect(load_customized_sql)
