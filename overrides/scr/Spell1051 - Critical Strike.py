from toee import *

def OnBeginSpellCast(spell):
    print "Critical Strike OnBeginSpellCast"
    print "spell.spellTarget_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Critical Strike OnSpellEffect"
    spell.duration = 0 #Active only for current round
    spellTarget = spell.target_list[0]
    mainhandWeapon = spell.caster.item_worn_at(item_wear_weapon_primary)

    if mainhandWeapon.obj_get_int(obj_f_weapon_flags) & OWF_RANGED_WEAPON:
        wrongWeaponType = True
    else:
        wrongWeaponType = False

    if wrongWeaponType:
        spell.caster.float_text_line("Melee Weapon required", tf_red)
        game.particles('Fizzle', spell.caster)
        spell.target_list.remove_target(spellTarget.obj)
    else:
        spellTarget.obj.condition_add_with_args('sp-Critical Strike', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-True Strike', spellTarget.obj)

    spell.spell_end(spell.id)

    
def OnBeginRound(spell):
    print "Critical Strike OnBeginRound"

def OnEndSpellCast(spell):
    print "Critical Strike OnEndSpellCast"