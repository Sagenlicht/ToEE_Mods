from toee import *

def OnBeginSpellCast(spell):
    print "Acid Fog OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Acid Fog OnSpellEffect"

    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/caster_level

    acidFogObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    casterInitiative = spell.caster.get_initiative()
    acidFogObject.d20_status_init()
    acidFogObject.set_initiative(casterInitiative)
    game.update_combat_ui()

    acidFogObject.condition_add_with_args('sp-Acid Fog', spell.id, spell.duration)

    spell.target_list.remove_list(targetsToRemove)

def OnBeginRound(spell):
    print "Acid Fog OnBeginRound"

def OnEndSpellCast(spell):
    print "Acid Fog OnEndSpellCast"

