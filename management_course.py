
from osv import osv, fields
import time

class course(osv.osv):
 _name = "management.course"
 _description = "Course"
 
 _columns = {
              "course_name" : fields.char("Course Name",size=256,required=True),
              "start_date" : fields.date("Start Date"),
              "end_date":fields.date("End Date"),
              "hours" : fields.float("Hours",digits=(6,2),help="Duration"),
              "instructor_ids": fields.one2many("instructor","partner_id","Instructor"),
              "attendee_ids": fields.one2many("res.partner","partner_id","Attendee"),
              "place": fields.char("Place of course",size=256,required=True),
              "technical_requirement" : fields.one2many("technical.requirement.course","requirement_course","Technical Requirement"),
            }
course()

class partner(osv.osv):
 _name = "res.partner"
 _description = "Attendee"
 _inherit = "res.partner"

 _columns = {
              "partner_id" : fields.many2one("management.course","Course",required=True,ondelete="cascade"),
              "cedula_rif" : fields.char("Cedula-Rif  ",size=12,required=True),
            } 
partner()

class partner_instructor(osv.osv):
 _name = "instructor"
 _description = "Course Instructor"
 _inherit = "res.partner"
 _table = ""
partner_instructor()

class technical_requirement_course(osv.osv):
 _name = "technical.requirement.course"
 _description = "Technical Requirement Course"
 
 _columns = {
              "requirement" : fields.char("Requirement",size=256,required=True),
              "requirement_course": fields.many2one("management.course","Requirement Course",required=True,ondelete="cascade"),
            }
technical_requirement_course()

