from toee import *

def OnBeginSpellCast(spell):
    print "Angelskin OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Angelskin OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/level
    spellTarget = spell.target_list[0].obj
    spellTargetAlignment = spellTarget.stat_level_get(stat_alignment)

    if spellTargetAlignment == ALIGNMENT_LAWFUL_GOOD: #Angelskin works only on LG targets
        spellTarget.condition_add_with_args('sp-Angelskin', spell.id, spell.duration)
        spell.target_list[0].partsys_id = game.particles('sp-Heroism', spellTarget)
    else:
        spellTarget.float_text_line("Wrong Alignment", tf_red)
        game.particles('Fizzle', spellTarget)
        spell.target_list.remove_target(spellTarget)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Angelskin OnBeginRound"

def OnEndSpellCast(spell):
    print "Angelskin OnEndSpellCast"