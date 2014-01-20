import logging
from osv import osv, fields
import time

_logger = logging.getLogger(__name__)

class course(osv.osv):
 _name = "management.course"
 _description = "Course"
 
 def get_certificates(self, cr, uid, ids, context=None):
  this = self.browse(cr, uid, ids)[0]
  _logger.info("%s" % this.name)
  for participant in this.participant_ids:
   _logger.info("%s" % participant.name)

  self.write(cr, uid, ids, {'state' : 'get',
                            'certificate_pdf' : out}, context=context)

  return {
   'type': 'ir.actions.act_window',
   'res_model': 'management.course',
   'view_mode': 'form',
   'view_type': 'form',
   'res_id': this.id ,
   'views': [(False, 'form')],
   'target': 'new',
  }

 _columns = {
              "name" : fields.char("Course Name",size=256,required=True),
              "start_date" : fields.date("Start Date"),
              "end_date":fields.date("End Date"),
              "hours" : fields.float("Hours",digits=(6,2),help="Duration"),
              "participant_ids": fields.one2many("participant","course_id","Participant"),
              "place": fields.char("Place of course",size=256,required=True),
              "technical_requirement" : fields.one2many("technical.requirement.course","requirement_course","Technical Requirement"),
              "certificate_pdf" : fields.binary("File", readonly=True),
              "state" : fields.selection([('choose', 'choose'),
                                          ('get', 'get')], )
            }

 _defaults = {
  'state' : 'choose',
 }

 def restart_state(self, cr, uid, ids, context=None):
  self.write(cr, uid, ids, {'state' : 'choose'}, context=context)
  return True

course()


class partner_participant(osv.osv):
 _name = "participant"
 _description = "Course Instructor"
 
 _columns = {
            "name" : fields.many2one("res.partner", "name", "Instructor"),
            "cedula_rif" : fields.char("Cedula-Rif",size=12),
            "course_id" : fields.many2one("management.course","Course",required=True,ondelete="cascade"),
            }
partner_participant()


class technical_requirement_course(osv.osv):
 _name = "technical.requirement.course"
 _description = "Technical Requirement Course"
 
 _columns = {
              "requirement" : fields.char("Requirement",size=256,required=True),
              "requirement_course": fields.many2one("management.course","Requirement Course",required=True,ondelete="cascade"),
            }
technical_requirement_course()

