
from osv import osv, fields
import time

class course(osv.osv):
 _name = "management.course"
 _description = "Course"
 
 _columns = {
              "course_name" : fields.char("Course Name",size=30,required=True),
              "start_date" : fields.date("Stard Date"),
              "end_date":fields.date("End Date"),
              "hours" : fields.float("Hours",digits=(6,2),help="Duration"),
              #"instructor": fields.one2many("res.users","user_id","Instructor"),
              "attendee_ids": fields.one2many("res.partner","partner_id","Attendee"),
              "place": fields.char("Place of course",size=40,required=True),
            }
course()

class partner(osv.osv):
 _name = "res.partner"
 _description = "Attendee"
 _inherit = "res.partner"
 _columns = {
              "partner_id" : fields.many2one("management.course","Course",required=True,ondelete="cascade"),
            } 
partner()

