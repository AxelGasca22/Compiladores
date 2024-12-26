
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSENTERO EQUAL FUNCION ID LBRACE LPAREN MINUS NUMBER PLUS RBRACE RPAREN SEMICOLONprograma : FUNCION ID LPAREN RPAREN LBRACE declaraciones RBRACEdeclaraciones : declaraciones declaracion\n                     | declaraciondeclaracion : ID EQUAL expresion SEMICOLONdeclaracion : ENTERO ID EQUAL expresion SEMICOLONdeclaracion : ENTERO ID SEMICOLONexpresion : expresion PLUS expresion\n                 | expresion MINUS expresionexpresion : NUMBERexpresion : ID'
    
_lr_action_items = {'FUNCION':([0,],[2,]),'$end':([1,12,],[0,-1,]),'ID':([2,6,8,9,10,11,13,18,19,20,21,22,26,],[3,7,7,-3,14,15,-2,15,-6,-4,15,15,-5,]),'LPAREN':([3,],[4,]),'RPAREN':([4,],[5,]),'LBRACE':([5,],[6,]),'ENTERO':([6,8,9,13,19,20,26,],[10,10,-3,-2,-6,-4,-5,]),'EQUAL':([7,14,],[11,18,]),'RBRACE':([8,9,13,19,20,26,],[12,-3,-2,-6,-4,-5,]),'NUMBER':([11,18,21,22,],[17,17,17,17,]),'SEMICOLON':([14,15,16,17,23,24,25,],[19,-10,20,-9,26,-7,-8,]),'PLUS':([15,16,17,23,24,25,],[-10,21,-9,21,-7,-8,]),'MINUS':([15,16,17,23,24,25,],[-10,22,-9,22,-7,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'declaraciones':([6,],[8,]),'declaracion':([6,8,],[9,13,]),'expresion':([11,18,21,22,],[16,23,24,25,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> FUNCION ID LPAREN RPAREN LBRACE declaraciones RBRACE','programa',7,'p_programa','compilador.py',61),
  ('declaraciones -> declaraciones declaracion','declaraciones',2,'p_declaraciones','compilador.py',65),
  ('declaraciones -> declaracion','declaraciones',1,'p_declaraciones','compilador.py',66),
  ('declaracion -> ID EQUAL expresion SEMICOLON','declaracion',4,'p_declaracion_asignacion','compilador.py',70),
  ('declaracion -> ENTERO ID EQUAL expresion SEMICOLON','declaracion',5,'p_declaracion_entero_asignado','compilador.py',74),
  ('declaracion -> ENTERO ID SEMICOLON','declaracion',3,'p_declaracion_entero_no_asignado','compilador.py',78),
  ('expresion -> expresion PLUS expresion','expresion',3,'p_expresion_binaria','compilador.py',82),
  ('expresion -> expresion MINUS expresion','expresion',3,'p_expresion_binaria','compilador.py',83),
  ('expresion -> NUMBER','expresion',1,'p_expresion_number','compilador.py',88),
  ('expresion -> ID','expresion',1,'p_expresion_id','compilador.py',92),
]
