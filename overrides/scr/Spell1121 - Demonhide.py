from toee import *

def OnBeginSpellCast(spell):
    print "Demonhide OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Demonhide OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/level
    spellTarget = spell.target_list[0].obj
    spellTargetAlignment = spellTarget.stat_level_get(stat_alignment)
    allowedAlignments = [NEUTRAL_EVIL, LAWFUL_EVIL, CHAOTIC_EVIL]

    if spellTargetAlignment in allowedAlignments: #Demonhide works only on evil targets
        spellTarget.condition_add_with_args('sp-Demonhide', spell.id, spell.duration)
        spell.target_list[0].partsys_id = game.particles('sp-True Strike', spellTarget)
    else:
        spellTarget.float_text_line("Not evil", tf_red)
        game.particles('Fizzle', spellTarget)
        spell.target_list.remove_target(spellTarget)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Demonhide OnBeginRound"

def OnEndSpellCast(spell):
    print "Demonhide OnEndSpellCast"