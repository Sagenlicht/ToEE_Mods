from toee import *

def OnBeginSpellCast(spell):
    print "Masters Touch OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Masters Touch OnSpellEffect"
    spell.duration = 10 * spell.caster_level # 1 Min/cl
    spellTarget = spell.target_list[0]

    itemTarget = spell.spell_get_menu_arg(RADIAL_MENU_PARAM_MIN_SETTING) # 1 = mainhand; 2 = offhand;
    if not itemTarget in range(1,3): #Fallback
        itemTarget = 1 #sets it to mainhand in fallback

    if itemTarget == 1:
        if spellTarget.obj.item_worn_at(item_wear_weapon_primary).type == obj_t_weapon:
            spellTarget.obj.condition_add_with_args('sp-Masters Touch', spell.id, spell.duration, item_wear_weapon_primary)
        else:
            spellTarget.obj.float_text_line("No weapon equipped", tf_red)
            game.particles('Fizzle', spellTarget.obj)
            spell.target_list.remove_target(spellTarget.obj)
    elif itemTarget == 2:
        if spellTarget.obj.item_worn_at(item_wear_weapon_secondary).type == obj_t_weapon:
            spellTarget.obj.condition_add_with_args('sp-Masters Touch', spell.id, spell.duration, item_wear_weapon_secondary)
        elif spellTarget.obj.item_worn_at(item_wear_shield).type == obj_t_armor:
            spellTarget.obj.condition_add_with_args('sp-Masters Touch', spell.id, spell.duration, item_wear_shield)
        else:
            spellTarget.obj.float_text_line("No weapon or shield equipped", tf_red)
            game.particles('Fizzle', spellTarget.obj)
            spell.target_list.remove_target(spellTarget.obj)
    else:
         spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end( spell.id)

def OnBeginRound(spell):
    print "Masters Touch OnBeginRound"

def OnEndSpellCast(spell):
    print "Masters Touch OnEndSpellCast"