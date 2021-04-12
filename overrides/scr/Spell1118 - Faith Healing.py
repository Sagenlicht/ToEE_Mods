from toee import *

def OnBeginSpellCast(spell):
    print "Faith Healing OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Faith Healing OnSpellEffect"
    
    spell.duration = 0 #current round
    spellTarget = spell.target_list[0].obj
    spellCasterDeity = spell.caster.get_deity()
    spellTargetDeity = spellTarget.get_deity()
    spellDamageDice = dice_new('1d8')
    spellDamageDice.bonus = min(spell.caster_level, 5) #capped at CL 5

    if spellCasterDeity == spellTargetDeity:
        if spellTarget.is_category_type(mc_type_undead): #undeads take damage from heal spells
            #save for half damage:
            if spellTarget.saving_throw_spell( spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id ): #success
                spellTarget.float_mesfile_line('mes\\spell.mes', 30001)
                #why negative and not positive? copied from cure spells
                spellTarget.spell_damage_with_reduction( spell.caster, D20DT_NEGATIVE_ENERGY, spellDamageDice, D20DAP_UNSPECIFIED, DAMAGE_REDUCTION_HALF, D20A_CAST_SPELL, spell.id )
            else:
                spellTarget.float_mesfile_line('mes\\spell.mes', 30002)
                spellTarget.spell_damage(spell.caster, D20DT_NEGATIVE_ENERGY, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id) #why negative and not positive? copied from cure spells
        else:
            spellTarget.spell_heal(spell.caster, spellDamageDice, D20A_CAST_SPELL, spell.id)
            spellTarget.healsubdual(spell.caster, spellDamageDice, D20A_CAST_SPELL, spell.id)
        game.particles('sp-Cure Light Wounds', spellTarget)
        
    else:
        spellTarget.float_text_line("Not same faith", tf_red)
        game.particles('Fizzle', spellTarget)

    spell.target_list.remove_target(spellTarget)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Faith Healing OnBeginRound"

def OnEndSpellCast(spell):
    print "Faith Healing OnEndSpellCast"