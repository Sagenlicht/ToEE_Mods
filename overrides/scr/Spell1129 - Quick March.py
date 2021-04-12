from toee import *

def OnBeginSpellCast(spell):
    print "Quick March OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Quick March OnSpellEffect"

    targetsToRemove = []
    spell.duration = 1 # 1 round

    for spellTarget in spell.target_list:
        if spellTarget.obj.is_friendly(spell.caster): #Quick March only affects allies
            spellTarget.partsys_id = game.particles('sp-Expeditious Retreat', spellTarget.obj)
            spellTarget.obj.condition_add_with_args('sp-Quick March', spell.id, spell.duration, spell.dc)
        else:
            targetsToRemove.append(spellTarget.obj)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Quick March OnBeginRound"

def OnEndSpellCast(spell):
    print "Quick March OnEndSpellCast"