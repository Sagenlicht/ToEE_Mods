from toee import *

def OnBeginSpellCast(spell):
    print "Frost Breath OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Frost Breath OnSpellEffect"

    targetsToRemove = []
    spell.duration = 0
    spellDamageDice = dice_new('1d4')
    spellDamageDice.number = min((spell.caster_level/2), 5) #capped at CL 10

    game.particles('sp-Cone of Cold', spell.caster)
    for spellTarget in spell.target_list:
        #Saving throw for half damage and avoid being dazed
        if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Reflex, D20STD_F_NONE, spell.caster, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
            spellTarget.obj.spell_damage_with_reduction(spell.caster, D20DT_COLD, spellDamageDice, D20DAP_UNSPECIFIED, DAMAGE_REDUCTION_HALF, D20A_CAST_SPELL, spell.id)
            targetsToRemove.append(spellTarget.obj)
        else:
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.obj.spell_damage(spell.caster, D20DT_COLD, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)
            spellTarget.obj.condition_add_with_args('sp-Daze', spell.id, 1)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Frost Breath OnBeginRound"

def OnEndSpellCast(spell):
    print "Frost Breath OnEndSpellCast"

