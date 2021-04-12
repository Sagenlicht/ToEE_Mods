from toee import *

def OnBeginSpellCast(spell):
    print "Fugue OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Fugue OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/cl

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    fugueObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    casterInitiative = spell.caster.get_initiative()
    fugueObject.d20_status_init()
    fugueObject.set_initiative(casterInitiative)

    fugueObject.condition_add_with_args('sp-Fugue', spell.id, spell.duration, spell.dc)
   
    spell.target_list.remove_list(targetsToRemove)
    #spell.spell_end(spell.id) #Spell end handled by fugueObject

def OnBeginRound(spell):
    print "Fugue OnBeginRound"

def OnEndSpellCast(spell):
    print "Fugue OnEndSpellCast"