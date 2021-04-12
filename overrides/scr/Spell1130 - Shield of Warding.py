from toee import *

def OnBeginSpellCast(spell):
    print "Shield of Warding OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Shield of Warding OnSpellEffect"
    
    spell.duration = 10 * spell.caster_level # 1 min/cl
    spellTarget = spell.target_list[0]
    shieldBonus = min ((1 + (spell.caster_level/5)), 5)

    #check if a shield is equipped
    if spellTarget.obj.item_worn_at(item_wear_shield).obj_get_int(obj_f_type) == obj_t_armor:
        spellTarget.obj.condition_add_with_args('sp-Shield of Warding', spell.id, spell.duration, shieldBonus)
        spellTarget.partsys_id = game.particles('sp-Shield of Faith', spellTarget.obj)
    else:
        spellTarget.obj.float_text_line("No shield equipped", tf_red)
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Shield of Warding OnBeginRound"

def OnEndSpellCast(spell):
    print "Shield of Warding OnEndSpellCast"