from toee import *

def OnBeginSpellCast(spell):
    print "Energized Shield Lesser OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Energized Shield Lesser OnSpellEffect"

    spell.duration = 1 * spell.caster_level
    spellTarget = spell.target_list[0]
    radialChoice = spell.spell_get_menu_arg(RADIAL_MENU_PARAM_MIN_SETTING)

    if radialChoice == 1:
        elementType = D20DT_ACID
        #spellParticles = 'sp-Resist Elements-acid'
    elif radialChoice == 2:
        elementType = D20DT_COLD
        #spellParticles = 'sp-Resist Elements-cold'
    elif radialChoice == 3:
        elementType = D20DT_ELECTRICITY
        #spellParticles = 'sp-Resist Elements-water'
    elif radialChoice == 4:
        elementType = D20DT_FIRE
        #spellParticles = 'sp-Resist Elements-fire'
    elif radialChoice == 5:
        elementType = D20DT_SONIC
        #spellParticles = 'sp-Resist Elements-sonic'

    itemToEnchant = spellTarget.obj.item_worn_at(item_wear_shield)

    if not itemToEnchant == OBJ_HANDLE_NULL:
        itemToEnchant.d20_status_init()
        if not itemToEnchant.condition_add_with_args('sp-Energized Shield Lesser', spell.id, spell.duration, elementType):
            #spellTarget.partsys_id = game.particles('sp-Sound Burst', spellTarget.obj)
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30000)
            game.particles('Fizzle', spellTarget.obj)
    else:
        spellTarget.obj.float_text_line("Shield required", tf_red)
        game.particles('Fizzle', spellTarget.obj)

    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Energized Shield Lesser OnBeginRound"

def OnEndSpellCast(spell):
    print "Energized Shield Lesser OnEndSpellCast"

