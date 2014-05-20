import logging
from osv import osv, fields
import time
import base64
from openerp import modules, tools
import subprocess
import pprint
import codecs
import time 
import re
_logger = logging.getLogger(__name__)

class course(osv.osv):
    _name = "management.course"
    _description = "Management Course"
    
    def get_certificates(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids)[0]
        path_module = modules.get_module_path('management-courses')
        file = codecs.open(path_module + "/course_data.txt", "w")
        
        instructor_id = self.browse(cr,uid,ids)
        for i in instructor_id[0].participant_ids:
            if i.is_instructor == True:
                instructor = i.name.name

        for participant in this.participant_ids:
            if participant.is_instructor == False:
                data = "%s,%s,%s,%s,%s,%s:%s\n" % (this.name,
                                                       time.strftime("%d/%m/%y", time.strptime(this.start_date, "%Y-%m-%d")),
                                 time.strftime("%d/%m/%y", time.strptime(this.end_date, "%Y-%m-%d")),
                                                       this.hours,
                                                       instructor,
                                                       participant.name.name,
                                                       participant.cedula_rif)
                file.write(data.encode('utf-8'))
        file.close()

        command = "perl " + path_module + "/generarcertificados.pl"
        process = subprocess.call(["perl", path_module + "/generarcertificados.pl"])

        file = open(path_module + 
                    "/" + 
                    this.name + 
                    ".pdf", "rb")
        
        fileContent = file.read()
        out = base64.encodestring(fileContent)

        self.write(cr, uid, ids, {'state' : 'get',
                                 'certificate_pdf' : out}, context=context)
        file.close()
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
        "user_id": fields.many2one('res.users', 'Instructor', select=True),
        "participant_ids": fields.many2many("res.partner", "course_partner_rel", "course_id", "name", "Participantes del Curso"),
        "company_ids":fields.many2one('res.partner', 'Company', select=True),
        "place": fields.char("Place of course",size=256,required=True),
        "technical_requirement" : fields.one2many("management.course.tecreq","requirement_course","Technical Requirement"),
        "certificate_pdf" : fields.binary("File", readonly=True),
        "state" : fields.selection([('choose', 'choose'),
                                    ('get', 'get')])
    }

    _defaults = {
        'state' : 'choose',
        "start_date" : lambda *a: time.strftime('%Y-%m-%d'),
        "end_date" :  lambda *a: time.strftime('%Y-%m-%d'),
      }

    def restart_state(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state' : 'choose'}, context=context)
        return True
        
course()
        
class technical_requirement_course(osv.osv):
    _name = "management.course.tecreq"
    _description = "Technical Requirement Course"

    _columns = {
        "name" : fields.many2one("management.course.requirement","name","Requirement Course"),
        "requirement_course": fields.many2one("management.course","Requirement Course",required=True,ondelete="cascade"),
    }
technical_requirement_course()

class requirement(osv.osv):
    _name = "management.course.requirement"
    _description = "Courses Requirements"

    _columns = {
                 "name" : fields.char("Requirement",size=256,required=True),
    }
requirement()
