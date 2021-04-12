from toee import *

def OnBeginSpellCast(spell):
    print "Blessed Aim OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Blessed Aim OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 10 * spell.caster_level # 1 min/cl

    for spellTarget in spell.target_list:
        targetIsFriendly = spellTarget.obj.is_friendly(spell.caster)
        if not targetIsFriendly: # Blessed Aim only affects allies
            targetsToRemove.append(spellTarget.obj)
        else:
            spellTarget.obj.condition_add_with_args('sp-Blessed Aim', spell.id, spell.duration)
            spellTarget.partsys_id = game.particles('sp-Faerie Fire', spellTarget.obj)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

    
def OnBeginRound(spell):
    print "Blessed Aim OnBeginRound"

def OnEndSpellCast(spell):
    print "Blessed Aim OnEndSpellCast"