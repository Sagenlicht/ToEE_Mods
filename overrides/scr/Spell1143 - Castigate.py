from toee import *

def OnBeginSpellCast(spell):
    print "Castigate OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Castigate OnSpellEffect"

    targetsToRemove = []
    spellCasterAlignmentAxis = []
    spell.duration = 0
    spellDamageDice = dice_new('1d4')
    spellCasterAlignment = spell.caster.critter_get_alignment()

    if spellCasterAlignment & ALIGNMENT_LAWFUL:
        spellCasterAlignmentAxis.append(ALIGNMENT_LAWFUL)
    elif spellCasterAlignment & ALIGNMENT_CHAOTIC:
        spellCasterAlignmentAxis.append(ALIGNMENT_CHAOTIC)
    else:
        spellCasterAlignmentAxis.append(ALIGNMENT_NEUTRAL)
    if spellCasterAlignment & ALIGNMENT_GOOD:
        spellCasterAlignmentAxis.append(ALIGNMENT_GOOD)
    elif spellCasterAlignment & ALIGNMENT_EVIL:
        spellCasterAlignment.append(ALIGNMENT_EVIL)
    else:
        spellCasterAlignmentAxis.append(ALIGNMENT_NEUTRAL)
    
    game.particles('sp-Sound Burst', spell.caster)
    
    for spellTarget in spell.target_list:
        print "Checking {} Alignment".format(spellTarget.obj)
        sameAlignment = False
        spellTargetAlignment = spellTarget.obj.critter_get_alignment()
        if not spellTargetAlignment & spellCasterAlignmentAxis[0] and not spellTargetAlignment & spellCasterAlignmentAxis[1]:
            print "No shared axis, full damage!"
            spellDamageDice.number = min(spell.caster_level, 10) #capped at CL 10
        elif spellTargetAlignment == spellCasterAlignment:
            print "Same Alignment, no damage!"
            sameAlignment = True
            spellTarget.obj.float_text_line("Same Alignment")
            game.particles('Fizzle', spellTarget.obj)
        else:
            print "One axis shared, half damage!"
            spellDamageDice.number = min((spell.caster_level/2), 5)
        
        if not sameAlignment:
            if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Fortitude, D20STD_F_NONE, spell.caster, spell.id): #success
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
                spellTarget.obj.spell_damage_with_reduction(spell.caster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, DAMAGE_REDUCTION_HALF, D20A_CAST_SPELL, spell.id)
            else:
                spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
                spellTarget.obj.spell_damage(spell.caster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)
        
        targetsToRemove.append(spellTarget.obj)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Castigate OnBeginRound"

def OnEndSpellCast(spell):
    print "Castigate OnEndSpellCast"

