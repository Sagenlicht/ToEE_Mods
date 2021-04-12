from toee import *

def OnBeginSpellCast(spell):
    print "Resistance Superior OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Resistance Superior OnSpellEffect"

    spell.duration = 14400 # 24h
    spellTarget = spell.target_list[0]

    spellTarget.partsys_id = game.particles('sp-Resistance', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-Resistance Superior', spell.id, spell.duration)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Resistance Superior OnBeginRound"

def OnEndSpellCast(spell):
    print "Resistance Superior OnEndSpellCast"