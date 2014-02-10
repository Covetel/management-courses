import time
from openerp.report import report_sxw

class certificates(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(certificates, self).__init__(cr, uid, name, context=context)

        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.management.course', 'management.course', 
                      '/home/xyklex/OpenERP-Modules/management-courses/report/report_certificates.rml', 
                      parser=certificates)
