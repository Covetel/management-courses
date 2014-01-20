import logging
from osv import osv, fields
import time

_logger = logging.getLogger(__name__)

class course(osv.osv):
	_name = "management.course"
 	_description = "Course"
 	_table = "management_course"

	def get_certificates(self, cr, uid, ids, context=None):
		_logger.info("Hola mundo")
		return True

 	_columns = {
			"name" : fields.char("Course Name",size=256,required=True),
            "start_date" : fields.date("Start Date"),
            "end_date":fields.date("End Date"),
            "hours" : fields.float("Hours",digits=(6,2),help="Duration"),
            "participant_ids": fields.one2many("participant","course_id","Participant"),
            "place": fields.char("Place of course",size=256,required=True),
            "technical_requirement" : fields.one2many("technical.requirement.course","requirement_course","Technical Requirement"),
            "certificate_pdf" : fields.binary("File", readonly=True),
    }
course()


class partner_participant(osv.osv):
	_name = "participant"
	_description = "Course Instructor"
	_table = "participant"
    
	_sql_constraints = [('cedula_rif','unique(cedula_rif)','!La cedula debe ser unica!')]

	_columns = {
	           "name" : fields.many2one("res.partner", "name", "Instructor"),
	           "cedula_rif" : fields.char("Cedula-Rif",size=12),
	           "course_id" : fields.many2one("management.course","Course",required=True,ondelete="cascade"),
               "is_instructor" : fields.boolean("Instructor"),
	           }
	
partner_participant()


class technical_requirement_course(osv.osv):
	_name = "technical.requirement.course"
	_description = "Technical Requirement Course"
	_table = "technical_requirement_course" 
	_columns = {
	             "requirement" : fields.char("Requirement",size=256,required=True),
	             "requirement_course": fields.many2one("management.course","Requirement Course",required=True,ondelete="cascade"),
	}
technical_requirement_course()

