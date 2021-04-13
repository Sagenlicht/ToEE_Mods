from toee import *

def OnBeginSpellCast(spell):
    print "Deific Vengeance OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Deific Vengeance OnSpellEffect"

    spellTarget = spell.target_list[0]
    spell.duration = 0
    spellDamageDice = dice_new('1d6')
    if spellTarget.obj.is_category_type(mc_type_undead):
        spellDamageDice.number = min(spell.caster_level, 10) #capped at CL 10
    else:
        spellDamageDice.number = min((spell.caster_level/2), 5) #capped at CL 10

    #Saving Throw for half damage
    if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id): #success
        spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
        spellTarget.obj.spell_damage_with_reduction(spell.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, DAMAGE_REDUCTION_HALF, D20A_CAST_SPELL, spell.id)
    else:
        spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
        spellTarget.obj.spell_damage(spell.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)

    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Deific Vengeance OnBeginRound"

def OnEndSpellCast(spell):
    print "Deific Vengeance OnEndSpellCast"

