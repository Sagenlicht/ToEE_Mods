from toee import *

def OnBeginSpellCast(spell):
    print "Storm of Elemental Fury OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Storm of Elemental Fury OnSpellEffect"

    targetsToRemove = []
    spell.duration = 3

    for spellTarget in spell.target_list:
        targetsToRemove.append(spellTarget.obj)

    stormOfElementalFuryObject = game.obj_create(OBJECT_SPELL_GENERIC, spell.target_loc)

    casterInitiative = spell.caster.get_initiative()
    stormOfElementalFuryObject.d20_status_init()
    stormOfElementalFuryObject.set_initiative(casterInitiative)
    game.update_combat_ui()

    stormOfElementalFuryObject.condition_add_with_args('sp-Storm of Elemental Fury', spell.id, spell.duration, spell.dc, 0)

    spell.target_list.remove_list(targetsToRemove)

def OnBeginRound(spell):
    print "Storm of Elemental Fury OnBeginRound"

def OnEndSpellCast(spell):
    print "Storm of Elemental Fury OnEndSpellCast"

