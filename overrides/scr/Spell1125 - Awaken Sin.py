from toee import *

def OnBeginSpellCast(spell):
    print "Awaken Sin OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    #game.particles("sp-evocation-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Awaken Sin OnSpellEffect"

    spellTarget = spell.target_list[0]
    spell.duration = 0
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = min(spell.caster_level, 10) #capped at CL 10
    neededAlignment = [ALIGNMENT_EVIL, ALIGNMENT_NEUTRAL_EVIL, ALIGNMENT_LAWFUL_EVIL, ALIGNMENT_CHAOTIC_EVIL]

    if spellTarget.obj.stat_level_get(stat_intelligence) >= 3: #Target needs an intelligence score of 3+
        intelligentEnough = True
    else:
        intelligentEnough = False
    
    if spellTarget.obj.stat_level_get(stat_alignment) in neededAlignment: #Target needs to be evil
        hasNeededAlignment = True
    else:
        hasNeededAlignment = False

    if intelligentEnough and hasNeededAlignment:
        #Saving Throw to negate; Awaken Sin is not a touch attack spell
        if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
            game.particles('Fizzle', spellTarget.obj)
        else:
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.obj.spell_damage(spell.caster, D20DT_SUBDUAL, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)
            spellTarget.obj.float_text_line("Stunned", tf_red)
            spellTarget.obj.condition_add_with_args('Stunned', 1, 0)
            if spellTarget.obj.is_unconscious(): #if unconscious after damage from awaken sin, additional wisdom damage
                wisdomDamageDice = dice_new('1d6')
                wisdomDamageDice.number = 1
                wisdomDamage = wisdomDamageDice.roll()
                spellTarget.obj.condition_add_with_args('Temp_Ability_Loss', stat_wisdom, wisdomDamage)
    else:
        spellTarget.obj.float_text_line("Immune", tf_red)
        game.particles('Fizzle', spellTarget.obj)

    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Awaken Sin OnBeginRound"

def OnEndSpellCast(spell):
    print "Awaken Sin OnEndSpellCast"