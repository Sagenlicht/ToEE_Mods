from toee import *

def OnBeginSpellCast(spell):
    print "Wail of Doom OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def	OnSpellEffect(spell):
    print "Wail of Doom OnSpellEffect"
    
    targetsToRemove = []
    spell.duration = 1 * spell.caster_level # 1 round/caster_level

    spellDamageDice = dice_new('1d4')
    spellDamageDice.number = min(spell.caster_level, 15) #capped at CL 15

    game.particles( 'sp-Ironthunder Horn', spell.target_loc )

    for spellTarget in spell.target_list:
        #Save for half damage and be shakened instead of panicked
        if spellTarget.obj.saving_throw_spell(spell.dc, D20_Save_Will, D20STD_F_NONE, spell.caster, spell.id): #success
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30001)
            spellTarget.obj.spell_damage_with_reduction(spell.caster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, DAMAGE_REDUCTION_HALF, D20A_CAST_SPELL, spell.id)
            spellTarget.obj.condition_add('Shaken Condition', 1)
        else:
            spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.obj.spell_damage(spell.caster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, spell.id)
            spellTarget.obj.condition_add('Panicked Condition', spell.duration)
        targetsToRemove.append(spellTarget.obj)

    spell.target_list.remove_list(targetsToRemove)
    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Wail of Doom OnBeginRound"

def OnEndSpellCast(spell):
    print "Wail of Doom OnEndSpellCast"