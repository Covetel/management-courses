import time

from openerp.report import report_sxw

class course(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context=None):
    		super(course, self).__init__(cr, uid, name, context=context)
        	self.localcontext.update({
        		'time': time,
        	})


report_sxw.report_sxw('report.management.course', 'management.course', 'addons/management-courses/report/certificates.rml',parser=course, header=False)
  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
  

