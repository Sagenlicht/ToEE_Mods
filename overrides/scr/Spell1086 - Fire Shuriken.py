from toee import *

def OnBeginSpellCast(spell):
    print "Fire Shuriken OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Fire Shuriken OnSpellEffect"

    spell.duration = 0
    spellTarget = spell.target_list[0]
    shurikensToCreate = min((spell.caster_level/3), 6) #capped at 6 Shuriken
    print "Shuriken created: ", shurikensToCreate

    for shuriken in range(shurikensToCreate):
        createdShruriken = game.obj_create(4998, spell.caster.location)
        spell.caster.item_get(createdShruriken)

    spell.caster.condition_add('sp-Fire Shuriken')
    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Fire Shuriken OnBeginRound"

def OnEndSpellCast(spell):
    print "Fire Shuriken OnEndSpellCast"