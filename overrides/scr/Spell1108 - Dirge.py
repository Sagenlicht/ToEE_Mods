from toee import *

def OnBeginSpellCast(spell):
    print "Dirge OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Dirge OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/cl
    #spellTarget = spell.target_list[0]

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    dirgeObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    casterInitiative = spell.caster.get_initiative()
    dirgeObject.d20_status_init()
    dirgeObject.set_initiative(casterInitiative)

    dirgeObject.condition_add_with_args('sp-Dirge', spell.id, spell.duration, spell.dc)
   
    spell.target_list.remove_list(targetsToRemove)
    #spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Dirge OnBeginRound"

def OnEndSpellCast(spell):
    print "Dirge OnEndSpellCast"