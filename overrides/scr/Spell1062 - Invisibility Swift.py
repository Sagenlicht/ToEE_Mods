from toee import *

def OnBeginSpellCast(spell):
    print "Invisibility, Swift OnBeginSpellCast"
    print "spell.spellTarget_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Invisibility, Swift OnSpellEffect"

    spell.duration = 0 #1 round; Condition gets removed at start of next turn so 1 self buff condition = 0
    spellTarget = spell.target_list[0]

    spellTarget.obj.condition_add_with_args('sp-Invisibility', spell.id, spell.duration, 0) #uses existing Invisibility spell
    spellTarget.partsys_id = game.particles('sp-Invisibility', spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Invisibility, Swift OnBeginRound"

def OnEndSpellCast(spell):
    print "Invisibility, Swift OnEndSpellCast"