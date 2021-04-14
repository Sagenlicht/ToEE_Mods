from toee import *

def OnBeginSpellCast(spell):
    print "Ghost Touch Armor OnBeginSpellCast"
    print "spell.target_list=", spell.target_list
    print "spell.caster=", spell.caster, " caster.level= ", spell.caster_level

def OnSpellEffect(spell):
    print "Ghost Touch Armor OnSpellEffect"

    spell.duration = 10 * spell.caster_level
    spellTarget = spell.target_list[0]

    #check if a armor is equipped
    if spellTarget.obj.item_worn_at(item_wear_armor).obj_get_int(obj_f_type) == obj_t_armor:
        spellTarget.obj.condition_add_with_args('sp-Ghost Touch Armor', spell.id, spell.duration)
        spellTarget.partsys_id = game.particles('sp-Heroism', spellTarget.obj)
    else:
        spellTarget.obj.float_text_line("No armor equipped", tf_red)
        game.particles('Fizzle', spellTarget.obj)
        spell.target_list.remove_target(spellTarget.obj)

    spell.spell_end(spell.id)

def OnBeginRound(spell):
    print "Ghost Touch Armor OnBeginRound"

def OnEndSpellCast(spell):
    print "Ghost Touch Armor OnEndSpellCast"

