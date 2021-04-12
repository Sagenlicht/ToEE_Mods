from toee import *

def OnBeginSpellCast(spell):
    print "Ray of Dizziness OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level
    game.particles("sp-evocation-conjure", spell.caster)

def OnSpellEffect(spell):
    print "Ray of Dizziness OnSpellEffect"

def OnBeginRound(spell):
    print "Ray of Dizziness OnBeginRound"

def OnBeginProjectile(spell, projectile, index_of_target):
    print "Ray of Dizziness OnBeginProjectile"
    projectile.obj_set_int(obj_f_projectile_part_sys_id, game.particles('sp-Ray of Frost', projectile))

def OnEndProjectile( spell, projectile, index_of_target ):
    print "Ray of Dizziness OnEndProjectile"
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
    spell.duration = 1 * spell.caster_level # 1 round/casterlevel
    game.particles_end(projectile.obj_get_int(obj_f_projectile_part_sys_id))

    if spell.caster.perform_touch_attack(spellTarget.obj) & D20CAF_HIT:
        spellTarget.partsys_id = game.particles('sp-Shout-Hit', spellTarget.obj)
        spellTarget.obj.condition_add_with_args('sp-Ray of Dizziness', spell.id, spell.duration)
    else:
        spellTarget.obj.float_mesfile_line('mes\\spell.mes', 30007)
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    ####################################################
    #     Using Shiningteds Weapon Focus(Ray) Fix      #
    ####################################################
    if casterHasWfRay:
        spell.caster.stat_base_set(stat_dexterity, savedOriginalDexterityValue)
    ####################################################

    spell.spell_end(spell.id)

def OnEndSpellCast(spell):
    print "Ray of Dizziness OnEndSpellCast"