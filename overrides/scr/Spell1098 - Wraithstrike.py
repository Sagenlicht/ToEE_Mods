from toee import *

def OnBeginSpellCast(spell):
    print "Wraithstrike OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Wraithstrike OnSpellEffect"

    spell.duration = 0 # current round
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Wraithstrike', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-True Strike', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Wraithstrike OnBeginRound"

def OnEndSpellCast(spell):
    print "Wraithstrike OnEndSpellCast"