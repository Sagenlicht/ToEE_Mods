from toee import *

def OnBeginSpellCast(spell):
    print "Hand of Divinity OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Hand of Divinity OnSpellEffect"

    spell.duration = 10 * spell.caster_level # 1 min/level
    spellTarget = spell.target_list[0].obj
    spellCasterDeity = spell.caster.get_deity()
    spellTargetDeity = spellTarget.get_deity()
    spellTargetAlignment = spellTarget.stat_level_get(stat_alignment)
    evilAlignments = [ALIGNMENT_EVIL, ALIGNMENT_NEUTRAL_EVIL, ALIGNMENT_LAWFUL_EVIL, ALIGNMENT_CHAOTIC_EVIL]
    
    searchID = 5000 + spellCasterDeity
    getDeityAlignment = game.get_mesline('mes\\deity.mes', searchID)
    if "Error" in getDeityAlignment: #safety check, if added lines are missing in deity.mes
        deityAlignment = spell.caster.stat_level_get(stat_alignment)
    else:
        deityAlignment = globals()[getDeityAlignment]

    if spellCasterDeity == spellTargetDeity or deityAlignment == spellTargetAlignment:
        if deityAlignment in evilAlignments:
            isProfaneBonus = 1
        else:
            isProfaneBonus = 0
        spellTarget.condition_add_with_args('sp-Hand of Divinity', spell.id, spell.duration, isProfaneBonus)
        spell.target_list[0].partsys_id = game.particles('sp-Heroism', spellTarget)
    else:
        spellTarget.float_text_line("Wrong Alignment", tf_red)
        game.particles('Fizzle', spellTarget)
        spell.target_list.remove_target(spellTarget)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Hand of Divinity OnBeginRound"

def OnEndSpellCast(spell):
    print "Hand of Divinity OnEndSpellCast"
