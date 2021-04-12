from toee import *

def OnBeginSpellCast(spell):
    print "Fell the Greatest Foe OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Fell the Greatest Foe OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]

    spellTarget.partsys_id = game.particles('sp-True Strike', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-Fell the Greatest Foe', spell.id, spell.duration)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Fell the Greatest Foe OnBeginRound"

def OnEndSpellCast(spell):
    print "Fell the Greatest Foe OnEndSpellCast"