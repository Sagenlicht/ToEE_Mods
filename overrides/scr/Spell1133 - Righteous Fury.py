from toee import *

def OnBeginSpellCast(spell):
    print "Righteous Fury OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Righteous Fury OnSpellEffect"

    spell.duration = 10 * spell.caster_level # 1 minutes/CL
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Righteous Fury', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Bullstrength', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Righteous Fury OnBeginRound"

def OnEndSpellCast(spell):
    print "Righteous Fury OnEndSpellCast"