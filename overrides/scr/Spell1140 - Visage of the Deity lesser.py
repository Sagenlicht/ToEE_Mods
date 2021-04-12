from toee import *

def OnBeginSpellCast(spell):
    print "Visage of the Deity lesser OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Visage of the Deity lesser OnSpellEffect"

    spell.duration = 1 * spell.caster_level
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Visage of the Deity lesser', spell.id, spell.duration)
    spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Visage of the Deity lesser OnBeginRound"

def OnEndSpellCast(spell):
    print "Visage of the Deity lesser OnEndSpellCast"

