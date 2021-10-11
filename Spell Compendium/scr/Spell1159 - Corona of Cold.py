from toee import *

def OnBeginSpellCast(spell):
    print "Corona of Cold OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Corona of Cold OnSpellEffect"

    spell.duration = 1 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Corona of Cold', spell.id, spell.duration, spell.dc)
    spellTarget.partsys_id = game.particles('sp-Corona of Cold', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Corona of Cold OnBeginRound"

def OnEndSpellCast(spell):
    print "Corona of Cold OnEndSpellCast"

