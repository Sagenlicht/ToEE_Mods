from toee import *

def OnBeginSpellCast(spell):
    print "Anarchic Storm OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Anarchic Storm OnSpellEffect"

    spell.duration = 1 * spell.caster_level # 1 round/caster_level
    spellTarget = spell.target_list[0]

    anarchicStormObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    casterInitiative = spell.caster.get_initiative()
    anarchicStormObject.d20_status_init()
    anarchicStormObject.set_initiative(casterInitiative)
    game.update_combat_ui()

    anarchicStormObject.condition_add_with_args('sp-Anarchic Storm', spell.id, spell.duration)

    spell.target_list.remove_target(spellTarget.obj)

    #spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Anarchic Storm OnBeginRound"

def OnEndSpellCast(spell):
    print "Anarchic Storm OnEndSpellCast"

