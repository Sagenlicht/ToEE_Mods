from toee import *

def OnBeginSpellCast(spell):
    print "Checkmates Light OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Checkmates Light OnSpellEffect"
    
    spell.duration = 1 *spell.caster_level # 1 round/casterlevel
    spellTarget = spell.target_list[0]
    spellBonus = min((spell.caster_level/3), 5) #Bonus is capped at cl 15 (max5)
    wornWeapon = spellTarget.obj.item_worn_at(item_wear_weapon_primary)

    if wornWeapon.obj_get_int(obj_f_type) == obj_t_weapon:
        if wornWeapon.obj_get_int(obj_f_weapon_flags) & OWF_RANGED_WEAPON:
            isMeleeWeapon = False
        else:
            isMeleeWeapon = True
    else:
        isMeleeWeapon = False

    if isMeleeWeapon:
        spellTarget.obj.condition_add_with_args('sp-Checkmates Light', spell.id, spell.duration, spellBonus)
        spellTarget.partsys_id = game.particles('sp-True Strike', spellTarget.obj)
    else:
        spell.caster.float_text_line("Melee weapon required", tf_red)
        game.particles('Fizzle', spell.caster)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)


def OnBeginRound(spell):
    print "Checkmates Light OnBeginRound"

def OnEndSpellCast(spell):
    print "Checkmates Light OnEndSpellCast"