from toee import *

def OnBeginSpellCast(spell):
    print "Veil of Shadow OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Veil of Shadow OnSpellEffect"

    spell.duration = 10 * spell.caster_level # 1 min/cl
    spellTarget = spell.target_list[0]

    checkOutdoor = game.is_outdoor()
    dayTime = game.time.time_game_in_hours(game.time)
    if dayTime in range(6,18): #includes 6 excludes 18
        daylightDispel = True
    else:
        daylightDispel = False

    if checkOutdoor and daylightDispel:
        spellTarget.obj.float_text_line("Dispelled by daylight")
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)
    else:
        spellTarget.partsys_id = game.particles('sp-Veil of Shadow', spell.caster)
        spellTarget.obj.condition_add_with_args('sp-Veil of Shadow', spell.id, spell.duration)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Veil of Shadow OnBeginRound"

def OnEndSpellCast(spell):
    print "Veil of Shadow OnEndSpellCast"