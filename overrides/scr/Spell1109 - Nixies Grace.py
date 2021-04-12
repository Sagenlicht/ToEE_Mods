from toee import *

def OnBeginSpellCast(spell):
    print "Nixies Grace OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Nixies Grace OnSpellEffect"

    spell.duration = 100 * spell.caster_level # 10 mins/level
    spellTarget = spell.target_list[0]

    spellTarget.partsys_id = game.particles('sp-Resistance', spell.caster)
    spellTarget.obj.condition_add_with_args('sp-Nixies Grace', spell.id, spell.duration)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Nixies Grace OnBeginRound"

def OnEndSpellCast(spell):
    print "Nixies Grace OnEndSpellCast"