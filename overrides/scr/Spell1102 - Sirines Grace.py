from toee import *

def OnBeginSpellCast(spell):
    print "Sirines Grace OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Sirines Grace OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/level
    spellTarget = spell.target_list[0]

    spellTarget.partsys_id = game.particles('sp-Heroism', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-Sirines Grace', spell.id, spell.duration)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Sirines Grace OnBeginRound"

def OnEndSpellCast(spell):
    print "Sirines Grace OnEndSpellCast"