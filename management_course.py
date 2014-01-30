import logging
from osv import osv, fields
import time
import base64
from openerp import modules, tools
import subprocess

_logger = logging.getLogger(__name__)

class course(osv.osv):
    _name = "management.course"
    _description = "Course"
    _table = "management_course"
    
    def get_certificates(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids)[0]
        path_module = modules.get_module_path('management-courses')
        file = open(path_module + "/course_data.txt", "w")

        for participant in this.participant_ids:
            file.write("%s,%s,%s,%s,%s,%s:%s\n" % (this.name,
                                                 this.start_date,
                                                 this.end_date,
                                                 this.hours,
                                                 "Instructor",
                                                 participant.name.name,
                                                 participant.cedula_rif))
        file.close()

        command = "perl " + path_module + "/generarcertificados.pl"
#        process = subprocess.Popen("perl", path_module + "/generarcertificados.pl")

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
        "participant_ids": fields.one2many("participant","course_id","Participant"),
        "company_ids": fields.many2one("res.partner","name","Company"),
        "place": fields.char("Place of course",size=256,required=True),
        "technical_requirement" : fields.one2many("technical.requirement.course","requirement_course","Technical Requirement"),
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


class partner_participant(osv.osv):
    _name = "participant"
    _description = "Course Instructor"
    _table = "participant"
    
    def _check_cedula(self,cr,uid,ids,cedula_rif,context=None):
        if cedula_rif.find("V-")!=-1 or cedula_rif.find("E-")!=-1:
            return True
        else:
            return False

    def _check_cedula_rif_numeros(self,cr,uid,ids,context=None):
        participants=self.browse(cr,uid,ids,context=context)
        for participant in participants:
            for caracter in participant.cedula_rif[2:]:
               if caracter.isalpha():
                    return False
            return True

    def _check_length_cedula(self,cr,uid,ids,context=None):
        participants=self.browse(cr,uid,ids,context=context)
        for participant in participants:
            if len(participant.cedula_rif[2:]) > 8 or len(participant.cedula_rif[2:]) < 8:
                return False
        return True
    
    def onchange_cedula(self,cr, uid,ids,cedula_rif,context=None):
        if cedula_rif != False:
            if self._check_cedula(cr,uid,ids,cedula_rif,context) == False:
                return {'value' : {'cedula_rif': ''}, 'warning' : {'title' : 'warning','message' : 'Cedula Invalida'}}
            else:
                return {'value' : {'cedula_rif' : cedula_rif}}
        else:
            return {'value': {'cedula_rif' : ''},'warning':{'title' : 'warning', 'message' : 'Campo cédula vacio'}}


    _columns = {
        "name" : fields.many2one("res.partner", "name", "Instructor"),
        "cedula_rif" : fields.char("Cedula-Rif",size=12,required=True),
        "course_id" : fields.many2one("management.course","Course",required=True,ondelete="cascade"),
        "is_instructor" : fields.boolean("Instructor"),
    }
        
partner_participant()


class technical_requirement_course(osv.osv):
    _name = "technical.requirement.course"
    _description = "Technical Requirement Course"
    _table = "technical_requirement_course" 
    _columns = {

        "name" : fields.many2one("requirement","name","Requirement Course"),
        "requirement_course": fields.many2one("management.course","Requirement Course",required=True,ondelete="cascade"),
    }
technical_requirement_course()

class requirement(osv.osv):
    _name = "requirement"
    _description = "Requirement"

    _columns = {
                 "name" : fields.char("Requirement",size=256,required=True),
               }
requirement()
