from toee import *

def OnBeginSpellCast(spell):
    print "Energy Vortex OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Energy Vortex OnSpellEffect"

    targetsToRemove = []
    spell.duration = 0
    spellDamageDice = dice_new('1d8')
    spellDamageDice.number = 1
    spellDamageDice.bonus = min(spell.caster_level, 20)
    radialChoice = spell.spell_get_menu_arg(RADIAL_MENU_PARAM_MIN_SETTING) # 1 = acid; 2 = cold; 3 = electricity; 4 = fire; 5-8 same + amplify flag
    if not radialChoice in range(1,9): #Fallback
        radialChoice = game.random_range(1,4) #element is chosen randomly no amplify option to avoid random suicides
    if radialChoice > 4:
        spellDamageDice.number = 2
        spellDamageDice.bonus *= 2
        isAmplified = True
    else:
        isAmplified = False
    if radialChoice == 1 or radialChoice == 5:
        spellDescriptor = D20DT_ACID
        game.particles('sp-Energy Vortex Acid', spell.caster)
    elif radialChoice == 2 or radialChoice == 6:
        spellDescriptor = D20DT_COLD
        game.particles('sp-Energy Vortex Cold', spell.caster)
    elif radialChoice == 3 or radialChoice == 7:
        spellDescriptor = D20DT_ELECTRICITY
        game.particles( 'sp-Chain Lightning', spell.target_loc )
        game.pfx_chain_lightning( spell.caster, spell.num_of_targets, spell.target_list )
    else:
        spellDescriptor = D20DT_FIRE
        game.particles('sp-Energy Vortex Fire', spell.caster)

    for spellTarget in spell.target_list:
        #Save for half damage:
        if spellTarget.obj.reflex_save_and_damage(spell.caster, spell.dc, D20_Save_Reduction_Half, D20STD_F_NONE, spellDamageDice, spellDescriptor, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
        else:
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
        targetsToRemove.append(spellTarget.obj)

    if isAmplified:
        spellDamageDice.number = 1
        spellDamageDice.bonus = min(spell.caster_level, 20)
        spell.caster.spell_damage(spell.caster, spellDescriptor, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Energy Vortex OnBeginRound"

def OnEndSpellCast(spell):
    print "Energy Vortex OnEndSpellCast"

