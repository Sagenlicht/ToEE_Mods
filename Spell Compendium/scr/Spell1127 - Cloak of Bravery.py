from toee import *

def OnBeginSpellCast(spell):
    print "Cloak of Bravery OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Cloak of Bravery OnSpellEffect"

    spell.duration = 100 * spell.caster_level # 10 minutes/level
    spellTarget = spell.target_list[0].obj
    spellBonus = min(spell.caster_level, 10) #bonus caps at cl 10

    spellTarget.condition_add_with_args('sp-Cloak of Bravery', spell.id, spell.duration, spellBonus)
    #spell.target_list[0].partsys_id = game.particles('sp-Heroism', spellTarget)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Cloak of Bravery OnBeginRound"

def OnEndSpellCast(spell):
    print "Cloak of Bravery OnEndSpellCast"