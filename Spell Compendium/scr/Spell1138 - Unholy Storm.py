from toee import *

def OnBeginSpellCast(spell):
    print "Unholy Storm OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Unholy Storm OnSpellEffect"

    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/caster_level
    spellTarget = spell.target_list[0]

    unholyStormObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    casterInitiative = spell.caster.get_initiative()
    unholyStormObject.d20_status_init()
    unholyStormObject.set_initiative(casterInitiative)
    game.update_combat_ui()

    unholyStormObject.condition_add_with_args('sp-Unholy Storm', spell.id, spell.duration)

    spell.target_list.remove_list(targetsToRemove)
    #spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Unholy Storm OnBeginRound"

def OnEndSpellCast(spell):
    print "Unholy Storm OnEndSpellCast"

