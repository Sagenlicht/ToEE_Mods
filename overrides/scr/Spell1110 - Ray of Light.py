from toee import *

def OnBeginSpellCast(spell):
    print "Ray of Light OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Ray of Light OnSpellEffect"

def OnBeginRound(spell):
    print "Ray of Light OnBeginRound"

def OnBeginProjectile(spell, projectile, index_of_target):
    print "Ray of Light OnBeginProjectile"
    projectile.obj_set_int(obj_f_projectile_part_sys_id, game.particles('sp-Ray of Frost', projectile))

def OnEndProjectile( spell, projectile, index_of_target ):
    print "Ray of Light OnEndProjectile"
    ####################################################
    #     Using Shiningteds Weapon Focus(Ray) Fix      #
    ####################################################
    if spell.caster.has_feat(feat_weapon_focus_ray):
        casterHasWfRay = True
    else:
        casterHasWfRay = False

    if casterHasWfRay:
        if spell.caster.has_feat(feat_greater_weapon_focus_ray):
            casterHasGreaterWfRay = True
        else:
            casterHasGreaterWfRay = False

    if casterHasWfRay:
        savedOriginalDexterityValue = spell.caster.stat_base_get(stat_dexterity)
        if casterHasGreaterWfRay:
            applyBonusToDexterity = savedOriginalDexterityValue + 4
        else:
            applyBonusToDexterity = savedOriginalDexterityValue + 2
        spell.caster.stat_base_set(stat_dexterity, applyBonusToDexterity)
    ####################################################

    spellTarget = spell.target_list[0]
    spell.duration = 0
    game.particles_end(projectile.obj_get_int(obj_f_projectile_part_sys_id))

    if spell.caster.perform_touch_attack(spellTarget.obj) & D20CAF_HIT:
        spellTarget.partsys_id = game.particles('sp-Arcane Eye-END', spellTarget.obj)
        blindnessDurationDice = dice_new('1d4')
        blindnessDuration = blindnessDurationDice.roll()
        spellTarget.obj.condition_add('Blindness', blindnessDuration)
        spellTarget.obj.float_text_line("Blinded", tf_red)
        game.create_history_freeform("{} is ~blinded~[TAG_BLINDED]\n\n".format(spellTarget.obj.description))
    else:
        spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30007)
        game.particles('Fizzle', spellTarget.obj)

    ####################################################
    #     Using Shiningteds Weapon Focus(Ray) Fix      #
    ####################################################
    if casterHasWfRay:
        spell.caster.stat_base_set(stat_dexterity, savedOriginalDexterityValue)
    ####################################################

    spell.target_list.remove_target(spellTarget.obj)
    spell.spell_end(spell.id)

def OnEndSpellCast(spell):
    print "Ray of Light OnEndSpellCast"