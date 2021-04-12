from toee import *

def OnBeginSpellCast(spell):
    print "Conviction OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Conviction OnSpellEffect"

    spell.duration = 100 * spell.caster_level
    spellTarget = spell.target_list[0]
    spellBonus = min((2 + (caster.caster_level/6)), 5) #Capped at CL 18 for a total bonus of +5
    print "Conviction Bonus: {}".format(spellBonus)

    spellTarget.obj.condition_add_with_args('sp-Conviction', spell.id, spell.duration, spellBonus)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Conviction OnBeginRound"

def OnEndSpellCast(spell):
    print "Conviction OnEndSpellCast"

