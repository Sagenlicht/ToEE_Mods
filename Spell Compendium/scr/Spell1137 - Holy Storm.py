from toee import *

def OnBeginSpellCast(spell):
    print "Holy Storm OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Holy Storm OnSpellEffect"

    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/caster_level
    spellTarget = spell.target_list[0]

    holyStormObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    casterInitiative = spell.caster.get_initiative()
    holyStormObject.d20_status_init()
    holyStormObject.set_initiative(casterInitiative)
    game.update_combat_ui()

    holyStormObject.condition_add_with_args('sp-Holy Storm', spell.id, spell.duration)

    spell.target_list.remove_list(targetsToRemove)
    #spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Holy Storm OnBeginRound"

def OnEndSpellCast(spell):
    print "Holy Storm OnEndSpellCast"

