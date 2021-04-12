from toee import *

def OnBeginSpellCast(spell):
    print "Dolorous Blow OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Dolorous Blow OnSpellEffect"

    spell.duration = 10 * spell.caster_level # 1 min/cl
    spellTarget = spell.target_list[0]

    if spell.caster.item_worn_at(item_wear_weapon_primary).obj_get_int(obj_f_type) == obj_t_weapon:
        spellTarget.obj.condition_add_with_args('sp-Dolorous Blow', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-True Strike', spellTarget.obj)
    else:
        spell.caster.float_text_line("Weapon required", tf_red)
        game.particles('Fizzle', spell.caster)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

    
def OnBeginRound(spell):
    print "Dolorous Blow OnBeginRound"

def OnEndSpellCast(spell):
    print "Dolorous Blow OnEndSpellCast"