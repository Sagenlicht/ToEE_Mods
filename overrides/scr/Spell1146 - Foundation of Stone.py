from toee import *

def OnBeginSpellCast(spell):
    print "Foundation of Stone OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Foundation of Stone OnSpellEffect"

    spell.duration = 1 * spell.caster_level

    for spellTarget in spell.target_list:
        spellTarget.obj.condition_add_with_args('sp-Foundation of Stone', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-Meld into Stone', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Foundation of Stone OnBeginRound"

def OnEndSpellCast(spell):
    print "Foundation of Stone OnEndSpellCast"

