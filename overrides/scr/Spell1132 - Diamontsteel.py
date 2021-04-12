from toee import *

def OnBeginSpellCast(spell):
    print "Diamondsteel OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Diamondsteel OnSpellEffect"
    
    spell.duration = 1 * spell.caster_level # 1 round/cl
    spellTarget = spell.target_list[0]

    #check if a armor is equipped
    if spellTarget.obj.item_worn_at(item_wear_armor).obj_get_int(obj_f_type) == obj_t_armor:
        spellTarget.obj.condition_add_with_args('sp-Diamondsteel', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-stoneskin', spellTarget.obj)
    else:
        spellTarget.obj.float_text_line("No armor equipped", tf_red)
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Diamondsteel OnBeginRound"

def OnEndSpellCast(spell):
    print "Diamondsteel OnEndSpellCast"