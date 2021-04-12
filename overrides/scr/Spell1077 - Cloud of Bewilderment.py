from toee import *

def OnBeginSpellCast(spell):
    print "Cloud of Bewilderment OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Cloud of Bewilderment OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/cl
    #spellTarget = spell.target_list[0]

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    cloudOfBewildermentObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    casterInitiative = spell.caster.get_initiative()
    cloudOfBewildermentObject.d20_status_init()
    cloudOfBewildermentObject.set_initiative(casterInitiative)

    cloudOfBewildermentObject.condition_add_with_args('sp-Cloud of Bewilderment', spell.id, spell.duration, spell.dc)
   
    spell.target_list.remove_list(targetsToRemove)
    #spell.spell_end(spell.id) #Spell end handled by cloudOfBewildermentObject

def OnBeginRound(spell):
    print "Cloud of Bewilderment OnBeginRound"

def OnEndSpellCast(spell):
    print "Cloud of Bewilderment OnEndSpellCast"