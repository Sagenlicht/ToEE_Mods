from toee import *

def OnBeginSpellCast(spell):
    print "Weapon of Energy OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Weapon of Energy OnSpellEffect"

    spell.duration = 1 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Weapon of Energy', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Weapon of Energy OnBeginRound"

def OnEndSpellCast(spell):
    print "Weapon of Energy OnEndSpellCast"

